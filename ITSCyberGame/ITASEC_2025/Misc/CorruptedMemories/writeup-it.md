# Corrupted Memories

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** corrupted_memories.png

---

## Descrizione

> Un ricordo digitale danneggiato... i primi frammenti sono corrotti ma l'immagine completa nasconde ancora la verità.
> Riuscirai a ricostruire ciò che è stato alterato?

---

## Soluzione

La hint parla esplicitamente di "primi frammenti corrotti", il che suggerisce un problema all'**header del file**. L'analisi iniziale lo conferma immediatamente.

### Passo 1 — Analisi Iniziale

```bash
$ file corrupted_memories.png
corrupted_memories.png: data
```

`file` non riconosce il formato, il magic number è assente o errato. ExifTool conferma:

```bash
$ exiftool corrupted_memories.png
Error: File format error
```

Binwalk trova però dati Zlib compressi all'offset 0x5B, coerente con un PNG i cui dati interni sono intatti ma il cui header è danneggiato.

```bash
$ binwalk corrupted_memories.png
DECIMAL       HEXADECIMAL     DESCRIPTION
91            0x5B            Zlib compressed data, compressed
```

### Passo 2 — Ispezione dei byte grezzi

```bash
$ xxd corrupted_memories.png | head -4
00000000: 0123 4567 89ab cdef 0000 000d 4948 4452  .#Eg........IHDR
00000010: 0000 04d0 0000 02b2 0806 0000 0014 de23  ...............#
00000020: 8e00 0000 0173 5247 4200 aece 1ce9 0000  .....sRGB.......
00000030: 0004 6741 4d41 0000 b18f 0bfc 6105 0000  ..gAMA......a...
```

I primi 8 byte sono `01 23 45 67 89 ab cd ef`, un placeholder sequenziale ovvio. Il magic number corretto di un file PNG è:

```
89 50 4E 47 0D 0A 1A 0A
```

Dal byte 8 in poi il file è intatto: si vede subito `49 48 44 52` ovvero `IHDR`, il primo chunk valido di ogni PNG.

### Passo 3 — Fix con `dd`

Basta sovrascrivere i primi 8 byte senza toccare il resto del file:

```bash
$ printf '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' | dd of=corrupted_memories.png bs=1 seek=0 conv=notrunc
8+0 records in
8+0 records out
8 bytes copied, 0,0011624 s, 6,9 kB/s
```

- `seek=0`: sovrascrive a partire dall'offset 0
- `conv=notrunc`: non tronca il file, lascia intatto tutto il resto

### Passo 4 — Verifica

```bash
$ file corrupted_memories.png
corrupted_memories.png: PNG image data, 1232 x 690, 8-bit/color RGBA, non-interlaced
```

Il file è ora un PNG valido. Aprendolo, la flag è visibile nell'immagine.