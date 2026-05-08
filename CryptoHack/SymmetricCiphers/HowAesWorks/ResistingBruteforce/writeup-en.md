# Resisting Bruteforce

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> What is the name for the best single-key attack against AES?

The challenge tests knowledge of the current state of AES cryptanalysis.

---

## Theoretical Background

### The security of AES-128

AES-128 operates on a 128-bit keyspace, meaning there are $2^{128}$ possible keys. To bruteforce AES-128, an attacker would need to try up to $2^{128} \approx 3.4 \times 10^{38}$ keys. To put this in perspective, even with the combined hashing power of the entire Bitcoin mining network, it has been estimated that exhaustively searching the 128-bit keyspace would take over **100 times the age of the universe**.

A block cipher is considered **computationally secure** if no attack exists that is significantly faster than exhaustive key search. More precisely, a cipher is theoretically "broken" if an attack is found that requires fewer than $2^k$ operations for a $k$-bit key, even if that attack remains practically infeasible.

### The Biclique Attack

The best known single-key attack against AES is the **biclique attack**, published by Bogdanov et al. in 2011. It applies to all three AES variants:

| Variant | Key size | Classical security | After biclique |
|:---:|:---:|:---:|:---:|
| AES-128 | 128 bits | $2^{128}$ | $2^{126.1}$ |
| AES-192 | 192 bits | $2^{192}$ | $2^{189.7}$ |
| AES-256 | 256 bits | $2^{256}$ | $2^{254.4}$ |

The attack reduces the security level of AES-128 by only **1.9 bits**, a negligible margin. It has not been improved upon in over a decade, and is not considered a credible practical threat.

The biclique attack works by constructing algebraic structures called **bicliques** in the AES key schedule and round function, allowing certain computations to be reused across multiple key candidates. It is a meet-in-the-middle technique applied to a small number of AES rounds, combined with exhaustive search over the remaining key bits.

### Quantum attacks on AES

Quantum computers do not fully break symmetric cryptosystems in the way they break RSA (via Shor's algorithm). Instead, **Grover's algorithm** provides a quadratic speedup for unstructured search, effectively halving the security level:

$$\text{Quantum security of AES-}k = \frac{k}{2} \text{ bits}$$

| Variant | Classical security | Quantum security (Grover) |
|:---:|:---:|:---:|
| AES-128 | 128 bits | 64 bits |
| AES-256 | 256 bits | 128 bits |

This is why **AES-256 is recommended** for post-quantum security: even after Grover's speedup, it retains 128 bits of security, the same as AES-128 in a classical setting, widely considered sufficient.

---

## Solution

The challenge asks for the name of the best single-key attack against AES. The answer is given directly in the challenge description: the **biclique attack**.

---

### Flag

```
crypto{biclique}
```

---

## Conclusions

This challenge surveys the current security posture of AES from three angles:

**Classical security:** AES-128 provides 128 bits of security minus a negligible 1.9-bit reduction from the biclique attack. For all practical purposes, AES-128 is unbreakable by brute force.

**Theoretical vs practical breaks:** in the academic sense, any attack faster than exhaustive search "breaks" a cipher. The biclique attack qualifies, but the improvement is so small that it poses no real-world threat. The distinction between a theoretical break and a practical break is crucial in applied cryptography.

**Quantum security:** Grover's algorithm halves the effective key length, making AES-128 equivalent to a 64-bit cipher in a quantum setting, potentially vulnerable. AES-256 retains 128 bits of quantum security, which is why it is the recommended choice for long-term data protection in a post-quantum world.