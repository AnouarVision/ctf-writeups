# Modular Arithmetic 2

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Using the prime $p = 65537$, calculate $273246787654^{65536} \bmod 65537$.

The challenge introduces finite fields, Fermat's Little Theorem and asks us to compute a modular exponentiation that can be solved by reasoning alone, no calculator required.

---

## Theoretical Background

### Fields vs. rings

When the modulus $m$ is **prime**, the integers modulo $m$ form a **field**, denoted $\mathbb{F}_p$ or $\text{GF}(p)$. A field is a set equipped with addition and multiplication where every non-zero element has both an additive inverse $b^+$ and a multiplicative inverse $b^*$:

$$a + b^+ = 0, \qquad a \cdot b^* = 1$$

When $m$ is **not prime**, the integers modulo $m$ form only a **ring**, multiplicative inverses do not exist for all elements. For example, in $\mathbb{Z}_6$, the element 2 has no multiplicative inverse since $\gcd(2, 6) = 2 \neq 1$.

The finite field $\mathbb{F}_p = \{0, 1, \dots, p-1\}$ is the mathematical structure underlying RSA, Diffie–Hellman and elliptic curve cryptography.

### Fermat's Little Theorem

**Theorem.** Let $p$ be prime and $a$ an integer with $p \nmid a$ (i.e. $a \not\equiv 0 \pmod{p}$). Then:

$$a^{p-1} \equiv 1 \pmod{p}$$

**Intuition.** Consider the set $\{1, 2, \dots, p-1\}$ — the non-zero elements of $\mathbb{F}_p$. Multiplying each element by $a$ (modulo $p$) permutes the set: it produces the same $p-1$ values in a different order. Therefore:

$$\prod_{k=1}^{p-1} (a \cdot k) \equiv \prod_{k=1}^{p-1} k \pmod{p}$$

$$a^{p-1} \cdot (p-1)! \equiv (p-1)! \pmod{p}$$

Since $\gcd((p-1)!, p) = 1$, we can divide both sides by $(p-1)!$:

$$a^{p-1} \equiv 1 \pmod{p} \qquad \square$$

### Consequence: $a^p \equiv a \pmod{p}$

Multiplying both sides of Fermat's theorem by $a$:

$$a^p \equiv a \pmod{p}$$

This holds even when $a \equiv 0 \pmod{p}$, making it a universal statement about all integers.

---

## Solution

### Verification on small examples

Before attacking the main problem, the challenge asks to verify the theorem on small cases:

| Expression | Value | Explanation |
|:---|:---:|:---|
| $3^{17} \bmod 17$ | $3$ | $a^p \equiv a \pmod{p}$ |
| $5^{17} \bmod 17$ | $5$ | $a^p \equiv a \pmod{p}$ |
| $7^{16} \bmod 17$ | $1$ | $a^{p-1} \equiv 1 \pmod{p}$ |

### Main problem: $273246787654^{65536} \bmod 65537$

We observe that $65537$ is prime (it is a well-known Fermat prime, $F_4 = 2^{2^4} + 1$) and that $65536 = 65537 - 1 = p - 1$. By Fermat's Little Theorem, for any $a$ with $p \nmid a$:

$$a^{p-1} \equiv 1 \pmod{p}$$

Since $273246787654$ is not divisible by $65537$, we conclude immediately:

$$273246787654^{65536} \equiv 1 \pmod{65537}$$

**No computation is needed.** The result follows directly from the theorem.

### Script

```python
#!/usr/bin/env python3

p = 65537

print(f"3^17 mod 17      = {pow(3, 17, 17)}")
print(f"5^17 mod 17      = {pow(5, 17, 17)}")
print(f"7^16 mod 17      = {pow(7, 16, 17)}")
print(f"273246787654^65536 mod 65537 = {pow(273246787654, p - 1, p)}")
```

Note: `pow(a, e, m)` uses Python's built-in **fast modular exponentiation** (square-and-multiply), which computes $a^e \bmod m$ in $O(\log e)$ multiplications. This is essential in cryptography where exponents are hundreds of digits long.

---

### Flag

```
1
```

---

## Conclusions

Fermat's Little Theorem is one of the cornerstones of public-key cryptography. Its generalisations are equally fundamental:

**Euler's theorem**:
for any $a$ with $\gcd(a, n) = 1$:

$$a^{\phi(n)} \equiv 1 \pmod{n}$$

where $\phi(n)$ is Euler's totient function. When $n = pq$ (product of two distinct primes, as in RSA), $\phi(n) = (p-1)(q-1)$.

**RSA correctness** rests directly on this: the decryption exponent $d$ satisfies $ed \equiv 1 \pmod{\phi(n)}$, so:

$$c^d = (m^e)^d = m^{ed} = m^{1 + k\phi(n)} = m \cdot (m^{\phi(n)})^k \equiv m \cdot 1^k = m \pmod{n}$$

Understanding Fermat's theorem, and why it works, is therefore the first step towards understanding RSA.