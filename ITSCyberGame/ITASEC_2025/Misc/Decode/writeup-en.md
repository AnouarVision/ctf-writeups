# Decode

**Competition:** ITSCyberGame<br>
**Category:** Misc<br>
**File:** decode.png

---

## Description

> It's not what it seems...

---

## Solution

The hint is already a compass: **"It's not what it seems"**. The most eye-catching element in the image is a decoy, and the real information is hidden in a detail that's easy to overlook.

### Step 1 — Initial File Analysis

```bash
$ file decode.png
decode.png: PNG image data, 3375 x 3375, 8-bit/color RGBA, non-interlaced

$ xxd decode.png | head -1
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR

$ exiftool decode.png
File Size         : 8.4 MB
Image Width       : 3375
Image Height      : 3375
Color Type        : RGB with Alpha
Creator Tool      : Canva (Renderer)
Title             : Untitled (Instagram Post) - 1

$ binwalk decode.png
DECIMAL       HEXADECIMAL     DESCRIPTION
0             0x0             PNG image, 3375 x 3375, 8-bit/color RGBA, non-interlaced
1274          0x4FA           Zlib compressed data, default compression
```

The file is a genuine PNG, no hidden files inside, nothing unusual in the metadata. Standard analysis leads nowhere.

### Step 2 — The Decoy: The Large QR

The image shows a large QR code overlaid on a lighthouse at sunset. The first instinct is to decode it, and that's exactly what the challenge wants you to do.

Decoding the large QR with any reader gives:

```
prova
```

Nothing useful. It's a decorative element added specifically to distract.

### Step 3 — The Hidden QR

Inspecting the high-resolution image (3375x3375), in the **bottom right corner** there's a second, much smaller QR code, almost camouflaged with the background.

```
┌──────────────────────────────────────┐
│                                      │
│       [Large QR - decoy]             │
│                                      │
│                          ┌────┐      │
│                          │ QR │ ← !  │
│                          └────┘      │
└──────────────────────────────────────┘
```

Scanning the bottom right corner of the original image with a QR reader:

```
flag{...}
```
