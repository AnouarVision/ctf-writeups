# Hex

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Decodificare la seguente stringa esadecimale per ottenere la flag.
> `63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d`

Non viene fornito alcuno script. La challenge fornisce direttamente una stringa esadecimale e chiede di convertirla nella corrispondente rappresentazione ASCII tramite la funzione `bytes.fromhex()` di Python.

---

## La codifica esadecimale

### Notazione posizionale e base 16

Il sistema decimale usa la base 10, rappresentando i numeri come combinazioni lineari di potenze di 10. Il sistema **esadecimale** usa la base 16, rappresentando i numeri come combinazioni lineari di potenze di 16. Ogni cifra assume uno dei 16 valori possibili, denotati dai simboli $\{0, 1, 2, \dots, 9, A, B, C, D, E, F\}$, dove $A = 10, B = 11, \dots, F = 15$.

Un numero esadecimale di $n$ cifre $d_{n-1} d_{n-2} \cdots d_1 d_0$ ha il seguente valore decimale:

$$N = \sum_{i=0}^{n-1} d_i \cdot 16^i$$

### Byte e coppie esadecimali

Un **byte** è una quantità a 8 bit, in grado di rappresentare $2^8 = 256$ valori distinti, compresi tra $0_{10}$ e $255_{10}$. In esadecimale, questo corrisponde all'intervallo $\texttt{00}_{16}$–$\texttt{FF}_{16}$: esattamente due cifre esadecimali sono sufficienti e necessarie per rappresentare un singolo byte. Questo è il motivo per cui l'esadecimale è la scelta naturale per la rappresentazione di dati a livello di byte.

### Da ASCII a hex

Il processo di codifica di una stringa ASCII $s = s_0 s_1 \cdots s_{n-1}$ si articola in due passi:

**Passo 1.** Convertire ogni carattere nel corrispondente code point ASCII tramite $\phi^{-1}$:

$$v_i = \phi^{-1}(s_i) \in \{0, \dots, 127\} \qquad \forall\, i \in \{0, \dots, n-1\}$$

**Passo 2.** Esprimere ogni code point come numero esadecimale a due cifre:

$$h_i = \text{hex}(v_i) \in \{\texttt{00}, \texttt{01}, \dots, \texttt{7f}\}$$

La stringa hex finale è la concatenazione $h_0 \,\|\, h_1 \,\|\, \cdots \,\|\, h_{n-1}$.

### Esempio svolto

Consideriamo il carattere `c`, primo byte del prefisso `crypto{`:

$$\phi^{-1}(\texttt{c}) = 99_{10}$$

Conversione di 99 in base 16:

$$99 = 6 \cdot 16^1 + 3 \cdot 16^0 \implies 99_{10} = \texttt{63}_{16}$$

Infatti la stringa hex inizia con `63`. La direzione di decodifica inverte semplicemente questo processo.

---

## Soluzione

### Script

```python
#!/usr/bin/env python3

hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"

print(bytes.fromhex(hex_string))
```

`bytes.fromhex()` prende una stringa esadecimale, la suddivide in coppie di cifre, converte ogni coppia nel corrispondente valore di byte e restituisce un oggetto `bytes`. Stampandolo direttamente si ottiene la rappresentazione ASCII di quei byte.

### Tabella di decodifica parziale (primi 7 byte)

Il prefisso `crypto{` funge da verifica che la decodifica sia corretta:

| Coppia hex | Decimale | $\phi(\cdot)$ |
|:---:|:---:|:---:|
| `63` | 99 | `c` |
| `72` | 114 | `r` |
| `79` | 121 | `y` |
| `70` | 112 | `p` |
| `74` | 116 | `t` |
| `6f` | 111 | `o` |
| `7b` | 123 | `{` |

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Due funzioni da memorizzare: `bytes.fromhex(s)` decodifica una stringa hex in un oggetto `bytes`; l'operazione inversa, `.hex()`, può essere invocata su qualsiasi oggetto `bytes` per ottenere la corrispondente stringa esadecimale.