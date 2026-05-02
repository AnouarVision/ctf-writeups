# Lemur XOR

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Due immagini sono state cifrate applicando uno XOR tra i loro byte RGB e la stessa chiave segreta. Recuperare il contenuto nascosto eseguendo uno XOR visuale tra i byte RGB delle due immagini.

Vengono forniti due file: `lemur.png` e `flag.png`. Entrambi appaiono come rumore colorato casuale, il risultato visivo atteso della cifratura XOR con una chiave pseudocasuale.

---

## Fondamenti teorici

### Cifratura XOR di immagini

Sia $K$ una chiave segreta interpretata come sequenza di byte, e siano $P_1$, $P_2$ due immagini in chiaro. Le loro versioni cifrate sono:

$$C_1 = P_1 \oplus K, \qquad C_2 = P_2 \oplus K$$

dove $\oplus$ denota lo XOR bit a bit applicato elemento per elemento a ogni byte RGB dell'immagine.

### Cancellazione della chiave

Per la proprietà auto-inverso dello XOR ($x \oplus x = 0$ e $x \oplus 0 = x$), applicando lo XOR ai due testi cifrati la chiave si annulla:

$$C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2 \oplus (K \oplus K) = P_1 \oplus P_2$$

Il risultato è indipendente da $K$. Non si recupera una singola immagine in chiaro, bensì lo XOR dei due testi in chiaro che è sufficiente a rivelare struttura visibile quando le due immagini sono sufficientemente diverse (ad esempio una fotografia e una flag con ampie regioni uniformi).

### Perché il riutilizzo della chiave è pericoloso

Questo attacco è una conseguenza diretta del **riutilizzo della chiave**. Se la stessa chiave $K$ viene usata per cifrare due messaggi diversi, un attaccante che ottiene entrambi i testi cifrati può eliminare la chiave con una sola operazione di XOR. Questo è l'analogo nel dominio delle immagini del classico attacco *two-time pad* ai cifrari a flusso.

---

## Soluzione

### Script

```python
#!/usr/bin/env python3

from PIL import Image
import numpy as np

img1 = np.array(Image.open("lemur.png"))
img2 = np.array(Image.open("flag.png"))

xored = np.bitwise_xor(img1, img2)

result = Image.fromarray(xored.astype(np.uint8))
result.save("xor_result.png")
```

**Passo 1.** Entrambe le immagini vengono caricate e convertite in array NumPy di forma `(327, 582, 3)`: altezza × larghezza × canali RGB, con dtype `uint8` (valori in $\{0, \dots, 255\}$).

**Passo 2.** `np.bitwise_xor()` applica l'operazione $c_1 \oplus c_2$ elemento per elemento a ogni byte dei tre canali di colore simultaneamente.

**Passo 3.** L'array risultante viene riconvertito in immagine e salvato.

### Risultato

Lo XOR delle due immagini cifrate rivela una fotografia di un lemure e una flag sovrapposte, esattamente $P_1 \oplus P_2$. La flag è leggibile perché l'immagine della flag contiene ampie regioni di colore uniforme: dove $P_2$ è costante, $P_1 \oplus P_2$ mantiene l'intera struttura di $P_1$ e viceversa.

---

### Flag

<img src="xor_result.png"></img>
