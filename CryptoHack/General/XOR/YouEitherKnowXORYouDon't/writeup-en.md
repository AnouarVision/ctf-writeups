# You either know, XOR you don't

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> The flag has been encrypted with a secret repeating key. Recover it.
> `0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104`

No key is provided. The ciphertext was produced with a multi-byte repeating XOR key of unknown length.

---

## Theoretical Background

### Repeating-key XOR cipher

Let $P = (p_0, p_1, \dots, p_{n-1})$ be the plaintext and $K = (k_0, k_1, \dots, k_{m-1})$ be the key of length $m$. The ciphertext is:

$$c_i = p_i \oplus k_{i \bmod m} \qquad \forall\, i \in \{0, \dots, n-1\}$$

The key repeats cyclically across the plaintext. For a short key and a long message, each key byte encrypts multiple plaintext bytes, one at every position $i$ where $i \equiv j \pmod{m}$ for key byte $j$.

### Known-plaintext prefix attack

Since all CryptoHack flags begin with the fixed prefix `crypto{`, we have a **known plaintext** of at least 7 bytes. Given the ciphertext bytes $c_0, c_1, \dots, c_6$ and the corresponding known plaintext bytes $p_0 = \texttt{c},\ p_1 = \texttt{r},\ \dots,\ p_6 = \texttt{\{}$, we can recover the key bytes directly:

$$k_{i \bmod m} = c_i \oplus p_i \qquad \forall\, i \in \{0, \dots, 6\}$$

This yields up to 7 key bytes, sufficient to fully recover a key of length $\leq 7$, or a partial key for longer keys.

---

## Solution

### Step 1 — Recover the key from the known prefix

XOR the first 7 bytes of the ciphertext with the ASCII encoding of `crypto{`:

| $i$ | $c_i$ | $p_i$ | $c_i \oplus p_i$ | Key byte |
|:---:|:---:|:---:|:---:|:---:|
| 0 | `0e` | `63` (`c`) | `6d` | `m` |
| 1 | `0b` | `72` (`r`) | `79` | `y` |
| 2 | `21` | `79` (`y`) | `58` | `X` |
| 3 | `3f` | `70` (`p`) | `4f` | `O` |
| 4 | `26` | `74` (`t`) | `52` | `R` |
| 5 | `04` | `6f` (`o`) | `6b` | `k` |
| 6 | `1e` | `7b` (`{`) | `65` | `e` |

The recovered bytes spell `myXORke`. Since the next byte of the key would be `y` to complete the English word, the full key is:

$$K = \texttt{myXORkey} \quad (m = 8)$$

### Step 2 — Decrypt the full ciphertext

```python
#!/usr/bin/env python3

hex_ciphertext = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

ciphertext = bytes.fromhex(hex_ciphertext)
key = b"myXORkey"

flag = bytes([c ^ key[i % len(key)] for i, c in enumerate(ciphertext)])
print(flag)
```

Each byte of the ciphertext is XOR-ed with the corresponding key byte at position $i \bmod 8$, recovering the original plaintext.

---

### Flag

```
crypto{...}
```

---

## Conclusions

This challenge demonstrates the **known-plaintext attack** on repeating-key XOR. The key insight is that a fixed, publicly known flag format leaks the first several bytes of the key immediately: since $c_i = p_i \oplus k_{i \bmod m}$, knowing $c_i$ and $p_i$ gives $k_{i \bmod m}$ directly.

More generally, any repeating-key XOR cipher is vulnerable once the key length is known or estimated, at that point, the ciphertext can be split into $m$ independent single-byte XOR streams, each attackable by brute force or frequency analysis.