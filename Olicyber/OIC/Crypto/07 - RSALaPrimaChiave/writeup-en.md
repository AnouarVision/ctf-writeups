# RSA: The First Key

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

> I received this data but I don't know how to use it. Can you help?

A file `dati.txt` is provided containing an RSA public key `(n, e)` and a list of 37 encrypted integers. The goal is to recover the plaintext message.

---

## Data analysis

```
e = 65537
n = 11599469215086283756239000323368207328888145111801687279952858519692571454576743213591474246385542521855249880051364427742007447330667804421622274846205769
c = [5880792219702857..., 4976972096947215..., ...]  # 37 values
```

Immediate observations:
- There are **37 ciphertexts** but only **20 distinct values**, many characters repeat.
- Encryption was done with textbook RSA, without padding.
- Each ciphertext represents **a single ASCII character**.

---

## Solution

### Step 1 — Vulnerability: codebook attack

RSA encryption of a message `m` with public key `(n, e)` is:

$$c = m^e \bmod n$$

If each message block is a single ASCII character, then $m \in \{32,\ldots,126\}$ (95 possible values). The plaintext space is therefore small and enumerable: an attacker can precompute a reverse dictionary:

$$\mathcal{D} = \{ m^e \bmod n \mapsto m \;|\; m \in [32,126] \}$$

Each ciphertext `c_i` is looked up in `\mathcal{D}` to recover the corresponding character. This is a classical codebook attack: with at most 95 modular exponentiations the whole message can be recovered.

The presence of only 20 distinct ciphertext values among 37 confirms the hypothesis; high-frequency characters (e.g. `_`, `e`, `3`) repeat as expected in natural text.

### Step 2 — Exploit (example)

```python
import ast

with open('dati.txt') as f:
    lines = f.read().strip().splitlines()

e = int(lines[0].split('=')[1].strip())
n = int(lines[1].split('=')[1].strip())
c = ast.literal_eval(lines[2].split('=', 1)[1].strip())

lookup = {pow(m, e, n): chr(m) for m in range(32, 127)}

flag = ''.join(lookup.get(ci, '?') for ci in c)
print(flag)
```

**Output:**
```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusions

> RSA without padding on very short messages is completely insecure: the deterministic structure of textbook RSA makes predictable plaintext map to predictable ciphertext.

Key takeaways:

1. **RSA is deterministic:** with the same key, the same message always produces the same ciphertext. Identical characters therefore map to identical ciphertexts, enabling frequency analysis.

2. **Padding is mandatory:** schemes like PKCS#1 v1.5 or OAEP introduce randomness so the same plaintext encrypts to different ciphertexts. Without padding RSA fails IND-CPA.

3. **Don't encrypt single characters with RSA:** use hybrid encryption, generate a random symmetric key, encrypt it with RSA-OAEP, and use AES (or another symmetric cipher) to encrypt the message.
