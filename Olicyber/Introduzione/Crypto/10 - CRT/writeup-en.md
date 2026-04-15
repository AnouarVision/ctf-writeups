# CRT (Chinese Remainder Theorem)

**Competition:** OliCyber <br>
**Category:** Crypto <br>
**Service:** `nc crypto-10.challs.olicyber.it 30003`

---

## Description

> In this challenge you will be asked to use the Chinese Remainder Theorem (CRT). This powerful tool finds solutions to a system of modular equations when all moduli are pairwise coprime.

The server provides a system of congruences and asks for $x$ modulo the product of the moduli.

---

## Mathematical background

**Chinese Remainder Theorem (CRT).** Let $n_1, n_2, \ldots, n_k$ be positive integers that are pairwise coprime, i.e. $\gcd(n_i, n_j) = 1$ for every $i \neq j$. Given arbitrary integers $a_1, a_2, \ldots, a_k$, the system:

$$x \equiv a_1 \pmod{n_1}$$
$$x \equiv a_2 \pmod{n_2}$$
$$\vdots$$
$$x \equiv a_k \pmod{n_k}$$

admits a **unique solution** modulo $N = n_1 \cdot n_2 \cdots \cdot n_k$:

$$x \equiv \sum_{i=1}^{k} a_i \cdot M_i \cdot (M_i^{-1} \bmod n_i) \pmod{N}$$

where $M_i = N / n_i$ is the product of all moduli except $n_i$, and $M_i^{-1} \bmod n_i$ is the modular inverse of $M_i$ modulo $n_i$ (which exists because $\gcd(M_i, n_i) = 1$).

---

## Solution

### Step 1 — Solve the system

The server gives the system:

$$x \equiv 7 \pmod{24}$$
$$x \equiv 11 \pmod{17}$$
$$x \equiv 22 \pmod{83}$$
$$x \equiv 5 \pmod{73}$$
$$x \equiv 41 \pmod{61}$$

Verify that the moduli $24, 17, 83, 73, 61$ are pairwise coprime; the CRT guarantees a unique solution modulo:

$$N = 24 \cdot 17 \cdot 83 \cdot 73 \cdot 61 = 150796392$$

For each $i$ compute $M_i = N / n_i$, then $y_i = M_i^{-1} \bmod n_i$ using the extended Euclidean algorithm, and finally sum $a_i \cdot M_i \cdot y_i$:

$$x = \left(\sum_{i=1}^{5} a_i \cdot M_i \cdot y_i\right) \bmod N = \mathbf{147960055}$$

**Answer:** `147960055`

---

### Script

```python
from functools import reduce

residues = [7, 11, 22, 5, 41]
moduli   = [24, 17, 83, 73, 61]

N = reduce(lambda a, b: a * b, moduli)

x = 0
for a, n in zip(residues, moduli):
    M = N // n
    y = pow(M, -1, n)
    x += a * M * y

print(x % N)
```

**Output:**
```
147960055
```

---

## Flag

```
flag{...}
```

---

## Conclusions

> The CRT turns a problem in a large ring $\mathbb{Z}/N\mathbb{Z}$ into $k$ independent problems in smaller rings $\mathbb{Z}/n_i\mathbb{Z}$.

Two important remarks:

1. **Ring isomorphism.** If the moduli are pairwise coprime, there is an isomorphism:

$$\mathbb{Z}/N\mathbb{Z} \;\cong\; \mathbb{Z}/n_1\mathbb{Z} \times \mathbb{Z}/n_2\mathbb{Z} \times \cdots \times \mathbb{Z}/n_k\,$$

Each element of $\mathbb{Z}/N\mathbb{Z}$ corresponds uniquely to a $k$-tuple of residues, which is why the solution is unique modulo $N$.

2. **`pow(base, -1, n)` in Python.** The server suggests exploring three-argument `pow`: `pow(M, -1, n)` computes the modular inverse of `M` modulo `n` using the extended Euclidean algorithm, exactly what is needed for CRT. More generally, `pow(base, exp, mod)` computes `base**exp % mod` efficiently via fast exponentiation.
