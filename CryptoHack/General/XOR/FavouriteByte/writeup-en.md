# Favourite Byte

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Some data has been hidden using XOR with a single secret byte. Decode the following hex string and recover the flag.
> `73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d`

No key is provided. The ciphertext has been encrypted with a single unknown byte, which must be recovered.

---

## Theoretical Background

### Single-byte XOR cipher

Let $C = (c_0, c_1, \dots, c_{n-1})$ be a ciphertext byte sequence obtained by XOR-ing each byte of a plaintext $P = (p_0, p_1, \dots, p_{n-1})$ with a fixed secret key $k \in \{0, \dots, 255\}$:

$$c_i = p_i \oplus k \qquad \forall\, i \in \{0, \dots, n-1\}$$

### Brute-force attack

Since the key space is $\{0, 1, \dots, 255\}$ — only 256 possible values — an exhaustive search is computationally trivial. For each candidate key $k' \in \{0, \dots, 255\}$, we compute:

$$p'_i = c_i \oplus k' \qquad \forall\, i$$

and check whether the resulting byte sequence $P'$ is a valid, printable ASCII string. In this challenge, we further know that the plaintext begins with the prefix `crypto{`, which provides an additional filter.

This attack is known as a **known-plaintext prefix attack** combined with brute force. Even without the prefix, frequency analysis on the candidate plaintexts would quickly identify the correct key by comparing the character frequency distribution of $P'$ against expected English text.

---

## Solution

### Script

```python
#!/usr/bin/env python3

hex_ciphertext = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

ciphertext = bytes.fromhex(hex_ciphertext)

for key in range(256):
    candidate = bytes([b ^ key for b in ciphertext])
    try:
        plaintext = candidate.decode("ascii")
        if plaintext.startswith("crypto{"):
            print(f"key = {key} ({hex(key)}): {plaintext}")
    except Exception:
        pass
```

The loop iterates over all 256 possible key values. For each candidate $k'$, every byte of `ciphertext` is XOR-ed with $k'$. If the result decodes as valid ASCII and begins with `crypto{`, the correct key has been found.

### Result

| Key (decimal) | Key (hex) | Plaintext |
|:---:|:---:|:---|
| 16 | `0x10` | `crypto{...}` |

The key is $k = 16 = \texttt{0x10}_{16} = 00010000_2$.

### Verification on the first byte

$$c_0 = \texttt{73}_{16} = 115_{10}, \qquad k = \texttt{10}_{16} = 16_{10}$$

$$p_0 = 115 \oplus 16 = 99_{10} = \texttt{63}_{16} \implies \text{chr}(99) = \texttt{c} \checkmark$$

---

### Flag

```
crypto{...}
```

---

## Conclusions

This challenge illustrates the fundamental weakness of single-byte XOR encryption: the key space is so small ($2^8 = 256$ values) that exhaustive search requires at most 256 decryption attempts, an operation that completes in microseconds on any modern machine. Even without a known-prefix filter, the correct key is trivially identified by visual inspection or automated frequency analysis.