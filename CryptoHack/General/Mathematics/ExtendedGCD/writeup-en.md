# Extended GCD

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Using the two primes $p = 26513,\ q = 32321$, find the integers $x, y$ such that $p \cdot x + q \cdot y = \gcd(p, q)$. Enter whichever of $x$ and $y$ is the lower number as the flag.

---

## Theoretical Background

### Bézout's Identity

For any two integers $a, b$ with $\gcd(a, b) = d$, there exist integers $x, y \in \mathbb{Z}$ called **Bézout coefficients**, such that:

$$a \cdot x + b \cdot y = d$$

This is known as **Bézout's Identity**. The coefficients $x$ and $y$ are not unique: if $(x_0, y_0)$ is a solution, then for any $k \in \mathbb{Z}$:

$$\left(x_0 + k \cdot \frac{b}{d},\quad y_0 - k \cdot \frac{a}{d}\right)$$

is also a solution. The Extended Euclidean Algorithm computes one particular pair $(x, y)$ efficiently.

### Expected GCD of two distinct primes

Since $p = 26513$ and $q = 32321$ are both prime and $p \neq q$, neither divides the other. The only positive common divisor is therefore 1:

$$\gcd(p, q) = 1$$

In this case, Bézout's Identity becomes:

$$p \cdot x + q \cdot y = 1$$

This is precisely the equation whose solution gives the **modular inverse** of $p$ modulo $q$ (and of $q$ modulo $p$), a computation central to RSA key generation.

### The Extended Euclidean Algorithm

The standard Euclidean Algorithm computes $\gcd(a, b)$ via the recurrence $\gcd(a, b) = \gcd(b, a \bmod b)$. The **Extended** version augments it to track the Bézout coefficients at each step.

At each iteration, two auxiliary sequences $\{x_i\}$ and $\{y_i\}$ are maintained such that the invariant:

$$r_i = a \cdot x_i + b \cdot y_i$$

holds throughout, where $r_i$ is the current remainder. Initialising with:

$$r_0 = a,\quad x_0 = 1,\quad y_0 = 0$$
$$r_1 = b,\quad x_1 = 0,\quad y_1 = 1$$

and applying the recurrence with quotient $q_i = \lfloor r_{i-1} / r_i \rfloor$:

$$r_{i+1} = r_{i-1} - q_i \cdot r_i$$
$$u_{i+1} = u_{i-1} - q_i \cdot x_i$$
$$v_{i+1} = v_{i-1} - q_i \cdot y_i$$

When $r_{i+1} = 0$, the algorithm terminates: $r_i = \gcd(a, b)$ and $(x_i, y_i)$ are the Bézout coefficients.

The recursive formulation is equivalent and more concise: at the base case $b = 0$, return $(a, 1, 0)$; otherwise recurse on $(b, a \bmod b)$ and back-substitute.

---

## Solution

### Script

```python
#!/usr/bin/env python3

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

p = 26513
q = 32321

gcd, x, y = extended_gcd(p, q)

print(f"gcd({p}, {q}) = {gcd}")
print(f"x = {x}")
print(f"y = {y}")
print(f"Verification: {p}*{x} + {q}*{y} = {p*x + q*y}")
print(f"Flag: {min(x, y)}")
```

### Recursive back-substitution

The recursion unwinds as follows. At each recursive call, the algorithm solves the sub-problem for $(b, a \bmod b)$ and obtains coefficients $(x_1, y_1)$ such that:

$$b \cdot x_1 + (a \bmod b) \cdot y_1 = \gcd$$

Since $a \bmod b = a - \lfloor a/b \rfloor \cdot b$, substituting:

$$b \cdot x_1 + (a - \lfloor a/b \rfloor \cdot b) \cdot y_1 = \gcd$$

$$a \cdot y_1 + b \cdot (x_1 - \lfloor a/b \rfloor \cdot y_1) = \gcd$$

Therefore:

$$x = y_1, \qquad y = x_1 - \lfloor a/b \rfloor \cdot y_1$$

### Result

| Quantity | Value |
|:---|:---:|
| $\gcd(p, q)$ | $1$ |
| $x$ | $10245$ |
| $y$ | $-8404$ |
| Verification: $p \cdot x + q \cdot y$ | $26513 \cdot 10245 + 32321 \cdot (-8404) = 1$ ✓ |

The lower of the two coefficients is $y = -8404$.

---

### Flag

```
-8404
```

---

## Conclusions

The Extended Euclidean Algorithm is one of the most important algorithms in computational number theory and applied cryptography. Its primary application is the computation of **modular inverses**: given $e$ and $\phi(n)$ with $\gcd(e, \phi(n)) = 1$, the algorithm finds $d$ such that $e \cdot d \equiv 1 \pmod{\phi(n)}$, i.e. $e \cdot d + \phi(n) \cdot k = 1$ for some $k \in \mathbb{Z}$. This $d$ is the RSA private exponent.

In Python, the modular inverse can also be computed directly as `pow(e, -1, phi_n)` (since Python 3.8) or via `Crypto.Util.number.inverse()` from PyCryptodome, both of which use the Extended Euclidean Algorithm internally.