# Fischietto

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** challenge_4.pdf (rinominato in challenge_4.png)

---

## Descrizione

> Questa immagine potrà sembrare casuale, ma racchiude molti significati e ricordi dal passato... e forse anche una flag.
> Nota: Il formato della flag è sempre flag{Qu3st4_e_un4_fl4g}. Tutto tranne la prima lettera è in minuscolo.

---

## Soluzione

### Passo 1 — Identificazione del file

Il file fornito ha estensione `.pdf`, ma il comando `file` rivela che in realtà è un PNG:

```bash
$ file challenge_4.pdf
challenge_4.pdf: PNG image data, 886 x 888, 8-bit/color RGBA, non-interlaced
```

Lo rinominiamo in `challenge_4.png` per poterlo analizzare correttamente.

### Passo 2 — Analisi con zsteg

`zsteg` rivela due cose nascoste nel file:

```bash
$ zsteg challenge_4.png
[?] 66804 bytes of extra data after image end (IEND), offset = 0x600ea
extradata:0   .. file: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 8 bit, mono 8000 Hz

b1,rgb,lsb,xy .. text: "flag{1m_g0nn4_
il resto della flag si trova in questo video!!! : https://www.youtube.com/watch?v=Z3J_MCbwaJ0"
```

Due scoperte:

1. **LSB steganography** nel canale RGB rivela la prima parte della flag: `flag{1m_g0nn4_` seguita da un troll che rimanda a un video YouTube.
2. **Dati extra dopo l'IEND** del PNG: un file WAV nascosto (66804 bytes, 8 bit mono 8000 Hz).

### Passo 3 — Estrazione del file WAV

Si cerca la firma `RIFF` nel file PNG e si estraggono tutti i dati da quell'offset in poi:

```python
python3 -c "
with open('challenge_4.png', 'rb') as f:
    data = f.read()
riff = data.find(b'RIFF')
with open('hidden.wav', 'wb') as f:
    f.write(data[riff:])
print('WAV estratto, size:', len(data[riff:]))
"
# WAV estratto, size: 66804
```

### Passo 4 — Analisi del file WAV

Il file audio dura circa 8.35 secondi e contiene una **singola frequenza a ~550 Hz**, non DTMF (che richiederebbe due frequenze simultanee). L'immagine del fischietto è l'hint diretto: il segnale è **Morse code** trasmesso come fischio.

### Passo 5 — Decodifica Morse

Il file `hidden.wav` può essere caricato sul decoder online:

https://morsecode.world/international/decoder/audio-decoder-adaptive.html

Non forniamo qui la seconda parte della flag: provate a decodificarla direttamente sul file audio o usando il decoder indicato.

(con alcune ripetizioni e rumore finale dovuto all'artefatto della decodifica).

### Passo 6 — Ricostruzione della flag

Combinando i due frammenti:
- Prima parte da LSB: `1m_g0nn4_`
- Seconda parte: non fornita qui (decodificatela voi dal file audio)

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge combinava tre livelli di analisi: riconoscere il vero formato del file, estrarre la prima parte della flag tramite LSB steganography con `zsteg` e ricavare la seconda parte da un file WAV nascosto dopo l'IEND del PNG. Il contenuto audio era Morse code a singola frequenza, coerente con l'immagine del fischietto, decodificabile tramite il sito morsecode.world.