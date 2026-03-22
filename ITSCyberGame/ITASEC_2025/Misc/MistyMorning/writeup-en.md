# Misty Morning

**Competition:** ITSCyberGame<br>
**Category:** Misc<br>
**File:** misty_morning.png

---

## Description

> A lone traveler left a hidden message among the mountain mists: only those who know how to look beyond the horizon will find it...

---

## Solution

The hint suggests to **"look beyond"**, not at the obvious content of the image, but at its hidden layers. In steganography, this means analyzing the bit planes of the individual color channels.

### Step 1 — Initial File Analysis

```bash
$ file misty_morning.png
misty_morning.png: PNG image data, 1782 x 791, 8-bit/color RGBA, non-interlaced

$ exiftool misty_morning.png
File Size         : 1009 kB
Image Width       : 1782
Image Height      : 791
Color Type        : RGB with Alpha

$ binwalk misty_morning.png
DECIMAL       HEXADECIMAL     DESCRIPTION
0             0x0             PNG image, 1782 x 791, 8-bit/color RGBA, non-interlaced
91            0x5B            Zlib compressed data, compressed
```

No hidden files, no useful metadata. Standard analysis leads nowhere.

### Step 2 — Bit Plane Analysis

Inspecting the RGBA values of the pixels, an unusual pattern emerges: the values of the **Blue channel** are not as uniform as you would expect from a natural misty background, showing small systematic variations that could encode information.

The tool **StegOnline** ([georgeom.net/StegOnline](https://georgeom.net/StegOnline)) allows you to visualize the individual bit planes of each color channel. Uploading the image and navigating to **Browse Bit Planes → Blue → Bit 3**, the flag text visually appears in the image:

```
flag{...}
```

Bit 3 of the Blue channel was the optimal level to make the text readable—deep enough to be invisible to the naked eye in the original image, but emerging once isolated.
