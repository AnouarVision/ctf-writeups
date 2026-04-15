# Modular Congruences

**Competition:** OliCyber <br>
**Category:** Crypto <br>
**Service:** `nc crypto-08.challs.olicyber.it 30001`

---

## Description

> As you may have guessed, cryptography makes extensive use of mathematical tools. Branches of mathematics dealing with discrete structures are particularly useful.

The server poses two questions about modular congruences. Answering both correctly returns the flag.

---

## Mathematical background

**Modular congruence.** Given $a, b, n \in \mathbb{Z}$ with $n > 0$, we say that $a$ is **congruent** to $b$ modulo $n$ if $n$ divides their difference:

$$a \equiv b \pmod{n} \iff n \mid (a - b)$$

Intuitively, $a$ and $b$ leave the same remainder when divided by $n$. The operation $a \bmod n$ returns the unique integer $r \in [0, n)$ such that $a \equiv r \pmod{n}$.

**Algebraic structure.** The set of residue classes $\mathbb{Z}/n\mathbb{Z} = \{[0],[1],\ldots,[n-1]\}$ forms an **abelian group** under modular addition, i.e. it satisfies:

- **Closure**: $[a] + [b] = [a+b] \in \mathbb{Z}/n\mathbb{Z}$
- **Associativity**: $([a]+[b])+[c] = [a]+([b]+[c])$
- **Identity element**: $[a] + [0] = [a]$
- **Inverse**: $\forall [a]\ \exists [-a] : [a]+[-a]=[0]$
- **Commutativity** (abelian): $[a]+[b]=[b]+[a]$

Adding modular multiplication, $(\mathbb{Z}/n\mathbb{Z}, +, \cdot)$ becomes a **quotient ring**, the structure underpinning RSA, Diffie–Hellman and elliptic-curve cryptography.

---

## Solution

### Step 1 — Modular reduction of a negative integer

The server asks:

```
-45 % 73 = ?
```

$-45 \bmod 73$ is simply the remainder of dividing $-45$ by $73$. Since $-45$ is negative but $|-45| < 73$, we can add the modulus once:

$$-45 + 73 = \mathbf{28}$$

**Answer:** `28`

---

### Step 2 — Checking congruence between two integers

The server asks:

```
323 == 615 (mod 100)? (yes/no)
```

Compute the remainder of each:

$$323 \bmod 100 = 23, \qquad 615 \bmod 100 = 15$$

Since $23 \neq 15$, we have $323 \not\equiv 615 \pmod{100}$.

**Answer:** `no`

---

## Flag

```
flag{...}
```

---

## Conclusions

> Modular arithmetic is the arithmetic of a clock: after the modulus, you start again from zero.

Two important notes:

1. **Sign of the remainder in Python vs C:** In Python `%` always returns a result in $[0, n)$ by definition. In C, however, `(-45) % 73 = -45`, a classic source of cryptographic bugs.

2. **Why $\mathbb{Z}/n\mathbb{Z}$ is fundamental in cryptography:** working in a quotient ring keeps numbers small (always in $[0,n)$) while performing arbitrarily complex operations, and allows formulating computationally hard problems, like the discrete logarithm, which are the basis of modern protocol security.
