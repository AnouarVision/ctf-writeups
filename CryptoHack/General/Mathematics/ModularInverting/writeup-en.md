# Modular Inverting

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Find the inverse element $d = 3^{-1}$ such that $3 \cdot d \equiv 1 \pmod{13}$.

---

## Theoretical Background

### Multiplicative inverse in $\mathbb{F}_p$

For every non-zero element $g$ in the finite field $\mathbb{F}_p$, there exists a unique integer $d \in \{1, \dots, p-1\}$ such that:

$$g \cdot d \equiv 1 \pmod{p}$$

This $d$ is called the **multiplicative inverse** of $g$ modulo $p$, written $g^{-1}$ or $d = g^{-1} \bmod p$.

The example given in the challenge confirms the definition:

$$7 \cdot 8 = 56 = 5 \cdot 11 + 1 \implies 7 \cdot 8 \equiv 1 \pmod{11}$$

So $7^{-1} \equiv 8 \pmod{11}$.

### Method 1 — Fermat's Little Theorem

The challenge hints at using Fermat's Little Theorem, which states that for any prime $p$ and $a \not\equiv 0 \pmod{p}$:

$$a^{p-1} \equiv 1 \pmod{p}$$

We can rewrite the left-hand side by factoring out one $a$:

$$a \cdot a^{p-2} \equiv 1 \pmod{p}$$

Comparing with the definition $a \cdot d \equiv 1 \pmod{p}$, we immediately identify:

$$d = a^{-1} \equiv a^{p-2} \pmod{p}$$

The multiplicative inverse of $a$ modulo a prime $p$ is simply $a$ raised to the power $p-2$, computed modulo $p$. This requires only a single modular exponentiation, an operation Python performs efficiently with `pow(a, p-2, p)`.

### Method 2 — Extended Euclidean Algorithm

The inverse can also be computed as the Bézout coefficient $x$ in:

$$a \cdot x + p \cdot y = \gcd(a, p) = 1 \implies a \cdot x \equiv 1 \pmod{p}$$

This is the more general method (it works even when $p$ is not prime, as long as $\gcd(a, p) = 1$) and is what Python's `pow(a, -1, p)` uses internally since Python 3.8.

### Comparison of the two methods

| Method | Applicable when | Complexity |
|:---|:---|:---|
| Fermat: $a^{p-2} \bmod p$ | $p$ prime | $O(\log p)$ multiplications |
| Extended GCD | $\gcd(a, m) = 1$ (any $m$) | $O(\log \min(a,m))$ divisions |

Both have the same asymptotic complexity. In cryptographic practice, the Extended GCD is preferred for generality, while Fermat's method is useful when $p$ is known to be prime and a modular exponentiation is already being computed.

---

## Solution

### Worked computation

We need $d$ such that $3 \cdot d \equiv 1 \pmod{13}$.

**Via Fermat's Little Theorem:**

$$d = 3^{13-2} \bmod 13 = 3^{11} \bmod 13$$

Computing step by step using repeated squaring:

$$3^1 = 3$$
$$3^2 = 9$$
$$3^4 = 9^2 = 81 \equiv 3 \pmod{13}$$
$$3^8 \equiv 3^2 = 9 \pmod{13}$$
$$3^{11} = 3^8 \cdot 3^2 \cdot 3^1 \equiv 9 \cdot 9 \cdot 3 = 243 \equiv 243 - 18 \cdot 13 = 243 - 234 = 9 \pmod{13}$$

**Verification:**

$$3 \cdot 9 = 27 = 2 \cdot 13 + 1 \implies 3 \cdot 9 \equiv 1 \pmod{13} \checkmark$$

### Script

```python
#!/usr/bin/env python3

p = 13
a = 3

# Method 1: Fermat's Little Theorem  →  a^-1 = a^(p-2) mod p
d_fermat = pow(a, p - 2, p)

# Method 2: built-in pow (Python 3.8+)
d_builtin = pow(a, -1, p)

print(f"Inverse of {a} mod {p} = {d_fermat}")
print(f"Verification: {a} * {d_fermat} mod {p} = {(a * d_fermat) % p}")
```

---

### Flag

```
9
```

---

## Conclusions

The multiplicative inverse is a fundamental operation in cryptography. Its two main applications in this course are:

**RSA key generation.** Given the public exponent $e$ and $\phi(n) = (p-1)(q-1)$, the private exponent is $d = e^{-1} \bmod \phi(n)$, computed via the Extended Euclidean Algorithm. The correctness of RSA decryption depends entirely on the existence and uniqueness of this inverse, which is guaranteed because $\gcd(e, \phi(n)) = 1$ by construction.

**Modular division.** Division by $a$ in $\mathbb{F}_p$ is defined as multiplication by $a^{-1}$: there is no "division" operation in modular arithmetic, only multiplication by the inverse.