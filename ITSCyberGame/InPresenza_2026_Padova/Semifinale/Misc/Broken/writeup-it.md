# Broken

**Competizione:** ITSCyberGame <br>
**Categoria:** Misc <br>
**Servizio:** `data.zip`

---

## Descrizione

Viene fornito uno zip contenente una cartella `challenge/` con un file `qr.png` apparentemente corrotto e una directory `.git/` nascosta. La descrizione recita:

> "Mi sa che ha rotto il QR, dannato AI agent!"

L'obiettivo è recuperare il QR leggibile e decodificarlo per ottenere la flag.

---

## Soluzione

### 1. Ricognizione iniziale

```bash
unzip -l data.zip
```

Lo zip contiene:
- `challenge/qr.png`: immagine QR 37×37 px (versione 5), non leggibile
- `challenge/.git/`: repository git con oggetti, log e refs

Prima anomalia evidente: il file atteso `.git/HEAD` è stato rinominato `.git/TESTA`.

```
challenge/.git/TESTA   ← dovrebbe essere HEAD
challenge/.git/objects/
challenge/.git/refs/heads/main
challenge/.git/refs/heads/dev
```

### 2. Vulnerabilità individuata — HEAD rinominato + storia git

Il trick classico di questa tipologia di challenge è **rinominare file critici di Git** per impedire ai tool standard di funzionare. In questo caso `HEAD` → `TESTA`.

Fix immediato:

```bash
cp .git/TESTA .git/HEAD
```

Dopodichè `git log` rivela la struttura completa:

```
301 commit su branch main  (tutti: "update: commit N")
  2 commit su branch dev   ("add qr code")
```

### 3. Analisi della struttura

**Branch `dev`** contiene il commit originale che aggiunge il QR:

```
e9941cf add qr code   ← il QR viene creato qui
```

**Branch `main`** contiene 300 commit successivi, ognuno dei quali modifica `qr.png` di **esattamente 1 pixel** (flip bianco↔nero), degradando progressivamente il QR fino a renderlo illeggibile:

```python
# Differenze pixel tra commit consecutivi = 1 esatto per tutti i 300 commit
Commit 1 (c4664b9): 1 pixel cambiati @ [[28, 9]]
Commit 2 (8656dca): 1 pixel cambiati @ [[16, 21]]
Commit 3 (d38cea2): 1 pixel cambiati @ [[32, 10]]
...
```

Il QR originale (37×37, 444 pixel neri su 1369 totali) è stato corrotto da 300 flip singoli di pixel.

### 4. Exploit — Recupero del QR originale

Il QR corretto si trova direttamente nel branch `dev`, prima che i commit su `main` lo corrompessero:

```bash
git show dev:qr.png > qr_original.png
```

Tentativo di decode con upscaling (il QR nativo 37px è troppo piccolo per i decoder standard):

```python
import zxingcpp
from PIL import Image

img = Image.open('qr_original.png')
# Upscaling 10x con interpolazione NEAREST per preservare i moduli binari
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

## Conclusioni

La challenge combina due tecniche:

1. **Git forensics**: rinomina di `HEAD` in `TESTA` per nascondere la storia git ai tool automatici. Soluzione: `cp .git/TESTA .git/HEAD`.

2. **QR degradation**: 300 commit che flippano un pixel alla volta il QR originale, rendendolo illeggibile senza però distruggerlo, il dato originale è recuperabile dal commit di origine nel branch `dev`.