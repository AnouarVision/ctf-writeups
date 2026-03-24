# Orbital Decay

**Competition:** ITSCyberGame
**Category:** Software
**File:** orbital_decay_5

---

## Description

> The satellite's memory dump produced this binary, but it doesn't seem to contain anything useful. Maybe some information can still be recovered...

---

## Solution

### Step 1 — Initial analysis

```bash
$ file orbital_decay_5
orbital_decay_5: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
dynamically linked, not stripped

$ checksec --file=orbital_decay_5
Partial RELRO   No canary   NX enabled   PIE enabled   38 Symbols
```

The binary is not stripped and includes symbols, which helps the analysis.

### Step 2 — strings

```bash
$ strings orbital_decay_5
--- SATELLITE MEMORY DUMP V4.0 ---
Showing dump diagnostics...
[ERROR] Buffer was captured, but no meaningful data was present.
[ERROR] Nothing to show. Bailing out, you're in your own - good luck.
main
show_diagnostics
SECRET_BEACON
```

`strings` reveals `main`, `show_diagnostics` and the symbol `SECRET_BEACON`.

### Step 3 — Disassembly

Inspecting `main` and `show_diagnostics` shows the diagnostics output points past the start of `SECRET_BEACON`, skipping the beginning of that data.

### Step 4 — .rodata dump

```bash
$ objdump -s -j .rodata orbital_decay_5

Contents of section .rodata:
[raw bytes omitted]
```

At the start of `SECRET_BEACON` there are bytes with `\x00` after each character, a UTF-16LE (wide) string. `strings` didn't show it because it only finds ASCII sequences.

Decoding those bytes yields a UTF-16LE string that corresponds to a flag. We do not reveal the full flag here: extract and decode the bytes from `.rodata` to reconstruct it yourself.

---

## Flag

```
flag{...}
```

---

## Conclusion

The flag was stored as a UTF-16LE wide string in `.rodata`, labeled by `SECRET_BEACON` and not referenced by program logic. `objdump -s -j .rodata` reveals the raw bytes; decoding them as UTF-16LE yields the flag (withheld here).