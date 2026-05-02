# Hex

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Decode the following hex string back into bytes to obtain the flag.
> `63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d`

No script is provided. The challenge supplies a raw hexadecimal string and asks us to convert it back to its ASCII representation using Python's `bytes.fromhex()` function.

---

## The Hexadecimal Encoding

### Positional notation and base-16

The decimal system uses base 10, representing numbers as linear combinations of powers of 10. The **hexadecimal** system uses base 16, representing numbers as linear combinations of powers of 16. Each digit takes one of 16 possible values, denoted by the symbols $\{0, 1, 2, \dots, 9, A, B, C, D, E, F\}$, where $A = 10, B = 11, \dots, F = 15$.

A hexadecimal number of $n$ digits $d_{n-1} d_{n-2} \cdots d_1 d_0$ has the following decimal value:

$$N = \sum_{i=0}^{n-1} d_i \cdot 16^i$$

### Bytes and hex pairs

A **byte** is an 8-bit quantity, capable of representing $2^8 = 256$ distinct values, ranging from $0_{10}$ to $255_{10}$. In hexadecimal, this corresponds to the range $\texttt{00}_{16}$ to $\texttt{FF}_{16}$: exactly two hexadecimal digits are sufficient and necessary to represent any single byte. This is why hexadecimal is the natural choice for byte-level data representation.

### From ASCII to hex

The encoding process for an ASCII string $s = s_0 s_1 \cdots s_{n-1}$ proceeds in two steps:

**Step 1.** Convert each character to its ASCII code point via $\phi^{-1}$:

$$v_i = \phi^{-1}(s_i) \in \{0, \dots, 127\} \qquad \forall\, i \in \{0, \dots, n-1\}$$

**Step 2.** Express each code point as a two-digit hexadecimal number:

$$h_i = \text{hex}(v_i) \in \{\texttt{00}, \texttt{01}, \dots, \texttt{7f}\}$$

The final hex string is the concatenation $h_0 \,\|\, h_1 \,\|\, \cdots \,\|\, h_{n-1}$.

### Worked example

Consider the character `c`, the first byte of the flag prefix `crypto{`:

$$\phi^{-1}(\texttt{c}) = 99_{10}$$

Converting 99 to base 16:

$$99 = 6 \cdot 16^1 + 3 \cdot 16^0 \implies 99_{10} = \texttt{63}_{16}$$

Indeed, the hex string begins with `63`. The decoding direction simply reverses this process.

---

## Solution

### Script

```python
#!/usr/bin/env python3

hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"

print(bytes.fromhex(hex_string))
```

`bytes.fromhex()` takes a hexadecimal string, splits it into pairs of digits, converts each pair to the corresponding byte value, and returns a `bytes` object. Printing it directly displays the ASCII representation of those bytes.

### Full decoding table (first 7 bytes)

The flag prefix `crypto{` serves as a verification that the decoding is correct:

| Hex pair | Decimal | $\phi(\cdot)$ |
|:---:|:---:|:---:|
| `63` | 99 | `c` |
| `72` | 114 | `r` |
| `79` | 121 | `y` |
| `70` | 112 | `p` |
| `74` | 116 | `t` |
| `6f` | 111 | `o` |
| `7b` | 123 | `{` |

---

### Flag

```
crypto{...}
```

---

## Conclusions

Two functions to commit to memory: `bytes.fromhex(s)` decodes a hex string into a `bytes` object; the inverse operation, `.hex()`, can be called on any `bytes` object to obtain the corresponding hex string.