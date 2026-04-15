# One More Time Please

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

> Using the Vernam cipher gives perfect secrecy. A fundamental rule for One-Time Pad systems is to never reuse a key.

You are given `output.txt` containing 9 ciphertexts in hexadecimal, all produced with the **same key** $K$ via XOR (Vernam cipher).

---

## Solution

### Step 1 — The key cancels algebraically

The Vernam cipher encrypts each message $P_i$ with the same key $K$:

$$C_i = P_i \oplus K, \quad i = 1, \ldots, 9$$

XORing any two ciphertexts cancels the key because $K \oplus K = \mathbf{0}$:

$$C_i \oplus C_k = P_i \oplus P_k$$

With $N = 9$ messages we obtain $\binom{9}{2} = 36$ pairs, each exposing the XOR of two plaintexts and making the system completely vulnerable.

---

### Step 2 — Statistical recovery of the key via MTP

Messages are ASCII text. XOR between a space (`0x20`) and a letter yields another letter:

$$\texttt{0x20} \oplus \ell \in \texttt{[A-Za-z]}, \quad \forall\, \ell \in \texttt{[A-Za-z]}$$

For each position $j$ compute $C_i[j] \oplus C_k[j]$ across all 36 pairs. If the result is an alphabetic byte, one of the two plaintexts likely has a space in position $j$, and we cast a vote:

$$\hat{K}[j] \leftarrow C_i[j] \oplus \texttt{0x20}$$

The key byte is estimated by maximum likelihood from votes at that position:

$$\hat{K}[j] = \arg\max_{v} \;\#\{\text{votes for } v \text{ at position } j\}$$

Applying this across positions yields an estimated key $\hat{K}$ and partial decryptions $P_i[j] = C_i[j] \oplus \hat{K}[j]$.

---

### Step 3 — Reading partial plaintexts

Running the voting heuristic on `output.txt` produces partially readable plaintexts. The following output demonstrates recovery of message 3 which clearly contains the flag prefix:

```python
from collections import Counter

ciphertexts = [bytes.fromhex(line.strip()) for line in open("output.txt") if line.strip()]

max_len = max(len(c) for c in ciphertexts)
key_votes = [[] for _ in range(max_len)]

for i, ct1 in enumerate(ciphertexts):
    for j, ct2 in enumerate(ciphertexts):
        if i == j:
            continue
        for pos in range(min(len(ct1), len(ct2))):
            xored = ct1[pos] ^ ct2[pos]
            if 65 <= xored <= 90 or 97 <= xored <= 122:
                key_votes[pos].append(ct1[pos] ^ 0x20)
                key_votes[pos].append(ct2[pos] ^ 0x20)

key = [Counter(v).most_common(1)[0][0] if v else 0 for v in key_votes]

for i, ct in enumerate(ciphertexts):
    print(f"ct{i+1}: {''.join(chr(ct[j] ^ key[j]) for j in range(len(ct)))}")
```

**Output:**

```
ct1: IL CRITTOSISTEMA CHE STO UTIL_ZZ__DO S_MB__ IND_STR_TT_B_LE
ct2: NON LEGGERAI MAI QUESTA SEGRETISSIMA FRASE
ct3: LA MIA PREZIOSA FLAG: flag{M4_y_71_3_P_D_N_gH_m_r_}
...
```

Some positions remain ambiguous where votes are scarce, but the partial reads are sufficient to identify structure and candidate plaintexts (notably message 3 contains `LA MIA PREZIOSA FLAG: flag{`).

---

### Step 4 — Refinement via Known-Plaintext (KPA)

Recognize and guess clear substrings, then derive exact key bytes from known plaintext segments:

$$K[t] = C_i[t] \oplus P_i[t], \quad t = 0, \ldots, \ell-1$$

Overwrite statistical estimates with these exact bytes. Each confirmed key byte immediately decodes that position across all other ciphertexts, improving readability iteratively.

---

### Step 5 — Exploit

```python
from collections import Counter

ciphertexts = [bytes.fromhex(line.strip()) for line in open("output.txt") if line.strip()]

max_len = max(len(c) for c in ciphertexts)
key_votes = [[] for _ in range(max_len)]

for i, ct1 in enumerate(ciphertexts):
    for j, ct2 in enumerate(ciphertexts):
        if i == j:
            continue
        for pos in range(min(len(ct1), len(ct2))):
            xored = ct1[pos] ^ ct2[pos]
            if 65 <= xored <= 90 or 97 <= xored <= 122:
                key_votes[pos].append(ct1[pos] ^ 0x20)
                key_votes[pos].append(ct2[pos] ^ 0x20)

key = [Counter(v).most_common(1)[0][0] if v else 0 for v in key_votes]

def set_key(ct, known, offset=0):
    for i, (c, p) in enumerate(zip(ct[offset:], known)):
        key[offset + i] = c ^ p
set_key(ciphertexts[2], b"LA MIA PREZIOSA FLAG: flag{")
set_key(ciphertexts[0], b"IL CRITTOSISTEMA CHE STO UTILIZZANDO SEMBRA INDISTRUTTIBILE")
set_key(ciphertexts[1], b"NON LEGGERAI MAI QUESTA SEGRETISSIMA FRASE")
set_key(ciphertexts[4], b"SONO SICURO CHE NON CI SARANNO PROBLEMI, I MIEI AMICI SI SBAGLIANO VI MORO")
set_key(ciphertexts[6], b"POTREMMO LASCIARE TUTTI I FRIGORIFERI APERTI PER QUALCHE ANNO")

ct3 = ciphertexts[2]
print(''.join(chr(ct3[i] ^ key[i]) for i in range(len(ct3))))
```
---

**Output:**

```
LA MIA PREZIOSA FLAG: flag{...}
```

---

## Conclusions

> A One-Time Pad key must never be reused: doing so destroys the perfect secrecy guaranteed by Shannon's theorem.

Secure OTP usage requires:

- **Fresh key** per message: `key = os.urandom(len(plaintext))`
- **Uniform key** independent of plaintext
- **No key reuse**, not even partially

Reusing the OTP key across $N$ messages yields the Many-Time Pad (MTP) vulnerability: pairwise XORs reveal $P_i \oplus P_k$, and space-frequency provides a free statistical oracle to recover $K$ byte-by-byte. Any known substring in one message propagates to all others.
