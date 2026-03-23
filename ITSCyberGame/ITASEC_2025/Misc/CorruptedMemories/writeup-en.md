# Corrupted Memories

**Competition:** ITSCyberGame
**Category:** Misc
**File:** corrupted_memories.png

---

## Description

> A damaged digital memory... the first fragments are corrupted but the complete image still hides the truth.
> Can you reconstruct what has been altered?

---

## Solution

The hint explicitly mentions "first fragments corrupted", which suggests a problem with the **file header**. Initial analysis confirms this.

### Step 1 — Initial analysis

```bash
$ file corrupted_memories.png
corrupted_memories.png: data
```

`file` does not recognize the format, meaning the magic number is missing or incorrect. `exiftool` reports an error as well:

```bash
$ exiftool corrupted_memories.png
Error: File format error
```

However, `binwalk` finds Zlib-compressed data at offset `0x5B`, consistent with a PNG whose internal data is intact but whose header is corrupted:

```bash
$ binwalk corrupted_memories.png
DECIMAL       HEXADECIMAL     DESCRIPTION
91            0x5B            Zlib compressed data, compressed
```

### Step 2 — Inspect raw bytes

A quick hexdump of the file shows the first 8 bytes are incorrect:

```bash
$ xxd corrupted_memories.png | head -4
00000000: 0123 4567 89ab cdef 0000 000d 4948 4452  .#Eg........IHDR
00000010: 0000 04d0 0000 02b2 0806 0000 0014 de23  ...............#
00000020: 8e00 0000 0173 5247 4200 aece 1ce9 0000  .....sRGB.......
00000030: 0004 6741 4d41 0000 b18f 0bfc 6105 0000  ..gAMA......a...
```

The first 8 bytes are `01 23 45 67 89 ab cd ef`, an obvious placeholder. The correct PNG signature (magic number) is:

```
89 50 4E 47 0D 0A 1A 0A
```

From byte 8 onward the file looks intact: `49 48 44 52` (`IHDR`) is visible, which is the first valid PNG chunk.

### Step 3 — Fix with `dd`

Overwrite the first 8 bytes with the correct PNG signature without changing the rest of the file:

```bash
$ printf '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' | dd of=corrupted_memories.png bs=1 seek=0 conv=notrunc
8+0 records in
8+0 records out
8 bytes copied, 0.0011624 s, 6.9 kB/s
```

- `seek=0`: write starting at offset 0
- `conv=notrunc`: do not truncate the file; leave the remainder intact

### Step 4 — Verify

```bash
$ file corrupted_memories.png
corrupted_memories.png: PNG image data, 1232 x 690, 8-bit/color RGBA, non-interlaced
```

The file is now a valid PNG. Opening it reveals the flag embedded in the image.