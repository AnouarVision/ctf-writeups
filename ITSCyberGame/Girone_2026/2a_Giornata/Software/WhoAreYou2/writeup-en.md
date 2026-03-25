# who_are_you_2

**Competition:** ITSCyberGame
**Category:** Software
**File:** who_are_you_2
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> OK, you're right — I wasn't careful declaring variables. This time I reordered everything neatly...

Updated version of `who_are_you`. The program still asks for your name and checks if you're root, but variables have been rearranged.

---

## Binary analysis

```bash
file who_are_you_2
# ELF 64-bit LSB executable, x86-64, stripped

checksec --file=who_are_you_2
# Partial RELRO | No canary | NX enabled | No PIE
```

### Difference from v1

From the disassembly we obtain the stack layout:

```
rbp-0xd0  →  USER   (buf+0x00, copied from getenv with strcpy)
rbp-0x6c  →  input  (buf+0x64, read by scanf("%s"))
```

In v1 the buffers were inverted: USER at `buf+0x64`, input at `buf+0x00`. This time:

- `strcmp1`: `strcmp(input, "root")` — input must be "root"
- `strcmp2`: `strcmp(USER, "root")` — the server USER is `cybergame_contestant`, not `root`

The input overflow cannot overwrite USER because USER is located at a lower address than the input area. A different approach is required.

---

## Solution

### Ret2win

The exploit bypasses checks by overwriting the **return address** with the address of the flag-printing block (`0x401214`):

```
0x401214: puts("Hi, root! Here's your flag")
0x401223: getenv("FLAG") + puts
```

**Padding calculation:**

```
input at rbp-0x6c
saved rbp at rbp
ret address at rbp+8

distance from input to ret = 0x6c + 8 = 116 bytes
```

**First strcmp issue:**

`strcmp(input, "root")` compares the whole input string. If the payload is `rootAAA...` the check fails. The trick is to place a **null byte** after `root`:

```python
payload = b"root\x00" + padding + ret_addr
```

`scanf("%s")` stops at whitespace (space, tab, newline) but not at null bytes, so the null byte is written into the buffer. `strcmp` stops at the null byte, so it sees only `"root"` and the comparison passes.

### Script

The automation script is provided separately as `who_are_you_2.py` in the challenge folder. Run it with:

```
python3 who_are_you_2.py
```

The script connects to the server, builds the payload with the null byte and the overflow needed, and prints the output; the full source is available in `who_are_you_2.py` for inspection or modification.

The message "Liar!" still appears because the second `strcmp` fails, but the ret2win makes the program jump to the flag-printing block at the final `ret`.

---

## Flag

```
flag{...}
```

---

## Conclusions

This challenge illustrates two key concepts. First: **ret2win** — when you cannot overwrite control variables, overwrite the return address to jump to the desired code. Second: `scanf("%s")` stops at whitespace but **not** at null bytes, allowing insertion of `\x00` to prematurely terminate the string `strcmp` compares.
