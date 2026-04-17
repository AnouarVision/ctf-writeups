# Software 02 - Libraries

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> Dynamically linked binaries must locate shared libraries on the system at runtime. Knowing how to find a binary's dependencies is useful. In this challenge the binary attempts to load some unusual libraries, which ones?

You are given a binary named `sw-02`. The goal is to find the "strange" libraries it tries to load.

---

## Static vs dynamic linking

When a program is compiled it usually depends on external code: memory management, I/O, string routines, networking, etc. External code can be embedded into the binary at compile time (static linking) or located and loaded at runtime (dynamic linking).

Dynamic linking is the norm on Linux because multiple programs can share a single copy of a library in memory (shared libraries). The previous challenge's `sw-01` was statically linked; `sw-02` is dynamically linked, which changes the analysis approach.

Before `main` runs, the dynamic linker (`ld-linux.so`) reads the list of required libraries from the ELF and attempts to load them. If a library is missing, the program won't start.

---

## Solution

### Step 1 — `ldd`

`ldd` (List Dynamic Dependencies) queries the dynamic linker to show the shared libraries a binary requires and where they resolve on the current system.

```bash
$ ldd sw-02
        linux-vdso.so.1 (0x00007f43be66e000)
        F => not found
        L => not found
        A => not found
        G => not found
        { => not found
        1 => not found
        d => not found
        8 => not found
        d => not found
        b => not found
        5 => not found
        5 => not found
        9 => not found
        } => not found
        libc.so.6 => /usr/lib/x86_64-linux-gnu/libc.so.6 (0x00007f43be43f000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f43be670000)
```

Alongside standard dependencies like `linux-vdso.so.1`, `libc.so.6` and the dynamic loader, the output contains one-character "libraries": `F`, `L`, `A`, `G`, `{`, `1`, `d`, `8`, `d`, `b`, `5`, `5`, `9`, `}` — all reported as `not found` because they are not real shared objects.

### Step 2 — Read between the lines

The dynamic linker reads dependency names from the ELF's `.dynamic` section (`DT_NEEDED`). The challenge author placed a sequence of single-character strings in that section. Reading them in the order `ldd` shows reconstructs the flag:

```
F L A G { 1 d 8 d b 5 5 9 }
```

---

### Flag

```
flag{1d8db559}
```

---

## Conclusions

This challenge highlights two recurring ideas in binary analysis:

- **`ldd` for reconnaissance**: before opening a disassembler, `ldd` reveals runtime dependencies and gives a quick profile of a binary's capabilities. A binary importing `libssl.so` probably does crypto; one importing `libpthread.so` uses threads; unexpected imports deserve attention.
- **ELF metadata as an information vector**: the flag was not in `.text` or `.rodata` but in the dynamic linking metadata. Any ELF section (`.dynamic`, `.symtab`, `.strtab`, `.note`, etc.) can hold useful data and should be inspected.

Note: `ldd` invokes the dynamic linker and should not be run on untrusted binaries in production. Use `readelf -d` to safely inspect the `.dynamic` section without triggering execution.
