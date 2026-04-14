# All Roads Lead to Rome

**Competition:** OliCyber<br>
**Category:** Crypto

---

## Description

>On an ancient parchment this quotation was found. Try to decrypt it:
>`cixd{xsb_zxbpxo_jlofqrof_qb_pxirqxkq}`

The title is a hint: "All roads lead to Rome", a direct reference to ancient Rome and therefore the Caesar cipher.

---

## Solution

### Step 1 — Caesar cipher

Each plaintext letter is replaced by the letter that is `n` positions further in the alphabet. The challenge hints at a classical Caesar shift.

Decryption formula (for lowercase letters):

```
P = (C + shift) mod 26
```

### Step 2 — Decrypting

Applying a shift of `+3` to each letter in the ciphertext yields:

```
Encrypted:    c  i  x  d  {  x  s  b  _  z  x  b  p  x  o  _  j  l  o  f  q  r  o  f  _  q  b  _  p  x  i  r  q  x  k  q  }
Deciphered:  f  l  a  g  { ... }
```

### Step 3 — Decryption script

```python
def caesar_decrypt(text, shift=3):
	result = ""
	for c in text:
		if c.isalpha():
			result += chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
		else:
			result += c
	return result

ciphertext = "cixd{xsb_zxbpxo_jlofqrof_qb_pxirqxkq}"
print(caesar_decrypt(ciphertext))
# Output: flag{...}
```

---

## Flag

flag{...}

---

## Conclusion

1. Recognizing `cixd{` → `flag{` reveals the shift quickly.
2. The Caesar cipher is insecure, only 25 possible keys, trivial to brute force.

