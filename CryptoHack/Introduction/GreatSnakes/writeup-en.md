# Great Snakes

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Run the provided Python script. It will output your flag.

A Python source file `great_snakes.py` is provided. Simply execute it and read the output.

---

## The XOR Operation

Before examining the script, it is worth recalling the mathematical foundation on which the solution rests.

### Definition

Let $a, b \in \mathbb{Z}$ be two non-negative integers. Their **bitwise XOR**, denoted $a \oplus b$, is defined by applying the logical exclusive-or to each corresponding pair of bits in the binary representation of $a$ and $b$.

Formally, if $a = \sum_{i} a_i \cdot 2^i$ and $b = \sum_{i} b_i \cdot 2^i$ with $a_i, b_i \in \{0, 1\}$, then:

$$a \oplus b = \sum_{i} (a_i \oplus b_i) \cdot 2^i$$

where the single-bit XOR is defined by the truth table:

| $a_i$ | $b_i$ | $a_i \oplus b_i$ |
|:---:|:---:|:---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### Relevant algebraic properties

The XOR operation over $\mathbb{Z}$ satisfies the following properties, which are worth keeping in mind throughout this course:

1. **Commutativity:** $a \oplus b = b \oplus a$
2. **Associativity:** $(a \oplus b) \oplus c = a \oplus (b \oplus c)$
3. **Identity element:** $a \oplus 0 = a$
4. **Self-inverse:** $a \oplus a = 0$

From property 4, a fundamental consequence follows immediately:

$$a \oplus b = c \implies a = c \oplus b$$

This is the **invertibility** of XOR, and it is precisely the property exploited in this challenge.

---

## Script Analysis

```python
ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]

print("".join(chr(o ^ 0x32) for o in ords))
```

The script defines a list of 21 integers $\{o_i\}_{i=0}^{20} \subset \mathbb{Z}$ and applies the following transformation to each element:

$$f(o_i) = \text{chr}(o_i \oplus k), \quad k = 0\text{x}32 = 50_{10}$$

where $\text{chr} : \mathbb{Z} \to \Sigma$ maps a Unicode code point to its corresponding character. The resulting characters are concatenated to form the flag.

### Worked example

Consider the first element of the list: $o_0 = 81$.

**Step 1.** Express both operands in binary:

$$81_{10} = 1010001_2, \qquad 50_{10} = 0110010_2$$

**Step 2.** Apply bitwise XOR column by column:

$$\begin{array}{r} 1010001 \\ \oplus \quad 0110010 \\ \hline 1100011 \end{array}$$

**Step 3.** Convert back to decimal:

$$1100011_2 = 2^6 + 2^5 + 2^1 + 2^0 = 64 + 32 + 2 + 1 = 99_{10}$$

**Step 4.** Map to character:

$$\text{chr}(99) = \texttt{c}$$

The same procedure applied to every $o_i$ yields the sequence of characters that compose the flag.

### Full decoding

Applying $f(o_i) = \text{chr}(o_i \oplus 50)$ to all 21 elements:

| $i$ | $o_i$ | $o_i \oplus 50$ | $\text{chr}(\cdot)$ |
|:---:|:---:|:---:|:---:|
| 0 | 81 | 99 | `c` |
| 1 | 64 | 114 | `r` |
| 2 | 75 | 121 | `y` |
| 3 | 66 | 112 | `p` |
| 4 | 70 | 116 | `t` |
| 5 | 93 | 111 | `o` |
| 6 | 73 | 123 | `{` |
| 7 | 72 | 122 | `z` |
| 8 | 1 | 51 | `3` |
| 9 | 92 | 110 | `n` |
| 10 | 109 | 95 | `_` |
| 11 | 2 | 48 | `0` |
| 12 | 84 | 102 | `f` |
| 13 | 109 | 95 | `_` |
| 14 | 66 | 112 | `p` |
| 15 | 75 | 121 | `y` |
| 16 | 70 | 116 | `t` |
| 17 | 90 | 104 | `h` |
| 18 | 2 | 48 | `0` |
| 19 | 92 | 110 | `n` |
| 20 | 79 | 125 | `}` |

---

### Flag

```
crypto{z3n_0f_pyth0n}
```

---

## Conclusions

This challenge illustrates one of the most elementary cryptographic primitives: **single-key XOR encoding**. Given a ciphertext vector $\mathbf{c} = (c_0, c_1, \dots, c_{n-1})$ and a known key $k$, the plaintext is recovered by applying the same operation again:

$$p_i = c_i \oplus k \qquad \forall\, i \in \{0, \dots, n-1\}$$

This follows directly from the self-inverse property: $(c_i \oplus k) \oplus k = c_i \oplus (k \oplus k) = c_i \oplus 0 = c_i$.