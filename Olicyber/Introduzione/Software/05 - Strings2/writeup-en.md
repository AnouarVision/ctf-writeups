# Software 05 - Strings 2

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> The program in this challenge is similar to the previous one, but `strings` won't help. Analyze `main` with Ghidra.

You are given a binary `sw-05` that verifies an input string. Unlike `sw-04`, the flag is not stored in cleartext and `strings` does not reveal it.

---

## Why `strings` fails

In `sw-04` the flag was a contiguous ASCII sequence visible to `strings`. Here the author stored the flag as **UTF-16LE**: each character occupies 2 bytes and the high byte is always `\x00`. As a result there are no runs of 4+ contiguous printable bytes, so `strings` finds nothing useful.

---

## Ghidra: disassembler and decompiler

Use Ghidra to inspect the binary. The Disassembly view shows raw instructions; the Decompiler reconstructs an approximate C-like pseudocode that is much easier to read.

Open the Decompiler window (`Window` → `Decompiler`) or right-click a function and choose `Decompile`.

Rename auto-generated locals (e.g. `local_218`) to meaningful names via right-click → `Rename Variable` (or `L`) once you understand their roles.

---

## Decompiled analysis

Ghidra's pseudocode for `main` shows the program reads user input, then reconstructs a `flag_reconstructed` buffer by taking every second byte from a raw `flag` array:

```c
for (i = 0; i < 0xe; i = i + 1) {
	flag_reconstructed[i] = flag[i * 2];
}

if (strcmp(input, flag_reconstructed) == 0) {
	puts("Giusto!");
}
```

The loop copies bytes at indices 0,2,4,... from `flag` into a compact ASCII string. This is precisely the transformation from UTF-16LE to ASCII: take every other byte.

---

## Extracting the flag

Dump `.rodata` and read every other byte. Example `objdump` output:

```bash
$ objdump -s -j .rodata sw-05

Contents of .rodata:
 2010 66006c00 61006700 7b003800 31003700  f.l.a.g.{.8.1.7.
 2020 35003000 65003600 33007d00 f09f9aa9  5.0.e.6.3.}.....
```

Taking the bytes at even indices yields:

```
66 6c 61 67 7b 38 31 37 35 30 65 36 33 7d
f  l  a  g  {  8  1  7  5  0  e  6  3  }
```

---

### Flag

```
flag{81750e63}
```

---

## Conclusions

This challenge demonstrates the value of a decompiler: `strings` is blind to interleaved/multibyte encodings, while Ghidra exposes the reconstruction logic. Understanding the transformation is enough to invert it and recover the plaintext.
