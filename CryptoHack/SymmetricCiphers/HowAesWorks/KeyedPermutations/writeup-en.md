# Keyed Permutations

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> AES performs a "keyed permutation", mapping every possible input block to a unique output block. What is the mathematical term for a one-to-one correspondence?

The challenge tests knowledge of a fundamental concept in mathematics and its role in block cipher design.

---

## Theoretical Background

### Functions, injections, surjections, bijections

Let $f : A \to B$ be a function between two sets $A$ and $B$.

- $f$ is **injective** (one-to-one) if distinct inputs map to distinct outputs:
$$a_1 \neq a_2 \implies f(a_1) \neq f(a_2)$$

- $f$ is **surjective** (onto) if every element of $B$ is the image of at least one element of $A$:
$$\forall\, b \in B,\ \exists\, a \in A : f(a) = b$$

- $f$ is **bijective** if it is both injective and surjective. A bijection establishes a perfect **one-to-one correspondence** between $A$ and $B$: every element of $A$ maps to exactly one element of $B$, and every element of $B$ has exactly one preimage in $A$.

A bijection from a finite set to itself is called a **permutation**.

### Why block ciphers must be bijections

A block cipher $E_k : \{0,1\}^n \to \{0,1\}^n$ maps $n$-bit input blocks to $n$-bit output blocks using a key $k$. For decryption to be possible, $E_k$ must be **invertible**, given a ciphertext block $c$, there must exist a unique plaintext block $m$ such that $E_k(m) = c$.

This is precisely the requirement of bijectivity. If $E_k$ were not injective, two different plaintexts would produce the same ciphertext, making decryption ambiguous. If $E_k$ were not surjective, some ciphertext blocks would have no corresponding plaintext, making them undecodable.

Since $E_k$ maps a finite set to itself (both domain and codomain are $\{0,1\}^n$), bijectivity is equivalent to being a permutation. The key $k$ selects which specific permutation to apply, hence the term **keyed permutation**.

### AES-128 as a keyed permutation

AES-128 operates on 128-bit (16-byte) blocks with a 128-bit key. The domain and codomain are both $\{0,1\}^{128}$, a set of $2^{128}$ elements. For each key $k$, AES-128 defines a distinct permutation on this set, one of many possible bijections from $\{0,1\}^{128}$ to itself.

The total number of possible permutations of $2^{128}$ elements is $(2^{128})!$, an astronomically large number. A secure block cipher should behave as if its key is selecting a permutation uniformly at random from this set, an ideal known as a **pseudorandom permutation (PRP)**.

---

### Flag

```
crypto{bijection}
```

---

## Conclusions

The concept of a bijection is foundational to the entire theory of symmetric encryption. Every secure block cipher: AES, DES, Camellia, PRESENT, is a keyed permutation. The security goal is that without knowledge of the key, the permutation should be computationally indistinguishable from a randomly chosen permutation of the block space.