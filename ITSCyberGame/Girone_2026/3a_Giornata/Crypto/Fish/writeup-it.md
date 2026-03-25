# Fish

**Competizione:** ITSCyberGame<br>
**Categoria:** Crypto<br>
**File:** `aziende.csv`, `pp.txt`, `encode3.txt`

---

## Descrizione

> Durante un'attività di Incident Response, il SOC ha recuperato tre elementi da un server aziendale compromesso:
> * Un database con l'elenco completo delle aziende
> * L'hash della password di un account di servizio
> * Un file contenente comunicazioni interne cifrate
>
> Dalle prime analisi è emerso che il reparto IT aveva implementato un sistema di cifratura "artigianale", convinto di aver raggiunto la segretezza perfetta. Purtroppo, alcune scelte progettuali discutibili potrebbero aver introdotto debolezze.
>
> Questo è il tuo punto di inizio:
> `Nzk2MjIwNGI2MjY1MjA2NjY4NzYyMDcxNjI3MDY4N2E3MjYxNjc3NjIwNjg2NjZlNjE3MTYyMjA3OTZlMjA2NjY3NzI2NjY2NmUyMDcwNzU3NjZlNjk3Mg==`

**Formato della flag:** `flag{testoinchiaro}`

---

## Soluzione

### 1. Decodifica del punto di partenza

La stringa fornita è Base64. Decodificandola:

```
Nzk2MjIwNGI2MjY1MjA2NjY4NzYyMDcxNjI3MDY4N2E3MjYxNjc3NjIwNjg2NjZlNjE3MTYyMjA3OTZlMjA2NjY3NzI2NjY2NmUyMDcwNzU3NjZlNjk3Mg==
  → (Base64)
7962204b62652066687620716270687a726167762068666e61716220796e2066677266666e207075766e6972
  → (Hex)
yb Kbe fhv qbphzragv hfnaqb yn fgrffn puvnir
  → (ROT13)
lo XOR sui documenti usando la stessa chiave
```

La hint è chiara: tutti i file sono cifrati con **XOR** usando **la stessa chiave**.

---

### 2. Cracking dell'hash (encode3.txt)

Il file `encode3.txt` contiene:

```
a670add1a2ed13ffccdb692e3eb385aff70d280d0f3f06c9b60424e2f47fd3d8
```

64 caratteri esadecimali → **SHA-256**.

La debolezza del sistema sta nella scelta della password: il formato è
**`NomeSenzaSpazi + AnnoFondazione`** per ogni azienda del CSV.
Si itera sul database con:

```python
import csv, hashlib

target = "a670add1a2ed13ffccdb692e3eb385aff70d280d0f3f06c9b60424e2f47fd3d8"

with open('aziende.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        password = row['Nome'].replace(' ', '') + row['AnnoFondazione']
        if hashlib.sha256(password.encode()).hexdigest() == target:
            print(f"Password trovata: {password}")
            break
```

```
Password trovata: LynxWorksMG89Tech2013
```

L'account di servizio appartiene all'azienda **LynxWorks MG89 Tech**, fondata nel **2013**.

---

### 3. Recupero della chiave XOR — Many-Time Pad Attack

`pp.txt` contiene 9 righe di testo cifrato in esadecimale. L'hint dice che è stato usato **lo stesso keystream XOR per tutti i messaggi**, questo è il classico errore del **Many-Time Pad**.

Se `C₁ = P₁ ⊕ K` e `C₂ = P₂ ⊕ K`, allora `C₁ ⊕ C₂ = P₁ ⊕ P₂`, eliminando la chiave. Con abbastanza ciphertext è possibile recuperare sia la chiave che i plaintext tramite analisi statistica.

Si applica un attacco statistico: per ogni posizione `i`, si cerca il byte di chiave `K[i]` tale che tutti i plaintext decifrati siano caratteri ASCII stampabili, massimizzando la presenza di lettere e spazi:

```python
import string

with open('pp.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip()]
ciphertexts = [bytes.fromhex(l) for l in lines]

key = []
for pos in range(max(len(c) for c in ciphertexts)):
    col = [c[pos] for c in ciphertexts if pos < len(c)]
    best_k, best_score = 0, -1
    for k in range(256):
        dec = [b ^ k for b in col]
        if not all(32 <= b <= 126 for b in dec):
            continue
        score = sum(2 if chr(b) in string.ascii_letters + ' ' else 1 for b in dec)
        if score > best_score:
            best_score, best_k = score, k
    key.append(best_k)
```

La chiave stimata contiene il pattern leggibile:
```
nome azienda e anno senza spazi[nome azienda e anno senza spazi...]
```

Con un **known-plaintext attack** di verifica (usando i plaintext quasi noti per XOR inverso), si conferma che la chiave ha esattamente **31 caratteri**:

```
nome azienda e anno senza spazi
```

Una chiave letteralmente descrittiva del proprio metodo di generazione, la debolezza "artigianale" annunciata nella challenge.

---

### 4. Decifratura dei messaggi

```python
def xor_decrypt(hex_data, key):
    ct = bytes.fromhex(hex_data)
    return bytes([ct[i] ^ ord(key[i % len(key)]) for i in range(len(ct))]).decode('utf-8')

key = "nome azienda e anno senza spazi"

with open('pp.txt', 'r') as f:
    for i, line in enumerate(f, 1):
        if line.strip():
            print(f"Riga {i}: {xor_decrypt(line.strip(), key)}")
```

```
Riga 1: Le policy aziendali richiedono attenzione durante ogni inserimento password.
Riga 2: L'utente deve compilare il campo previsto seguendo le regole comunicate.
Riga 3: E' necessario verificare la tastiera prima di confermare i dati inseriti.
Riga 4: Si raccomanda di usare un contesto riservato durante l'accesso al portale.
Riga 5: Ogni credenziale va digitata con cura, evitando condivisioni non autorizzate.
Riga 6: In caso di errore, la procedura prevede un nuovo tentativo guidato e sicuro.
Riga 7: Il sistema puo' richiedere controlli aggiuntivi prima della conferma finale.
Riga 8: Le indicazioni interne invitano a mantenere riservati codici e passaggi.
Riga 9: Il rispetto delle policy supporta continuita' operativa e tutela dei dati.
```

Tutti e 9 i messaggi sono comunicazioni interne sulle policy di sicurezza IT, nessuna flag esplicita nel testo. La flag è la password dell'account di servizio recuperata al passo 2.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge illustra tre vulnerabilità reali concatenate:

1. **Many-Time Pad**: riusare la stessa chiave XOR su più messaggi distrugge la confidenzialità. È lo stesso motivo per cui il Vernam cipher richiede che la chiave sia usata una sola volta (*one-time pad*).

2. **Password debole e prevedibile**: costruire la password concatenando campi di un database pubblico (`NomeSenzaSpazi + Anno`) la rende vulnerabile a un attacco a dizionario mirato, senza bisogno di wordlist generiche.

3. **Chiave autoreferenziale**: usare come chiave la stringa che *descrive* il metodo di generazione della chiave stessa (`"nome azienda e anno senza spazi"`) è una debolezza critica, sfruttabile con un attacco statistico non appena si hanno più ciphertext.