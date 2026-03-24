# the_grocery_leak

**Competition:** ITSCyberGame
**Category:** Crypto
**Files:** Lista_Spesa.ods, secure_encryptor.py, grocery.txt

---

## Description

> We intercepted communications from a group of digital smugglers. They exchange encrypted messages, but the hexadecimal key used to decrypt them appears hidden in plain sight: inside a simple shopping list... yet the numbers don't add up.

Three files are provided: an ODS spreadsheet, the Python script used to encrypt, and a text file with the ciphertext.

---

## File analysis

### secure_encryptor.py

The script reveals the encryption algorithm: a repeated-key XOR with a key of exactly 6 bytes.

```python
def secure_algorithm(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
```

The key must be exactly 6 bytes (12 hex characters).

### grocery2.txt

The ciphertext in hex:

```
7458371fe1db6004354be8c54d473e48eacc235a3127f288715f650ae7
```

### Lista_Spesa1.ods

The spreadsheet contains 20 rows of shopping list entries, each with 6 products. Every row has `Product`, `Qty`, `Price`, `TOTAL`. The `TOTAL` column should be `Qty × Price`, but in many rows it equals `Price + Qty`, the sums don't match, as hinted.

---

## Solution

### Identify anomalous rows

Inspecting the sheet shows some rows where every product has `Qty = 1` and `TOTAL = Price + 1`. In these rows the **prices interpreted as hexadecimal bytes** form recognizable patterns:

| ID | Prices (decimal) | Prices (hex) |
|---:|---|---|
| 5  | 26, 43, 60, 77, 94, 111   | `1a 2b 3c 4d 5e 6f` |
| 7  | 18, 52, 86, 120, 154, 188 | `12 34 56 78 9a bc` |
| 10 | 161, 178, 195, 212, 229, 246 | `a1 b2 c3 d4 e5 f6` |
| 12 | 222, 173, 190, 239, 32, 37 | `de ad be ef 20 25` |
| 16 | 186, 220, 31, 254, 224, 31 | `ba dc 1f fe e0 1f` |
| 18 | 31, 31, 31, 31, 31, 31    | `1f 1f 1f 1f 1f 1f` |
| 19 | 192, 255, 238, 136, 153, 170 | `c0 ff ee 88 99 aa` |

Each special row is a candidate 6-byte key.

### Brute-force candidate keys

```python
ciphertext = bytes.fromhex("7458371fe1db6004354be8c54d473e48eacc235a3127f288715f650ae7")

candidates = {
    "ID5":  "1a2b3c4d5e6f",
    "ID7":  "123456789abc",
    "ID10": "a1b2c3d4e5f6",
    "ID12": "deadbeef2025",
    "ID16": "badc1ffee01f",
    "ID18": "1f1f1f1f1f1f",
    "ID19": "c0ffee8899aa",
}

for name, key_hex in candidates.items():
    key = bytes.fromhex(key_hex)
    decrypted = bytes([ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))])
    print(f"{name} ({key_hex}): {decrypted.decode('utf-8', errors='replace')}")
```

Output:

```
ID5  (1a2b3c4d5e6f): ns\x0bR...  (not readable)
ID7  (123456789abc): flag{...}
ID10 (a1b2c3d4e5f6): ...         (not readable)
...
```

The correct key is the row 7 sequence: `123456789abc`.

---

## Flag

```
flag{...}
```

---

## Conclusions

The key was hidden in the shopping list prices: reading them as hexadecimal bytes, the prices of row 7 form `12 34 56 78 9a bc`. The mismatched totals (`Price + Qty`) were the hint to spot anomalous rows with `Qty = 1`. The encryption was a simple repeated-key XOR with a short fixed-length key (6 bytes), making a brute-force check of a few candidates trivial.
