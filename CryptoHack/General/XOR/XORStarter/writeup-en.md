# XOR Starter

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> XOR each character of the string `label` with the integer 13. Convert the resulting integers back to a string and submit the flag as `crypto{new_string}`.

The challenge is solved entirely with a short Python one-liner.

---

## Theoretical Background

### The XOR operator

XOR (*exclusive or*) is a binary bitwise operator defined by the following truth table:

| $a$ | $b$ | $a \oplus b$ |
|:---:|:---:|:---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

For multi-bit integers, XOR is applied **bit by bit** to each corresponding pair of bits. For example:

$$0110_2 \oplus 1010_2 = 1100_2$$

### XOR of a string with an integer key

Given a string $S = s_0 s_1 \cdots s_{n-1}$ and an integer key $k$, the XOR cipher produces the output string $S' = s'_0 s'_1 \cdots s'_{n-1}$ where each character is transformed as:

$$s'_i = \phi\!\left(\phi^{-1}(s_i) \oplus k\right)$$

with $\phi^{-1}$ mapping a character to its Unicode code point and $\phi$ mapping a code point back to a character.

---

## Solution

### Worked computation

The key is $k = 13 = 00001101_2$. Each character of `label` is processed as follows:

| $i$ | $s_i$ | $\phi^{-1}(s_i)$ | Binary | $\oplus\ 00001101$ | Result | $s'_i$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | `l` | 108 | $01101100$ | $01100001$ | 97 | `.` |
| 1 | `a` | 97 | $01100001$ | $01101100$ | 108 | `.` |
| 2 | `b` | 98 | $01100010$ | $01101111$ | 111 | `.` |
| 3 | `e` | 101 | $01100101$ | $01101000$ | 104 | `.` |
| 4 | `l` | 108 | $01101100$ | $01100001$ | 97 | `.` |

Note that `l` $\oplus$ 13 = `a` and `a` $\oplus$ 13 = `l`: the two characters are each other's XOR image under key 13, a direct consequence of the self-inverse property $(\phi^{-1}(s_i) \oplus k) \oplus k = \phi^{-1}(s_i)$.

### Script

```python
#!/usr/bin/env python3

message = "label"
key = 13

print("".join(chr(ord(c) ^ key) for c in message))
```

The expression `ord(c) ^ key` computes $\phi^{-1}(s_i) \oplus k$, and `chr()` maps the result back to the corresponding character. `"".join()` concatenates all characters into the final string.

---

### Flag

```
crypto{...}
```

---

## Conclusions

This challenge introduces XOR at the character level, the simplest possible form of a **stream cipher**: a fixed key byte is XOR-ed with each byte of the plaintext in sequence.

**Invertibility.** Since $\phi^{-1}(s'_i) \oplus k = (\phi^{-1}(s_i) \oplus k) \oplus k = \phi^{-1}(s_i)$, encryption and decryption are the same operation. The same function with the same key recovers the original string.