# Broken

**Competition:** ITSCyberGame <br>
**Category:** Misc <br>
**Service:** `data.zip`

---

## Description

You are given a ZIP containing a `challenge/` folder with an apparently corrupted `qr.png` and a hidden `.git/` directory. The hint reads:

> "I think the AI broke the QR, damn agent!"

The goal is to recover a readable QR code and decode it to obtain the flag.

---

## Solution

### 1. Recon

List the archive contents:

```bash
unzip -l data.zip
```

Contents include:
- `challenge/qr.png`: 37×37 px QR (version 5), not readable
- `challenge/.git/`: a Git repository with objects, logs and refs

One notable anomaly: `.git/HEAD` has been renamed to `.git/TESTA`.

### 2. Finding the trick — renamed HEAD + repo history

This challenge uses a classic trick: critical Git files are renamed to hide history from standard tools. Here `HEAD` → `TESTA`.

Fix it locally:

```bash
cp .git/TESTA .git/HEAD
```

Now `git log` shows the history:

```
301 commits on branch main (all: "update: commit N")
2 commits on branch dev ("add qr code")
```

### 3. Repo analysis

The `dev` branch contains the original commit that added the QR:

```
e9941cf add qr code  ← QR created here
```

Branch `main` contains 300 subsequent commits, each flipping exactly one pixel (black↔white) in `qr.png`, progressively degrading the QR until it's unreadable.

Example analysis (pixel diffs between consecutive commits):

```
Commit 1 (c4664b9): 1 pixel changed @ [[28, 9]]
Commit 2 (8656dca): 1 pixel changed @ [[16, 21]]
... (300 flips total)
```

### 4. Recover the original QR

The untouched QR is available on `dev` before the destructive commits:

```bash
git show dev:qr.png > qr_original.png
```

Decode by upscaling (37px is too small for many decoders):

```python
from PIL import Image
import zxingcpp

img = Image.open('qr_original.png')
img_big = img.resize((370, 370), Image.NEAREST)
results = zxingcpp.read_barcodes(img_big)
print(results[0].text)
```

Output:

```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusion

The challenge combines two techniques:

1. **Git forensics:** renaming `HEAD` to `TESTA` prevents casual use of `git` tools; restoring the file recovers full history.
2. **QR degradation:** the QR was gradually corrupted by 300 single-pixel flips on `main`; the original is preserved in `dev`.
