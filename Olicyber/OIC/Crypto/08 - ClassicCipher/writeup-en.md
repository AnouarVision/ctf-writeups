# Classic Cipher

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description
> Ciphertext: `xcqv{gvyavn_zvztv_etvtddlnxcgy}`
---

## Code analysis

```python
def generateKey():
    start = random.randint(1, 25)
    key = "".join([alphabet[start:], alphabet[0:start]])
    return key
```

The initial key is a cyclic rotation of the alphabet by `start` positions to the left:

$$K^{(0)} = \sigma^{\text{start}}(\mathcal{A})$$

where $\mathcal{A} = (\texttt{a}, \texttt{b}, \ldots, \texttt{z})$ and $\sigma$ is the left-rotation operator by one step on $\mathbb{Z}_{26}$.

```python
def encrypt(plain, key):
    for k in range(len(plain)):
        i = alphabet.index(character)
        characterEncrypted = key[i]
        key = "".join([key[len(key)-1:], key[0:len(key)-1]])
```

At each step $t$, the letter at position $i$ is encrypted as $K^{(t)}[i]$, then the key is rotated one step to the **right**:

$$K^{(t+1)} = \sigma^{-1}(K^{(t)})$$

---

## Mathematical model

Let $\mathcal{A} = \{0,1,\ldots,25\}$ be the alphabet identified with $\mathbb{Z}_{26}$. The key at step $t$ is:

$$K^{(t)}[j] = (j + \text{start} - t) \bmod 26 \qquad \forall j \in \mathbb{Z}_{26}$$

The encryption of the character at position $i$ and step $t$ is therefore:

$$C_t = K^{(t)}[P_t] = (P_t + \text{start} - t) \bmod 26$$

where $P_t \in \mathbb{Z}_{26}$ is the numeric value of the plaintext letter.

Decryption is obtained by inverting the map:

$$P_t = (C_t - \text{start} + t) \bmod 26$$

This structure is analogous to an elementary rotor machine: the key is not static but evolves deterministically with each encrypted character, introducing a dependence on the message position $t$.

---

## Solution

### Step 1 — Key space

The parameter `start` is sampled uniformly from $\{1,\ldots,25\}$, producing a key space of cardinality:

$$|\mathcal{K}| = 25$$

This makes brute force trivial: $O(25 \cdot n)$ operations, where $n$ is the ciphertext length.

### Step 2 — Known Plaintext Attack

The flag format is known: the first four plaintext characters are `flag`, corresponding to $P = (5,11,0,6)$ in $\mathbb{Z}_{26}$.

For $t=0$ (first character):

$$C_0 = (P_0 + \text{start}) \bmod 26$$
$$\texttt{x} = (5 + \text{start}) \bmod 26$$
$$\text{start} = (23 - 5) \bmod 26 = 18$$

Verify on subsequent positions:

$$t=1: \quad C_1 = (11 + 18 - 1) \bmod 26 = 28 \bmod 26 = 2 \quad \longrightarrow \quad \texttt{c} \checkmark$$
$$t=2: \quad C_2 = (0 + 18 - 2) \bmod 26 = 16 \quad \longrightarrow \quad \texttt{q} \checkmark$$
$$t=3: \quad C_3 = (6 + 18 - 3) \bmod 26 = 21 \quad \longrightarrow \quad \texttt{v} \checkmark$$

The key is uniquely determined: $\text{start} = 18$.

### Step 3 — Full decryption

Applying $P_t = (C_t - 18 + t) \bmod 26$ to every alphabetic character:

```python
alphabet = "abcdefghijklmnopqrstuvwxyz"

def decrypt(ciphertext, start):
    key = alphabet[start:] + alphabet[:start]
    plaintext = ""
    for c in ciphertext:
        if c.islower():
            i = key.index(c)
            plaintext += alphabet[i]
            key = key[-1:] + key[:-1]
        elif c.isupper():
            i = key.index(c.lower())
            plaintext += alphabet[i].upper()
            key = key[-1:] + key[:-1]
        else:
            plaintext += c
    return plaintext

ciphertext = "xcqv{gvyavn_zvztv_etvtddlnxcgy}"
print(decrypt(ciphertext, 18))
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusions

This challenge illustrates three fundamental properties of elementary rotor ciphers:

1. **Insufficient key space**: $|\mathcal{K}| = 25$ is negligible. For secure ciphers the key space should satisfy $|\mathcal{K}| \ge 2^{128}$, making enumeration infeasible under brute-force complexity assumptions.

2. **Key rotation does not add entropy**: the function $K^{(t)}[j] = (j + \text{start} - t) \bmod 26$ is fully determined by the single scalar parameter $\text{start} \in \mathbb{Z}_{25}$. The dependence on $t$ is linear and invertible, offering no cryptanalytic protection.

3. **Known Plaintext Attack is immediate**: the linearity of the encryption map in $\mathbb{Z}_{26}$ allows recovering $\text{start}$ from the single pair $(P_0, C_0)$, reducing the attack to one modular subtraction. Modern ciphers like AES are designed to resist KPA even with many known pairs.
