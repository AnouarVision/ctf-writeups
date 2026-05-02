# Base64

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Prendere la stringa hex fornita, decodificarla in bytes e poi codificarla in Base64.
> `72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf`


---

## La codifica Base64

### Alfabeto e raggruppamento dei bit

**Base64** è uno schema di codifica da binario a testo che rappresenta dati binari arbitrari come una stringa di caratteri ASCII stampabili. Il suo alfabeto è composto esattamente da 64 simboli:

$$\mathcal{A} = \{\texttt{A}\text{–}\texttt{Z},\ \texttt{a}\text{–}\texttt{z},\ \texttt{0}\text{–}\texttt{9},\ \texttt{+},\ \texttt{/}\}$$

Poiché $|\mathcal{A}| = 64 = 2^6$, ogni carattere Base64 codifica esattamente **6 bit** di dati binari. La codifica opera su gruppi di **3 byte** (24 bit) alla volta, mappandoli in **4 caratteri Base64**:

$$3 \text{ byte} \times 8 \text{ bit/byte} = 24 \text{ bit} = 4 \times 6 \text{ bit} \longrightarrow 4 \text{ caratteri Base64}$$

Questo produce un rapporto di espansione di $\frac{4}{3}$: ogni 3 byte di input generano 4 caratteri di output.

### Procedura di codifica formale

Data una sequenza di byte $B = (b_0, b_1, b_2)$, i quattro indici Base64 $i_0, i_1, i_2, i_3 \in \{0, \dots, 63\}$ si ottengono partizionando la concatenazione a 24 bit $b_0 \,\|\, b_1 \,\|\, b_2$ in quattro gruppi da 6 bit:

$$i_0 = b_0 \gg 2$$

$$i_1 = \bigl((b_0 \mathbin{\&} \texttt{0x03}) \ll 4\bigr) \mathbin{|} (b_1 \gg 4)$$

$$i_2 = \bigl((b_1 \mathbin{\&} \texttt{0x0F}) \ll 2\bigr) \mathbin{|} (b_2 \gg 6)$$

$$i_3 = b_2 \mathbin{\&} \texttt{0x3F}$$

Ogni indice $i_k$ viene poi mappato al carattere corrispondente in $\mathcal{A}$.

### Padding

Quando il numero totale di byte non è multiplo di 3, il gruppo finale viene completato con bit a zero e uno o due caratteri `=` vengono aggiunti all'output per segnalare il padding:

- 1 byte rimanente $\to$ 2 caratteri Base64 $+$ `==`
- 2 byte rimanenti $\to$ 3 caratteri Base64 $+$ `=`

In questa challenge l'input è di 27 byte ($27 = 9 \times 3$), quindi non è richiesto alcun padding.

### Esempio svolto

Consideriamo i primi tre byte della stringa hex `72bca9`:

$$\texttt{72}_{16} = 114_{10} = 01110010_2$$
$$\texttt{bc}_{16} = 188_{10} = 10111100_2$$
$$\texttt{a9}_{16} = 169_{10} = 10101001_2$$

Concatenando i 24 bit: $011100101011110010101001$

Suddivisione in quattro gruppi da 6 bit:

| Gruppo | Bit | Indice | $\mathcal{A}[\cdot]$ |
|:---:|:---:|:---:|:---:|
| $i_0$ | $011100$ | $28$ | `c` |
| $i_1$ | $101011$ | $43$ | `r` |
| $i_2$ | $110010$ | $50$ | `y` |
| $i_3$ | $101001$ | $41$ | `p` |

I primi quattro caratteri dell'output Base64 sono `cryp`, coerente con il prefisso della flag `crypto/`.

---

## Soluzione

### La pipeline a due stadi

La trasformazione completa può essere espressa come composizione:

$$\text{output} = \text{Base64}\bigl(\text{fromHex}(\text{hex\_string})\bigr)$$

**Passo 1.** Decodificare la stringa hex in un oggetto `bytes` tramite `bytes.fromhex()`.

**Passo 2.** Codificare i byte risultanti in Base64 tramite `base64.b64encode()`.

### Script

```python
#!/usr/bin/env python3

import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

raw_bytes = bytes.fromhex(hex_string)

print(base64.b64encode(raw_bytes))
```

`bytes.fromhex()` converte ogni coppia hex nel corrispondente valore di byte. `base64.b64encode()` prende l'oggetto `bytes` risultante e restituisce la sua codifica Base64 come oggetto `bytes` contenente solo caratteri ASCII stampabili.

---

### Flag

```
crypto/.../
```