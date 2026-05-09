# Modes of Operation Starter

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Get acquainted with the API interface and use it to retrieve the flag.

Two API endpoints are available:

- `GET /block_cipher_starter/encrypt_flag/`: encrypts the flag with AES-ECB and returns the ciphertext hex.
- `GET /block_cipher_starter/decrypt/<ciphertext>/`: decrypts any hex ciphertext with the same AES-ECB key and returns the plaintext hex.

---

## Theoretical Background

### ECB Mode (Electronic Codebook)

**ECB** is the simplest AES mode of operation. Each 16-byte block of plaintext is encrypted independently with the same key:

$$C_i = E_k(P_i)$$

Because encryption and decryption are inverses:

$$P_i = D_k(C_i)$$

there is no chaining, no IV, and no randomness between blocks. This has two critical consequences:

1. **Determinism**: the same plaintext block always produces the same ciphertext block under the same key. This leaks structural information about the plaintext (the famous "ECB penguin" problem).
2. **Arbitrary decryption**: anyone with access to the decryption endpoint can decrypt any ciphertext, including the encrypted flag, without ever knowing the key.

This second property is exactly what this challenge exploits.

---

## Solution

The attack is a single two-step interaction with the API:

**Step 1.** Call `encrypt_flag` to obtain the ciphertext of the flag:

```
GET /block_cipher_starter/encrypt_flag/
→ {"ciphertext": "<hex>"}
```

**Step 2.** Pass that ciphertext directly to `decrypt`:

```
GET /block_cipher_starter/decrypt/<hex>/
→ {"plaintext": "<hex>"}
```

**Step 3.** Decode the plaintext hex to ASCII.

### Script

```python
#!/usr/bin/env python3

import requests

BASE = "https://aes.cryptohack.org/block_cipher_starter"

ct = requests.get(f"{BASE}/encrypt_flag/").json()["ciphertext"]
print("Ciphertext:", ct)

pt_hex = requests.get(f"{BASE}/decrypt/{ct}/").json()["plaintext"]
print("Plaintext hex:", pt_hex)

flag = bytes.fromhex(pt_hex).decode()
print("Flag:", flag)
```

---

### Flag

```
crypto{...}
```

---

## Conclusions

This challenge illustrates the most fundamental weakness of ECB mode: **the decryption oracle**. If an attacker has access to a decryption endpoint that uses the same key as the encryption, and the endpoint accepts arbitrary ciphertexts, then no ciphertext is secret, including one produced by the server itself.