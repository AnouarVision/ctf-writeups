# Modular Inverse

**Competition:** OliCyber  
**Category:** Crypto  
**Service:** `nc crypto-09.challs.olicyber.it 30002`

---

## Description

> The arithmetic of integers modulo n differs in many ways from ordinary arithmetic. A crucial distinction is what it means to compute the inverse of an integer modulo n.

The server asks three questions about modular inverses and the extended Euclidean algorithm. Answering all correctly returns the flag.

---

## Mathematical background

**GCD and Bézout's identity.** Given $a, b \in \mathbb{Z}$, their greatest common divisor $d = \gcd(a,b)$ satisfies **Bézout's identity**: there exist $x, y \in \mathbb{Z}$ such that

$$x \cdot a + y \cdot b = \gcd(a, b)$$

The coefficients $x, y$ are computed with the **extended Euclidean algorithm**, which backtracks the steps of the Euclidean division.

**Modular inverse.** The inverse of $a$ modulo $n$ is an integer $a^{-1} \in \mathbb{Z}/n\mathbb{Z}$ such that

$$a \cdot a^{-1} \equiv 1 \pmod{n}$$

From Bézout's identity with $b = n$:

$$x \cdot a + y \cdot n = \gcd(a, n)$$

Reducing modulo $n$ gives $x \cdot a \equiv \gcd(a,n) \pmod{n}$. Therefore $a^{-1}$ exists iff $\gcd(a,n) = 1$, i.e. $a$ and $n$ are **coprime**. In that case $a^{-1} \equiv x \pmod{n}$.

**Divisibility property of congruence.** If $a \equiv b \pmod{n}$ and $d \mid n$, then

$$a \equiv b \pmod{d}$$

since $n \mid (a-b)$ and $d \mid n$ imply $d \mid (a-b)$.

---

## Solution

### Step 1 — Bézout coefficients

The server asks:

```
a = 54, b = 177, find x,y such that x*a + y*b == GCD(a,b)
```

Apply the extended Euclidean algorithm:

$$177 = 3 \cdot 54 + 15$$
$$54 = 3 \cdot 15 + 9$$
$$15 = 1 \cdot 9 + 6$$
$$9 = 1 \cdot 6 + 3$$
$$6 = 2 \cdot 3 + 0$$

So $\gcd(54,177) = 3$. Back-substituting:

$$3 = 9 - 1 \cdot 6 = 9 - 1 \cdot (15 - 9) = 2 \cdot 9 - 15$$
$$= 2(54 - 3 \cdot 15) - 15 = 2 \cdot 54 - 7 \cdot 15$$
$$= 2 \cdot 54 - 7(177 - 3 \cdot 54) = 23 \cdot 54 + (-7) \cdot 177$$

$$\boxed{x = 23, \quad y = -7}$$

**Check:** $23 \cdot 54 + (-7) \cdot 177 = 1242 - 1239 = 3 = \gcd(54,177)$ ✓

**Answer:** `x = 23`, `y = -7`

---

### Step 2 — Modular invertibility

The server asks:

```
Is 54 invertible mod 177? (yes/no)
```

From the previous step $\gcd(54,177) = 3 \neq 1$. Since 54 and 177 are not coprime, 54 **is not invertible** modulo 177.

**Answer:** `no`

---

### Step 3 — Compute modular inverse

The server asks:

```
What is the inverse of 55 modulo 83?
```

Check $\gcd(55,83)=1$ (83 is prime), so an inverse exists. Extended Euclidean algorithm:

$$83 = 1 \cdot 55 + 28$$
$$55 = 1 \cdot 28 + 27$$
$$28 = 1 \cdot 27 + 1$$
$$27 = 27 \cdot 1 + 0$$

Back-substitute:

$$1 = 28 - 1 \cdot 27 = 28 - (55 - 28) = 2 \cdot 28 - 55$$
$$= 2(83 - 55) - 55 = 2 \cdot 83 - 3 \cdot 55$$

So $x = -3$, therefore:

$$55^{-1} \equiv -3 \equiv 83 - 3 = \mathbf{80} \pmod{83}$$

**Check:** $55 \cdot 80 = 4400 = 53 \cdot 83 + 1 \equiv 1 \pmod{83}$ ✓

**Answer:** `80`

---

## Script

```python
from math import gcd

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = extended_gcd(b, a % b)
    return d, y, x - (a // b) * y

d, x, y = extended_gcd(54, 177)
print(f"x={x}, y={y}, gcd={d}")

print("si" if gcd(54, 177) == 1 else "no")

_, inv, _ = extended_gcd(55, 83)
print(inv % 83)
```

**Output:**
```
x=23, y=-7, gcd=3
no
80
```

---

## Flag

```
flag{...}
```

---

## Conclusions

> A modular inverse exists iff $\gcd(a,n)=1$: coprimality is the necessary and sufficient condition.

Three key concepts from this challenge:

1. **The extended Euclidean algorithm** does more than compute the $\gcd$: it also provides Bézout coefficients, which are exactly the coefficients needed to compute modular inverses. This is the computational backbone of RSA, where the private exponent $d$ is the inverse of $e$ modulo $\phi(n)$. 

2. **Not every integer is invertible modulo $n$:** the multiplicative group $(\mathbb{Z}/n\mathbb{Z})^*$ contains exactly the invertible elements and has order $\phi(n)$ (Euler's totient). If $n$ is prime, every non-zero element is invertible and $\mathbb{Z}/n\mathbb{Z}$ is a field.

3. **Congruence preserves divisibility by divisors of the modulus:** if $a \equiv b \pmod{n}$ and $d \mid n$, then $a \equiv b \pmod{d}$. This property is frequently used to reduce the modulus and simplify proofs in cryptography.
