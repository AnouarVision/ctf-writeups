# A Difficult Communication

**Competition:** OliCyber <br>
**Category:** Crypto <br>
**Service:** `nc crypto-13.challs.olicyber.it 30006`

---

## Description

> This challenge is similar to the previous one, but here you must choose the Diffie–Hellman parameters yourself.

The server asks for a safe prime $p$ (>=1024 bits) and a generator $g$, performs a DH exchange with Alice, and then uses the shared secret to encrypt a message with AES‑CBC.

---

## Background

Safe prime: a prime $p$ is called a safe prime when $q=(p-1)/2$ is also prime. For a safe prime the group $(\mathbb{Z}/p\mathbb{Z})^*$ has order $p-1=2q$, whose only prime factors are $2$ and $q$. This resists Pohlig–Hellman reductions that exploit factorization of the group order.

Primitive generator: an element $g$ is a primitive root iff its order is exactly $p-1$. For $p=2q+1$ it suffices to check:
$$g^2\not\equiv1\pmod p\quad\text{and}\quad g^q\not\equiv1\pmod p.$$
If any of those equalities holds the element lies in a proper subgroup (orders 1, 2 or $q$).

That explains why $g=2$ was rejected: for the chosen $p$ one has $2^q\equiv1\pmod p$, so 2 has order $q$ rather than $p-1$ and only generates a subgroup of index 2.

---

## Solution

### Step 1 — Choose parameters

Use the RFC 3526 MODP 1536-bit safe prime for $p$ (well-known and verified). Compute $q=(p-1)/2$ and search the smallest $g\ge2$ satisfying the two checks above. Example Python snippet:

```py
q = (p - 1) // 2
for g in range(2, 100):
    if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
        print(g)  # g = 11
        break
```

The first valid generator in this example is `g = 11`.

---

### Step 2 — DH exchange

Pick a random private key $b\in[2,p-2]$ and compute your public key $A=g^b\bmod p$, send it to Alice and receive Alice's public key $B$ (hex). The shared secret is
$$S=B^b\bmod p = g^{ab}\bmod p.$$

---

### Step 3 — AES‑CBC decryption

Alice encrypts the message with AES‑CBC using the first 16 bytes of the shared secret $S$ as the AES key:

```py
shared_bytes = S.to_bytes((S.bit_length() + 7) // 8, 'big')
key = shared_bytes[:16]
cipher = AES.new(key, AES.MODE_CBC, IV)
plaintext = unpad(cipher.decrypt(ct), 16)
```

(This KDF is weak in practice; a proper HKDF should be used.)

---

### Exploit (example)

The Italian writeup includes a full working exploit using the RFC 3526 1536-bit prime, a chosen private exponent `b` and Alice's provided public value (hex). Converting the computed shared secret to bytes and taking the first 16 bytes as AES key, decrypting the provided IV+ciphertext yields the flag.

Example output:

```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Notes

- Use safe primes to avoid Pohlig–Hellman attacks.
- Rejecting `g=2` was correct: it generated a subgroup of order `q`, reducing security.
- Do not use raw DH output bytes as a symmetric key in production; apply a KDF such as HKDF.
