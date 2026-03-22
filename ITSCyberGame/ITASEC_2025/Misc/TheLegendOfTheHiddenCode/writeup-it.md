# The Legend of the Hidden Code

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** the_legend_of_hidden_code.png

---

## Descrizione

> Nel mondo di Hyrule non tutto è come appare. Alcuni segreti si nascondono dietro la facciata proprio come un cuore segreto dietro una parete di mattoni. Non limitarti a guardare; scava nel profondo per trovare la verità.

---

## Soluzione

La hint è chiara: **"Non limitarti a guardare; scava nel profondo"**. Il segreto non è nell'immagine stessa, ma in ciò che sta sotto la superficie "i metadati".

### Passo 1 — Analisi Iniziale del File

```bash
$ file the_legend_of_hidden_code.png
the_legend_of_hidden_code.png: PNG image data, 833 x 1280, 8-bit/color RGBA, non-interlaced

$ binwalk the_legend_of_hidden_code.png
DECIMAL       HEXADECIMAL     DESCRIPTION
0             0x0             PNG image, 833 x 1280, 8-bit/color RGBA, non-interlaced
633           0x279           Zlib compressed data, compressed
```

File PNG autentico, nessun file nascosto al suo interno. `binwalk` non rivela nulla di interessante.

### Passo 2 — Analisi dei Metadati con Exiftool

La hint suggerisce di "scavare nel profondo". In forensics, scavare in profondità significa guardare i metadati del file:

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