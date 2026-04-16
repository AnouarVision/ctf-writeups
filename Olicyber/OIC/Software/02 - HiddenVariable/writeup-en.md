# Hidden Variable

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> I can't find my variable :( can you help me?

An x86-64 ELF binary is provided. At runtime it prints a "corrupted" flag and an error message. The goal is to find the hidden variable that contains the real flag.

---

## Binary analysis

### Step 1 — Initial reconnaissance

```bash
file hidden_variable
# ELF 64-bit LSB pie executable, x86-64, not stripped

strings hidden_variable
# "La tua flag"
# "f_ag{."          ← corrupted flag (decoy)
# "Accidenti, sembra corrotta! Dove avrò lasciato l'originale?"
# "fl4g"            ← suspicious symbol in the symbol table
```

The binary is **not stripped**: the symbol table is present and reveals a `fl4g` symbol in `.data`. The runtime-printed flag is intentionally corrupted as a decoy.

---

### Step 2 — Inspect `.rodata`

`main` prints two strings via `puts`. Inspecting `.rodata` shows:

```
2008: "La tua flag .. f_ag{...#[..."   ← corrupted flag with non-ASCII bytes
2030: "Accidenti, sembra corrotta!..."
```

The string at `0x2008` contains non-ASCII bytes instead of the correct flag characters — a red herring inserted to confuse shallow static analysis.

---

### Step 3 — Inspect `.data` and symbol `fl4g`

```bash
nm hidden_variable | grep fl
# 0000000000004020 D fl4g

objdump -s -j .data hidden_variable
```

At address `0x4020` the data looks like:

```
4020: 66000000 6c000000 61000000 67000000   f...l...a...g...
4030: 7b000000 75000000 6e000000 75000000   {...u...n...u...
4040: 35000000 33000000 64000000 5f000000   5...3...d..._...
...
```

The variable `fl4g` is an **array of 32-bit integers** (`int[]`) in little-endian. Each element holds a single ASCII character in its least significant byte, with the upper three bytes zero. This hides the string from `strings`, which looks for contiguous ASCII bytes — here ASCII bytes are separated by three null bytes.

---

### Step 4 — Reconstruct the flag

Extract the first byte of every 4-byte group:

```python
data = bytes.fromhex(
    '66000000 6c000000 61000000 67000000'
    '7b000000 75000000 6e000000 75000000'
    '35000000 33000000 64000000 5f000000'
    '76000000 34000000 72000000 35000000'
    '5f000000 34000000 72000000 33000000'
    '5f000000 35000000 37000000 31000000'
    '31000000 5f000000 63000000 30000000'
    '6d000000 70000000 31000000 6c000000'
    '33000000 64000000 7d000000'.replace(' ', '')
)
flag = ''.join(chr(data[i]) for i in range(0, len(data), 4))
print(flag)
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

## Conclusions

Unused variables in source code can still be compiled into the binary and remain discoverable via static analysis, especially if the binary is not stripped.

Three key observations:

1. **`strings` is not enough:** the `strings` tool looks for contiguous ASCII runs (default length 4). Storing a string as an `int[]` with one character per 32-bit element separates ASCII bytes with three zeros and hides the string from `strings`. Inspect `.data` with `objdump -s` or use a disassembler (Ghidra) to find this pattern.

2. **Not stripped = symbol table present:** when a binary is not stripped, global variable symbols (`D` entries in `nm`) are available. The `fl4g` symbol revealed the hidden variable's address. Production builds typically use `strip` to remove these symbols and hinder reverse engineering.

3. **The `.rodata` decoy:** the corrupted flag printed at runtime is a basic anti-reversing decoy that may cause an analyst to stop searching. Always perform a systematic inspection of all binary sections before concluding.
