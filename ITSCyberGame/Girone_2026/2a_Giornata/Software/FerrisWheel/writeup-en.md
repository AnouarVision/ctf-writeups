# ferris_wheel

**Competition:** ITSCyberGame
**Category:** Software
**File:** ferris_wheel_2

---

## Description

> Someone rewrote the ticket validator in Rust to be "memory safe", but inputs now make a strange ride...

The name hints at Rust's mascot (Ferris) and the iterator `.cycle()` used inside the program.

---

## Binary analysis

```bash
file ferris_wheel_2
# ELF 64-bit PIE executable, x86-64, with debug info

checksec --file=ferris_wheel_2
# Full RELRO | No canary | NX enabled | PIE enabled
```

Debug symbols reveal functions and iterator usage: `Bytes`, `cycle`, `zip`, `map`, this suggests a cyclic-key additive scheme.

---

## Reverse engineering `check_flag`

Disassembling the check shows the logic:

- The input length is checked to be 29 bytes.
- The code obtains `input.bytes()` and a 6-byte key, then calls `key.iter().cycle()`.
- It zips `input.bytes()` with the cycled key and maps each pair with `(a + b) & 0xff`.
- The mapped result is zipped with a hardcoded `expected` array and compared with `all(|(a,b)| a == b)`.

In short:

```
for i in 0..29:
    (input[i] + key[i % 6]) & 0xff == expected[i]
```

---

## Extract key and expected bytes

Using the binary's .rodata (addresses shown in the analysis):

```python
with open('ferris_wheel_2','rb') as f:
    data = f.read()

expected = data[0x9c13:0x9c13+29]
key      = data[0x9c30:0x9c30+6]
```

Found values (example):
- Key (6 bytes): `42 13 37 66 01 99`
- Expected (29 bytes): `a8 7f 98 cd 7c fc bb 76 68 97 64 f8 73 87 6a d8 35 0d 72 85 96 d3 35 fd b0 46 aa d9 7e`

---

## Decrypt

Invert the transformation to recover the flag bytes:

```python
flag = bytes((expected[i] - key[i % 6]) % 256 for i in range(29))
print(flag.decode())
```

---

## Flag

```
flag{...}
```

---

## Conclusions

The challenge implements an additive cyclic cipher with a 6-byte key using Rust iterator combinators (`.bytes()`, `.cycle()`, `.zip()`, `.map()`). Because the binary contains debug symbols, extracting the key and expected array from .rodata makes decryption straightforward: subtract the cycled key from the expected bytes modulo 256.
