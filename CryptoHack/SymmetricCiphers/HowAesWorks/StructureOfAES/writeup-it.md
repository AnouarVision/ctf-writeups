# Structure of AES

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Scrivere una funzione `matrix2bytes` per convertire una matrice 4×4 di interi in un array di 16 byte e inviare il testo in chiaro risultante come flag.

Viene fornito un file Python con la funzione `bytes2matrix` già implementata. Occorre scrivere l'inverso `matrix2bytes` e applicarlo alla matrice fornita per recuperare la flag.

---

## Fondamenti teorici

### AES-128: panoramica della struttura

AES-128 cifra un blocco di testo in chiaro da 128 bit (16 byte) usando una chiave da 128 bit. Il testo in chiaro viene disposto come una **matrice 4×4 di byte** (lo *stato*) e trasformato attraverso una sequenza di round. Ogni round applica quattro operazioni invertibili che insieme forniscono confusione e diffusione, le due proprietà identificate da Claude Shannon negli anni '40 come necessarie per un cifrario sicuro.

Per una visualizzazione più chiara del processo, si rimanda a questa animazione:
https://formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng-html5.html

<img src="input.png">

La pipeline di cifratura completa è:

**1. Key Expansion (Key Schedule)**
Dalla chiave da 128 bit vengono derivate 11 separate *round key* da 128 bit, una per ogni step `AddRoundKey` (iniziale + 10 round).

<img src="KeyExpansions.gif">

**2. AddRoundKey iniziale**
Lo stato viene messo in XOR con la round key 0 prima che inizi qualsiasi round
<img src="AddRoundKeyIniziale.png">

**3. Round 1–9 (round principali)**
Ciascuno dei 9 round principali applica quattro step in sequenza:

- **SubBytes**: ogni byte dello stato viene sostituito da un byte diverso tramite una tabella di sostituzione fissa non lineare (S-box). Questo fornisce *confusione*: oscura la relazione tra chiave e testo cifrato
<img src="subBytes.gif">

- **ShiftRows**: le ultime tre righe della matrice di stato vengono ciclicamente traslate a sinistra rispettivamente di 1, 2 e 3 posizioni. Questo garantisce che i byte di colonne diverse si mescolino tra i round
<img src="shiftRows.gif">

- **MixColumns**: ogni colonna dello stato viene trattata come un polinomio su $\text{GF}(2^8)$ e moltiplicata per una matrice fissa. Questo fornisce *diffusione*: ogni byte di output dipende da tutti e quattro i byte di input della colonna
<img src="mixColumns.gif">

- **AddRoundKey**: lo stato viene messo in XOR con la round key corrente.

**4. Round finale (round 10)**
Identico ai round 1–9, ma **MixColumns è omesso**. Questo rende la decifratura strutturalmente simmetrica alla cifratura
<img src="RoundFinale.png">

### Layout della matrice di stato

I 16 byte del testo in chiaro vengono disposti nella matrice di stato **per colonne**:

$$
\left[
\begin{array}{cccc}
b_0 & b_4 & b_8 & b_{12} \\
b_1 & b_5 & b_9 & b_{13} \\
b_2 & b_6 & b_{10} & b_{14} \\
b_3 & b_7 & b_{11} & b_{15}
\end{array}
\right]
$$

Si noti l'ordinamento column-major: i byte 0–3 riempiono la prima colonna, i byte 4–7 la seconda e così via. Questo è importante quando si implementano correttamente `bytes2matrix` e `matrix2bytes`.

Nell'implementazione fornita, `bytes2matrix` usa l'ordinamento **row-major** (ogni riga della matrice corrisponde a 4 byte consecutivi), che è una semplificazione valida e comune per le challenge.

---

## Soluzione

### Analisi di `bytes2matrix`

```python
def bytes2matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]
```

Divide l'input di 16 byte in quattro chunk consecutivi da 4 byte, ognuno dei quali diventa una riga della matrice. L'operazione inversa deve riassemblare quelle righe in una sequenza piatta di byte.

### Implementazione di `matrix2bytes`

```python
def matrix2bytes(matrix):
    return bytes(val for row in matrix for val in row)
```

L'espressione generatrice annidata itera su ogni riga, poi su ogni valore all'interno di quella riga, appiattendo la matrice 4×4 in una sequenza di 16 interi. `bytes()` converte la sequenza in un oggetto `bytes`.

### Script completo

```python
#!/usr/bin/env python3

def bytes2matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    return bytes(val for row in matrix for val in row)

matrix = [
    [99,  114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97,  116],
    [114, 105, 120, 125],
]

print(matrix2bytes(matrix))
```

### Output

```
b'crypto{...}'
```

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge stabilisce due funzioni di utilità: `bytes2matrix` e `matrix2bytes`. Verranno riutilizzate in ogni challenge AES successiva. La rappresentazione a matrice di stato è il fondamento su cui operano SubBytes, ShiftRows, MixColumns e AddRoundKey.

Il punto chiave sulla struttura di AES è che la sua sicurezza non si basa su un singolo elegante problema matematico (come RSA si basa sulla fattorizzazione degli interi). Al contrario, è costruita da molte operazioni semplici, veloci e individualmente deboli la cui composizione raggiunge una forte confusione e diffusione.
