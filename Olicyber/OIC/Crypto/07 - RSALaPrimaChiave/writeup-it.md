# RSA: la prima chiave

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Ho ricevuto questi dati ma non so come utilizzarli. Sapresti aiutarmi?

Viene fornito un file `dati.txt` contenente una chiave pubblica RSA $(n, e)$ e una lista di 37 interi cifrati. L'obiettivo è decifrare il messaggio.

---

## Analisi dei dati

```
e = 65537
n = 11599469215086283756239000323368207328888145111801687279952858519692571454576743213591474246385542521855249880051364427742007447330667804421622274846205769
c = [5880792219702857..., 4976972096947215..., ...]  # 37 valori
```

Osservazioni immediate:
- Ci sono **37 ciphertext** ma solo **20 valori distinti**, molti caratteri si ripetono
- Il testo cifrato è prodotto con RSA in modalità *textbook*, senza padding
- Ogni ciphertext corrisponde a **un singolo carattere** ASCII

---

## Soluzione

### Step 1 — Identificazione della vulnerabilità: codebook attack

In RSA, la cifratura di un messaggio $m$ con chiave pubblica $(n, e)$ è:

$$c = m^e \bmod n$$

Se il messaggio è un singolo carattere ASCII, allora $m \in \{32, 33, \ldots, 126\}$, solo 95 valori possibili. Lo spazio dei plaintext è **finito e piccolo**: un attaccante può precalcolare tutti i possibili ciphertext e costruire un dizionario inverso:

$$\mathcal{D} = \left\{ m^e \bmod n \;\mapsto\; m \;\middle|\; m \in [32, 126] \right\}$$

Ogni ciphertext $c_i$ viene poi cercato in $\mathcal{D}$ per ottenere il carattere corrispondente. Questo è un **attacco a codebook**: con 95 operazioni di esponenziazione modulare si rompe l'intero sistema.

La presenza di soli 20 valori distinti su 37 ciphertext conferma l'ipotesi, i caratteri più frequenti (come `_`, `e`, `3`) compaiono più volte, come atteso in un testo naturale.

### Step 2 — Exploit

```python
import ast

with open('dati.txt') as f:
    content = f.read()

lines = content.strip().split('\n')
e = int(lines[0].split('=')[1].strip())
n = int(lines[1].split('=')[1].strip())
c = ast.literal_eval(lines[2].split('=', 1)[1].strip())

lookup = {pow(m, e, n): chr(m) for m in range(32, 127)}

flag = ''.join(lookup.get(ci, '?') for ci in c)
print(flag)
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

> RSA senza padding su messaggi brevi è completamente insicuro: la struttura deterministica della cifratura trasforma ogni plaintext prevedibile in un ciphertext predicibile.

Tre osservazioni fondamentali:

1. **RSA è deterministico:** a parità di chiave, lo stesso messaggio produce sempre lo stesso ciphertext. Questo significa che due caratteri uguali producono ciphertext identici, come osservato nei 20 valori distinti su 37. Questa proprietà rende RSA *textbook* vulnerabile ad analisi della frequenza, esattamente come il cifrario di Cesare, ma nel dominio modulare.

2. **Il padding è obbligatorio:** lo standard PKCS#1 v1.5 e il più moderno OAEP (Optimal Asymmetric Encryption Padding) introducono casualità nel processo di cifratura, garantendo che lo stesso plaintext produca ciphertext diversi ad ogni esecuzione. Senza padding, RSA non è semanticamente sicuro, non soddisfa nemmeno la proprietà IND-CPA (indistinguibilità sotto attacco a plaintext scelto).

3. **Non si cifra mai un carattere alla volta:** RSA è progettato per cifrare chiavi simmetriche o hash, non dati arbitrari direttamente. Il pattern corretto è **cifratura ibrida**: si genera una chiave AES casuale, la si cifra con RSA-OAEP, e si usa AES per cifrare il messaggio. Questo combina la sicurezza della crittografia asimmetrica con l'efficienza e la sicurezza semantica di quella simmetrica.