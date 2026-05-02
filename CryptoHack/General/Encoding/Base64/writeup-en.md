# Base64

**Competition:** CryptoHack<br>
**Category:** Crypto / Introduction

---

## Description

> Take the hex string below, decode it into bytes and then encode it into Base64.
> `72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf`

---

## The Base64 Encoding

### Alphabet and bit grouping

**Base64** is a binary-to-text encoding scheme that represents arbitrary binary data as a string of printable ASCII characters. Its alphabet consists of exactly 64 symbols:

$$\mathcal{A} = \{\texttt{A}\text{–}\texttt{Z},\ \texttt{a}\text{–}\texttt{z},\ \texttt{0}\text{–}\texttt{9},\ \texttt{+},\ \texttt{/}\}$$

Since $|\mathcal{A}| = 64 = 2^6$, each Base64 character encodes exactly **6 bits** of binary data. The encoding operates on groups of **3 bytes** (24 bits) at a time, mapping them to **4 Base64 characters**:

$$3 \text{ bytes} \times 8 \text{ bits/byte} = 24 \text{ bits} = 4 \times 6 \text{ bits} \longrightarrow 4 \text{ Base64 characters}$$

This gives an expansion ratio of $\frac{4}{3}$: every 3 bytes of input produce 4 characters of output.

### Formal encoding procedure

Given a byte sequence $B = (b_0, b_1, b_2)$, the four Base64 indices $i_0, i_1, i_2, i_3 \in \{0, \dots, 63\}$ are obtained by partitioning the 24-bit concatenation $b_0 \,\|\, b_1 \,\|\, b_2$ into four 6-bit groups:

$$i_0 = b_0 \gg 2$$

i1 = ((b0 & 0x03) << 4) | (b1 >> 4)

i2 = ((b1 & 0x0F) << 2) | (b2 >> 6)

i3 = b2 & 0x3F

Each index $i_k$ is then mapped to its corresponding character in $\mathcal{A}$.

### Padding

When the total number of bytes is not a multiple of 3, the final group is padded with zero bits and one or two `=` characters are appended to the output to signal the padding:

- 1 remaining byte $\to$ 2 Base64 chars $+$ `==`
- 2 remaining bytes $\to$ 3 Base64 chars $+$ `=`

In this challenge, the input is 27 bytes ($27 = 9 \times 3$), so no padding is required.

### Worked example

Consider the first three bytes of the hex string `72bca9`:

$$\texttt{72}_{16} = 114_{10} = 01110010_2$$
$$\texttt{bc}_{16} = 188_{10} = 10111100_2$$
$$\texttt{a9}_{16} = 169_{10} = 10101001_2$$

Concatenating the 24 bits: $011100101011110010101001$

Splitting into four 6-bit groups:

| Group | Bits | Index | $\mathcal{A}[\cdot]$ |
|:---:|:---:|:---:|:---:|
| $i_0$ | $011100$ | $28$ | `c` |
| $i_1$ | $101011$ | $43$ | `r` |
| $i_2$ | $110010$ | $50$ | `y` |
| $i_3$ | $101001$ | $41$ | `p` |

The first four characters of the Base64 output are `cryp`, consistent with the flag prefix `crypto/`.

---

## Solution

### The two-step pipeline

The full transformation can be expressed as the composition:

output = Base64(fromHex(hex_string))

**Step 1.** Decode the hex string into a `bytes` object using `bytes.fromhex()`.

**Step 2.** Encode the resulting bytes into Base64 using `base64.b64encode()`.

### Script

```python
#!/usr/bin/env python3

import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

raw_bytes = bytes.fromhex(hex_string)

print(base64.b64encode(raw_bytes))
```

`bytes.fromhex()` converts each hex pair to the corresponding byte value. `base64.b64encode()` takes the resulting `bytes` object and returns its Base64 encoding as a `bytes` object containing only printable ASCII characters.

---

### Flag

```
crypto/.../
```
