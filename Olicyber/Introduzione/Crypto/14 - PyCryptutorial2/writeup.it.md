# PyCryptutorial 2

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc cr14.challs.olicyber.it 30007`

---

## Descrizione

> Per concludere la sezione introduttiva alle challenge di crittografia, riprendiamo in mano PyCryptodome. In questa challenge ti verrà richiesto di utilizzare la porzione di libreria riguardante funzioni di hash, crittografia asimmetrica e alcune funzioni miscellanee.

Il server pone cinque quesiti su hash, HMAC, chiavi DSA e primalità. Rispondere correttamente a tutti restituisce la flag.

---

## Soluzione

### Step 1 — Hash SHA3-384

Il server chiede:

```
msg = 'hash_me_pls'
SHA3-384(msg) = ?
```

SHA3-384 è una funzione di hash crittografica della famiglia Keccak, con digest di 384 bit = 48 byte. A differenza di SHA-2, SHA-3 è basata su una costruzione *sponge* anziché Merkle-Damgård.

```python
from Crypto.Hash import SHA3_384

h = SHA3_384.new()
h.update('hash_me_pls'.encode())
print(h.hexdigest())
```

**Output:**
```
2daba465e04884079b220e455061be60740e2739cfc864c8dd650f8ec688700aa046d78d408725bb5e6f9fb6a387af25
```

---

### Step 2 — HMAC-SHA224

Il server chiede il MAC del messaggio con chiave e hash specificati:

```
Hash = SHA-224
key.hex() = 'a0969b8259d73d619c500da29e8e0e169aa0c71943707ab2e1e82bfb0e5fc65b'
msg = 'La mia integrità è importante!'
```

**HMAC** (Hash-based Message Authentication Code) garantisce l'integrità e l'autenticità di un messaggio. Dato un hash $H$ con blocchi di dimensione $B$, la costruzione è:

$$\text{HMAC}(K, m) = H\!\left((K \oplus \text{opad}) \| H\!\left((K \oplus \text{ipad}) \| m\right)\right)$$

dove $\text{ipad} = \texttt{0x36}^B$ e $\text{opad} = \texttt{0x5C}^B$.

```python
from Crypto.Hash import HMAC, SHA224

key = bytes.fromhex('a0969b8259d73d619c500da29e8e0e169aa0c71943707ab2e1e82bfb0e5fc65b')
h = HMAC.new(key, 'La mia integrità è importante!'.encode('utf-8'), SHA224)
print(h.hexdigest())
```

**Output:**
```
53246be22141f11ea9dbc93c4d4ce486c726401d76adc4d901629b11
```

---

### Step 3 — Estrazione parametri chiave DSA

Il server fornisce una chiave DSA codificata in formato DER e chiede i parametri $x$, $g$, $q$.

**DSA** (Digital Signature Algorithm) opera in un sottogruppo ciclico di ordine $q$ del gruppo moltiplicativo $(\mathbb{Z}/p\mathbb{Z})^*$. I parametri sono:
- $p$: primo grande (modulo)
- $q$: primo che divide $p-1$ (ordine del sottogruppo)
- $g$: generatore del sottogruppo di ordine $q$
- $x$: chiave privata, $x \in [1, q-1]$
- $y = g^x \bmod p$: chiave pubblica

```python
from Crypto.PublicKey import DSA

key = DSA.import_key(bytes.fromhex('3082025a...'))
print(f"x = {key.x}")
print(f"g = {key.g}")
print(f"q = {key.q}")
```

**Output:**
```
x = 178754102630780949657156804783723575105266101658277178106272920043
g = 26889620844978844541675649538418431761971476784081805970749116788...
q = 18149454321975056401440128528567616877710863748281779964914588693987
```

---

### Step 4 — Generazione di un primo da 1414 bit

Il server chiede un numero primo di esattamente 1414 bit. Si usa `getPrime` di PyCryptodome, che internamente applica il test di Miller-Rabin per garantire la primalità con alta probabilità:

```python
from Crypto.Util.number import getPrime

p = getPrime(1414)
print(p)
```

**Output:**
```
267527908544283261916792786274966684890694136452906221337497507...
```

---

### Step 5 — Test di primalità

Il server fornisce un numero e chiede se è primo. Si usa `isPrime`, che applica anch'esso Miller-Rabin:

```python
from Crypto.Util.number import isPrime

p = 104786674500545199644698024951321722188680347802224708014442438...
print('si' if isPrime(p) else 'no')
```

**Output:**
```
no
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> Conoscere una libreria crittografica non significa solo sapere che esiste, ma capire cosa fa internamente ogni funzione e quando usarla correttamente.

Quattro concetti fondamentali emersi dal tutorial:

1. **SHA-3 vs SHA-2:** SHA-3 (Keccak) usa una costruzione *sponge*, i dati vengono assorbiti in uno stato interno e poi estratti, mentre SHA-2 usa Merkle-Damgård. Le due famiglie sono complementari: SHA-3 è resistente ad attacchi di *length extension* che affliggono SHA-2 in certe configurazioni.

2. **HMAC non è hash(key || msg):** la costruzione naive `H(key || msg)` è vulnerabile agli attacchi di *length extension* su SHA-2. HMAC risolve il problema con il doppio hashing con chiavi derivate da `ipad` e `opad`, garantendo sicurezza provabile sotto l'assunzione che $H$ sia una PRF.

3. **Parametri DSA e sicurezza:** la sicurezza di DSA dipende dalla difficoltà del DLP nel sottogruppo di ordine $q$. La chiave privata $x$ deve essere tenuta segreta, il riutilizzo del nonce $k$ nella firma porta al recupero immediato di $x$, come dimostrato negli attacchi alla PlayStation 3.

4. **Test di Miller-Rabin:** `getPrime` e `isPrime` usano Miller-Rabin, un test probabilistico di primalità. Con $t$ iterazioni la probabilità di falso positivo è al più $4^{-t}$. PyCryptodome usa un numero di iterazioni sufficiente a rendere questa probabilità trascurabile in pratica.