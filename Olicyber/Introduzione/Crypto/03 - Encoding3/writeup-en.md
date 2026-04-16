# Encoding 3

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

Data is often represented as integers in cryptography. In this challenge the flag is split in two parts: the first is Base64-encoded, the second is an integer in base 10 that must be converted to bytes (big-endian).

```
ZmxhZ3t3NDF0XzF0c19hbGxfYjE=
664813035583918006462745898431981286737635929725
```

---

## Solution

### Step 1 — Base64 decode

Base64 encodes byte sequences into 64 printable ASCII characters. Decode the first part with `b64decode`:

```py
from base64 import b64decode
part1 = b64decode('ZmxhZ3t3NDF0XzF0c19hbGxfYjE=').decode()
```

This yields the opening `flag{...`.

---

### Step 2 — Integer to bytes (big-endian)

Convert the decimal integer to a big-endian byte sequence and decode to text:

```py
n = 664813035583918006462745898431981286737635929725
part2 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
```

This yields the closing `...}`.

---

### Script

```py
from base64 import b64decode

part1 = b64decode('ZmxhZ3t3NDF0XzF0c19hbGxfYjE=').decode()
n = 664813035583918006462745898431981286737635929725
part2 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
print(part1 + part2)
```

Output:

```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Notes

- Base64 is a reversible representation, not encryption.
- Big-endian (network byte order) is the standard for cryptographic integers (RSA/DSA/ECDSA).
