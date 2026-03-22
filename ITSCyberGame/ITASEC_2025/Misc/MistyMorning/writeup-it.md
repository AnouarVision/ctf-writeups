# Misty Morning

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** misty_morning.png

---

## Descrizione

> Un viaggiatore solitario ha lasciato un messaggio nascosto tra le nebbie delle montagne: solo chi sa guardare oltre l'orizzonte potrà trovarlo...

---

## Soluzione

La hint suggerisce di **"guardare oltre"**, non il contenuto ovvio dell'immagine, ma i suoi livelli nascosti. In steganografia, questo significa analizzare i bit plane dei singoli canali colore.

### Passo 1 — Analisi Iniziale del File

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

Nessun file nascosto, nessun metadata utile. L'analisi standard non porta da nessuna parte.

### Passo 2 — Analisi dei Bit Plane

Ispezionando i valori RGBA dei pixel, emerge un pattern anomalo: i valori del **canale Blue** non sono uniformi come ci si aspetterebbe da uno sfondo nebbioso naturale, presentano piccole variazioni sistematiche che potrebbero codificare informazioni.

Lo strumento **StegOnline** ([georgeom.net/StegOnline](https://georgeom.net/StegOnline)) permette di visualizzare i singoli bit plane di ogni canale colore. Caricando l'immagine e navigando in **Browse Bit Planes → Blue → Bit 3**, il testo della flag appare visivamente scritto nell'immagine:

```
flag{...}
```

Il bit 3 del canale Blue era il livello ottimale per rendere il testo leggibile, abbastanza profondo da essere invisibile a occhio nudo nell'immagine originale, ma emergente una volta isolato.