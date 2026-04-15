# RSA Helpline

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc crypto-11.challs.olicyber.it 30004`

---

## Descrizione

> Moduli, potenze, inversi... Che confusione! RSA non è affatto una passeggiata.

Il server guida passo per passo attraverso la costruzione del cifrario RSA: dalla scelta dei primi alla cifratura e decifratura di un messaggio. Rispondere correttamente a ogni quesito restituisce la flag.

---

## Background matematico

**Schema RSA.** RSA si fonda su tre risultati: la difficoltà computazionale della fattorizzazione intera, la funzione di Eulero e il Teorema di Eulero.

**Funzione di Eulero.** $\phi(n)$ conta gli interi in $[1, n-1]$ coprimi con $n$. Per $n = p*q$ con $p, q$ primi distinti:

$$\phi(n) = (p-1)(q-1)$$

**Teorema di Eulero.** Per ogni $a$ coprimo con $n$:

$$a^{\phi(n)} \equiv 1 \pmod{n}$$

**Generazione delle chiavi RSA.**
1. Si scelgono due primi $p, q$ e si calcola $n = p*q$
2. Si sceglie $e$ con $\gcd(e, \phi(n)) = 1$ → chiave pubblica $(n, e)$
3. Si calcola $d = e^{-1} \bmod \phi(n)$ → chiave privata $d$

**Cifratura e decifratura.**

$$c = m^e \bmod n \qquad m = c^d \bmod n$$

La correttezza segue dal Teorema di Eulero: poiché $ed \equiv 1 \pmod{\phi(n)}$, esiste $k \in \mathbb{Z}$ tale che $ed = 1 + k\phi(n)$, quindi:

$$c^d = (m^e)^d = m^{ed} = m^{1+k\phi(n)} = m \cdot (m^{\phi(n)})^k \equiv m \cdot 1^k = m \pmod{n}$$

---

## Soluzione

### Step 1 — Calcolo del modulo

Il server fornisce $p = 11$, $q = 19$:

$$n = p \cdot q = 11 \cdot 19 = \mathbf{209}$$

---

### Step 2 — Funzione di Eulero

$$\phi(n) = (p-1)(q-1) = 10 \cdot 18 = \mathbf{180}$$

---

### Step 3 — Cifratura

Si sceglie $m = 42$, $e = 7$. Si verifica $\gcd(7, 180) = 1$ ✓.

$$c = m^e \bmod n = 42^7 \bmod 209$$

Tramite esponenziazione modulare (`pow(42, 7, 209)`):

$$c = \mathbf{158}$$

---

### Step 4 — Calcolo dell'esponente privato

Si calcola $d = e^{-1} \bmod \phi(n) = 7^{-1} \bmod 180$ con l'algoritmo di Euclide esteso:

$$180 = 25 \cdot 7 + 5$$
$$7 = 1 \cdot 5 + 2$$
$$5 = 2 \cdot 2 + 1$$

Risalendo: $1 = 5 - 2 \cdot 2 = 5 - 2(7-5) = 3 \cdot 5 - 2 \cdot 7 = 3(180 - 25 \cdot 7) - 2 \cdot 7 = 3 \cdot 180 - 77 \cdot 7$

$$d = -77 \bmod 180 = \mathbf{103}$$

**Verifica:** $7 \cdot 103 = 721 = 4 \cdot 180 + 1 \equiv 1 \pmod{180}$ ✓

---

### Step 5 — Decifratura

$$m = c^d \bmod n = 158^{103} \bmod 209 = \mathbf{42}$$

**Verifica:** `pow(158, 103, 209) == 42` ✓

---

### Script

```python
p, q = 11, 19
n = p * q
phi = (p - 1) * (q - 1)
m = 42
e = 7

c = pow(m, e, n)
d = pow(e, -1, phi)
m_dec = pow(c, d, n)

print(f"n={n}, phi={phi}, c={c}, d={d}, m_dec={m_dec}")
```

**Output:**
```
n=209, phi=180, c=158, d=103, m_dec=42
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> La sicurezza di RSA non dipende dall'algoritmo in sé, ma dall'impossibilità computazionale di fattorizzare $n$ per ricavare $\phi(n)$ e quindi $d$.

Tre osservazioni fondamentali emerse dal tutorial:

1. **`pow(m, e, n)` è obbligatorio:** calcolare `m**e % n` in Python prima eleva alla potenza (producendo un numero con milioni di cifre) e poi riduce modulo $n$. L'esponenziazione modulare invece mantiene i risultati intermedi sempre in $[0, n)$, riducendo la complessità da $O(e)$ moltiplicazioni a $O(\log e)$ tramite il metodo *square-and-multiply*.

2. **$\gcd(e, \phi(n)) = 1$ è indispensabile:** senza questa condizione $e$ non sarebbe invertibile modulo $\phi(n)$, l'esponente privato $d$ non esisterebbe e la decifratura sarebbe impossibile. La scelta più comune in pratica è $e = 65537 = 2^{16}+1$, primo di Fermat con pochi bit a 1 per rendere l'esponenziazione veloce.

3. **La fattorizzazione di $n$ è il segreto vero:** conoscere $p$ e $q$ permette di calcolare $\phi(n) = (p-1)(q-1)$ e quindi $d$. Per questo $n$ è pubblico ma $p, q$ devono restare privati e devono essere abbastanza grandi (oggi almeno 2048 bit ciascuno) da rendere la fattorizzazione computazionalmente intrattabile.