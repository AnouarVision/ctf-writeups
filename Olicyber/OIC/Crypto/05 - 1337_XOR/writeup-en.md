# 1337_XOR

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

> I encrypted my flag. The key is too long to brute-force, sorry you won't be able to decrypt it :D

Two files are provided: `encrypt.py` (the encryption code) and `output.txt` (the ciphertext in hex).

---

## Code analysis

Excerpt (relevant lines):

```python
key = os.urandom(6)
xor(FLAG, key * (len(FLAG)//len(key) + 1)).hex()
```

The key is a random 6-byte value (`os.urandom(6)`) repeated to cover the plaintext length. Encryption is byte-wise XOR:

```
C[i] = P[i] ⊕ K[i mod 6]
```

where `P` is plaintext, `K` is the 6-byte key, and `C` is the ciphertext.

---

## Solution

### Step 1 — Math model

Let $P\in\{0,...,255\}^n$ be the plaintext, $K\in\{0,...,255\}^6$ the key, and $C\in\{0,...,255\}^n$ the ciphertext. The encryption map is

$$C_i = P_i \oplus K_{i \bmod 6} \qquad \forall i$$

XOR is its own inverse: $(a\oplus b)\oplus b = a$.

### Step 2 — Known-plaintext attack

The flag format is known: `flag{...}`. That gives 5 known bytes at positions $i=0..4$:

```
P[0:5] = 0x66 0x6c 0x61 0x67 0x7b  # 'f','l','a','g','{'
```

Therefore for $i=0..4$:

$$K_{i} = C_i \oplus P_i$$

This recovers 5 of the 6 key bytes. The remaining byte $K_5$ can be brute-forced over 256 possibilities — trivial compared to brute-forcing the full 6-byte key space.

### Step 3 — Verify candidate

For each candidate for the sixth byte, reconstruct the full key and XOR-decrypt the ciphertext. The correct key yields an ASCII-printable plaintext ending with `}`.

### Step 4 — Script

```python
ciphertext = bytes.fromhex("27893459dc8772d66261ff8633ba1e5097c10fba257293872fd2664690e975d2015fc4fd3c")

known = b"flag{"
key_partial = bytes([known[i] ^ ciphertext[i] for i in range(5)])

for b in range(256):
    key_candidate = key_partial + bytes([b])
    plaintext = bytes([ciphertext[i] ^ key_candidate[i % 6] for i in range(len(ciphertext))])
    try:
        s = plaintext.decode('ascii')
        if s.endswith('}') and all(32 <= c < 127 for c in plaintext):
            print(f"Key: {key_candidate.hex()}")
            print(f"Flag: {s}")
    except:
        pass
```

---

## Flag

```
flag{...}
```

---

## Conclusions

1. XOR is involutive: known plaintext reveals key bytes directly.
2. Reusing a short key across a long message is insecure — periodicity lets you attack each key position independently.
3. Key length alone isn't sufficient: a repeated 6-byte key is far from a One-Time Pad.
