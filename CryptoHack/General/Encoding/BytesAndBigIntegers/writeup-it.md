# Bytes and Big Integers

**Competizione:** CryptoHack<br>
**Categoria:** Crypto / Introduzione

---

## Descrizione

> Convertire il seguente intero nel messaggio originale:
> `11515195063862318899931685488813747395775516287289682636499965282714637259206269`

Viene fornito un intero decimale di grandi dimensioni. La challenge richiede di riconvertirlo nel messaggio ASCII originale usando la funzione `long_to_bytes()` di PyCryptodome.

---

## Da messaggi a numeri

### La convenzione di codifica

I criptosistemi come RSA operano su elementi di $\mathbb{Z}_n$, ovvero su interi. I messaggi in chiaro, tuttavia, sono sequenze di caratteri. Un modo canonico e reversibile per mappare un messaggio $M = m_0 m_1 \cdots m_{k-1}$ in un intero $N$ si articola in tre passi:

**Passo 1.** Convertire ogni carattere nel corrispondente code point ASCII:

$$v_i = \phi^{-1}(m_i) \in \{0, \dots, 127\} \qquad \forall\, i \in \{0, \dots, k-1\}$$

**Passo 2.** Esprimere ogni code point come valore esadecimale a due cifre e concatenare:

$$H = h_0 \,\|\, h_1 \,\|\, \cdots \,\|\, h_{k-1}, \qquad h_i = \text{hex}(v_i)$$

**Passo 3.** Interpretare la stringa hex risultante come intero in base 16:

$$N = \sum_{i=0}^{k-1} v_i \cdot 256^{k-1-i}$$

Questo equivale a trattare la sequenza di byte come un intero senza segno in ordine **big-endian**: il primo byte occupa la posizione più significativa.

### Esempio illustrativo

Per la stringa `HELLO`:

| Carattere | ASCII | Hex |
|:---:|:---:|:---:|
| `H` | 72 | `48` |
| `E` | 69 | `45` |
| `L` | 76 | `4c` |
| `L` | 76 | `4c` |
| `O` | 79 | `4f` |

Stringa hex concatenata: `48454c4c4f`

Valore decimale:

$$N = 72 \cdot 256^4 + 69 \cdot 256^3 + 76 \cdot 256^2 + 76 \cdot 256^1 + 79 \cdot 256^0 = 310400273487$$

### L'operazione inversa

Dato un intero $N$, la sequenza di byte originale si recupera estraendo ripetutamente il byte meno significativo e dividendo per 256:

$$b_{k-1} = N \bmod 256, \quad N \leftarrow \lfloor N / 256 \rfloor$$

ripetendo fino a $N = 0$, poi invertendo i byte raccolti. Questo è esattamente ciò che `long_to_bytes()` implementa internamente.

In modo più compatto, $N$ espresso in base 16 restituisce direttamente la stringa hex concatenata, che viene poi suddivisa in coppie di byte e decodificata tramite $\phi$.

---

## Soluzione

### Script

```python
#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes

ciphertext_int = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

print(long_to_bytes(ciphertext_int))
```

`long_to_bytes()` converte l'intero nella sua rappresentazione big-endian come sequenza di byte, che Python stampa come stringa ASCII.

### Verifica

Per verificare manualmente il risultato, si converte l'intero in esadecimale:

$$11515195063862318899931685488813747395775516287289682636499965282714637259206269_{10} = \texttt{63727970746f7b336e633064316e365f62336e645f6e756d355f6e5f627974337d}_{16}$$

Suddividendo in coppie di byte e applicando $\phi$:

| Hex | Decimale | Carattere |
|:---:|:---:|:---:|
| `63` | 99 | `c` |
| `72` | 114 | `r` |
| `79` | 121 | `y` |
| `70` | 112 | `p` |
| `74` | 116 | `t` |
| `6f` | 111 | `o` |
| `7b` | 123 | `{` |
| `33` | 51 | `.` |
| `6e` | 110 | `.` |
| `63` | 99 | `.` |
| `30` | 48 | `.` |
| `64` | 100 | `.` |
| `31` | 49 | `.` |
| `6e` | 110 | `.` |
| `36` | 54 | `.` |
| `5f` | 95 | `.` |
| `62` | 98 | `.` |
| `33` | 51 | `.` |
| `6e` | 110 | `.` |
| `64` | 100 | `.` |
| `5f` | 95 | `.` |
| `6e` | 110 | `.` |
| `75` | 117 | `.` |
| `6d` | 109 | `.` |
| `35` | 53 | `.` |
| `5f` | 95 | `.` |
| `6e` | 110 | `.` |
| `5f` | 95 | `.` |
| `62` | 98 | `.` |
| `79` | 121 | `.` |
| `74` | 116 | `.` |
| `33` | 51 | `.` |
| `7d` | 125 | `}` |

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge formalizza la conversione **messaggio → intero** che costituisce il fondamento di ogni criptosistema algebrico. In RSA, ad esempio, il testo in chiaro è un intero $m \in \mathbb{Z}_n$ e la cifratura è l'esponenziazione modulare $c = m^e \bmod n$. Affinché ciò abbia senso, la stringa originale deve prima essere convertita in $m$ tramite la procedura descritta sopra, un passo noto come **encoding**.

Due funzioni di PyCryptodome da memorizzare: `bytes_to_long(b)` converte un oggetto `bytes` nella sua rappresentazione intera; `long_to_bytes(n)` esegue l'operazione inversa. Entrambe trattano la sequenza di byte come big-endian, che è la convenzione standard nei protocolli crittografici.