# Whistle (Fischietto)

**Competition:** ITSCyberGame
**Category:** Misc
**File:** challenge_4.pdf (renamed to challenge_4.png)

---

## Description

> This image may look random, but it contains many meanings and memories from the past... and maybe a flag.
> Note: The flag format is always flag{Qu3st4_e_un4_fl4g}. Everything except the first letter is lowercase.

---

## Solution

### Step 1 — File identification

The provided file has a `.pdf` extension, but the `file` command shows it's actually a PNG:

```bash
$ file challenge_4.pdf
challenge_4.pdf: PNG image data, 886 x 888, 8-bit/color RGBA, non-interlaced
```

It was renamed to `challenge_4.png` for further analysis.

### Step 2 — Analysis with zsteg

`zsteg` reveals two hidden things inside the file:

```bash
$ zsteg challenge_4.png
[?] 66804 bytes of extra data after image end (IEND), offset = 0x600ea
extradata:0   .. file: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 8 bit, mono 8000 Hz

b1,rgb,lsb,xy .. text: "flag{1m_g0nn4_
the rest of the flag is in this video!!! : https://www.youtube.com/watch?v=Z3J_MCbwaJ0"
```

Two discoveries:

1. **LSB steganography** in the RGB channel reveals the first part of the flag: `flag{1m_g0nn4_` followed by a troll pointing to a fake YouTube video.
2. **Extra data after the IEND** of the PNG: a hidden WAV file (66804 bytes, 8-bit mono 8000 Hz).

### Step 3 — Extracting the WAV file

Search for the `RIFF` signature inside the PNG and extract everything from that offset:

```python
python3 -c "
with open('challenge_4.png', 'rb') as f:
    data = f.read()
riff = data.find(b'RIFF')
with open('hidden.wav', 'wb') as f:
    f.write(data[riff:])
print('WAV extracted, size:', len(data[riff:]))
"
# WAV extracted, size: 66804
```

### Step 4 — WAV analysis

The audio is about 8.35 seconds long and contains a single frequency at ~550 Hz, not DTMF. The whistle image is a hint: the signal is **Morse code** transmitted as a whistle tone.

### Step 5 — Morse decoding

You can load `hidden.wav` into an online decoder:

https://morsecode.world/international/decoder/audio-decoder-adaptive.html

We do not provide the second part of the flag here: try decoding it yourself from the audio file or using the decoder linked above.

### Step 6 — Reconstructing the flag

Combining the two fragments:
- First part from LSB: `1m_g0nn4_`
- Second part: not provided here (decode it yourself from the audio)

The full flag is withheld: `flag{...}`

---

## Conclusion

This challenge combined format detection (the file was actually a PNG), LSB steganography to obtain the first part of the flag, and a hidden WAV appended after IEND that encoded the second part as Morse. The audio is a single-tone whistle consistent with the image hint and can be decoded with the linked Morse audio decoder.
