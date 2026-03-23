# The Answer to the Ultimate Question of Life, the Universe, and Everything

**Competition:** ITSCyberGame
**Category:** Crypto

---

## Description

> The answer to the ultimate question of life, the universe, and everything.
> Sometimes a mathematical operation can look effective but becomes trivial if repeated...
> `1a7e7a751c5f1d75441a5e7558194b1b1b53`

---

## Solution

### Step 1 — Identify the key

The title references *The Hitchhiker's Guide to the Galaxy* by Douglas Adams: the answer to the ultimate question of life, the universe and everything is **42**.

### Step 2 — Identify the operation

The description mentions a "repetitive mathematical operation": XOR byte-by-byte with a fixed key is the most common such operation in CTFs. XORing every byte with the same value is trivial to reverse when the key is known.

### Step 3 — Decrypt

Use XOR with key `42` (decimal, i.e. `0x2A`) on each byte of the hex input:

```python
data = bytes.fromhex('1a7e7a751c5f1d75441a5e7558194b1b1b53')
result = ''.join(chr(b ^ 42) for b in data)
print(result)
```

```bash
$ python3 solve.py
...
```

---

## Flag

```
flag{...}
```
