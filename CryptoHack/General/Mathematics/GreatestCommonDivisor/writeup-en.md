# Greatest Common Divisor

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Calculate $\gcd(a, b)$ for $a = 66528,\ b = 52920$.

The challenge introduces the concept of the Greatest Common Divisor, asks us to implement Euclid's Algorithm and apply it to the given pair of integers.

---

## Theoretical Background

### Definition

Given two positive integers $a, b \in \mathbb{Z}^+$, their **Greatest Common Divisor** is defined as:

$$\gcd(a, b) = \max\{d \in \mathbb{Z}^+ : d \mid a \text{ and } d \mid b\}$$

That is, the largest integer $d$ that divides both $a$ and $b$ without remainder.

### Coprimality

Two integers $a, b$ are said to be **coprime** (or relatively prime) if:

$$\gcd(a, b) = 1$$

This does not require either integer to be prime; it only requires that they share no common factor greater than 1. A few notable cases:

- If $a$ and $b$ are both prime and $a \neq b$, then $\gcd(a, b) = 1$.
- If $a$ is prime and $b < a$, then $a \nmid b$, so $\gcd(a, b) = 1$.
- If $a$ is prime and $b > a$, it is possible that $a \mid b$ (e.g. $a = 3,\ b = 6$), hence $\gcd(a, b) = a \neq 1$. Coprimality is therefore not guaranteed.

Coprimality is a fundamental concept in RSA: the public exponent $e$ must satisfy $\gcd(e, \lambda(n)) = 1$, where $\lambda(n)$ is the Carmichael totient of the modulus.

---

## Euclid's Algorithm

### The key theorem

The algorithm rests on the following identity, which holds for all $a, b \in \mathbb{Z}^+$ with $b \neq 0$:

$$\gcd(a, b) = \gcd(b,\ a \bmod b)$$

**Proof.** Let $r = a \bmod b$, so $a = qb + r$ for some $q \in \mathbb{Z}$. Any common divisor of $a$ and $b$ must also divide $r = a - qb$, and any common divisor of $b$ and $r$ must also divide $a = qb + r$. The set of common divisors of $(a, b)$ therefore coincides with the set of common divisors of $(b, r)$, and in particular their maxima coincide.

### The algorithm

Applying the identity repeatedly:

$$\gcd(a, b) = \gcd(b, r_1) = \gcd(r_1, r_2) = \cdots = \gcd(r_{k-1}, 0) = r_{k-1}$$

where $r_i = r_{i-2} \bmod r_{i-1}$. The sequence of remainders is strictly decreasing ($b > r_1 > r_2 > \cdots \geq 0$), so termination is guaranteed. When the remainder reaches zero, the last non-zero remainder is $\gcd(a, b)$.

---

## Solution

### Worked computation: $\gcd(66528,\ 52920)$

The algorithm proceeds as follows, at each step replacing $(a, b)$ with $(b,\ a \bmod b)$:

**Step 1.**

$$66528 = 52920 \cdot 1 + 13608 \implies \gcd(66528,\ 52920) = \gcd(52920,\ 13608)$$

**Step 2.**

$$52920 = 13608 \cdot 3 + 12096 \quad (13608 \cdot 3 = 40824,\ 52920 - 40824 = 12096)$$

$$\implies \gcd(52920,\ 13608) = \gcd(13608,\ 12096)$$

**Step 3.**

$$13608 = 12096 \cdot 1 + 1512 \quad (13608 - 12096 = 1512)$$

$$\implies \gcd(13608,\ 12096) = \gcd(12096,\ 1512)$$

**Step 4.**

$$12096 = 1512 \cdot 8 + 0 \quad (1512 \cdot 8 = 12096)$$

$$\implies \gcd(12096,\ 1512) = \gcd(1512,\ 0) = 1512$$

The remainder has reached zero. The last non-zero remainder is $\boxed{1512}$.

### Summary table

| Step | $a$ | $b$ | $q = \lfloor a/b \rfloor$ | $r = a \bmod b$ |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 66528 | 52920 | 1 | 13608 |
| 2 | 52920 | 13608 | 3 | 12096 |
| 3 | 13608 | 12096 | 1 | 1512 |
| 4 | 12096 | 1512 | 8 | **0** |

### Script

```python
#!/usr/bin/env python3

a = 66528
b = 52920

while b > 0:
    r = a % b
    a = b
    b = r

print(f"gcd = {a}")
```

The loop implements the recurrence $\gcd(a, b) = \gcd(b, a \bmod b)$ directly: at each iteration, `a` takes the value of `b` and `b` takes the remainder `r = a % b`. When `b` reaches zero, `a` holds the GCD.

---

### Answer

$$\gcd(66528,\ 52920) = 1512$$

---

## Conclusions

In Python, the GCD is available as `math.gcd(a, b)` in the standard library (since Python 3.5) and does not require any external dependency. However, implementing the algorithm from scratch, as this challenge asks, is the surest way to internalise the recurrence $\gcd(a, b) = \gcd(b, a \bmod b)$.

This recurrence will reappear in more advanced settings: the **Extended Euclidean Algorithm** augments it to compute integers $x, y$ such that $ax + by = \gcd(a, b)$ (Bézout's identity), which is the foundation for computing modular inverses, an operation central to RSA key generation and decryption.