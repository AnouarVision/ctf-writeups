# PyCryptutorial 1

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc crypto-07.challs.olicyber.it 30000`

---

## Descrizione

> PyCryptodome è una libreria che vedrai utilizzata molto spesso nelle challenge di crittografia: conoscerne la struttura e i pacchetti base è molto importante.

Il server pone tre quesiti in sequenza, ognuno richiedendo di cifrare o decifrare un messaggio con un algoritmo diverso usando la libreria `pycryptodome`. Rispondere correttamente a tutti e tre restituisce la flag.

---

## Soluzione

### Step 1 — DES-CBC con padding X9.23

Il server fornisce:
- **Cipher:** DES (Data Encryption Standard, blocchi da 64 bit = 8 byte)
- **Mode:** CBC (Cipher Block Chaining)
- **Key:** `a3fc337c90c03f3a`
- **Plaintext:** `La lunghezza di questa frase non è divisibile per 8`
- **Padding:** X9.23

**Analisi del padding X9.23.** Sia $\ell = |P|$ la lunghezza in byte del plaintext e $b = 8$ la dimensione del blocco DES. Il numero di byte di padding necessari è:

$$n = b - (\ell \bmod b) = 8 - (52 \bmod 8) = 8 - 4 = 4$$

Lo schema X9.23 riempie i primi $n-1$ byte con zeri e l'ultimo con il valore $n$:

$$P' = P \| \underbrace{00\,00\,00}_{n-1 \text{ zeri}} \| \underbrace{04}_{n}$$

**Analisi di CBC.** In modalità CBC ogni blocco plaintext $P_i$ viene XORato con il blocco cifrato precedente prima di essere dato in input ad AES:

$$C_0 = \text{IV}, \qquad C_i = E_K(P_i \oplus C_{i-1})$$

Il server non specifica l'IV, pertanto si utilizza il valore canonico $\text{IV} = \mathbf{0}^{64}$ (8 byte nulli), ovvero:

$$\text{IV} = \texttt{0000000000000000}$$

```python
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

key = bytes.fromhex('a3fc337c90c03f3a')
iv  = b'\x00' * 8
pt  = 'La lunghezza di questa frase non è divisibile per 8'.encode('utf-8')

cipher = DES.new(key, DES.MODE_CBC, iv)
ct = cipher.encrypt(pad(pt, 8, style='x923'))
print(ct.hex())
```

**Output:**
```
a0e9487b1c1fafcd87a5c5845e1e0a8918baae80a4a1fe59f7456d13c0bcaa5b115ba060da82e6965e3659f554e03c9eb416d41494b4a2be
```

---

### Step 2 — AES-256-CFB con padding PKCS#7

Il server fornisce:
- **Cipher:** AES-256 (blocchi da 128 bit = 16 byte, chiave da 256 bit = 32 byte)
- **Mode:** CFB (Cipher Feedback) con segment size = 24 bit
- **Plaintext:** `Mi chiedo cosa significhi il numero nel nome di questo algoritmo.`
- **Padding:** PKCS#7 (block size = 16)
- **Scelta:** il server delega a noi la scelta di chiave e IV

**Analisi del padding PKCS#7.** Sia $\ell = 65$ byte. Il padding è:

$$n = 16 - (65 \bmod 16) = 16 - 1 = 15$$

Ogni byte di padding vale $n$:

$$P' = P \| \underbrace{0\text{F} \cdots 0\text{F}}_{15}$$

**Analisi di CFB con segment size $s$.** In modalità CFB il keystream è generato cifrando il registro di shift $SR$:

$$O_i = E_K(SR_i)$$

I primi $s$ bit di $O_i$ vengono XORati con i successivi $s$ bit di plaintext:

$$C_i = P_i \oplus O_i[0:s]$$

Il registro viene aggiornato shiftando: $SR_{i+1} = (SR_i \ll s) \| C_i$.

Con $s = 24$ bit = 3 byte, ogni iterazione processa 3 byte di plaintext.

Si sceglie chiave e IV tutti nulli per semplicità:

$$K = \mathbf{0}^{256}, \qquad \text{IV} = \mathbf{0}^{128}$$

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = b'\x00' * 32
iv  = b'\x00' * 16
pt  = 'Mi chiedo cosa significhi il numero nel nome di questo algoritmo.'.encode('utf-8')

cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=24)
ct = cipher.encrypt(pad(pt, 16, style='pkcs7'))
print(ct.hex())
```

