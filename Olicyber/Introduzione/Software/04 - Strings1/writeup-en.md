# Software 04 - Strings 1

**Competition:** OliCyber <br>
**Category:** Software

---

## Description

> These programs prompt for a flag (or any string) and check its correctness. A useful tool to find all printable strings inside a file is `strings`.

You are given a binary `sw-04` that asks for the flag and verifies it. The goal is to extract the flag.

---

## How string checks work

When a program compares user input with an expected string, that expected string must exist somewhere inside the binary. The compiler typically stores it in the `.rodata` section as a null-terminated ASCII sequence. It is static data embedded in the file at compile time.

This is the simplest and most common case in introductory reverse-engineering challenges: the flag is stored in cleartext and compared with `strcmp`. There is no encryption or obfuscation — the string is there to be found.

---

## Solution

### Step 1 — the `strings` command

`strings` scans a binary for printable ASCII sequences (default minimum length 4) and prints them. It does not need ELF awareness — it just detects text patterns in the raw bytes.

```bash
$ strings sw-04
```

Among the many lines (library names, symbols, debug messages), the following stand out:

```
flag{0cca06f6}
 Qual' la flag? :
 Sbagliato! Prova ancora
 Giusto!
```

The flag is stored in cleartext. The program compares the input with the stored string using `strcmp` and prints `Giusto!` on success or `Sbagliato! Prova ancora` otherwise.

### Step 2 — why this works

The flag is a compile-time constant. The C compiler places it into the read-only data segment. `strings` simply finds it there.

This is why `strings` should be the first tool you run against any challenge binary: in simple cases it solves the task instantly and, in all cases, it reveals error messages, symbol names and library usage that guide further analysis.

---

### Flag

```
flag{0cca06f6}
```

---

## Conclusions

This challenge teaches the fundamental point that security by obscurity is not security: storing the flag plainly in the binary is trivial to defeat. Later challenges will use hashes, transforms or distributed checks, but `strings` remains a valuable reconnaissance tool for discovering helpful clues before deeper analysis.
