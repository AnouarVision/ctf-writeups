# Decode

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** decode.png

---

## Descrizione

> Non è come sembra...

---

## Soluzione

La hint è già una bussola: **"Non è come sembra"**. L'elemento più vistoso dell'immagine è un diversivo e la vera informazione si trova in un dettaglio che si tende a ignorare.

### Passo 1 — Analisi Iniziale del File

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
Title             : Senza titolo (Post Instagram) - 1

$ binwalk decode.png
DECIMAL       HEXADECIMAL     DESCRIPTION
0             0x0             PNG image, 3375 x 3375, 8-bit/color RGBA, non-interlaced
1274          0x4FA           Zlib compressed data, default compression
```

Il file è un PNG autentico, nessun file nascosto al suo interno, nulla di anomalo nei metadati. L'analisi standard non porta da nessuna parte.

### Passo 2 — Il diversivo: il QR Grande

L'immagine mostra un QR code di grandi dimensioni sovrapposto a un faro al tramonto. Il primo istinto è decodificarlo ed è esattamente ciò che la challenge vuole che tu faccia.

Decodificando il QR grande con qualsiasi lettore, il risultato è:

```
prova
```

Niente di utile. È un elemento decorativo inserito appositamente per distrarre.

### Passo 3 — Il QR nascosto

Ispezionando l'immagine ad alta risoluzione (3375x3375), nell'**angolo in basso a destra** è presente un secondo QR code, molto più piccolo e quasi mimetizzato con lo sfondo.

```
┌──────────────────────────────────────┐
│                                      │
│       [QR grande - diversivo]        │
│                                      │
│                          ┌────┐      │
│                          │ QR │ ← !  │
│                          └────┘      │
└──────────────────────────────────────┘
```

Puntando un lettore QR sull'angolo in basso a destra dell'immagine originale:

```
flag{...}
```