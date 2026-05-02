# Bytes and Big Integers

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Convert the following integer back into a message:
> `11515195063862318899931685488813747395775516287289682636499965282714637259206269`

A large decimal integer is provided. The challenge requires converting it back into the original ASCII message using PyCryptodome's `long_to_bytes()` function.

---

## From Messages to Numbers

### The encoding convention

Cryptosystems such as RSA operate on elements of $\mathbb{Z}_n$ — that is, on integers. Plaintext messages, however, are sequences of characters. A canonical and reversible way to map a message $M = m_0 m_1 \cdots m_{k-1}$ into an integer $N$ proceeds in three steps:

**Step 1.** Convert each character to its ASCII code point:

$$v_i = \phi^{-1}(m_i) \in \{0, \dots, 127\} \qquad \forall\, i \in \{0, \dots, k-1\}$$

**Step 2.** Express each code point as a two-digit hexadecimal value and concatenate:

$$H = h_0 \,\|\, h_1 \,\|\, \cdots \,\|\, h_{k-1}, \qquad h_i = \text{hex}(v_i)$$

**Step 3.** Interpret the resulting hex string as a base-16 integer:

$$N = \sum_{i=0}^{k-1} v_i \cdot 256^{k-1-i}$$

This is equivalent to treating the byte sequence as a **big-endian** unsigned integer: the first byte occupies the most significant position.

### Illustrative example

For the string `HELLO`:

| Character | ASCII | Hex |
|:---:|:---:|:---:|
| `H` | 72 | `48` |
| `E` | 69 | `45` |
| `L` | 76 | `4c` |
| `L` | 76 | `4c` |
| `O` | 79 | `4f` |

Concatenated hex: `48454c4c4f`

Decimal value:

$$N = 72 \cdot 256^4 + 69 \cdot 256^3 + 76 \cdot 256^2 + 76 \cdot 256^1 + 79 \cdot 256^0 = 310400273487$$

### The inverse operation

Given an integer $N$, the original byte sequence is recovered by repeatedly extracting the least significant byte and dividing by 256:

$$b_{k-1} = N \bmod 256, \quad N \leftarrow \lfloor N / 256 \rfloor$$

repeating until $N = 0$, then reversing the collected bytes. This is precisely what `long_to_bytes()` implements internally.

More compactly, $N$ expressed in base 16 gives back the concatenated hex string directly, which is then split into byte pairs and decoded via $\phi$.

---

## Solution

### Script

```python
#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes

ciphertext_int = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

print(long_to_bytes(ciphertext_int))
```

`long_to_bytes()` converts the integer to its big-endian byte representation, then Python prints it as an ASCII string.

### Verification

To verify the result manually, convert the integer to hexadecimal:

$$11515195063862318899931685488813747395775516287289682636499965282714637259206269_{10} = \texttt{63727970746f7b336e633064316e365f62336e645f6e756d355f6e5f627974337d}_{16}$$

Splitting into byte pairs and applying $\phi$:

| Hex | Decimal | Character |
|:---:|:---:|:---:|
| `63` | 99 | `c` |
| `72` | 114 | `r` |
| `79` | 121 | `y` |
| `70` | 112 | `p` |
| `74` | 116 | `t` |
| `6f` | 111 | `o` |
| `7b` | 123 | `{` |
| `33` | 51 | `3` |
| `6e` | 110 | `n` |
| `63` | 99 | `c` |
| `30` | 48 | `0` |
| `64` | 100 | `d` |
| `31` | 49 | `1` |
| `6e` | 110 | `n` |
| `36` | 54 | `6` |
| `5f` | 95 | `_` |
| `62` | 98 | `b` |
| `33` | 51 | `3` |
| `6e` | 110 | `n` |
| `64` | 100 | `d` |
| `5f` | 95 | `_` |
| `6e` | 110 | `n` |
| `75` | 117 | `u` |
| `6d` | 109 | `m` |
| `35` | 53 | `5` |
| `5f` | 95 | `_` |
| `6e` | 110 | `n` |
| `5f` | 95 | `_` |
| `62` | 98 | `b` |
| `79` | 121 | `y` |
| `74` | 116 | `t` |
| `33` | 51 | `3` |
| `7d` | 125 | `}` |

---

### Flag

```
crypto{3nc0d1n6_b3nd_num5_n_byt3}
```

---

## Conclusions

This challenge formalises the **message-to-integer** conversion that underpins every algebraic cryptosystem. In RSA, for instance, plaintext is an integer $m \in \mathbb{Z}_n$ and encryption is the modular exponentiation $c = m^e \bmod n$. For this to make sense, the original string must first be converted into $m$ via the procedure described above, a step known in the literature as **encoding**.

Two functions from PyCryptodome to commit to memory: `bytes_to_long(b)` converts a `bytes` object to its integer representation; `long_to_bytes(n)` performs the inverse. Both treat the byte sequence as big-endian, which is the standard convention in cryptographic protocols.