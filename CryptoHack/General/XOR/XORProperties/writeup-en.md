# XOR Properties

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Three random keys have been XOR'd together and with the flag. Use the properties of XOR to undo the encryption and recover the flag.

The following hex-encoded values are provided:

```
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
```

---

## Theoretical Background

### The four properties of XOR

| Property | Statement |
|:---|:---|
| Commutative | $A \oplus B = B \oplus A$ |
| Associative | $A \oplus (B \oplus C) = (A \oplus B) \oplus C$ |
| Identity | $A \oplus 0 = A$ |
| Self-inverse | $A \oplus A = 0$ |

Together, these four properties make $(\{0,1\}^n, \oplus)$ an **abelian group**. The most operationally useful consequence is the **cancellation law**: for any $A, K$, if $C = A \oplus K$ then $C \oplus K = A \oplus K \oplus K = A \oplus 0 = A$. XOR-ing with the key a second time undoes the encryption.

---

## Solution

### Algebraic derivation

The three steps each apply the cancellation law to isolate an unknown from a known XOR relation.

**Step 1 — Recover KEY2**

$$\text{KEY2} \oplus \text{KEY1} = R_1 \implies \text{KEY2} = R_1 \oplus \text{KEY1}$$

**Step 2 — Recover KEY3**

$$\text{KEY2} \oplus \text{KEY3} = R_2 \implies \text{KEY3} = R_2 \oplus \text{KEY2}$$

**Step 3 — Recover FLAG**

By commutativity and associativity, the order of keys in the ciphertext is irrelevant:

$$C = \text{FLAG} \oplus \text{KEY1} \oplus \text{KEY2} \oplus \text{KEY3}$$

$$\text{FLAG} = C \oplus \text{KEY1} \oplus \text{KEY2} \oplus \text{KEY3}$$

Each key cancels itself: $\text{KEY}_i \oplus \text{KEY}_i = 0$, leaving only FLAG.

### Script

```python
#!/usr/bin/env python3

hex_key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
hex_key2_xor_key1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
hex_key2_xor_key3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
hex_flag_xor_key1_xor_key3_xor_key2 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

key1 = bytes.fromhex(hex_key1)
key2_xor_key1 = bytes.fromhex(hex_key2_xor_key1)
key2 = bytes([a ^ b for a, b in zip(key2_xor_key1, key1)])

key2_xor_key3 = bytes.fromhex(hex_key2_xor_key3)
key3 = bytes([a ^ b for a, b in zip(key2_xor_key3, key2)])

ciphertext = bytes.fromhex(hex_flag_xor_key1_xor_key3_xor_key2)
flag = bytes([a ^ b ^ c ^ d for a, b, c, d in zip(ciphertext, key1, key2, key3)])

print(flag)
```

### Step-by-step

| Step | Known | Unknown | Operation |
|:---:|:---|:---|:---|
| 1 | KEY1, KEY2 $\oplus$ KEY1 | KEY2 | $\text{KEY2} = (K2 \oplus K1) \oplus K1$ |
| 2 | KEY2, KEY2 $\oplus$ KEY3 | KEY3 | $\text{KEY3} = (K2 \oplus K3) \oplus K2$ |
| 3 | KEY1, KEY2, KEY3, ciphertext | FLAG | $\text{FLAG} = C \oplus K1 \oplus K2 \oplus K3$ |

---

### Flag

```
crypto{...}
```

---

## Conclusions

This challenge demonstrates that XOR encryption is only as strong as the secrecy of its keys. When partial information about the keys is available, here, XOR combinations of the keys are given directly, the algebraic structure of XOR allows the unknowns to be reconstructed one by one, until the plaintext is fully exposed.