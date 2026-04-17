# Software 06 - Strings 3

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> This challenge is similar to the previous one, but the flag is not stored in cleartext. Analyze `main` with Ghidra and determine how the program checks the input against the flag.

You are given a binary `sw-06` that verifies an input string. Neither `strings` nor `objdump -s` reveal the flag in plaintext: it is protected via XOR.

---

## Decompiled code analysis

Ghidra produces the following pseudocode for `main`:

```c
undefined8 main(void)
{
	int result_memcmp;
	size_t sVar2;
	long in_FS_OFFSET;
	size_t input_len;
	undefined8 i;
	byte input_buf[264];
	long stack_canary;

	stack_canary = *(long *)(in_FS_OFFSET + 0x28);
	memset(input_buf, 0, 0x100);
	do {
		printf("Qual è la flag? : ");
		fgets((char *)input_buf, 0x100, stdin);
		sVar2 = strlen((char *)input_buf);
		if (sVar2 != 0) {
			input_len = sVar2;
			if (input_buf[sVar2 - 1] == 10) {
				input_len = sVar2 - 1;
				input_buf[sVar2 - 1] = 0;
			}
			if (input_len == 0xe) {
				for (i = 0; i < 0xe; i = i + 1) {
					input_buf[i] = input_buf[i] ^ key[i];
				}
				result_memcmp = memcmp(input_buf, flag, 0xe);
				if (result_memcmp == 0) {
					puts("Giusto!");
					return 0;
				}
			}
		}
		puts("Sbagliato! Prova ancora");
	} while( true );
}
```

After renaming variables for clarity, the logic is straightforward: the program reads a 14-byte input, XORs each input byte with a corresponding `key[i]`, then compares the result with the stored `flag` bytes using `memcmp`.

---

## XOR is reversible

The check implements:

```
for i in 0..13:
	(input[i] ^ key[i]) == flag[i]
```

Since XOR is its own inverse, the original plaintext flag bytes can be recovered by XORing the stored `flag` array with `key`:

```
plaintext[i] = flag[i] ^ key[i]
```

No brute force is needed if both `flag[]` and `key[]` are present in the binary.

---

## Extracting arrays with `objdump`

Dump `.rodata` to locate the two contiguous 14-byte arrays (separated by two padding bytes):

```bash
$ objdump -s -j .rodata sw-06

Contents of .rodata:
 2000 01000200 00000000 d45cdcbb 6b1ed34a  .........\..k..J
 2010 4a5ed2df ac7c0000 b230bddc 107ae17b  J^...|...0...z.{
 2020 2c3be2ec 9901f09f 9aa92051 75616c27  ,;........ Qual'
```

At offset `0x2008` two 14-byte arrays are present:

```
key[]  @ 0x2008: d4 5c dc bb 6b 1e d3 4a 4a 5e d2 df ac 7c
flag[] @ 0x201a: b2 30 bd dc 10 7a e1 7b 2c 3b e2 ec 99 01
```

---

## Decryption script

```python
key  = bytes.fromhex("d45cdcbb6b1ed34a4a5ed2dfac7c")
flag = bytes.fromhex("b230bddc107ae17b2c3be2ec9901")

plaintext = bytes([f ^ k for f, k in zip(flag, key)])
print(plaintext.decode())
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusions

This challenge demonstrates why XOR with a key stored alongside the ciphertext provides no protection. If both `flag[]` and `key[]` are present in the binary, a static analysis recovers the plaintext immediately. Also note the use of `memcmp` (which compares fixed-length buffers) rather than `strcmp`.
