# Modular Arithmetic 1

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Calculate the following and enter the smaller of the two results as the flag:
> $$11 \equiv x \pmod{6}$$
> $$8146798528947 \equiv y \pmod{17}$$

---

## Theoretical Background

### Congruence and the modulo operation

Given two integers $a, b$ and a positive integer $m$, we say that $a$ is **congruent to $b$ modulo $m$**, written:

$$a \equiv b \pmod{m}$$

if and only if $m \mid (a - b)$, i.e. $m$ divides $a - b$ exactly. Equivalently, $b$ is the remainder of the Euclidean division of $a$ by $m$:

$$a = q \cdot m + b, \qquad 0 \leq b < m, \quad q = \lfloor a / m \rfloor$$

The set of all integers congruent to $b$ modulo $m$ forms an **equivalence class**:

$$[b]_m = \{\dots,\ b - 2m,\ b - m,\ b,\ b + m,\ b + 2m,\ \dots\}$$

The collection of all such classes $\{[0]_m, [1]_m, \dots, [m-1]_m\}$ forms the **ring of integers modulo $m$**, denoted $\mathbb{Z}/m\mathbb{Z}$ or $\mathbb{Z}_m$.

### The clock analogy

The most intuitive model is a 12-hour clock. After 12, the counter resets to 0: $13 \equiv 1 \pmod{12}$, $15 \equiv 3 \pmod{12}$. The example from the challenge statement — $4 + 9 = 1$ — makes perfect sense on a clock face: starting at 4 and adding 9 hours lands on 1.

### Key property: size independence

The modulo operation reduces any integer, however large, to a value in $\{0, 1, \dots, m-1\}$. This is why cryptographic systems can work with enormous numbers (hundreds of digits) while keeping all intermediate results bounded: every operation is performed modulo some fixed $m$.

---

## Solution

### Script

```python
#!/usr/bin/env python3

x = 11 % 6
y = 8146798528947 % 17

print(f"x = 11 mod 6 = {x}")
print(f"y = 8146798528947 mod 17 = {y}")
print(f"flag = {min(x, y)}")
```

### Worked computation

**First reduction: $11 \bmod 6$**

$$11 = 1 \cdot 6 + 5 \implies 11 \equiv 5 \pmod{6}$$

**Second reduction: $8146798528947 \bmod 17$**

Python's `%` operator handles arbitrarily large integers natively, so no manual long division is needed. The result is:

$$8146798528947 = 479223442879 \cdot 17 + 4 \implies 8146798528947 \equiv 4 \pmod{17}$$

### Result

| Expression | Value |
|:---|:---:|
| $11 \bmod 6$ | $5$ |
| $8146798528947 \bmod 17$ | $4$ |
| $\min(x, y)$ | $4$ |

---

### Flag

```
4
```

---

## Conclusions

Modular arithmetic is the mathematical foundation on which virtually every cryptographic primitive is built. In RSA, encryption is the modular exponentiation $c = m^e \bmod n$; in Diffie–Hellman, the shared secret is derived from $g^{ab} \bmod p$; in elliptic curve cryptography, all point operations are performed modulo a prime $p$.

The `%` operator in Python computes the non-negative remainder for positive moduli, which is the standard convention in cryptography. For negative integers, Python's behaviour differs from some other languages (e.g. C), always returning a result in $\{0, \dots, m-1\}$.