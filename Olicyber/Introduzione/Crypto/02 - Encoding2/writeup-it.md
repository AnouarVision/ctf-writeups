# Encoding 2

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Convenzionalmente le sequenze di bit vengono divise in byte: sottosequenze adiacenti di 8 bit ciascuna. La codifica esadecimale permette di rappresentarli in modo molto conveniente.

Viene fornita una stringa esadecimale. La flag si ottiene convertendola nella corrispondente sequenza di byte.

```
666c61677b68337834646563696d616c5f63346e5f62335f41424144424142457d
```

---

## Soluzione

### Step 1 — Struttura della codifica esadecimale

La codifica esadecimale (Base16) rappresenta ogni byte come due cifre esadecimali. Un byte è una sequenza di 8 bit, che si spezza in due nibble da 4 bit ciascuno:

$$\underbrace{0110}_{6}\underbrace{1110}_{e} \longrightarrow \texttt{6e}$$

Ogni nibble assume un valore in $\{0,\ldots,15\}$, rappresentato dai caratteri `0-9` e `a-f`. L'encoding è quindi una biiezione:

$$\{0,\ldots,255\} \longleftrightarrow \{\texttt{00}, \texttt{01}, \ldots, \texttt{ff}\}$$

Una stringa esadecimale di $2n$ caratteri rappresenta esattamente $n$ byte.

### Step 2 — Script

```python
s = '666c61677b68337834646563696d616c5f63346e5f62335f41424144424142457d'
print(bytes.fromhex(s).decode())
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

> La codifica esadecimale non è cifratura: è una rappresentazione alternativa degli stessi bit, reversibile da chiunque senza alcuna chiave.

Due osservazioni fondamentali:

1. **Compattezza vs Base2:** rappresentare $n$ byte in binario richiede $8n$ caratteri; in esadecimale ne bastano $2n$, un fattore 4 di compressione della rappresentazione testuale. Per questo motivo hash, chiavi crittografiche, indirizzi di memoria e digest sono quasi sempre mostrati in esadecimale.

2. **`ABADBABE` è un riferimento storico:** `0xABADBABE` è una *magic number* usata da alcune implementazioni di Java per marcare i file `.class` corrotti o non validi, analoga al più noto `0xDEADBEEF` usato come valore sentinella in debugging e nei core dump. La presenza di parole leggibili in valori esadecimali è una tecnica mnemonica comune tra i programmatori di sistemi.