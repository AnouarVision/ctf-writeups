# Crypting on Structure

**Competition:** OliCyber<br>
**Category:** Crypto

---

## Description

> Decode me!
>
`AAAABAAAAAAAABAABBBAABBABABAAABAABABAABAABBBABAABBAAAAABAABABAABBBBAAA`
>
>The flag is not in the standard format, so decrypt and insert the message inside `flag{...}`.

---

## Solution

### Step 1 — Ciphertext analysis

The text contains only two symbols: `A` and `B`. This suggests a binary encoding. The title "Crypting on Structure" hints that information lies in the structure, how symbols are grouped.

There are 70 characters, divisible by 5 → 14 groups of 5 symbols.

---

### Step 2 — Bacon's cipher

The Baconian cipher (Francis Bacon, 1605) encodes letters as sequences of 5 symbols chosen from two values (here `A` and `B`):

```
A = AAAAA    (00000 = 0)
B = AAAAB    (00001 = 1)
C = AAABA    (00010 = 2)
...
Z = BBAAB    (11001 = 25)
```

With `A = 0` and `B = 1`, each 5-symbol group is a 5-bit binary number indicating a letter index.

---

### Step 3 — Decryption

Split the ciphertext into groups of 5:

```
AAAAB AAAAA AAABA ABBBA ABBAB ABAAA BAABA BAABA ABBBA BAABB AAAAA BAABA BAABB BBAAA
```

Convert each group to decimal and map to letters (A=0):

```
AAAAB = 00001 = 1  → B
AAAAA = 00000 = 0  → A
AAABA = 00010 = 2  → C
ABBBA = 01110 = 14 → O
ABBAB = 01101 = 13 → N
ABAAA = 01000 = 8  → I
BAABA = 10010 = 18 → S
BAABA = 10010 = 18 → S
ABBBA = 01110 = 14 → O
BAABB = 10011 = 19 → T
AAAAA = 00000 = 0  → A
BAABA = 10010 = 18 → S
BAABB = 10011 = 19 → T
BBAAA = 11000 = 24 → Y
```

Result: `BACONISSOTASTY`

---

### Step 4 — Decryption script

```python
def bacon_decrypt(text):
    groups = [text[i:i+5] for i in range(0, len(text), 5)]
    result = ""
    for group in groups:
        val = int(group.replace('A', '0').replace('B', '1'), 2)
        result += chr(val + ord('A'))
    return result

ciphertext = "AAAABAAAAAAAABAABBBAABBABABAAABAABABAABAABBBABAABBAAAAABAABABAABBBBAAA"
print(bacon_decrypt(ciphertext))
# Output: BACONISSOTASTY
```

---

## Flag

flag{baconissotasty}

---

## Conclusion

1. Two symbols grouped in fives → Baconian cipher.
2. The Bacon cipher is an early steganographic method, historically used to hide messages by varying typography.
