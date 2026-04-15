# I like hashes

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Ho applicato una funzione di hash su ogni parte della flag, non la troverai mai!

Viene fornito un file `ct.txt` contenente 32 righe, ciascuna con un hash esadecimale di 64 caratteri.

---

## Analisi del ciphertext

Ogni riga è una stringa di 64 caratteri esadecimali, ovvero 256 bit, la dimensione esatta del digest prodotto da **SHA-256**. Il file contiene 32 righe con soli 15 hash distinti su 32, il che implica che il plaintext contiene caratteri ripetuti. Questa osservazione è già sufficiente a escludere qualsiasi schema di cifratura semanticamente sicuro.

---

## Modello matematico

Sia $\mathcal{M} = \{0,1\}^*$ lo spazio dei messaggi e $\mathcal{H} = \{0,1\}^{256}$ lo spazio dei digest. La funzione SHA-256 è definita come:

$$H : \mathcal{M} \longrightarrow \mathcal{H}$$

con le proprietà di resistenza alla preimmagine, seconda preimmagine e collisione. Il file di ciphertext è la sequenza:

$$\mathcal{C} = \bigl(H(P_0),\ H(P_1),\ \ldots,\ H(P_{n-1})\bigr)$$

dove ogni $P_i \in \Sigma$ è un **singolo carattere** del plaintext, con $\Sigma$ l'insieme dei caratteri ASCII stampabili, $|\Sigma| = 95$.

---

## Soluzione

### Step 1 — Identificazione della vulnerabilità

La cifratura carattere per carattere con una funzione deterministica $H$ è formalmente equivalente a un **cifrario a sostituzione monoalfabetica** su $\Sigma$, dove la tabella di sostituzione è:

$$\tau : \Sigma \longrightarrow \mathcal{H}, \qquad \tau(c) = H(c)$$

Un cifrario a sostituzione monoalfabetica è sicuro solo se $|\Sigma|$ è sufficientemente grande da rendere l'enumerazione computazionalmente intrattabile. Nel nostro caso:

$$|\Sigma| = 95 \ll 2^{128}$$

Lo spazio delle preimmagini candidate è quindi **banalmente enumerabile**.

### Step 2 — Costruzione della Rainbow Table

Si costruisce la tabella di lookup inversa $\tau^{-1} : \mathcal{H} \rightharpoonup \Sigma$ calcolando $H(c)$ per ogni $c \in \Sigma$:

$$\tau^{-1}(h) = c \iff H(c) = h$$

Questo richiede esattamente $|\Sigma| = 95$ valutazioni di SHA-256, un'operazione con complessità $O(|\Sigma|)$, trascurabile per qualsiasi sistema di calcolo moderno.

### Step 3 — Decifratura

Per ogni hash $\mathcal{C}_i$ nel file, si recupera il carattere originale:

$$P_i = \tau^{-1}(\mathcal{C}_i)$$

poiché SHA-256 è deterministico, la mappa $\tau$ è iniettiva su $\Sigma$ (nessuna collisione pratica per input di un singolo byte), garantendo l'unicità della soluzione.

### Step 4 — Script

```python
from hashlib import sha256

hashes = open("ct.txt").read().strip().split('\n')

rainbow = {sha256(chr(c).encode()).hexdigest(): chr(c) for c in range(32, 127)}

flag = "".join(rainbow[h] for h in hashes)
print(flag)
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge illustra una proprietà fondamentale delle funzioni di hash crittografiche che viene sistematicamente fraintesa:

1. **SHA-256 non è una funzione di cifratura**: una funzione di hash è progettata per essere resistente alla preimmagine su input arbitrari di lunghezza variabile, non per nascondere informazioni in contesti dove lo spazio degli input è finito e piccolo. La resistenza alla preimmagine garantisce che dato $h$ sia computazionalmente intrattabile trovare $m$ tale che $H(m) = h$ quando $m$ è scelto uniformemente da $\{0,1\}^*$. Quando invece $m \in \Sigma$ con $|\Sigma| = 95$, l'enumerazione esaustiva è banale.

2. **Il determinismo è fatale in assenza di sale**: poiché $H$ è deterministica, $H(c) = H(c)$ per ogni occorrenza dello stesso carattere $c$, preservando la distribuzione di frequenza del plaintext. Questo è esattamente il difetto del cifrario di Cesare e di ogni sostituzione monoalfabetica: la struttura statistica del messaggio sopravvive alla cifratura. L'aggiunta di un sale casuale per ogni carattere avrebbe impedito questo attacco, ma avrebbe anche reso il sistema non invertibile senza trasmettere il sale.

3. **La sicurezza crittografica richiede entropia adeguata**: cifrare indipendentemente ogni unità atomica del messaggio, indipendentemente dalla primitiva usata, riduce la sicurezza complessiva alla sicurezza di cifrare un singolo simbolo da un alfabeto di taglia $|\Sigma|$. Per $|\Sigma| = 95$, il sistema offre al più $\log_2(95) \approx 6.57$ bit di sicurezza per carattere, ordini di grandezza al di sotto degli standard moderni ($\geq 128$ bit).