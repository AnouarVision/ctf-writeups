# PyCryptutorial 1

**Competition:** OliCyber <br>
**Category:** Crypto <br>
**Service:** `nc crypto-07.challs.olicyber.it 30000`

---

## Description

> PyCryptodome is a library you will often see in crypto challenges: knowing its structure and basic modules is important.

The server presents three tasks in sequence, each requiring encrypting or decrypting a message with a different algorithm using the `pycryptodome` library. Correctly answering all three returns the flag.

---

## Solution

### Step 1 — DES-CBC with X9.23 padding

The server provides:
- **Cipher:** DES (block size 64 bits = 8 bytes)
- **Mode:** CBC (Cipher Block Chaining)
- **Key:** `a3fc337c90c03f3a`
- **Plaintext:** `La lunghezza di questa frase non è divisibile per 8`
- **Padding:** X9.23

Let $\ell = |P|$ be the plaintext length in bytes and $b=8$ the DES block size. The number of padding bytes is:

$$n = b - (\ell \bmod b) = 8 - (52 \bmod 8) = 8 - 4 = 4$$

X9.23 fills the first $n-1$ bytes with zeros and the last byte with the value $n$:

$$P' = P \| \underbrace{00\,00\,00}_{n-1\ text{ zeros}} \| \underbrace{04}_{n}$$

CBC mode: each plaintext block $P_i$ is XORed with the previous ciphertext block before encryption:

$$C_0 = \text{IV}, \qquad C_i = E_K(P_i \oplus C_{i-1})$$

The server does not specify the IV, so we use the canonical zero IV $\text{IV} = \mathbf{0}^{64}$ (8 null bytes):

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

### Step 2 — AES-256-CFB with PKCS#7 padding

The server provides:
- **Cipher:** AES-256 (block size 128 bits = 16 bytes, key 256 bits = 32 bytes)
- **Mode:** CFB with segment size = 24 bit
- **Plaintext:** `Mi chiedo cosa significhi il numero nel nome di questo algoritmo.`
- **Padding:** PKCS#7 (block size = 16)
- **Choice:** we select key and IV

PKCS#7 padding: with $\ell = 65$ bytes,

$$n = 16 - (65 \bmod 16) = 16 - 1 = 15$$

Each padding byte equals $n$:

$$P' = P \| \underbrace{0\text{F} \cdots 0\text{F}}_{15}$$

CFB with segment size $s$: the keystream is produced by encrypting the shift register $SR$:

$$O_i = E_K(SR_i)$$
$$C_i = P_i \oplus O_i[0:s]$$
$$SR_{i+1} = (SR_i \ll s) \| C_i$$

With $s = 24$ bits = 3 bytes, each iteration processes 3 plaintext bytes.

We choose key and IV as all zeros for simplicity:

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

### Step 3 — ChaCha20 decryption

The server provides:
- **Cipher:** ChaCha20 (stream cipher, no padding)
- **Key:** `dae63562689a68d48cb5f6836f0d7f3f637b2d3ca78f04f238d959c327b64640`
- **Ciphertext:** `4767f0f7e5d321260199293b6b5efb6f0553a9c893817190a3cb4de0`
- **Nonce:** `4dbbca0e8bc2506f`

ChaCha20 generates a keystream $\mathbf{k}$ from key $K$ and nonce $N$, then XORs with plaintext:

$$C = P \oplus \mathbf{k}(K,N)$$

Decryption is identical to encryption:

$$P = C \oplus \mathbf{k}(K,N)$$

No padding is required since ChaCha20 operates bytewise.

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

## Conclusions

> The mode of operation is as important as the choice of algorithm: CBC, CFB and stream ciphers have fundamentally different properties, requirements and vulnerabilities.

The three tasks illustrate three symmetric cryptography paradigms:

1. **Block cipher with deterministic padding (DES-CBC + X9.23):** CBC introduces sequential dependency between blocks via $C_i = E_K(P_i \oplus C_{i-1})$; X9.23 ensures block-aligned length. A zero IV is acceptable in a tutorial but catastrophic in production: two messages with the same first block yield the same $C_1$.

2. **Block cipher used in stream mode (AES-256-CFB):** CFB turns a block cipher into a stream-like construction via ciphertext feedback; `segment_size` sets processing granularity. PKCS#7 is used to pad the plaintext to a multiple of the block size before encryption even if processing is done in segments.

3. **Native stream cipher (ChaCha20):** $C = P \oplus \mathbf{k}(K,N)$ makes encryption and decryption identical; the nonce must be unique per message under the same key, otherwise reuse exposes plaintext XORs and reproduces the Many-Time Pad vulnerability.
