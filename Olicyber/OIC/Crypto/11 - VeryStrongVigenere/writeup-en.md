# Very Strong Vigenere

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

>The competitor wrote: "Since I discovered Vigenère I feel completely safe!"
`fzau{ncn_isors_cviovw_pwcqoze}`

The flag is encrypted with the Vigenère cipher. The goal is to recover the key and decrypt the message.

---

## The Vigenère Cipher

Vigenère operates on the alphabet $\mathbb{Z}_{26}$, mapping each letter to its index: $\texttt{a} \mapsto 0,\ \texttt{b} \mapsto 1,\ \ldots,\ \texttt{z} \mapsto 25$.

Let $P = (P_0, P_1, \ldots, P_{n-1}) \in \mathbb{Z}_{26}^n$ be the plaintext, $K = (K_0, K_1, \ldots, K_{m-1}) \in \mathbb{Z}_{26}^m$ the key of length $m$, and $C = (C_0, C_1, \ldots, C_{n-1}) \in \mathbb{Z}_{26}^n$ the ciphertext. Encryption is defined by:

$$C_i = (P_i + K_{i \bmod m}) \bmod 26 \qquad \forall i \in \{0, \ldots, n-1\}$$

Decryption is the inverse operation, obtained by subtracting the key in $\mathbb{Z}_{26}$:

$$P_i = (C_i - K_{i \bmod m}) \bmod 26 \qquad \forall i \in \{0, \ldots, n-1\}$$

Non-alphabetic characters (symbols, punctuation) are transmitted unchanged and **do not advance the key index**.

---

## Solution

### Step 1 — Known Plaintext Attack

The flag format is known: the first five plaintext characters are $P = (\texttt{f}, \texttt{l}, \texttt{a}, \texttt{g}, \texttt{\{} )$, corresponding to the values $(5,11,0,6)$ in $\mathbb{Z}_{26}$ (the brace is non-alphabetic and ignored).

The corresponding ciphertext is $C = (\texttt{f}, \texttt{z}, \texttt{a}, \texttt{u}, \texttt{\{} )$, i.e. $(5,25,0,20)$.

Applying the inversion formula for each position:

$$K_{i \bmod m} = (C_i - P_i) \bmod 26$$

$$K_0 = (5 - 5) \bmod 26 = 0 \quad \longrightarrow \quad \texttt{a}$$
$$K_1 = (25 - 11) \bmod 26 = 14 \quad \longrightarrow \quad \texttt{o}$$
$$K_2 = (0 - 0) \bmod 26 = 0 \quad \longrightarrow \quad \texttt{a}$$
$$K_3 = (20 - 6) \bmod 26 = 14 \quad \longrightarrow \quad \texttt{o}$$

The obtained sequence is $\texttt{aoao}$, which immediately reveals a key of period $m = 2$:

$$K = (\texttt{a}, \texttt{o}) \quad \Longrightarrow \quad K = (0,\ 14)$$

---

### Step 2 — Full decryption

With $K = (0,14)$ and $m = 2$, apply decryption to every alphabetic character of the ciphertext:

$$P_i = (C_i - K_{i \bmod 2}) \bmod 26$$

| $i$ | $C_i$ | $K_{i \bmod 2}$ | $P_i$ | Letter |
|-----|--------|-----------------|--------|-------|
| 0 | $\texttt{f}=5$ | $K_0=0$ | $5$ | f |
| 1 | $\texttt{z}=25$ | $K_1=14$ | $11$ | l |
| 2 | $\texttt{a}=0$ | $K_0=0$ | $0$ | a |
| 3 | $\texttt{u}=20$ | $K_1=14$ | $6$ | g |
| 4 | $\texttt{n}=13$ | $K_0=0$ | $13$ | n |
| 5 | $\texttt{c}=2$ | $K_1=14$ | $(2-14) \bmod 26 = 14$ | o |
| $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ |

---

### Step 3 — Decryption script

```python
def vigenere_decrypt(ciphertext, key):
    result = ""
    ki = 0
    for c in ciphertext:
        if c.isalpha():
            k = ord(key[ki % len(key)]) - ord('a')
            p = (ord(c.lower()) - ord('a') - k) % 26
            result += chr(p + ord('a'))
            ki += 1
        else:
            result += c
    return result

ciphertext = "fzau{ncn_isors_cviovw_pwcqoze}"
key = "ao"
print(vigenere_decrypt(ciphertext, key))
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusions

This challenge illustrates the structural weakness of the Vigenère cipher when the key is short.

1. **The Known Plaintext Attack breaks the scheme**: the additive structure in $\mathbb{Z}_{26}$ allows recovering the key from a single known $(P_i, C_i)$ pair. With the flag format known, four characters suffice to reconstruct the whole key.

2. **Key length is the critical parameter**: a key of period $m$ reduces the problem to $m$ independent Caesar ciphers, each attackable separately. In the limit $m = n$ (key as long as the message, used once) you obtain the One-Time Pad, which is provably secure by Shannon's theorem. With $m = 2$ the security is equivalent to two overlapping Caesar ciphers.