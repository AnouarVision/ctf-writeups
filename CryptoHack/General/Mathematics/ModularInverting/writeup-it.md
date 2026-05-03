# Modular Inverting

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Trovare l'elemento inverso $d = 3^{-1}$ tale che $3 \cdot d \equiv 1 \pmod{13}$.

---

## Fondamenti teorici

### Inverso moltiplicativo in $\mathbb{F}_p$

Per ogni elemento non nullo $g$ nel campo finito $\mathbb{F}_p$, esiste un unico intero $d \in \{1, \dots, p-1\}$ tale che:

$$g \cdot d \equiv 1 \pmod{p}$$

Questo $d$ è detto **inverso moltiplicativo** di $g$ modulo $p$, scritto $g^{-1}$ o $d = g^{-1} \bmod p$.

L'esempio fornito nella challenge conferma la definizione:

$$7 \cdot 8 = 56 = 5 \cdot 11 + 1 \implies 7 \cdot 8 \equiv 1 \pmod{11}$$

Quindi $7^{-1} \equiv 8 \pmod{11}$.

### Metodo 1 — Piccolo Teorema di Fermat

La challenge suggerisce di usare il Piccolo Teorema di Fermat, che afferma che per qualsiasi primo $p$ e $a \not\equiv 0 \pmod{p}$:

$$a^{p-1} \equiv 1 \pmod{p}$$

Possiamo riscrivere il membro sinistro fattorizzando una $a$:

$$a \cdot a^{p-2} \equiv 1 \pmod{p}$$

Confrontando con la definizione $a \cdot d \equiv 1 \pmod{p}$, identifichiamo immediatamente:

$$d = a^{-1} \equiv a^{p-2} \pmod{p}$$

L'inverso moltiplicativo di $a$ modulo un primo $p$ è semplicemente $a$ elevato alla potenza $p-2$, calcolato modulo $p$. Questo richiede una sola esponenziazione modulare, operazione che Python esegue efficientemente con `pow(a, p-2, p)`.

### Metodo 2 — Algoritmo di Euclide Esteso

L'inverso può essere calcolato anche come coefficiente di Bézout $x$ in:

$$a \cdot x + p \cdot y = \gcd(a, p) = 1 \implies a \cdot x \equiv 1 \pmod{p}$$

Questo è il metodo più generale (funziona anche quando $p$ non è primo, purché $\gcd(a, p) = 1$) ed è quello usato internamente da `pow(a, -1, p)` di Python dalla versione 3.8.

### Confronto tra i due metodi

| Metodo | Applicabile quando | Complessità |
|:---|:---|:---|
| Fermat: $a^{p-2} \bmod p$ | $p$ primo | $O(\log p)$ moltiplicazioni |
| Euclide Esteso | $\gcd(a, m) = 1$ (qualsiasi $m$) | $O(\log \min(a,m))$ divisioni |

Entrambi hanno la stessa complessità asintotica. Nella pratica crittografica, l'Euclide Esteso è preferito per generalità, mentre il metodo di Fermat è utile quando $p$ è noto essere primo e si sta già calcolando un'esponenziazione modulare.

---

## Soluzione

### Calcolo svolto

Cerchiamo $d$ tale che $3 \cdot d \equiv 1 \pmod{13}$.

**Tramite il Piccolo Teorema di Fermat:**

$$d = 3^{13-2} \bmod 13 = 3^{11} \bmod 13$$

Calcolo passo per passo con lo square-and-multiply:

$$3^1 = 3$$
$$3^2 = 9$$
$$3^4 = 9^2 = 81 \equiv 3 \pmod{13}$$
$$3^8 \equiv 3^2 = 9 \pmod{13}$$
$$3^{11} = 3^8 \cdot 3^2 \cdot 3^1 \equiv 9 \cdot 9 \cdot 3 = 243 \equiv 243 - 18 \cdot 13 = 243 - 234 = 9 \pmod{13}$$

**Verifica:**

$$3 \cdot 9 = 27 = 2 \cdot 13 + 1 \implies 3 \cdot 9 \equiv 1 \pmod{13} \checkmark$$

### Script

```python
#!/usr/bin/env python3

p = 13
a = 3

# Metodo 1: Piccolo Teorema di Fermat  →  a^-1 = a^(p-2) mod p
d_fermat = pow(a, p - 2, p)

# Metodo 2: pow built-in (Python 3.8+)
d_builtin = pow(a, -1, p)

print(f"Inverso di {a} mod {p} = {d_fermat}")
print(f"Verifica: {a} * {d_fermat} mod {p} = {(a * d_fermat) % p}")
```

---

### Flag

```
9
```

---

## Conclusioni

L'inverso moltiplicativo è un'operazione fondamentale in crittografia. Le sue due principali applicazioni in questo corso sono:

**Generazione delle chiavi RSA**:
dato l'esponente pubblico $e$ e $\phi(n) = (p-1)(q-1)$, l'esponente privato è $d = e^{-1} \bmod \phi(n)$, calcolato tramite l'Algoritmo di Euclide Esteso. La correttezza della decifratura RSA dipende interamente dall'esistenza e unicità di questo inverso, garantite perché $\gcd(e, \phi(n)) = 1$ per costruzione.

**Divisione modulare**:
la divisione per $a$ in $\mathbb{F}_p$ è definita come moltiplicazione per $a^{-1}$: non esiste un'operazione di "divisione" nell'aritmetica modulare, solo moltiplicazione per l'inverso.