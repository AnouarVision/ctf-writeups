# Encoding 1

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Un encoding è un sistema di segnali o simboli convenzionalmente designati per rappresentare un'informazione. ASCII è un codice standard che permette di rappresentare del testo attraverso sequenze di 7 bit.

Viene fornita una lista di interi. La flag si ottiene convertendo ogni numero nel corrispondente carattere ASCII.

```
[102, 108, 97, 103, 123, 117, 103, 104, 95, 78, 117, 109, 66, 51, 114, 53, 95, 52, 49, 114, 51, 52, 100, 121, 125]
```

---

## Soluzione

### Step 1 — Lo standard ASCII

ASCII (American Standard Code for Information Interchange) definisce una biiezione tra i numeri interi $\{0, \ldots, 127\}$ e un insieme di 128 simboli: lettere maiuscole e minuscole, cifre, punteggiatura e caratteri di controllo. Ogni simbolo è rappresentato da 7 bit, estesi a 8 (1 byte) per convenienza:

$$\texttt{chr}(102) = \texttt{'f'}, \quad \texttt{chr}(108) = \texttt{'l'}, \quad \texttt{chr}(97) = \texttt{'a'}, \quad \texttt{chr}(103) = \texttt{'g'}, \ldots$$

La decodifica è semplicemente l'applicazione della funzione $\texttt{chr}: \mathbb{Z} \to \text{char}$ a ogni elemento della lista.

### Step 2 — Script

```python
nums = [102, 108, 97, 103, 123, 117, 103, 104, 95, 78, 117, 109,
        66, 51, 114, 53, 95, 52, 49, 114, 51, 52, 100, 121, 125]
print(''.join(chr(n) for n in nums))
```

**Output:**
```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> Ogni informazione digitale è una sequenza di bit. ASCII è il primo livello di astrazione che trasforma quei bit in testo leggibile, tutto il resto della crittografia si costruisce sopra questa base.

Due osservazioni fondamentali:

1. **Encoding ≠ cifratura:** ASCII è una convenzione pubblica e universale, non fornisce alcuna segretezza. Chiunque conosca lo standard (cioè tutti) può decodificare immediatamente una sequenza di valori ASCII. Un encoding diventa utile in crittografia solo quando combinato con una trasformazione che dipende da una chiave segreta.

2. **Tutto è numeri:** a livello fondamentale, un testo è una sequenza di interi, un intero è una sequenza di byte, un byte è una sequenza di 8 bit. Questa catena di encoding: bit → byte → intero → carattere → testo, è il filo conduttore di tutte le challenge di questa sezione e, più in generale, di tutta la crittografia applicata. Capire come navigare tra questi livelli di rappresentazione è la prima competenza che un crittografo deve padroneggiare.