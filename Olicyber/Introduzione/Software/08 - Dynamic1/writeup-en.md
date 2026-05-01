# Software 08 - Dynamic 1

**Competition:** OliCyber<br>
**Category:** Software

---

## Description

> This binary calls `open(FLAG)`. Find the flag using `ltrace`, a tool that traces library calls made by a program.

You are given a binary `sw-08`. The objective is to find the flag by performing dynamic analysis, observing the program at runtime rather than disassembling it.

---

## Static vs dynamic analysis

So far we've used static tools: `strings`, `objdump`, `readelf`, and Ghidra. Those inspect the file without executing it.

Dynamic analysis complements static techniques: run the program in a controlled environment and observe what it does at runtime, which functions it calls, which syscalls it issues, which files it opens, what it writes to memory. Dynamic methods are essential when code is obfuscated, encrypted, or depends on runtime state.

This challenge introduces two core Linux dynamic tools: `ltrace` and `strace`.

---

## The `ltrace` command

`ltrace` (library call tracer) intercepts and logs calls to shared-library functions made by the program. For each call it prints the function name, the passed arguments, and the return value.

Run the program under `ltrace`:

```bash
$ ltrace ./sw-08
```

Output:

```
puts("✨ Executing open(FLAG})...")                    = 29
open("flag{...}", 0, 024114303620)              = -1
++ exited (status 0) +++
```

The trace shows two library calls:

- `puts(...)` prints the introductory message. The return value `29` is the number of characters written.
- `open("flag{...}", ...)` attempts to open a file whose name is the flag. The return value `-1` indicates the file does not exist on the current filesystem (expected), but the first argument passed to `open()` contains the flag in cleartext, `ltrace` reveals it before the kernel handles the syscall.

---

### Flag

```
flag{...}
```

---

## Conclusions

Key lessons:

- **`ltrace` captures arguments before execution**: it prints function arguments at the moment of the call, regardless of whether the call later fails. Even if `open()` returns `-1`, the filename is already visible.
- **Return values are informative**: `open()` returning `-1` confirms the file doesn't exist locally; on a real CTF server the call might succeed and return a file descriptor.
- **Dynamic analysis limitations**: `ltrace` traces dynamic library calls (e.g., `libc` functions) but not direct syscalls or internal static functions. For syscalls use `strace`; for internal functions use a debugger such as `gdb`. Together these tools cover different visibility levels at runtime.

