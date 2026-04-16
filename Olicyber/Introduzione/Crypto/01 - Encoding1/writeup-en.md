# Encoding 1

**Competition:** OliCyber <br>
**Category:** Crypto

---

## Description

> An encoding is a system of signals or symbols designated to represent information. ASCII is a standard that maps integers to characters using 7-bit codes.

You are given a list of integers. The flag is obtained by converting each number to its corresponding ASCII character.

```
[102, 108, 97, 103, 123, 117, 103, 104, 95, 78, 117, 109, 66, 51, 114, 53, 95, 52, 49, 114, 51, 52, 100, 121, 125]
```

---

## Solution

### Step 1 — ASCII standard

ASCII (American Standard Code for Information Interchange) maps integers {0..127} to 128 symbols (letters, digits, punctuation, control chars). Each symbol can be obtained with Python's `chr()`.

### Step 2 — Decode

Convert each integer to a character and join:

```python
nums = [102,108,97,103,123,117,103,104,95,78,117,109,66,51,114,53,95,52,49,114,51,52,100,121,125]
print(''.join(chr(n) for n in nums))
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

- Encoding is not encryption: ASCII is public and reversible.
- At the lowest level, text is just numbers; understanding representations (bits → bytes → integers → chars) is essential.
