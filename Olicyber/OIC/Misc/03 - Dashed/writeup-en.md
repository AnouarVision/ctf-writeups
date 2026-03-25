# Dashed

**Competition:** OliCyber
**Category:** Misc
**File:** `dashed.txt`

---

## Description

> "This morning I received an email that contained this message, but I can't understand what it is. Can you help me decipher it?"

A text file containing a sequence of dots and dashes. The goal is to decode the message and find the flag.

---

## Solution

### 1. Initial reconnaissance

The file contains only `.`, `-` and `,` separated by spaces. Immediate recognition: **Morse code**. The title "Dashed" is an extra hint (dash = `-`).

### 2. Encoding layers

The message is encoded in **4 nested layers**:

```
Morse → Hex (0x30/0x31) → Binary → Base64 → ROT13
```

Layer 1 — Morse:
Decoding the Morse yields a sequence of hexadecimal values separated by commas:

```
0X30,0X31,0X31,0X30,0X30,0X30,0X31,0X31,...
```

Layer 2 — Hex → Binary:
`0x30` = `'0'`, `0x31` = `'1'`. The hex sequence represents a binary string:

```
011000110011001101101100...
```

Layer 3 — Binary → Base64:
Grouping the bits into bytes and converting to ASCII produces a Base64 string:

```
c3ludHtDQUVTQVJfTUUhLWwwaF9UMDdfdkdfZTF0dUchfQo=
```

Layer 4 — Base64 → ROT13:
Decoding the Base64 yields ROT13-encoded text:

```
synt{CAESAR_ME!-l0h_T07_vG_e1tuG!}
```

Applying ROT13 produces the flag.

### 3. Python script

```python
import re, base64, codecs

MORSE = {
	'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
	'..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
	'-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
	'.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
	'..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
	'--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
	'....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
	'----.': '9', '--..--': ',', '.-.-.-': '.', '..--..': '?',
}

# Layer 1: Morse → hex string
text = open('dashed.txt').read().strip()
tokens = text.split(' ')
morse_decoded = ''.join(MORSE.get(t, '') for t in tokens)

# Layer 2: extract hex values (0X30/0X31) → binary string
hex_vals = re.findall(r'0X([0-9A-F]{2})', morse_decoded)
binary_str = ''.join(chr(int(h, 16)) for h in hex_vals)

# Layer 3: binary → Base64 string
b64 = ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str)-7, 8))

# Layer 4: Base64 → ROT13 → flag
rot13 = base64.b64decode(b64).decode()
flag = codecs.decode(rot13.strip(), 'rot13')
print(flag)
```

---

## Flag

```
flag{...}
```

---

## Conclusions

Classic multi-layer encoding challenge. The key is recognizing each layer in the correct order: the title "Dashed" points to Morse, the `0x30`/`0x31` values point to binary masked as hex, the trailing `=` betrays Base64, and the `synt{` prefix indicates ROT13 on a `flag{` token.
