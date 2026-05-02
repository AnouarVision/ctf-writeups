# XOR Starter

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Applicare lo XOR tra ogni carattere della stringa `label` e l'intero 13. Convertire gli interi risultanti in una stringa e inviare la flag come `crypto{new_string}`.

La challenge si risolve interamente con un breve one-liner Python.

---

## Fondamenti teorici

### L'operatore XOR

Lo XOR (*or esclusivo*) è un operatore binario bit a bit definito dalla seguente tavola di verità:

| $a$ | $b$ | $a \oplus b$ |
|:---:|:---:|:---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Per interi a più bit, lo XOR viene applicato **bit per bit** a ogni coppia corrispondente di bit. Ad esempio:

$$0110_2 \oplus 1010_2 = 1100_2$$

### XOR di una stringa con una chiave intera

Data una stringa $S = s_0 s_1 \cdots s_{n-1}$ e una chiave intera $k$, il cifrario XOR produce la stringa di output $S' = s'_0 s'_1 \cdots s'_{n-1}$ dove ogni carattere è trasformato come:

$$s'_i = \phi\!\left(\phi^{-1}(s_i) \oplus k\right)$$

con $\phi^{-1}$ che mappa un carattere nel suo code point Unicode e $\phi$ che riconverte un code point nel carattere corrispondente.

---

## Soluzione

### Calcolo svolto

La chiave è $k = 13 = 00001101_2$. Ogni carattere di `label` viene elaborato come segue:

| $i$ | $s_i$ | $\phi^{-1}(s_i)$ | Binario | $\oplus\ 00001101$ | Risultato | $s'_i$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | `l` | 108 | $01101100$ | $01100001$ | 97 | `.` |
| 1 | `a` | 97 | $01100001$ | $01101100$ | 108 | `.` |
| 2 | `b` | 98 | $01100010$ | $01101111$ | 111 | `.` |
| 3 | `e` | 101 | $01100101$ | $01101000$ | 104 | `.` |
| 4 | `l` | 108 | $01101100$ | $01100001$ | 97 | `.` |

Si noti che `l` $\oplus$ 13 = `a` e `a` $\oplus$ 13 = `l`: i due caratteri sono l'immagine XOR l'uno dell'altro sotto la chiave 13, conseguenza diretta della proprietà auto-inverso $(\phi^{-1}(s_i) \oplus k) \oplus k = \phi^{-1}(s_i)$.

### Script

```python
#!/usr/bin/env python3

message = "label"
key = 13

print("".join(chr(ord(c) ^ key) for c in message))
```

L'espressione `ord(c) ^ key` calcola $\phi^{-1}(s_i) \oplus k$, e `chr()` mappa il risultato nel carattere corrispondente. `"".join()` concatena tutti i caratteri nella stringa finale.

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge introduce lo XOR a livello di carattere, la forma più semplice possibile di **cifrario a flusso**: un byte di chiave fisso viene messo in XOR con ogni byte del testo in chiaro in sequenza.

**Invertibilità.** Poiché $\phi^{-1}(s'_i) \oplus k = (\phi^{-1}(s_i) \oplus k) \oplus k = \phi^{-1}(s_i)$, cifratura e decifratura sono la stessa operazione. La stessa funzione con la stessa chiave recupera la stringa originale.