# QRCode

**Competizione:** FSCS 2022
**Categoria:** Misc
**File:** `flag.png`

---

## Descrizione
> Nous avons récupéré ce QRcode que nous n’arrivons pas à lire : pouvez-vous nous aider ?

Viene fornita un'immagine PNG contenente un QR code che nessun lettore riesce a decodificare. L'obiettivo è capire perché e ripristinarlo.

---

## Soluzione

### 1. Ricognizione iniziale

Aprendo l'immagine, a prima vista il QR code sembra normale. Tuttavia, confrontandolo con un QR code classico, si nota subito qualcosa di anomalo:

> **I 3 grandi quadrati negli angoli (in alto a sinistra, in alto a destra, in basso a sinistra) sono "vuoti": hanno il bordo nero esterno ma mancano del quadrato nero 3×3 interno.**

Questi tre quadrati si chiamano **Finder Pattern** e sono descritti nello standard `ISO/IEC 18004:2015` (e anche su [Wikipedia - QR code](https://en.wikipedia.org/wiki/QR_code)).

### 2. Vulnerabilità individuata — Finder Pattern mancanti

I **Finder Pattern** sono le strutture 7×7 moduli negli angoli del QR code. La loro struttura è:

```
█ █ █ █ █ █ █
█           █
█   █ █ █   █   ← il quadrato 3x3 interno è quello che manca
█   █ █ █   █
█   █ █ █   █
█           █
█ █ █ █ █ █ █
```

Senza il quadrato interno, **nessun decoder riesce a localizzare e orientare il QR**. Quei 3 quadrati neri interni sono stati eliminati deliberatamente.

---

### 3. Fix con tool online — Paint.NET / Photopea / GIMP

Si può risolvere con qualsiasi editor di immagini che permetta di disegnare rettangoli pieni. Di seguito le istruzioni per **Photopea** (gratuito, online, no install):

#### Passi su [photopea.com](https://www.photopea.com)

1. **Apri l'immagine**
   - Vai su `File → Open` e carica `flag.png`

2. **Seleziona il colore nero**
   - Clicca sul quadratino del colore in basso a sinistra nella toolbar
   - Imposta il colore su `#000000` (nero puro)

3. **Seleziona lo strumento Rettangolo di Selezione**
   - Premi `M` oppure clicca l'icona del rettangolo tratteggiato nella toolbar

4. **Disegna il quadrato interno nel finder pattern in alto a sinistra**
   - Il finder è nell'angolo TL. Il quadrato interno 3×3 si trova a circa **2 moduli dal bordo** del finder
   - Nell'immagine (450×450 px), il finder TL va da pixel ~40 a ~110
   - Seleziona l'area interna: circa da pixel **(60, 60) a (90, 90)**
   - Poi vai su `Edit → Fill` e scegli **Foreground Color** (nero) → `OK`

5. **Ripeti per il finder in alto a destra**
   - Si trova nell'angolo TR, stessa altezza del primo
   - Seleziona l'area interna: circa da pixel **(360, 60) a (390, 90)**
   - `Edit → Fill → Foreground Color`

6. **Ripeti per il finder in basso a sinistra**
   - Si trova nell'angolo BL
   - Seleziona l'area interna: circa da pixel **(60, 360) a (90, 390)**
   - `Edit → Fill → Foreground Color`

7. **Salva l'immagine**
   - `File → Export As → PNG`

---

> **Nota:** se non sei sicuro delle coordinate esatte, basta disegnare un quadrato nero "abbastanza grande" dentro ciascun grande quadrato bianco. Non serve precisione al pixel, anche un rettangolo approssimativo funziona, come confermato dall'autore della challenge.

---

### 4. Qr ottenuto e da scansionare

![Snapshot decriptata](qr_fixed.png)


---

## Flag

```
FCSC{...}
```

---

## Conclusioni

Prima di applicare tecniche complesse, osservare l'immagine e confrontarla con lo standard di riferimento. Un'anomalia visiva ovvia può essere la chiave della soluzione.