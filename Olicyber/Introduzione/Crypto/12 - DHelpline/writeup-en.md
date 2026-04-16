# DH Helpline

**Competition:** OliCyber <br>
**Category:** Crypto <br>
**Service:** `nc crypto-12.challs.olicyber.it 30005`

---

## Description

> One of the classic hard problems in asymmetric cryptography is the discrete logarithm.

This challenge asks several short questions about the discrete logarithm and the Diffie–Hellman protocol. Answering all correctly returns the flag.

---

## Background

If $p$ is prime, the multiplicative group $(\mathbb{Z}/p\mathbb{Z})^*$ has order $p-1$ and is cyclic: there exists a generator $g$ whose powers produce every element of the group. The discrete logarithm problem (DLP) asks, given $g$ and $h$, to find $x$ such that $g^x\equiv h\pmod p$. Diffie–Hellman key exchange uses this hardness: if Alice publishes $A=g^a$ and Bob publishes $B=g^b$, the shared secret is $S=g^{ab}=A^b=B^a$.

---

## Solution

### Step 1 — Euler's totient for prime $p$

The server asks how many positive integers less than $p$ are coprime with $p$. For prime $p$ this is $\varphi(p)=p-1$.
Answer: `p-1`

---

### Step 2 — Discrete log of a power of 2

Compute $\log_2(65536)\bmod p$ where $p=295698861441889376682620757082475676757$. Since $65536=2^{16}$ and $65536<p$, the exponent is $16$.
Answer: `16`

---

### Step 3 — Discrete log of 11 base 2 modulo 29

Find $x$ such that $2^x\equiv 11\pmod{29}$. Using modular exponentiation we find:
```py
pow(2,25,29) # => 11
```
So $x=25$.
Answer: `25`

---

### Step 4 — Diffie–Hellman exchange

Server gives $p=61$, $g=2$, and server public key $B=18$. Choose private key $b=5$ so our public key is:
$$A=g^b\bmod p=2^5\bmod61=32.$$
Compute the shared secret:
$$S=B^b\bmod p=18^5\bmod61=32.$$
So send public key `32` and the shared secret is `32`.

---

## Script

```python
p, g = 61, 2
B_server = 18
b = 5

A_pub = pow(g, b, p)
shared = pow(B_server, b, p)

print(f"Public key: {A_pub}")
print(f"Shared secret: {shared}")

print(pow(2, 25, 29))
```

Output:

```
Public key: 32
Shared secret: 32
11
```

---

## Flag

```
flag{...}
```

---

## Notes

- Diffie–Hellman is a key-agreement protocol, not an encryption scheme.
- Security relies on the hardness of the DLP and on choosing strong group parameters.