**Output:**
```
91fce047764172cde0cd3bab1d197ac2a7cb9ee96562e95e6f4664d25009ba2f051bffb79db7655902a378e3085c745c987440adfb30cbed677120b437e7f9e3412d6e7b4534250cb0c51b3632e16dcf
```

---

### Step 3 — Decifratura ChaCha20

Il server fornisce:
- **Cipher:** ChaCha20 (stream cipher, nessun padding)
- **Key:** `dae63562689a68d48cb5f6836f0d7f3f637b2d3ca78f04f238d959c327b64640`
- **Ciphertext:** `4767f0f7e5d321260199293b6b5efb6f0553a9c893817190a3cb4de0`
- **Nonce:** `4dbbca0e8bc2506f`

**Analisi di ChaCha20.** ChaCha20 è uno stream cipher: genera un keystream $\mathbf{k}$ deterministico a partire da chiave $K$ e nonce $N$, quindi cifra con XOR:

$$C = P \oplus \mathbf{k}(K, N)$$

Poiché XOR è la sua stessa inversa, la decifratura è identica alla cifratura:

$$P = C \oplus \mathbf{k}(K, N)$$

Non è richiesto padding in quanto ChaCha20 opera byte per byte.

```python
from Crypto.Cipher import ChaCha20

key   = bytes.fromhex('dae63562689a68d48cb5f6836f0d7f3f637b2d3ca78f04f238d959c327b64640')
ct    = bytes.fromhex('4767f0f7e5d321260199293b6b5efb6f0553a9c893817190a3cb4de0')
nonce = bytes.fromhex('4dbbca0e8bc2506f')

cipher = ChaCha20.new(key=key, nonce=nonce)
print(cipher.decrypt(ct).decode('ascii'))
```

**Output:**
```
Decrypting with mambo rhythm
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> La scelta della modalità operativa è tanto importante quanto la scelta dell'algoritmo: CBC, CFB e gli stream cipher hanno proprietà, requisiti e vulnerabilità radicalmente diverse.

I tre quesiti illustrano altrettanti paradigmi fondamentali della crittografia simmetrica:

1. **Block cipher con padding deterministico (DES-CBC + X9.23):** la modalità CBC introduce dipendenza sequenziale tra i blocchi tramite $C_i = E_K(P_i \oplus C_{i-1})$; il padding X9.23 garantisce che la lunghezza del messaggio sia sempre un multiplo del blocco. L'IV nullo è accettabile in un tutorial ma catastrofico in produzione: due messaggi con lo stesso primo blocco produrrebbero lo stesso $C_1$.

2. **Block cipher in modalità stream (AES-256-CFB):** CFB trasforma un block cipher in uno stream cipher tramite feedback del ciphertext nel registro di shift; il parametro `segment_size` determina la granularità dell'elaborazione. PKCS#7 è richiesto per portare il plaintext a lunghezza multipla del blocco prima della cifratura, pur operando poi a segmenti di 3 byte.

3. **Stream cipher nativo (ChaCha20):** la struttura $C = P \oplus \mathbf{k}(K,N)$ rende cifratura e decifratura identiche; il nonce deve essere **unico per ogni messaggio** con la stessa chiave, riutilizzarlo esporrebbe lo XOR dei plaintext, riproducendo esattamente la vulnerabilità del Many-Time Pad.