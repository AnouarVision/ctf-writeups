# The Legend of the Hidden Code

**Competition:** ITSCyberGame<br>
**Category:** Misc<br>
**File:** the_legend_of_hidden_code.png

---

## Description

> In the world of Hyrule, not everything is as it seems. Some secrets hide behind the facade just like a secret heart behind a wall of bricks. Don't just look; dig deep to find the truth.

---

## Solution

The hint is clear: **"Don't just look; dig deep"**. The secret is not in the image itself, but in what lies beneath the surface — the metadata.

### Step 1 — Initial File Analysis

```bash
$ file the_legend_of_hidden_code.png
the_legend_of_hidden_code.png: PNG image data, 833 x 1280, 8-bit/color RGBA, non-interlaced

$ binwalk the_legend_of_hidden_code.png
DECIMAL       HEXADECIMAL     DESCRIPTION
0             0x0             PNG image, 833 x 1280, 8-bit/color RGBA, non-interlaced
633           0x279           Zlib compressed data, compressed
```

Genuine PNG file, no hidden files inside. `binwalk` reveals nothing interesting.

### Step 2 — Metadata Analysis with Exiftool

The hint suggests to "dig deep". In forensics, digging deep means looking at the file's metadata:

```bash
$ exiftool the_legend_of_hidden_code.png
```

```
File Size         : 91 kB
Image Width       : 833
Image Height      : 1280
Color Type        : RGB with Alpha
User Comment      : flag{...}     ← !
```
