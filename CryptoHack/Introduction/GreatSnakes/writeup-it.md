# Great Snakes

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Eseguire lo script Python fornito. Stamperà la flag.

Viene fornito il file sorgente `great_snakes.py`. Basta eseguirlo e leggere l'output.

---

## L'operazione XOR

Prima di analizzare lo script, vale la pena richiamare il fondamento matematico su cui si basa la soluzione.

### Definizione

Siano $a, b \in \mathbb{Z}$ due interi non negativi. Il loro **XOR bit a bit**, denotato $a \oplus b$, è definito applicando l'or esclusivo logico a ciascuna coppia corrispondente di bit nelle rappresentazioni binarie di $a$ e $b$.

Formalmente, se $a = \sum_{i} a_i \cdot 2^i$ e $b = \sum_{i} b_i \cdot 2^i$ con $a_i, b_i \in \{0, 1\}$, allora:

$$a \oplus b = \sum_{i} (a_i \oplus b_i) \cdot 2^i$$

dove lo XOR su singolo bit è definito dalla seguente tavola di verità:

| $a_i$ | $b_i$ | $a_i \oplus b_i$ |
|:---:|:---:|:---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### Proprietà algebriche rilevanti

L'operazione XOR su $\mathbb{Z}$ soddisfa le seguenti proprietà, da tenere a mente:

1. **Commutatività:** $a \oplus b = b \oplus a$
2. **Associatività:** $(a \oplus b) \oplus c = a \oplus (b \oplus c)$
3. **Elemento neutro:** $a \oplus 0 = a$
4. **Auto-inverso:** $a \oplus a = 0$

Dalla proprietà 4 segue immediatamente una conseguenza fondamentale:

$$a \oplus b = c \implies a = c \oplus b$$

Questa è l'**invertibilità** dello XOR ed è esattamente la proprietà sfruttata in questa challenge.

---

## Analisi dello script

```python
ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]

print("".join(chr(o ^ 0x32) for o in ords))
```

Lo script definisce una lista di 21 interi $\{o_i\}_{i=0}^{20} \subset \mathbb{Z}$ e applica a ciascun elemento la seguente trasformazione:

$$f(o_i) = \text{chr}(o_i \oplus k), \quad k = 0\text{x}32 = 50_{10}$$

dove $\text{chr} : \mathbb{Z} \to \Sigma$ mappa un code point Unicode nel carattere corrispondente. I caratteri risultanti vengono concatenati per formare la flag.

### Esempio svolto

Consideriamo il primo elemento della lista: $o_0 = 81$.

**Passo 1.** Esprimere entrambi gli operandi in binario:

$$81_{10} = 1010001_2, \qquad 50_{10} = 0110010_2$$

**Passo 2.** Applicare lo XOR bit a bit colonna per colonna:

$$\begin{array}{r} 1010001 \\ \oplus \quad 0110010 \\ \hline 1100011 \end{array}$$

**Passo 3.** Riconvertire in decimale:

$$1100011_2 = 2^6 + 2^5 + 2^1 + 2^0 = 64 + 32 + 2 + 1 = 99_{10}$$

**Passo 4.** Mappare al carattere:

$$\text{chr}(99) = \texttt{c}$$

La stessa procedura applicata a ogni $o_i$ produce la sequenza di caratteri che compone la flag.

### Decodifica completa

Applicando $f(o_i) = \text{chr}(o_i \oplus 50)$ a tutti i 21 elementi:

| $i$ | $o_i$ | $o_i \oplus 50$ | $\text{chr}(\cdot)$ |
|:---:|:---:|:---:|:---:|
| 0 | 81 | 99 | `c` |
| 1 | 64 | 114 | `r` |
| 2 | 75 | 121 | `y` |
| 3 | 66 | 112 | `p` |
| 4 | 70 | 116 | `t` |
| 5 | 93 | 111 | `o` |
| 6 | 73 | 123 | `{` |
| 7 | 72 | 122 | `z` |
| 8 | 1 | 51 | `3` |
| 9 | 92 | 110 | `n` |
| 10 | 109 | 95 | `_` |
| 11 | 2 | 48 | `0` |
| 12 | 84 | 102 | `f` |
| 13 | 109 | 95 | `_` |
| 14 | 66 | 112 | `p` |
| 15 | 75 | 121 | `y` |
| 16 | 70 | 116 | `t` |
| 17 | 90 | 104 | `h` |
| 18 | 2 | 48 | `0` |
| 19 | 92 | 110 | `n` |
| 20 | 79 | 125 | `}` |

---

### Flag

```
crypto{z3n_0f_pyth0n}
```

---

## Conclusioni

Questa challenge illustra una delle primitive crittografiche più elementari: la **codifica XOR a chiave singola**. Dato un vettore di testo cifrato $\mathbf{c} = (c_0, c_1, \dots, c_{n-1})$ e una chiave nota $k$, il testo in chiaro si recupera applicando nuovamente la stessa operazione:

$$p_i = c_i \oplus k \qquad \forall\, i \in \{0, \dots, n-1\}$$

Ciò segue direttamente dalla proprietà auto-inverso: $(c_i \oplus k) \oplus k = c_i \oplus (k \oplus k) = c_i \oplus 0 = c_i$.