# QRCode

**Competition:** FSCS 2022 (intro) <br>
**Category:** Misc <br>
**File:** `flag.png`

---

## Description
> Nous avons récupéré ce QRcode que nous n’arrivons pas à lire : pouvez-vous nous aider ?

An image PNG containing a QR code is provided; no reader can decode it. The goal is to understand why and restore it.

---

## Solution

### 1. Initial reconnaissance

At first glance the QR code looks normal. However, comparing it to a standard QR code reveals an anomaly:

**The three large squares in the corners (top-left, top-right, bottom-left) are "empty": they have the outer black border but the inner 3×3 black square is missing.**

These three squares are called the Finder Patterns and are described in the `ISO/IEC 18004:2015` standard (see [Wikipedia - QR code](https://en.wikipedia.org/wiki/QR_code)).

### 2. Identified issue — missing Finder Pattern center

Finder Patterns are 7×7 module structures in the QR code corners. Their layout is:

```
█ █ █ █ █ █ █
█           █
█   █ █ █   █   ← the inner 3×3 square is missing
█   █ █ █   █
█   █ █ █   █
█           █
█ █ █ █ █ █ █
```

Without the inner square, decoders cannot locate and orient the QR code. The three inner 3×3 black squares were deliberately removed.

---

### 3. Fix using an image editor — Paint.NET / Photopea / GIMP

This can be fixed with any image editor that allows drawing filled rectangles. Below are steps for **Photopea** (free, online):

#### Steps on [photopea.com](https://www.photopea.com)

1. **Open the image**
   - `File → Open` and load `flag.png`

2. **Select black as the foreground color** (`#000000`)

3. **Select the rectangular selection tool** (`M`)

4. **Fill the inner square of the finder pattern in the top-left corner**
   - The inner 3×3 square sits about 2 modules from the finder border.
   - In the example image (450×450 px), the TL finder spans roughly pixels ~40 to ~110.
   - Select approximately `(60,60) to (90,90)` and use `Edit → Fill → Foreground Color`.

5. **Repeat for the top-right finder**
   - Select approximately `(360,60) to (390,90)` and fill with black.

6. **Repeat for the bottom-left finder**
   - Select approximately `(60,360) to (90,390)` and fill with black.

7. **Export the fixed image**
   - `File → Export As → PNG`

**Note:** Exact pixel coordinates are not critical — drawing a suitably sized black square inside each finder is sufficient, as confirmed by the challenge author.

---

### 4. Scan the repaired QR

After restoring the three inner squares, the QR code can be scanned normally.

![Decrypted snapshot](qr_fixed.png)

---

## Flag

```
FCSC{...}
```

---

## Conclusion

Before applying complex techniques, visually inspect artifacts and compare them to standards. A clear visual anomaly is often the key.
