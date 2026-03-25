# Bright Sun

**Competizione:** OliCyber
**Categoria:** Misc
**File:** `Bright_Sun.png`

---

## Descrizione

> *"In un vecchio hard disk ho trovato una foto di una vacanza al mare risalente a tanti anni fa. Ricordo ancora le giornate in spiaggia sotto l'ombrellone in costume e occhiali da sole! Chissà perché tra tutte le foto è rimasta solo questa..."*

Una foto di un tramonto su una spiaggia (Ipanema, Rio de Janeiro). L'obiettivo è trovare la flag nascosta nell'immagine.

---

## Soluzione

### 1. Vulnerabilità individuata — Steganografia visiva

La flag è scritta direttamente sui **pixel ad alta luminosità** del disco solare (zona sovraesprosta), invisibile a occhio nudo a causa del clipping del bianco.

**Tecnica:** i pixel nella zona 220–255 (alte luci / highlights) contengono testo sovrapposto all'immagine. Abbassando la luminosità e alzando il contrasto, quella zona smette di saturare al bianco e il testo diventa leggibile.

### 3. Exploit — Photopea (online, no install)

1. Aprire [photopea.com](https://www.photopea.com)
2. `File` → `Open` → caricare `Bright_Sun.png`
3. `Image` → `Adjustments` → `Brightness/Contrast`
4. Abbassare la **Brightness** fino a rendere visibile il testo nel sole
5. Zoomare sul disco solare (in alto a sinistra) → la flag appare in chiaro

---

## Flag

`flag{...}`

---

## Conclusioni

Nessun tool classico di steganografia (steghide, outguess, zsteg, binwalk) è utile in questa challenge. La flag è nascosta con **steganografia visiva pura**: il testo è scritto direttamente sui pixel della zona più luminosa dell'immagine (il sole), sfruttando il fatto che l'occhio umano non distingue variazioni cromatiche nella zona di clipping del bianco.