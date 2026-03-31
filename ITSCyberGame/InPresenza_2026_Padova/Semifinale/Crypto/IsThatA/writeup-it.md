# Is that a...?

**Competizione:** ITSCyberGame<br>
**Categoria:** Crypto<br>
**File:** `pdf.csv`

---

## Descrizione

> Scusate raga ma cosa sono i magic bytes? Anywaysss, credo che per trovare la flag troverai ben altri problemi sul tuo percorso... sempre che tu riesca a scovarlo ;)

---

## Soluzione

### Passo 1 — Analisi del file fornito

Il file si chiama `pdf.csv`, suggerendo un CSV di PDF, ma il nome è fuorviante. Il primo passo è verificare i **magic bytes**, ovvero i primi byte che identificano il vero formato indipendentemente dall'estensione:

```bash
$ file pdf.csv
pdf.csv: PNG image data, 976 x 549, 8-bit/color RGB, non-interlaced
```

I magic bytes `89 50 4E 47 0D 0A 1A 0A` corrispondono alla firma del formato **PNG** (`\x89PNG`). Il file viene rinominato in `pdf.png` per procedere.

### Passo 2 — Metadati nascosti nei chunk PNG

Un file PNG è strutturato in **chunk**, ognuno con un tipo identificativo a 4 byte. Oltre ai chunk standard (`IHDR`, `IDAT`, `IEND`) esistono chunk ausiliari come `iTXt` (testo internazionale) ed `eXIf` (metadati EXIF). Si analizzano tutti i chunk non-standard:

```python
import struct

with open('pdf.png', 'rb') as f:
    data = f.read()

pos = 8  # salta la firma PNG
while pos < len(data):
    length = struct.unpack('>I', data[pos:pos+4])[0]
    chunk_type = data[pos+4:pos+8].decode('ascii', errors='replace')
    chunk_data = data[pos+8:pos+8+length]
    pos += 12 + length
    if chunk_type not in ('IHDR', 'IDAT', 'IEND'):
        print(f'{chunk_type}: {chunk_data.decode("utf-8", errors="replace")}')
    if chunk_type == 'IEND':
        break
```

Nel chunk `eXIf` e nel chunk `iTXt` con chiave `Make` si trova:

```
"password:kd2paqx0jx"
```

### Passo 3 — ZIP nascosto dopo l'IEND

Il chunk `IEND` marca la **fine ufficiale** di un PNG, qualsiasi dato che segue viene ignorato dai visualizzatori. Si cerca la firma ZIP (`PK\x03\x04`) oltre l'IEND:

```python
pk_pos = data.find(b'PK\x03\x04')
# → offset 529689 (ben oltre la fine del PNG)

zip_data = data[pk_pos:]
with open('hidden.zip', 'wb') as f:
    f.write(zip_data)
```

Lo ZIP è protetto con **crittografia AES** (metodo 99), non supportata da `unzip` standard. Si usa `pyzipper`:

```python
import pyzipper

with pyzipper.AESZipFile('hidden.zip') as z:
    print(z.namelist())  # ['HELLOTHERE.png']
    z.extractall('.', pwd=b'kd2paqx0jx')
```

### Passo 4 — Analisi steganografica di HELLOTHERE.png

Il file estratto è un PNG 1200×1200 RGBA. Si estraggono i **piani di bit LSB** (Least Significant Bit) di ogni canale colore, tecnica classica di steganografia visiva che nasconde dati nel bit meno significativo di ogni pixel, invisibile a occhio nudo:

```python
from PIL import Image
import numpy as np

img = Image.open('HELLOTHERE.png')
arr = np.array(img)

for ch, name in enumerate(['R', 'G', 'B', 'A']):
    plane = ((arr[:,:,ch] & 1) * 255).astype(np.uint8)
    Image.fromarray(plane, 'L').save(f'lsb_{name}.png')
```

Visualizzando i piani LSB, l'immagine rivela la flag leggibile direttamente.

---

## Flag

![HELLOTHERE LSB plane](lsb_R.png)

---

## Conclusioni

La challenge prevedeva quattro layer sovrapposti: un file con **estensione falsa** smascherato dai magic bytes, una **password nascosta nei metadati PNG** all'interno di chunk non-standard, un **archivio AES-ZIP appeso dopo l'IEND** (invisibile ai visualizzatori comuni) e infine la **steganografia LSB** sull'immagine finale. Ogni passo sbloccava il successivo, rendendo necessaria la conoscenza di tecniche diverse in sequenza.