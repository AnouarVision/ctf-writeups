# XOR 1

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

XOR (exclusive OR) is a simple and widely used operation to obfuscate data. You are given two hex-encoded messages; XORing them byte-wise recovers the plaintext flag.

```
m1 = 158bbd7ca876c60530ee0e0bb2de20ef8af95bc60bdf
m2 = 73e7dc1bd30ef6576f883e79edaa48dcd58e6aa82aa2
```

---

## Solution

### Step 1 — XOR definition

XOR is a binary operation with truth table:

0 ⊕ 0 = 0, 0 ⊕ 1 = 1, 1 ⊕ 0 = 1, 1 ⊕ 1 = 0

Applied to byte sequences, it operates bitwise on corresponding positions.

### Step 2 — Key property

XOR is an involution: (A ⊕ K) ⊕ K = A. This is the basis of OTP and stream ciphers: encrypt and decrypt are the same operation.

### Step 3 — Script

```python
m1 = bytes.fromhex('158bbd7ca876c60530ee0e0bb2de20ef8af95bc60bdf')
m2 = bytes.fromhex('73e7dc1bd30ef6576f883e79edaa48dcd58e6aa82aa2')
print(bytes(x ^ y for x, y in zip(m1, m2)).decode())
```

Output:

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

- XOR is linear over GF(2)^n; while efficient and reversible, used alone it is insecure — modern ciphers add non-linearity (S-boxes, rotations) to break linear structure.
