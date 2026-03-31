# Shuffled Snapshot

**Competizione:** ITSCyberGame<br>
**Categoria:** Crypto<br>
**File:** `snapshot.bin`, `pubkey.txt`

---

## Descrizione

> Avete presente quando le immagini si corrompono? Beh oggi non è proprio il caso, questa è solo criptata. INCREDIBILMENTE criptata...

---

## Soluzione

### Passo 1 — Analisi dei file forniti

`pubkey.txt` contiene una chiave RSA pubblica:

```
n = 871013614924877797546595892294532560519922870857806731421802158788666364217562314967714182421931
e = 65537
```

Il modulo `n` è di soli **319 bit**, enormemente più piccolo del minimo sicuro (2048 bit). Questo è il primo segnale: la chiave è vulnerabile alla fattorizzazione.

`snapshot.bin` è un file binario di **5480 byte**, non riconosciuto da `file` come alcun formato standard:

```bash
$ file snapshot.bin
snapshot.bin: data
$ wc -c snapshot.bin
5480 snapshot.bin
```

### Passo 2 — Struttura del file cifrato

`n` è lungo **40 byte** (319 bit → ceiling a 40 byte). Dividendo la dimensione del file:

```
5480 / 40 = 137 blocchi esatti
```

Il file è composto da **137 ciphertext RSA da 40 byte ciascuno**, cifrati in modalità **ECB (textbook RSA senza padding)**, ogni blocco è indipendente dagli altri.

### Passo 3 — Fattorizzazione di n

Con `n` di soli 319 bit, la fattorizzazione è banale usando `sympy`:

```python
from sympy import factorint
n = 871013614924877797546595892294532560519922870857806731421802158788666364217562314967714182421931
print(factorint(n))
```

Risultato:

```
p = 933281101772064062160042018090078644844919576771
q = 933281101772064062160042093647942370759242995961
```

Verifica: `p * q == n`

Si calcola la chiave privata:

```python
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
# d = 406739714530127410716328496693194294553484589463588399511048244052240010320256445856697362519873
```

### Passo 4 — Decriptazione dei blocchi

Si decripta ogni blocco da 40 byte con RSA testbook (`m = c^d mod n`), mantenendo il risultato su **29 byte fissi** (con zero-padding a sinistra):

```python
data = open('snapshot.bin', 'rb').read()
n_bytes = 40
chunks = [data[i:i+n_bytes] for i in range(0, len(data), n_bytes)]

plaintexts = []
for c in chunks:
    ct = int.from_bytes(c, 'big')
    pt = pow(ct, d, n)
    pt_bytes = pt.to_bytes(29, 'big')
    plaintexts.append(pt_bytes)
```

Esaminando i blocchi decriptati si nota una struttura costante: **il primo byte di ogni blocco è un indice** (da 0 a 136) e i restanti **28 byte sono il payload**. Questo è il meccanismo "shuffled" del titolo: i blocchi sono stati rimescolati e l'indice permette di riordinarli.

```
Blocco raw 0:  idx=103, payload=88dd0775ebadb77674...
Blocco raw 1:  idx=107, payload=bf3d51fc1bfe2f7ef1...
Blocco raw 2:  idx= 25, payload=c8dcb9738bc728140a...
...
Blocco raw 37: idx=  0, payload=00000eea89504e470d0a1a0a...  ← PNG magic!
Blocco raw 38: idx=  1, payload=08020000001db3e567...
```

### Passo 5 — Riordinamento e ricostruzione del file

Si ordinano i blocchi per indice e si concatenano i payload:

```python
sorted_pts = sorted(plaintexts, key=lambda x: x[0])
reassembled = b''.join(pt[1:] for pt in sorted_pts)
```

Il payload del blocco con indice `0` inizia con `00 00 0e ea 89 50 4e 47...`. I 4 byte `00 00 0e ea` sono un prefisso del formato interno; il PNG vero e proprio inizia con `89 50 4e 47` (`\x89PNG`):

```python
png_start = reassembled.find(b'\x89PNG')
png_data = reassembled[png_start:]
```

Struttura PNG verificata:

```
IHDR  — width=700, height=220, 8-bit RGB
IDAT  — 3761 byte di dati compressi (zlib OK, 462220 byte decompressi)
IEND  — fine file
```

### Passo 6 — Immagine

Il file PNG ottenuto dal reassemblaggio risulta valido e viene aperto correttamente. L’immagine (700×220, RGB) contiene direttamente la stringa della flag, visibile senza necessità di ulteriori elaborazioni.

---

## Flag

![Snapshot decriptata](snapshot_decrypted.png)

---

## Conclusioni

La challenge combinava tre vulnerabilità in cascata: un modulo RSA di soli 319 bit (fattorizzabile in pochi secondi), la cifratura ECB blocco per blocco senza padding (textbook RSA) e il rimescolamento dell'ordine dei blocchi con indice embedded nel plaintext. Riordinati i blocchi e ricostruito il PNG, la flag era leggibile nell'immagine.