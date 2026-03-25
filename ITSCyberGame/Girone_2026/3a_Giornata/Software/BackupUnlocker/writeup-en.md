# backup_unlocker

**Competition:** ITSCyberGame
**Category:** Software
**File:** `backup_unlocker_3`

---

## Description

> I forgot the password for my backup and this proprietary authentication system looks properly obfuscated. Can you help me recover it?

An ELF 64-bit executable is provided. The goal is to analyze it statically to extract the correct password.

---

## Solution

### 1. File identification

```
file backup_unlocker_3
```

```
ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
```

The binary is not stripped; function names are preserved. A quick `strings` pass reveals two interesting symbols:

```
_TIG_EL_eTtb_1_stringEncoder
complex_function
```

No cleartext password is present: strings are assembled at runtime by the encoder.

---

### 2. Static analysis: `_TIG_EL_eTtb_1_stringEncoder`

This function is a large state machine that, depending on an ID passed as the first argument (`edi`), writes a string byte-by-byte into a buffer. The string never appears in readable form in the binary; each `movb $0xNN, (%rax)` places a single byte.

In `main`, before comparing against user input, the function is called with `edi=2`:

```asm
mov $0x2, %edi
lea litStr2, %rsi
call _TIG_EL_eTtb_1_stringEncoder   ; builds the comparison string
...
call strcmp@plt                      ; compares transformed input vs litStr2
```

Decoding the `movb` sequence for case `id=2` yields the hardcoded target string:

```
fogp{g3x0w3y_l0nn_n0ae_u4q4}
```

---

### 3. Static analysis: `complex_function`

Before `strcmp`, each character of user input is passed to `complex_function(char, position)`. The core of the function (case `0xb` of the state machine) implements:

```asm
movsbl -0x14(%rbp), %eax        ; char
lea    -0x61(%rax), %edx       ; char - 'a'
mov    -0x4(%rbp), %eax        ; constant = 3
imul   -0x18(%rbp), %eax       ; 3 * position
add    %eax, %edx              ; (char - 'a') + 3 * pos
; modular division by 26 via multiplication with magic number 0x4ec4ec4f
; final result:
add    $0x61, %eax             ; + 'a'
```

In Python:

```python
char_enc = (ord(char) - ord('a') + 3 * position) % 26 + ord('a')
```

Non-lowercase characters (`_`, `{`, `}`, digits) are returned unchanged.

This is a Vigenère-like transformation with a positional fixed key `k = 3`.

---

### 4. Inversion and password recovery

To recover the original password invert the transformation:

```python
char_orig = (ord(char_enc) - ord('a') - 3 * position) % 26 + ord('a')
```

Full script:

```python
encoded = 'fogp{g3x0w3y_l0nn_n0ae_u4q4}'

def invert(s):
	result = []
	pos = 0
	for c in s:
		if 'a' <= c <= 'z':
			result.append(chr((ord(c) - ord('a') - 3 * pos) % 26 + ord('a')))
			pos += 1
		else:
			result.append(c)
			pos += 1
	return ''.join(result)

print(invert(encoded))
```

```
flag{...}
```

Verification:

```bash
echo "flag{...}" | ./backup_unlocker_3
# Backup unlocked!
```

---

## Flag

```
flag{...}
```

---

## Conclusions

The binary uses two combined obfuscation layers:

1. Runtime string encoding: no readable strings exist in the file; `_TIG_EL_eTtb_1_stringEncoder` assembles them byte-by-byte at runtime, defeating a naive `strings` scan.
2. Input transformation: `complex_function` applies a positional Vigenère-like shift (`k=3`) to each letter of the input before comparison. The check compares the transformed input to the target string rather than comparing plaintext.

Both transformations are deterministic and invertible: knowing the encoded target string in the binary and the transformation law allows recovering the original password purely via static analysis, without executing the program.

