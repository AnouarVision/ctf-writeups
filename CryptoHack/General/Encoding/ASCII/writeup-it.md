# ASCII

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Convertire il seguente array di interi nei corrispondenti caratteri ASCII per ottenere la flag.
> `[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`

In questa challenge non viene fornito alcuno script. Viene fornita direttamente una lista di interi e si chiede di decodificarla manualmente o programmaticamente tramite la funzione `chr()` di Python.

---

## Lo standard ASCII

**ASCII** (*American Standard Code for Information Interchange*) è uno standard di codifica a 7 bit che mappa gli interi $\{0, 1, \dots, 127\}$ su un insieme fisso di caratteri. Formalmente, definisce una biiezione:

$$\phi : \{0, 1, \dots, 127\} \to \Sigma$$

dove $\Sigma$ è l'insieme dei caratteri ASCII, che comprende caratteri di controllo (0–31), caratteri stampabili (32–126) e il carattere di cancellazione (127).

### Struttura della codifica

I 128 code point sono organizzati come segue:

| Intervallo | Contenuto |
|:---:|:---|
| $0 - 31$ | Caratteri di controllo non stampabili (a capo, tabulazione, ecc.) |
| $32 - 47$ | Spazio e simboli di punteggiatura |
| $48 - 57$ | Cifre decimali `0`–`9` |
| $65 - 90$ | Lettere latine maiuscole `A`–`Z` |
| $97 - 122$ | Lettere latine minuscole `a`–`z` |
| $123 - 126$ | Punteggiatura: `{`, `\|`, `}`, `~` |

Vale la pena ricordare due relazioni aritmetiche notevoli:

$$\phi^{-1}(\texttt{A}) = 65, \quad \phi^{-1}(\texttt{a}) = 97 \implies \phi^{-1}(\texttt{a}) - \phi^{-1}(\texttt{A}) = 32$$

La differenza tra una lettera minuscola e la corrispondente maiuscola è sempre esattamente 32, il che equivale a invertire il bit 5 della rappresentazione binaria.

---

## Soluzione

### La mappa di decodifica

Dato il vettore di interi $\mathbf{v} = (v_0, v_1, \dots, v_{n-1})$, la flag si ottiene applicando la funzione di decodifica ASCII $\phi$ elemento per elemento e concatenando i risultati:

$$\text{flag} = \phi(v_0) \,\|\, \phi(v_1) \,\|\, \cdots \,\|\, \phi(v_{n-1})$$

In Python, $\phi$ è implementata dalla funzione built-in `chr()`, mentre il suo inverso $\phi^{-1}$ è implementato da `ord()`.

### Script

```python
#!/usr/bin/env python3

ascii_codes = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

print("".join(chr(code) for code in ascii_codes))
```

La list comprehension itera su ogni intero `code` in `ascii_codes`, applica `chr()` per ottenere il carattere corrispondente, e `"".join()` concatena tutti i caratteri in un'unica stringa.

### Tabella di decodifica completa

| $i$ | $v_i$ | $\phi(v_i)$ |
|:---:|:---:|:---:|
| 0 | 99 | `c` |
| 1 | 114 | `r` |
| 2 | 121 | `y` |
| 3 | 112 | `p` |
| 4 | 116 | `t` |
| 5 | 111 | `o` |
| 6 | 123 | `{` |
| 7 | 65 | `.` |
| 8 | 83 | `.` |
| 9 | 67 | `.` |
| 10 | 73 | `.` |
| 11 | 73 | `.` |
| 12 | 95 | `.` |
| 13 | 112 | `.` |
| 14 | 114 | `.` |
| 15 | 49 | `.` |
| 16 | 110 | `.` |
| 17 | 116 | `.` |
| 18 | 52 | `.` |
| 19 | 98 | `.` |
| 20 | 108 | `.` |
| 21 | 51 | `.` |
| 22 | 125 | `}` |

---

### Flag

```
crypto{...}
```