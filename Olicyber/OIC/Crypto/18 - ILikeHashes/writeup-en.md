# I like hashes

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

> I hashed every part of the flag, you'll never find it!

You are given a file `ct.txt` containing 32 lines, each a 64-character hexadecimal hash.

---

## Ciphertext analysis

Each line is a 64-character hex string, 256 bits, the exact digest size of **SHA-256**. The file contains 32 lines but only 15 distinct hashes, which implies repeated plaintext characters. This already rules out any semantically secure scheme.

---

## Mathematical model

Let $\mathcal{M} = \{0,1\}^*$ be the message space and $\mathcal{H} = \{0,1\}^{256}$ the digest space. SHA-256 is a function

$$H : \mathcal{M} \longrightarrow \mathcal{H}$$

with preimage, second-preimage and collision resistance properties. The ciphertext file is the sequence

$$\mathcal{C} = \bigl(H(P_0),\ H(P_1),\ \ldots,\ H(P_{n-1})\bigr)$$

where every $P_i \in \Sigma$ is a single character of the plaintext, and $\Sigma$ is the set of printable ASCII characters with $|\Sigma| = 95$.

---

## Solution

### Step 1 — Identify the vulnerability

Hashing each character independently with a deterministic function $H$ is formally equivalent to a **monoalphabetic substitution cipher** on $\Sigma$, where the substitution table is:

$$\tau : \Sigma \longrightarrow \mathcal{H}, \qquad \tau(c) = H(c)$$

Such a substitution cipher is secure only if $|\Sigma|$ is large enough to make enumeration infeasible. Here

$$|\Sigma| = 95 \ll 2^{128}$$

so the preimage space is trivially enumerable.

### Step 2 — Build the lookup (rainbow) table

Construct the inverse lookup $\tau^{-1} : \mathcal{H} \rightharpoonup \Sigma$ by computing $H(c)$ for every $c \in \Sigma$:

$$\tau^{-1}(h) = c \iff H(c) = h$$

This requires exactly $|\Sigma| = 95$ SHA-256 evaluations, i.e. $O(95)$ time, negligible on modern hardware.

### Step 3 — Decrypt

For every hash $\mathcal{C}_i$ in the file, recover the original character:

$$P_i = \tau^{-1}(\mathcal{C}_i)$$

Because SHA-256 is deterministic and collisions are negligible for single-byte inputs, the mapping is injective over $\Sigma$ and the solution is unique.

### Step 4 — Script

```python
from hashlib import sha256

hashes = open("ct.txt").read().strip().split('\n')

rainbow = {sha256(chr(c).encode()).hexdigest(): chr(c) for c in range(32, 127)}

flag = "".join(rainbow[h] for h in hashes)
print(flag)
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusions

This challenge highlights a common misunderstanding about cryptographic hash functions:

1. **SHA-256 is not an encryption primitive**: it is designed to resist preimage finding over arbitrary-length inputs, not to hide information when the input space is small and enumeratable. When $m \in \Sigma$ with $|\Sigma| = 95$, exhaustive search is trivial.

2. **Determinism is fatal without salt**: $H(c) = H(c)$ for repeated occurrences of the same character, preserving plaintext frequency distribution. This is the same weakness of monoalphabetic substitution ciphers.

3. **Adequate entropy is required**: encrypting each atomic unit independently reduces security to that of encrypting a single symbol from an alphabet of size $|\Sigma|$. For $|\Sigma| = 95$ this yields at most $\log_2(95) \approx 6.57$ bits of security per character, far below modern standards ($\ge 128$ bits).
