# Software 07 - Stack 1

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> This program builds the flag on the stack using `mov` instructions and then exits. Often it's useful to inspect raw disassembly in addition to the decompiled output.

You are given a binary `sw-07`. The flag is neither in `.rodata` nor in a global variable — it is constructed byte-by-byte on the stack at runtime via `mov` instructions.

---

## Why the decompiler is not enough

Decompilers like Ghidra reconstruct high-level logic, but their output can hide low-level details. Use the decompiler to understand structure and the disassembly to see exact instructions. In this challenge the disassembly reveals a sequence of `movb` instructions writing immediate bytes to stack offsets, which is how the flag is assembled.

---

## Disassembly analysis

Dump the `.text` section:

```bash
$ objdump -d -j .text sw-07
```

In `main` you'll find a sequence of `movb` instructions that store immediate bytes to increasing offsets from `rbp`:

```asm
115f:  c6 85 f0 fe ff ff 66    movb   $0x66,-0x110(%rbp)
1166:  c6 85 f1 fe ff ff 6c    movb   $0x6c,-0x10f(%rbp)
116d:  c6 85 f2 fe ff ff 61    movb   $0x61,-0x10e(%rbp)
...
11c1:  c6 85 fe fe ff ff 00    movb   $0x0, -0x102(%rbp)
```

Each `movb` writes one ASCII byte to the stack; offsets start at `-0x110` and increment by 1, so the bytes form a contiguous string on the stack.

---

## Reading the flag

The immediates written in order are (hex → ASCII):

- 0x66 → `f`
- 0x6c → `l`
- 0x61 → `a`
- 0x67 → `g`
- 0x7b → `{`
- 0x66 → .
- 0x63 → .
- 0x32 → .
- 0x66 → .
- 0x34 → .
- 0x34 → .
- 0x39 → .
- 0x62 → .
- 0x7d → `}`

Putting them together:

```
flag{...}
```

---

## Conclusions

- The stack is a transient area for local data; strings built on the stack at runtime do not appear in the file's `.rodata` and won't be found by `strings` or `objdump -s`.
- Use disassembly to see low-level operations (e.g., per-byte `mov`) that the decompiler may summarize.

