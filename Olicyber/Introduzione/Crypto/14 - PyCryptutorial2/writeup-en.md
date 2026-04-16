# PyCryptutorial 2

**Competition:** OliCyber <br>
**Category:** Crypto <br>
**Service:** `nc cr14.challs.olicyber.it 30007`

---

## Description

> This challenge finishes the introductory PyCryptodome tutorial.

The server asks five short questions about hash functions, HMAC, DSA key parameters and primality testing. Correct answers return the flag.

---

## Solution

### Step 1 — SHA3‑384 hash

Compute SHA3‑384 of the ASCII string `hash_me_pls` using PyCryptodome:

```py
from Crypto.Hash import SHA3_384

h = SHA3_384.new()
h.update(b'hash_me_pls')
print(h.hexdigest())
```

Output:

```
2daba465e04884079b220e455061be60740e2739cfc864c8dd650f8ec688700aa046d78d408725bb5e6f9fb6a387af25
```

---

### Step 2 — HMAC‑SHA224

Given `key.hex() = 'a0969b82...5fc65b'` and message `La mia integrità è importante!`, compute HMAC with SHA‑224:

```py
from Crypto.Hash import HMAC, SHA224

key = bytes.fromhex('a0969b8259d73d619c500da29e8e0e169aa0c71943707ab2e1e82bfb0e5fc65b')
h = HMAC.new(key, 'La mia integrità è importante!'.encode('utf-8'), SHA224)
print(h.hexdigest())
```

Output:

```
53246be22141f11ea9dbc93c4d4ce486c726401d76adc4d901629b11
```

---

### Step 3 — Extract DSA parameters

The server provides a DER-encoded DSA key. Use PyCryptodome to import it and read `x`, `g`, `q`:

```py
from Crypto.PublicKey import DSA

key = DSA.import_key(der_bytes)
print(key.x)
print(key.g)
print(key.q)
```

Example output (values truncated in README):

```
x = 178754102630780949657156804783723575105266101658277178106272920043
g = 26889620844978... (large)
q = 18149454321975056401440128528567616877710863748281779964914588693987
```

---

### Step 4 — Generate a 1414‑bit prime

Use `getPrime(1414)` from `Crypto.Util.number` (Miller–Rabin based) to produce a probable prime of exactly 1414 bits.

```py
from Crypto.Util.number import getPrime
p = getPrime(1414)
print(p)
```

---

### Step 5 — Primality test

Given an integer, use `isPrime(n)` from `Crypto.Util.number` to decide primality (probabilistic Miller–Rabin). Answer with `si` (yes) or `no` accordingly.

```py
from Crypto.Util.number import isPrime
print('si' if isPrime(n) else 'no')
```

---

## Flag

```
flag{...}
```

---

## Notes

- SHA‑3 uses a sponge construction, different from SHA‑2.
- HMAC resists length‑extension attacks; do not replace it with naive `H(key||msg)`.
- DSA security depends on parameters and correct nonce use.
- `getPrime`/`isPrime` use Miller–Rabin with sufficient iterations for practical safety.
