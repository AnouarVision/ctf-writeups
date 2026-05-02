# ASCII

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Convert the following integer array to its corresponding ASCII characters to obtain the flag.
> `[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`

No script is provided this time. The challenge supplies a raw list of integers and asks us to decode it manually or programmatically using Python's `chr()` function.

---

## The ASCII Standard

**ASCII** (*American Standard Code for Information Interchange*) is a 7-bit character encoding standard that maps the integers $\{0, 1, \dots, 127\}$ to a fixed set of characters. Formally, it defines a bijection:

$$\phi : \{0, 1, \dots, 127\} \to \Sigma$$

where $\Sigma$ is the ASCII character set, which includes control characters (0–31), printable characters (32–126), and the delete character (127).

### Structure of the encoding

The 128 code points are organised as follows:

| Range | Content |
|:---:|:---|
| $0 - 31$ | Non-printable control characters (newline, tab, etc.) |
| $32 - 47$ | Space and punctuation symbols |
| $48 - 57$ | Decimal digits `0`–`9` |
| $65 - 90$ | Uppercase Latin letters `A`–`Z` |
| $97 - 122$ | Lowercase Latin letters `a`–`z` |
| $123 - 126$ | Punctuation: `{`, `\|`, `}`, `~` |

Two noteworthy arithmetic relationships are worth remembering:

$$\phi^{-1}(\texttt{A}) = 65, \quad \phi^{-1}(\texttt{a}) = 97 \implies \phi^{-1}(\texttt{a}) - \phi^{-1}(\texttt{A}) = 32$$

The difference between a lowercase letter and its uppercase counterpart is always exactly 32, which corresponds to flipping bit 5 of the binary representation.

---

## Solution

### The decoding map

Given the integer array $\mathbf{v} = (v_0, v_1, \dots, v_{n-1})$, the flag is obtained by applying the ASCII decoding function $\phi$ element-wise and concatenating the results:

$$\text{flag} = \phi(v_0) \,\|\, \phi(v_1) \,\|\, \cdots \,\|\, \phi(v_{n-1})$$

In Python, $\phi$ is implemented by the built-in `chr()` function, while its inverse $\phi^{-1}$ is implemented by `ord()`.

### Script

```python
#!/usr/bin/env python3

ascii_codes = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

print("".join(chr(code) for code in ascii_codes))
```

The list comprehension iterates over each integer `code` in `ascii_codes`, applies `chr()` to obtain the corresponding character, and `"".join()` concatenates all characters into a single string.

### Full decoding table

| $i$ | $v_i$ | $\phi(v_i)$ |
|:---:|:---:|:---:|
| 0 | 99 | `c` |
| 1 | 114 | `r` |
| 2 | 121 | `y` |
| 3 | 112 | `p` |
| 4 | 116 | `t` |
| 5 | 111 | `o` |
| 6 | 123 | `{` |
| 7 | 65 | `.` |
| 8 | 83 | `.` |
| 9 | 67 | `.` |
| 10 | 73 | `.` |
| 11 | 73 | `.` |
| 12 | 95 | `.` |
| 13 | 112 | `.` |
| 14 | 114 | `.` |
| 15 | 49 | `.` |
| 16 | 110 | `.` |
| 17 | 116 | `.` |
| 18 | 52 | `.` |
| 19 | 98 | `.` |
| 20 | 108 | `.` |
| 21 | 51 | `.` |
| 22 | 125 | `}` |

---

### Flag

```
crypto{...}
```