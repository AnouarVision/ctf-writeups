 # Software 09 - Dynamic 2

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> This binary behaves like Dynamic 1 but is statically linked. `ltrace` no longer works, use `strace` instead.

You are given a binary `sw-09`. It attempts the same behavior as `sw-08` (opening a file named with the flag), but because it is statically linked you must trace syscalls instead of library calls.

---

## Why `ltrace` fails on static binaries

`ltrace` hooks calls to shared-library functions (like `libc`) via the dynamic linker and the PLT. A statically linked binary contains libc code inside the executable and does not use the PLT, so `ltrace` has no interception point.

`file` shows the difference:

```
sw-08: ELF 64-bit, dynamically linked   <- `ltrace` works
sw-09: ELF 64-bit, statically linked    <- `ltrace` does not work
```

---

## The `strace` command

`strace` traces syscalls — the kernel-level interface every process uses. It works regardless of static or dynamic linking because syscalls always pass through the kernel.

Run the program under `strace`:

```bash
$ strace ./sw-09
```

Output:

```
write(1, "✨ Executing open(FLAG})...\n", 29) = 29
openat(AT_FDCWD, "flag{...}", O_RDONLY) = -1 ENOENT (No such file or directory)
```

The trace shows the program writing the intro message and then issuing `openat()` with a pathname that contains the flag in cleartext. The call fails (ENOENT) because the file is not present locally, but the pathname argument reveals the flag.

---

## `ltrace` vs `strace`

| | `ltrace` | `strace` |
|---|---:|---:|
| Intercepts | Library calls (PLT) | Kernel syscalls |
| Works on static binaries | No | Yes |
| Output verbosity | Compact, library-focused | Verbose, syscall-focused |

In this case `open()` inside libc ends up as the `openat()` syscall, which `strace` captures and prints the filename argument.

---

### Flag

```
flag{...}
```

---

## Conclusions

- `strace` is universal: it works on any Linux binary because it observes syscalls.
- Static linking removes the PLT hook but does not hide syscall arguments; the flag still appears as an argument to `openat()`.
- When analyzing noisy `strace` output use filtering: `strace -e trace=openat,read,write ./bin 2>&1 | grep open` or `strace -e trace=openat ./bin`.
