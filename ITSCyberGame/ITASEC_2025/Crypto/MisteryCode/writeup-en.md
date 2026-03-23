# Mystery Code

**Competition:** ITSCyberGame<br>
**Category:** Crypto<br>

---

## Description

> A Squid Game participant found a small note hidden under his bed written in an incomprehensible code. The note seems to contain a secret clue about the next game he and the other participants will face, but no one knows how to read it.
>
> The message on the note is: `synt{7u3_134f7_p4a_j4gpu_7u3_s10j_j4ea3!}`

---

## Solution

The hint is in the description: **"incomprehensible code"**. The structure `synt{...}` is very similar to the `flag{...}` format, which immediately suggests a simple alphabetic substitution.

### Step 1 — Recognizing the Cipher

Looking at the ciphertext `synt{...}`, you notice that:

- `synt` is 4 characters long, just like `flag`
- The structure with curly braces is identical to the flag format

Mapping letter by letter:

```
s → f
y → l
n → a
t → g
```

The shift between `f→s`, `l→y`, `a→n`, `g→t` is always **13 positions**. This is **ROT13**.

### Step 2 — Deciphering the Message

Applying ROT13 to the entire ciphertext gives the flag:

```python
import codecs
cipher = "synt{7u3_134f7_p4a_j4gpu_7u3_s10j_j4ea3!}"
print(codecs.decode(cipher, 'rot_13')) #flag{...}
```
