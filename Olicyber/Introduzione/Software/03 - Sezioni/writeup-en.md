# Software 03 - Sections

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> ELF files are composed of multiple sections. In this challenge one ELF contains a mysterious section, what does it hold?

You are given a binary named `sw-03`. The goal is to find the contents of an unusual section.

---

## ELF section structure

An ELF file is not a monolithic stream of machine instructions; it is a container organized in sections, each with a name, size and purpose. The linker assembles sections, the loader maps them into memory, and debuggers consult them. Knowing the section layout is essential for binary analysis.

Common sections include:

- `.text`: executable code
- `.rodata`: read-only data, typically constant strings
- `.data`: initialized global variables
- `.bss`: uninitialized globals (occupies memory but not file space)
- `.plt` / `.got`: runtime linking support
- `.dynamic`: dynamic linker metadata
- `.debug_*`: debug information generated with `-g`

Authors and challenge makers may add arbitrary sections with any name. The section header table is just an array of descriptors, so any name is allowed.

---

## Solution

### Step 1 — list sections with `objdump -h`

`objdump -h` lists all sections and their attributes:

```bash
$ objdump -h sw-03
```

Among the standard sections one entry stands out:

```
25 .super-secret-section  0000001c  0000000000000000 ...
                           CONTENTS, READONLY
```

The section is named `.super-secret-section`, has size `0x1c` (28 bytes), and a VMA of `0` (not mapped at runtime). It is static data not loaded into memory during execution — a hidden container inside the file.

### Step 2 — inspect raw contents with `objdump -s`

Use `-s` with `-j` to dump a section's raw bytes in hex and ASCII:

```bash
$ objdump -s -j .super-secret-section sw-03

Contents of section .super-secret-section:
 0000 46004c00 41004700 7b006400 30003300  F.L.A.G.{.d.0.3.
 0010 6c007600 6e003400 69007d00           l.v.n.4.i.}.
```

The dump shows every meaningful byte separated by a null byte (`\x00`): the section stores a UTF-16LE string (ASCII characters encoded as 16-bit little-endian units). Reading the non-null bytes in order yields:

```
46 4c 41 47 7b 64 30 33 6c 76 6e 34 69 7d
F  L  A  G  {  d  0  3  l  v  n  4  i  }
```

### Step 3 — why not use `-d`?

`objdump -d` disassembles bytes as machine instructions. If applied to a data section it produces meaningless instructions:

```
0:   46 00 4c 00 41    add %r9b,0x41(%rax,%r8,1)
5:   00 47 00          add %al,0x0(%rdi)
...
```

That output is noise because the bytes are data, not code. Use `-s` to read raw data and `-d` for `.text` only.

---

### Flag

```
flag{d03lvn4i}
```

---

## Conclusions

Three lessons:

- **ELF sections are explorable metadata**: run `objdump -h` before disassembling; unusual section names or attributes merit investigation.
- **`objdump -s` is the right tool for raw data**: hex + ASCII dumps make strings and data patterns obvious.
- **Not all ELF content is executed**: sections with VMA 0 are not loaded at runtime and can contain hidden data that a code-only analysis would miss.
