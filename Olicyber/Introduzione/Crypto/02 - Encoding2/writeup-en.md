# Encoding 2

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

Hexadecimal encoding (base16) represents bytes as pairs of hex digits. You are given a hex string, convert it to bytes and decode to obtain the flag.

```
666c61677b68337834646563696d616c5f63346e5f62335f41424144424142457d
```

---

## Solution

### Step 1 — Hex encoding

Each byte is two hex characters (two nibbles of 4 bits). A hex string of length 2n represents n bytes. Use `bytes.fromhex()` in Python to convert.

### Step 2 — Decode

```python
s = '666c61677b68337834646563696d616c5f63346e5f62335f41424144424142457d'
print(bytes.fromhex(s).decode())
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

- Hex is a reversible representation of raw bytes, not encryption.
- Hex is compact for human-readable binary digests and keys.
