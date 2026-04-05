# À l'aise

**Competition:** FCSC 2022 (intro)
**Category:** Crypto

---

## Description
This challenge gives a message encrypted with the classical Vigenère cipher. The key is `FCSC` and the ciphertext is:

```
Gqfltwj emgj clgfv ! Aqltj rjqhjsksg ekxuaqs, ua xtwk
n'feuguvwb gkwp xwj, ujts f'npxkqvjgw nw tjuwcz
ugwygjtfkf qz uw efezg sqk gspwonu. Jgsfwb-aqmu f
Pspygk nj 29 cntnn hqzt dg igtwy fw xtvjg rkkunqf.
```

The flag is the name of the city mentioned in the plaintext.

---

## Solution

### 1. Quick reconnaissance

Key: `FCSC`. No cracking needed, decrypt directly with the known key.

### 2. Vigenère overview

Encryption formula:

$$C_i = (P_i + K_{i \bmod |key|}) \bmod 26$$

Decryption:

$$P_i = (C_i - K_{i \bmod |key|}) \bmod 26$$

Non-alphabetic characters (spaces, punctuation, newlines) are skipped and do not advance the key index.

### 3. Decryption script

```python
def vigenere_decrypt(ct, key):
    key = key.upper()
    pt = []
    ki = 0
    for c in ct:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - ord('A')
            base = ord('A') if c.isupper() else ord('a')
            pt.append(chr((ord(c) - base - shift) % 26 + base))
            ki += 1
        else:
            pt.append(c)
    return ''.join(pt)

ct = """Gqfltwj emgj clgfv ! Aqltj rjqhjsksg ekxuaqs, ua xtwk
n'feuguvwb gkwp xwj, ujts f'npxkqvjgw nw tjuwcz
ugwygjtfkf qz uw efezg sqk gspwonu. Jgsfwb-aqmu f
Pspygk nj 29 cntnn hqzt dg igtwy fw xtvjg rkkunqf."""

print(vigenere_decrypt(ct, "FCSC"))
```

**Output:**

```
Bonjour cher eleve ! Votre progression scolaire, au vu
d'elements bien sur, nous n'envisageons de changer
votre orientation ou de cycle que gracieux. Rendez-vous a
Nantes le 29 avril pour de feter de votre passion.
```

The city mentioned is **Nantes**.

---

## Flag

FCSC{Nantes}

---

## Notes

Introductory Vigenère task: with the key known, decrypting is straightforward. Remember to skip non-letter characters when advancing the key index.
