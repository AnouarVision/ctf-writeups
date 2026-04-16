# XOR 2

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

When the key is short and repeated, XOR encryption becomes vulnerable to brute force. This challenge provides a ciphertext XORed with a single-byte key. The plaintext does not include `flag{...}` — build the flag as `flag{` + plaintext + `}`.

```
ciphertext = 104e137f425954137f74107f525511457f5468134d7f146c4c
```

---

## Solution

### Step 1 — Keyspace size

The key is a single byte, so |K| = 2^8 = 256. Brute force over 256 candidates is trivial: try each key and check for printable ASCII.

### Step 2 — Decrypt

For each candidate `k` compute `pt = bytes(b ^ k for b in ct)`. Accept plaintexts whose bytes are all printable ASCII (32..126).

### Step 3 — Script

```python
ct = bytes.fromhex('104e137f425954137f74107f525511457f5468134d7f146c4c')

for key in range(256):
    pt = bytes(b ^ key for b in ct)
    try:
        text = pt.decode('ascii')
        if all(32 <= ord(c) < 127 for c in text):
            print(f"key=0x{key:02x}: {text}")
    except UnicodeDecodeError:
        pass
```

Output shows the readable plaintext for `key = 0x20` (32).

---

## Flag

```
flag{...}
```

---

## Notes

- A one-byte key reduces the OTP to a Caesar-like cipher over bytes; the keyspace collapse makes brute force trivial.
- Always use a key at least as long as the message for OTP security, or use a secure stream cipher with a large seed.
