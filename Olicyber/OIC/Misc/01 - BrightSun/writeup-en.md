# Bright Sun

**Competition:** OliCyber
**Category:** Misc
**File:** `Bright_Sun.png`

---

## Description

> "On an old hard disk I found a photo from a beach holiday many years ago. I still remember the days on the beach under the umbrella in swimsuit and sunglasses! I wonder why only this picture remained..."

A sunset photo over a beach (Ipanema, Rio de Janeiro). The goal is to find the flag hidden in the image.

---

## Solution

### 1. Identified vulnerability — Visual steganography

The flag is written directly on the **high-luminance** pixels of the sun disk (overexposed area), which are invisible to the naked eye due to white clipping.

Technique: pixels in the 220–255 brightness range (highlights) contain overlaid text. Reducing brightness and increasing contrast removes clipping and reveals the text.

### 3. Exploit — Photopea (online, no install)

1. Open https://www.photopea.com
2. File → Open → load `Bright_Sun.png`
3. Image → Adjustments → Brightness/Contrast
4. Lower **Brightness** until the text in the sun becomes visible
5. Zoom into the sun disk (top-left area) → the flag appears clearly

---

## Flag

```
flag{...}
```

---

## Conclusions

No classic steganography tools (steghide, outguess, zsteg, binwalk) are useful here. The flag is hidden with pure visual steganography: the text is painted directly onto the brightest pixels of the image (the sun), exploiting the fact that the human eye cannot perceive subtle color variations in clipped white areas.
