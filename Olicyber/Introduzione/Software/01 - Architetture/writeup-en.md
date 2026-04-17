# Software 01 - Architectures

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> The first challenge asks to determine the architecture for which an ELF binary was compiled. The flag format is `flag{architecture}`.

You are given a binary file named `sw-01`. The goal is to identify the target CPU architecture.

---

## The ELF format

On Linux, executable files usually follow the ELF (Executable and Linkable Format). It's a structured container with a header describing important metadata the OS uses to load and run the program.

The first 64 bytes contain the ELF header, which tells you, among other things:

- whether the file is 32- or 64-bit
- whether it uses little-endian or big-endian encoding
- the machine type (target architecture)
- the program entry point
- where sections and segments live

Knowing the ELF header layout is essential for binary analysis.

---

## Solution

### Step 1 — `file`

The quickest tool to inspect an unknown binary is `file`. It looks at the magic bytes and matches known signatures:

```bash
$ file sw-01
sw-01: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV),
       statically linked, BuildID[sha1]=0073012c38af01374a53569a0d79290259d34d8d,
       not stripped
```

This shows at a glance that the binary is:

- `ELF 64-bit` — a 64-bit ELF
- `LSB` — little-endian
- **`ARM aarch64`** — compiled for AArch64 (ARM 64-bit)
- `statically linked` and `not stripped`

That already gives the correct architecture, but it's useful to verify with a precise ELF inspector.

---

### Step 2 — `readelf`

`readelf -h sw-01` prints the ELF header fields:

```bash
$ readelf -h sw-01
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  Type:                              EXEC (Executable file)
  Machine:                           AArch64
  Entry point address:               0x40010c
  ...
```

Key fields:

- Magic bytes `7f 45 4c 46` identify the file as ELF.
- `Class: ELF64` confirms 64-bit.
- `Data: little endian` shows byte order.
- `Machine: AArch64` (value 0xB7) is the authoritative field that indicates the target CPU architecture.

---

### Flag

```
flag{aarch64}
```

---

## Conclusions

Start every unknown binary analysis with `file` for a quick fingerprint, then use `readelf` to inspect ELF internals (header `-h`, sections `-S`, segments `-l`, symbols `-s`). Knowing where `.text`, `.data`, `.plt`, and `.got` live is essential for deeper reverse engineering and exploitation.
