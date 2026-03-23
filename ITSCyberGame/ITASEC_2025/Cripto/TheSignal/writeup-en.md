# The Signal

**Competition:** ITSCyberGame<br>
**Category:** Cryptography<br>
**File:** the_signal.txt

---

## Description

> A group intercepted an encrypted message from an allied group, saying it contains the key to break their defenses, but no one knows how to read it.

---

## Solution

The message is encrypted in **three stacked layers**: Binary Morse → Base64 → ROT47.

### Step 1 — Binary Morse

The symbols do not follow standard Morse code: there are only two distinct values, `----- ` and `.----`, which immediately recall a `0` and a `1`. This is **binary encoding disguised as Morse**.

Mapping each token:

```
-----  →  0
.----  →  1
```

You get a long bit string. Grouping it into blocks of 8 and converting each byte to ASCII:

```python
signal = "----- .---- ----- ----- .---- .---- .---- ----- ..."
tokens = signal.split()

bits = ""
for t in tokens:
	if t == "-----":
		bits += "0"
	elif t == ".----":
		bits += "1"

chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
result = "".join(chars)
# → Nz0yOExST1Q0Nz5jRDxkMD5fQ2IwZjljPzA9YkVFYkNkTg==
```

The result is a recognizable Base64 string due to the `==` padding at the end.

### Step 2 — Base64

Decoding the Base64 string:

```python
import base64
b64 = "Nz0yOExST1Q0Nz5jRDxkMD5fQ2IwZjljPzA9YkVFYkNkTg=="
decoded = base64.b64decode(b64).decode()
# → 7=28LROT47>cD<d0>_Cb0f9c?0=bEEbCdN
```

The result is a string of apparently random ASCII characters. The substring `LROT` is a clue: **ROT**ation cipher.

### Step 3 — ROT47

Looking at the first 4 characters `7=28`, you notice that the format `flag{...}` also has 4 initial characters. Calculating the ASCII difference:

```
f (102) - 7 (55) = 47  (not a standard Caesar)
```

Instead, applying a rotation over the entire set of printable ASCII characters (from `!` to `~`, 94 total) with a shift of **47**—the classic **ROT47**:

```python
s = "7=28LROT47>cD<d0>_Cb0f9c?0=bEEbCdN"

result = ""
for c in s:
	if 33 <= ord(c) <= 126:
		result += chr((ord(c) - 33 + 47) % 94 + 33)

print(result)
# → flag{...}
```

---

## Complete Script

```python
import base64

# Step 1: Binary Morse → bits → ASCII (Base64)
signal = open("the_signal.txt").read().strip()
tokens = signal.split()

bits = "".join("0" if t == "-----" else "1" for t in tokens)
b64 = "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# Step 2: Base64 → encrypted string
s = base64.b64decode(b64).decode()

# Step 3: ROT47 → flag
flag = "".join(chr((ord(c) - 33 + 47) % 94 + 33) if 33 <= ord(c) <= 126 else c for c in s)
print(flag)
```
