# RSA Helpline

**Competition:** OliCyber <br>
**Category:** Crypto <br>
**Service:** `nc crypto-11.challs.olicyber.it 30004`

---

## Description

> Moduli, powers, inverses... what a mess! RSA is not trivial.

The server walks through RSA key generation, encryption and decryption. Answering every question correctly returns the flag.

---

## Mathematical background

**RSA scheme.** RSA relies on three facts: the difficulty of integer factorization, Euler's totient function, and Euler's theorem.

**Euler's totient function.** $\phi(n)$ counts integers in $[1,n-1]$ that are coprime with $n$. For $n=p\cdot q$ with distinct primes $p,q$:

$$\phi(n) = (p-1)(q-1)$$

**Euler's theorem.** For any $a$ coprime with $n$:

$$a^{\phi(n)} \equiv 1 \pmod{n}$$

**RSA key generation.**
1. Choose two primes $p, q$ and compute $n = p \cdot q$.
2. Choose $e$ with $\gcd(e, \phi(n)) = 1$ → public key $(n, e)$.
3. Compute $d = e^{-1} \bmod \phi(n)$ → private exponent $d$.

**Encryption / decryption.**

$$c = m^e \bmod n \qquad m = c^d \bmod n$$

Correctness follows from Euler's theorem because if $ed \equiv 1 \pmod{\phi(n)}$ then $ed = 1 + k\phi(n)$ for some $k$, so $m^{ed} = m^{1+k\phi(n)} = m (m^{\phi(n)})^k \equiv m \pmod{n}$.

---

## Solution

### Step 1 — Compute the modulus

Given $p = 11$, $q = 19$:

$$n = p \cdot q = 11 \cdot 19 = \mathbf{209}$$

---

### Step 2 — Euler's totient

$$\phi(n) = (p-1)(q-1) = 10 \cdot 18 = \mathbf{180}$$

---

### Step 3 — Encryption

Choose $m = 42$, $e = 7$. Verify $\gcd(7,180)=1$ ✓.

$$c = m^e \bmod n = 42^7 \bmod 209$$

Using modular exponentiation (`pow(42, 7, 209)`):

$$c = \mathbf{158}$$

---

### Step 4 — Compute private exponent

Compute $d = e^{-1} \bmod \phi(n) = 7^{-1} \bmod 180$ with the extended Euclidean algorithm.

Euclidean steps:

$$180 = 25 \cdot 7 + 5$$
$$7 = 1 \cdot 5 + 2$$
$$5 = 2 \cdot 2 + 1$$

Back-substitute to get $1 = 3 \cdot 180 - 77 \cdot 7$, hence

$$d = -77 \bmod 180 = \mathbf{103}$$

Check: $7 \cdot 103 = 721 = 4 \cdot 180 + 1 \equiv 1 \pmod{180}$ ✓

---

### Step 5 — Decryption

$$m = c^d \bmod n = 158^{103} \bmod 209 = \mathbf{42}$$

Check: `pow(158, 103, 209) == 42` ✓

---

### Script

```python
p, q = 11, 19
n = p * q
phi = (p - 1) * (q - 1)
m = 42
e = 7

c = pow(m, e, n)
d = pow(e, -1, phi)
m_dec = pow(c, d, n)

print(f"n={n}, phi={phi}, c={c}, d={d}, m_dec={m_dec}")
```

**Output:**
```
n=209, phi=180, c=158, d=103, m_dec=42
```

---

## Flag

```
flag{...}
```

---

## Conclusions

> The security of RSA does not depend on the algorithm itself but on the infeasibility of factoring $n$ to recover $\phi(n)$ and thus $d$.

Three key remarks from this tutorial:

1. **Use modular exponentiation (`pow(m, e, n)`)**: naive `m**e % n` builds huge intermediate values; `pow` keeps intermediates reduced and runs in $O(\log e)$ via square-and-multiply.

2. **$\gcd(e, \phi(n)) = 1$ is mandatory**: otherwise $e$ isn't invertible modulo $\phi(n)$ and $d$ does not exist. Practically, $e=65537$ is a common choice.

3. **Factoring $n$ is the actual secret**: knowing $p,q$ yields $\phi(n)$ and thus $d$; hence $p,q$ must be kept private and sufficiently large.
