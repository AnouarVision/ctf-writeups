# CRT

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc crypto-10.challs.olicyber.it 30003`

---

## Descrizione

> In questa challenge ti verrà richiesto di fare uso del Teorema Cinese del Resto. Questo è un potente strumento che permette di trovare soluzioni di un sistema di equazioni modulari in cui tutti i moduli sono a due a due coprimi.

Il server fornisce un sistema di congruenze e chiede di trovare $x$ modulo il prodotto dei moduli.

---

## Background matematico

**Teorema Cinese del Resto (CRT).** Siano $n_1, n_2, \ldots, n_k$ interi positivi a due a due coprimi, ovvero $\gcd(n_i, n_j) = 1$ per ogni $i \neq j$. Dati $a_1, a_2, \ldots, a_k$ interi arbitrari, il sistema:

$$x \equiv a_1 \pmod{n_1}$$
$$x \equiv a_2 \pmod{n_2}$$
$$\vdots$$
$$x \equiv a_k \pmod{n_k}$$

ammette **un'unica soluzione** modulo $N = n_1 \cdot n_2 \cdots n_k$:

$$x \equiv \sum_{i=1}^{k} a_i \cdot M_i \cdot (M_i^{-1} \bmod n_i) \pmod{N}$$

dove $M_i = N / n_i$ è il prodotto di tutti i moduli tranne $n_i$, e $M_i^{-1} \bmod n_i$ è l'inverso modulare di $M_i$ rispetto a $n_i$ (che esiste in quanto $\gcd(M_i, n_i) = 1$).

---

## Soluzione

### Step 1 — Risoluzione del sistema

Il server fornisce il sistema:

$$x \equiv 7 \pmod{24}$$
$$x \equiv 11 \pmod{17}$$
$$x \equiv 22 \pmod{83}$$
$$x \equiv 5 \pmod{73}$$
$$x \equiv 41 \pmod{61}$$

Si verifica che i moduli $24, 17, 83, 73, 61$ sono a due a due coprimi, quindi il CRT garantisce un'unica soluzione modulo:

$$N = 24 \cdot 17 \cdot 83 \cdot 73 \cdot 61 = 150796392$$

Per ogni $i$ si calcola $M_i = N / n_i$, poi $y_i = M_i^{-1} \bmod n_i$ con l'algoritmo di Euclide esteso, e infine si somma $a_i \cdot M_i \cdot y_i$:

$$x = \left(\sum_{i=1}^{5} a_i \cdot M_i \cdot y_i\right) \bmod N = \mathbf{147960055}$$

**Risposta:** `147960055`

---

### Script

```python
from functools import reduce

residues = [7, 11, 22, 5, 41]
moduli   = [24, 17, 83, 73, 61]

N = reduce(lambda a, b: a * b, moduli)

x = 0
for a, n in zip(residues, moduli):
    M = N // n
    y = pow(M, -1, n)
    x += a * M * y

print(x % N)
```

**Output:**
```
147960055
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> Il CRT trasforma un problema su un anello grande $\mathbb{Z}/N\mathbb{Z}$ in $k$ problemi indipendenti su anelli più piccoli $\mathbb{Z}/n_i\mathbb{Z}$.

Due osservazioni fondamentali:

1. **Isomorfismo di anelli.** Il CRT afferma che, se i moduli sono a due a due coprimi, vale l'isomorfismo:

$$\mathbb{Z}/N\mathbb{Z} \;\cong\; \mathbb{Z}/n_1\mathbb{Z} \;\times\; \mathbb{Z}/n_2\mathbb{Z} \;\times\; \cdots \;\times\; \mathbb{Z}/n_k\mathbb{Z}$$

Ogni elemento di $\mathbb{Z}/N\mathbb{Z}$ corrisponde univocamente a una $k$-upla di resti. Questo è il motivo per cui la soluzione è unica modulo $N$.

2. **`pow(base, -1, n)` in Python.** Il server suggerisce di esplorare `pow` con tre argomenti: `pow(M, -1, n)` calcola l'inverso modulare di $M$ modulo $n$ usando l'algoritmo di Euclide esteso internamente, esattamente ciò che serve per il CRT. Più in generale, `pow(base, exp, mod)` calcola $\text{base}^{\text{exp}} \bmod \text{mod}$ in tempo $O(\log \text{exp})$ tramite esponenziazione veloce, che è il cuore computazionale di RSA.