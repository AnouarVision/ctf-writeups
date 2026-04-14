# Secure Key Generator

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Abbiamo trovato su un server remoto un file crittato di cui non conosciamo l'origine e il programma usato per generare la chiave di cifratura.

Vengono forniti due file: `key_generator.py` (il generatore della chiave) e `flag.enc` (il file cifrato).

---

## Analisi del codice

```python
def generate_secure_key():
    ts = int(datetime.timestamp(datetime.now()))
    h = sha256(int_to_bytes(ts)).digest()

    seed = int_from_bytes(h[32:])
    key = h[:32]

    random.seed(seed)
    for _ in range(32):
        key += bytes([random.randint(0, 255)])

    return key
```

La chiave è composta da due parti concatenate:

- **Parte deterministica** (32 byte): `h[:32]` = SHA-256 del timestamp Unix corrente
- **Parte pseudo-casuale** (32 byte): output di `random.randint` seedato con `int_from_bytes(h[32:])`

La chiave finale ha dimensione $|K| = 64$ byte.

---

## Soluzione

### Step 1 — Prima vulnerabilità: il seed è sempre zero
Siccome l'hash SHA-256 dell'orario è lungo esattamente 32 byte, dall'indice 32 in poi non c'è niente. Python non dà errore, restituisce silenziosamente una sequenza vuota.
Convertire una sequenza vuota in numero dà 0.

Di conseguenza:

$$\texttt{h[32:]} = \varepsilon \quad \text{(sequenza vuota)}$$

La funzione `int_from_bytes` applicata alla sequenza vuota restituisce:

$$\texttt{seed} = \int_{\mathbb{F}_2^*}(\varepsilon) = 0$$

Pertanto `random.seed(0)` è **sempre** la chiamata effettuata, indipendentemente dal timestamp. La parte pseudo-casuale della chiave è **completamente deterministica e costante** per qualsiasi esecuzione del programma:

$$K[32:64] = \text{costante} = \texttt{c5d71484f8cf9bf4b7...}$$

Questa è una grave violazione del principio di **indistinguibilità computazionale**: i 32 byte pseudo-casuali non aggiungono alcuna entropia alla chiave.

---

### Step 2 — Seconda vulnerabilità: entropia ridotta al timestamp

L'unica fonte di entropia rimasta è il timestamp Unix in secondi:

$$K[0:32] = \text{SHA-256}(\texttt{int\_to\_bytes}(t_s))$$

Il commento nel codice fornisce un riferimento temporale diretto:

```python
# 2021-03-21 17:37:40
```

Questo corrisponde al timestamp Unix $t_{\text{hint}} = 1616348260$ (UTC+1). Lo spazio di ricerca si riduce quindi a una finestra temporale ragionevole attorno a questa data.

Formalmente, invece di cercare in $\{0, \ldots, 2^{256}-1\}$ (spazio delle chiavi SHA-256), cerchiamo in:

$$\mathcal{T} = \{ t_{\text{hint}} + \delta \mid \delta \in [-\Delta, +\Delta] \}$$

con $\Delta = 86400$ (un giorno), ottenendo $|\mathcal{T}| = 172801$ candidati, un attacco a **forza bruta fattibile** in pochi secondi.

---

### Step 3 — Identificazione del tipo di cifratura

Il file cifrato ha dimensione 35116 byte, **non divisibile per 16**, il che esclude AES in modalità CBC (che richiede padding al multiplo del blocco). Il file è stato cifrato con **AES-OFB** (Output Feedback Mode), una modalità a flusso che non richiede padding e produce un ciphertext della stessa lunghezza del plaintext.

In AES-OFB la cifratura è definita come:

$$O_0 = \text{IV}, \quad O_j = \text{AES}_K(O_{j-1})$$
$$C_i = P_i \oplus O_{\lfloor i/16 \rfloor}[i \bmod 16]$$

dove $K = K[0:32]$ (chiave AES-256) e $\text{IV} = K[32:48]$.

---

### Step 4 — Attacco: brute force sul timestamp

Per ogni candidato $t \in \mathcal{T}$:

1. Calcola $K = \text{GenerateKey}(t)$
2. Decifra i primi 48 byte con AES-OFB
3. Verifica se il plaintext inizia con la magic signature `%PDF` (`\x25\x50\x44\x46`)

Il timestamp corretto è $t^* = 1616264040$, corrispondente a `2021-03-21 16:37:40 UTC`, esattamente **un'ora prima** del timestamp nel commento (che era espresso in UTC+1).

---

### Step 5 — Exploit

```python
from hashlib import sha256
from datetime import datetime
import random
from Crypto.Cipher import AES

def int_to_bytes(x):
    if x == 0:
        return b''
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def generate_key_for_ts(ts):
    h = sha256(int_to_bytes(ts)).digest()
    seed = int_from_bytes(h[32:])
    key = h[:32]
    random.seed(seed)
    for _ in range(32):
        key += bytes([random.randint(0, 255)])
    return key

ciphertext = open('flag.enc', 'rb').read()
hint_ts = int(datetime(2021, 3, 21, 17, 37, 40).timestamp())

for delta in range(-86400, 86400):
    ts = hint_ts + delta
    key = generate_key_for_ts(ts)
    cipher = AES.new(key[:32], AES.MODE_OFB, key[32:48])
    pt = cipher.decrypt(ciphertext[:48])
    if pt[:4] == b'%PDF':
        print(f"Timestamp found: {ts} (delta={delta}s)")
        cipher2 = AES.new(key[:32], AES.MODE_OFB, key[32:48])
        open('flag_decrypted.pdf', 'wb').write(cipher2.decrypt(ciphertext))
        print("Decrypted file saved as flag_decrypted.pdf")
        break
```

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge illustra tre errori critici di progettazione crittografica:

1. **Slicing fuori dai limiti non è un errore silenzioso, è un bug semantico**: `h[32:]` su un digest SHA-256 di 32 byte restituisce silenziosamente `b''`, azzerando tutta l'entropia della componente pseudo-casuale. In Python lo slicing out-of-bounds non lancia eccezioni, rendendo questo tipo di bug particolarmente insidioso.

2. **Il timestamp in secondi non è una sorgente di entropia adeguata per una chiave crittografica**: uno spazio di $\approx 10^5$ candidati è banalmente esplorabile. Un generatore crittograficamente sicuro come `os.urandom()` avrebbe reso l'attacco computazionalmente intrattabile.

3. **I commenti nel codice sono informazioni**: la data `# 2021-03-21 17:37:40` ha ridotto ulteriormente lo spazio di ricerca da miliardi di secondi a qualche centinaio, rendendo il bruteforce istantaneo.

La correzione corretta sarebbe:
```python
key = os.urandom(48)  # 32 byte chiave AES + 16 byte IV, tutti casuali
```