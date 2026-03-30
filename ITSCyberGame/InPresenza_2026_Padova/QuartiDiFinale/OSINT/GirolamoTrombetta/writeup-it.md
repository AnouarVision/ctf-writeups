# Girolamo Trombetta

**Competizione:** ITSCyberGame
**Categoria:** OSINT

---

## Descrizione

> Un hacker internazionale sta mettendo in difficoltà gli aiuti umanitari in zone ad alto rischio di incendio. Grazie a lunghe ricerche e investigazioni abbiamo trovato la username del suo laptop, puoi aiutarci a trovare la sua password? Sappiamo solo che una delle zone che sta lasciando quasi industurbate è quella nella foto (scattata qualche settimana fa). Sembra che la sua password sia il nome scientifico di una specie animale estinta nelle zone limitrofe e l'anno della sua estinzione. flag{nome_nome_anno in numero}

---

## Soluzione

### 1. Ricognizione iniziale — Analisi dell'immagine

L'immagine fornita è uno screenshot da un sistema di monitoraggio satellitare degli incendi (NASA FIRMS / MODIS/VIIRS). Si riconoscono:

- **Macchie rosse**: hotspot di incendio attivo rilevati da satellite
- **Vegetazione densa verde**: foreste collinari/montane
- **Un lago**: al centro-nord del frame
- **Un insediamento urbano**: a est con pattern stradale radiale
- **Zone con meno hotspot**: aree boschive protette o meno soggette ad incendio

**Tool utilizzati per la geolocalizzazione:**
- Analisi morfologica della vegetazione (foresta subtropicale/monsonica)
- Pattern urbano tipico di città asiatica di medie dimensioni
- Disposizione lago + città + strade

### 2. Geolocalizzazione — Cina

La zona è in **Cina**, probabilmente nella fascia del bacino dello **Yangtze** o della Cina meridionale/sud-occidentale (Sichuan/Yunnan/Hunan), aree note per:

- Alta frequenza di incendi stagionali (stagione secca inverno-primavera)
- Presenza di ecosistemi fluviali endemici
- Zona di intervento umanitario internazionale

La caratteristica del "lago" e del centro urbano a est del frame è compatibile con diversi centri urbani cinesi sul bacino dello Yangtze, il più lungo fiume della Cina e terzo al mondo.

### 3. Identificazione della specie estinta

**Criterio di ricerca:** specie animale **estinta nelle zone limitrofe** alla zona mostrata, con anno documentato.

La specie più iconica e scientificamente documentata estinta in Cina è il **Baiji**, o delfino dello Yangtze.

| Campo | Dettaglio |
|-------|-----------|
| Nome comune | Baiji / Delfino dello Yangtze / "Dea dello Yangtze" |
| Nome scientifico | *Lipotes vexillifer* (Miller, 1918) |
| Habitat | Fiume Yangtze (Changjiang), Cina |
| Causa estinzione | Industrializzazione, pesca con elettroshock, reti da pesca, diga delle Tre Gole, inquinamento |
| Anno dichiarazione estinzione | **2006** |
| Status IUCN | Critically Endangered (Possibly Extinct) / funzionalmente estinto |

**Timeline dell'estinzione:**
- Pre-1950: ~6.000 individui stimati
- 1980: ~400 individui
- 1997-1999: solo 13 individui contati
- Novembre 2001: ultimo avvistamento verificato (femmina gravida arenata a Zhenjiang)
- Maggio 2002: ultimo individuo fotografato (sezione Tongling)
- **Dicembre 2006**: spedizione internazionale di 6 settimane su tutto il range storico → **zero baiji rilevati** → dichiarato estinto
- 2007: presunto avvistamento non confermato
- Il baiji rappresenta la **prima estinzione documentata di un vertebrato acquatico "megafaunale"** in oltre 50 anni

*Lipotes* = greco "rimasto indietro"; *vexillifer* = latino "portabandiera" (dal pinnino dorsale che ricorda una bandierina).

### 4. Costruzione della flag

Il formato richiesto è `flag{nome_nome_anno}`, dove il nome scientifico usa underscore come separatore:

```
Lipotes_vexillifer → nome genere + underscore + epiteto specifico
2006 → anno di dichiarazione dell'estinzione
```

---

## Flag

```
flag{Lipotes_vexillifer_2006}
```

---

## Conclusioni

Questa challenge OSINT ha richiesto tre fasi distinte:

1. **Geolocalizzazione da immagine satellitare**: riconoscere la mappa come screenshot FIRMS con hotspot di incendio e identificare la regione geografica (Cina) tramite morfologia del territorio, pattern urbano e vegetazione.

2. **Ricerca della specie estinta**: a partire dalla zona (bacino dello Yangtze / Cina), identificare l'animale più iconicamente estinto nell'area. Il Baiji (*Lipotes vexillifer*) è la risposta corretta: primo delfino dichiarato estinto per cause umane dirette, endemico dello Yangtze.

3. **Formattazione corretta**: applicare il formato `flag{genere_specie_anno}` con anno = 2006 (anno della spedizione che ne ha certificato la scomparsa).