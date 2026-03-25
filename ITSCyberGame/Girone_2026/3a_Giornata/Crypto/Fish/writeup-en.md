# Fish

**Competition:** ITSCyberGame
**Category:** Crypto
**Files:** `aziende.csv`, `pp.txt`, `encode3.txt`

---

## Description

> During an Incident Response activity, the SOC recovered three items from a compromised company server:
> * A database containing the full list of companies
> * The password hash of a service account
> * A file containing internal communications encrypted
>
> Early analysis showed the IT department implemented a "homegrown" encryption system, convinced they had achieved perfect secrecy. Unfortunately, some questionable design choices introduced weaknesses.
>
> This is your starting point:
> `Nzk2MjIwNGI2MjY1MjA2NjY4NzYyMDcxNjI3MDY4N2E3MjYxNjc3NjIwNjg2NjZlNjE3MTYyMjA3OTZlMjA2NjY3NzI2NjY2NmUyMDcwNzU3NjZlNjk3Mg==`

**Flag format:** `flag{plaintext}`

---

## Solution

### 1. Decoding the starting string

The provided string is Base64. Decoding it:

```
Nzk2MjIwNGI2MjY1MjA2NjY4NzYyMDcxNjI3MDY4N2E3MjYxNjc3NjIwNjg2NjZlNjE3MTYyMjA3OTZlMjA2NjY3NzI2NjY2NmUyMDcwNzU3NjZlNjk3Mg==
  → (Base64)
7962204b62652066687620716270687a726167762068666e61716220796e2066677266666e207075766e6972
  → (Hex)
yb Kbe fhv qbphzragv hfnaqb yn fgrffn puvnir
  → (ROT13)
use XOR on the documents using the same key
```

The hint is clear: all files were encrypted with XOR using the same key.

---

### 2. Cracking the hash (`encode3.txt`)

`encode3.txt` contains:

```
a670add1a2ed13ffccdb692e3eb385aff70d280d0f3f06c9b60424e2f47fd3d8
```

64 hexadecimal characters → **SHA-256**.

The system's weakness is the password format: `NameWithoutSpaces + YearFounded` for each company in the CSV. Iterate over the database:

```python
import csv, hashlib

target = "a670add1a2ed13ffccdb692e3eb385aff70d280d0f3f06c9b60424e2f47fd3d8"

with open('aziende.csv', 'r', encoding='utf-8') as f:
	reader = csv.DictReader(f, delimiter=';')
	for row in reader:
		password = row['Nome'].replace(' ', '') + row['AnnoFondazione']
		if hashlib.sha256(password.encode()).hexdigest() == target:
			print(f"Password found: {password}")
			break
```

```
Password found: LynxWorksMG89Tech2013
```

The service account belongs to **LynxWorks MG89 Tech**, founded in **2013**.

---

### 3. Recovering the XOR key — Many-Time Pad Attack

`pp.txt` contains 9 lines of hex-encoded ciphertext. The hint states the same keystream XOR was used for all messages — the classic **Many-Time Pad** mistake.

If `C1 = P1 ⊕ K` and `C2 = P2 ⊕ K`, then `C1 ⊕ C2 = P1 ⊕ P2`, which removes the key. With enough ciphertexts you can recover both the key and plaintexts via statistical analysis.

One approach: for each byte position `i`, try all possible key bytes and select the one that yields printable ASCII across the ciphertexts, favoring letters and spaces.

```python
import string

with open('pp.txt', 'r') as f:
	lines = [l.strip() for l in f if l.strip()]
ciphertexts = [bytes.fromhex(l) for l in lines]

key = []
for pos in range(max(len(c) for c in ciphertexts)):
	col = [c[pos] for c in ciphertexts if pos < len(c)]
	best_k, best_score = 0, -1
	for k in range(256):
		dec = [b ^ k for b in col]
		if not all(32 <= b <= 126 for b in dec):
			continue
		score = sum(2 if chr(b) in string.ascii_letters + ' ' else 1 for b in dec)
		if score > best_score:
			best_score, best_k = score, k
	key.append(best_k)
```

The estimated key contains the readable pattern:

```
companynameandyearwithoutspaces[companynameandyearwithoutspaces...]
```

Using a known-plaintext verification (and the recovered fragments), the key length is confirmed to be **31 bytes** and the key is literally the descriptive string:

```
nome azienda e anno senza spazi
```

So the team used as keystream the literal description of how they built passwords.

---

### 4. Decrypting the messages

```python
def xor_decrypt(hex_data, key):
	ct = bytes.fromhex(hex_data)
	return bytes([ct[i] ^ ord(key[i % len(key)]) for i in range(len(ct))]).decode('utf-8')

key = "nome azienda e anno senza spazi"

with open('pp.txt', 'r') as f:
	for i, line in enumerate(f, 1):
		if line.strip():
			print(f"Line {i}: {xor_decrypt(line.strip(), key)}")
```

Example outputs (translated):

```
Line 1: Company policies require attention when entering passwords.
Line 2: The user must fill the expected field following communicated rules.
Line 3: It is necessary to check the keyboard before confirming entered data.
Line 4: It is recommended to use a private context when accessing the portal.
Line 5: Every credential must be typed carefully, avoiding unauthorized sharing.
Line 6: In case of error, the procedure provides a guided secure retry.
Line 7: The system may require additional checks before final confirmation.
Line 8: Internal guidelines urge keeping codes and procedures confidential.
Line 9: Compliance with policies supports operational continuity and data protection.
```

None of the messages contain an explicit flag. The flag is the service account password recovered in step 2.

---

## Flag

```
flag{...}
```

---

## Conclusions

The challenge demonstrates three chained real-world vulnerabilities:

1. **Many-Time Pad**: Reusing the same XOR keystream across multiple messages destroys confidentiality, the reason a one-time pad must never be reused.
2. **Weak, predictable passwords**: Building passwords from public database fields (`NameWithoutSpaces + Year`) enables a targeted dictionary attack without large wordlists.
3. **Self-descriptive key**: Using as the key the literal description of how the key is generated (`"nome azienda e anno senza spazi"`) is critically weak and trivially exploitable when multiple ciphertexts are available.
