# Inverso Modulare

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc crypto-09.challs.olicyber.it 30002`

---

## Descrizione

> L'aritmetica dei numeri interi modulo n è in molti punti differente da quella usuale. Una distinzione cruciale è cosa significhi calcolare l'inverso di un certo intero modulo n.

Il server pone tre quesiti sugli inversi modulari e sull'algoritmo di Euclide esteso. Rispondere correttamente a tutti restituisce la flag.

---

## Background matematico

**MCD e identità di Bézout.** Dati $a, b \in \mathbb{Z}$, il loro massimo comun divisore $d = \gcd(a,b)$ soddisfa l'**identità di Bézout**: esistono $x, y \in \mathbb{Z}$ tali che:

$$x \cdot a + y \cdot b = \gcd(a, b)$$

I coefficienti $x, y$ si calcolano con l'**algoritmo di Euclide esteso**, che percorre a ritroso i passi della divisione euclidea.

**Inverso modulare.** L'inverso di $a$ modulo $n$ è l'intero $a^{-1} \in \mathbb{Z}/n\mathbb{Z}$ tale che:

$$a \cdot a^{-1} \equiv 1 \pmod{n}$$

Dall'identità di Bézout con $b = n$:

$$x \cdot a + y \cdot n = \gcd(a, n)$$

Riducendo modulo $n$ si ottiene $x \cdot a \equiv \gcd(a,n) \pmod{n}$. Quindi $a^{-1}$ esiste se e solo se $\gcd(a,n) = 1$, ovvero $a$ e $n$ sono **coprimi**. In tal caso $a^{-1} = x \bmod n$.

**Proprietà di divisibilità della congruenza.** Se $a \equiv b \pmod{n}$ e $d \mid n$, allora:

$$a \equiv b \pmod{d}$$

Questo perché $n \mid (a-b)$ e $d \mid n$ implicano $d \mid (a-b)$.

---

## Soluzione

### Step 1 — Coefficienti di Bézout

Il server chiede:

```
a = 54, b = 177, trova x,y tali che x*a + y*b == GCD(a,b)
```

Si applica l'algoritmo di Euclide esteso:

$$177 = 3 \cdot 54 + 15$$
$$54 = 3 \cdot 15 + 9$$
$$15 = 1 \cdot 9 + 6$$
$$9 = 1 \cdot 6 + 3$$
$$6 = 2 \cdot 3 + 0$$

Quindi $\gcd(54, 177) = 3$. Risalendo la catena:

$$3 = 9 - 1 \cdot 6 = 9 - 1 \cdot (15 - 9) = 2 \cdot 9 - 15$$
$$= 2(54 - 3 \cdot 15) - 15 = 2 \cdot 54 - 7 \cdot 15$$
$$= 2 \cdot 54 - 7(177 - 3 \cdot 54) = 23 \cdot 54 + (-7) \cdot 177$$

$$\boxed{x = 23, \quad y = -7}$$

**Verifica:** $23 \cdot 54 + (-7) \cdot 177 = 1242 - 1239 = 3 = \gcd(54,177)$ ✓

**Risposta:** `x = 23`, `y = -7`

---

### Step 2 — Invertibilità modulare

Il server chiede:

```
54 è invertibile mod 177? (si/no)
```

Dal passo precedente si sa che $\gcd(54, 177) = 3 \neq 1$. Poiché $54$ e $177$ non sono coprimi, $54$ **non è invertibile** modulo $177$.

**Risposta:** `no`

---

### Step 3 — Calcolo dell'inverso modulare

Il server chiede:

```
Qual è l'inverso di 55 modulo 83?
```

Si verifica che $\gcd(55, 83) = 1$ (83 è primo, quindi ogni intero non multiplo di 83 è invertibile). Si applica l'algoritmo di Euclide esteso:

$$83 = 1 \cdot 55 + 28$$
$$55 = 1 \cdot 28 + 27$$
$$28 = 1 \cdot 27 + 1$$
$$27 = 27 \cdot 1 + 0$$

Risalendo:

$$1 = 28 - 1 \cdot 27 = 28 - (55 - 28) = 2 \cdot 28 - 55$$
$$= 2(83 - 55) - 55 = 2 \cdot 83 - 3 \cdot 55$$

Quindi $x = -3$, ovvero:

$$55^{-1} \equiv -3 \equiv 83 - 3 = \mathbf{80} \pmod{83}$$

**Verifica:** $55 \cdot 80 = 4400 = 53 \cdot 83 + 1 \equiv 1 \pmod{83}$ ✓

**Risposta:** `80`

---

### Script

```python
from math import gcd

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = extended_gcd(b, a % b)
    return d, y, x - (a // b) * y

d, x, y = extended_gcd(54, 177)
print(f"x={x}, y={y}, gcd={d}")

print("si" if gcd(54, 177) == 1 else "no")

_, inv, _ = extended_gcd(55, 83)
print(inv % 83)
```

**Output:**
```
x=23, y=-7, gcd=3
no
80
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> L'inverso modulare esiste se e solo se $\gcd(a,n)=1$: la coprimalità è la condizione necessaria e sufficiente.

Tre concetti fondamentali emersi da questa challenge:

1. **L'algoritmo di Euclide esteso** non si limita a calcolare il $\gcd$: fornisce anche i coefficienti di Bézout, che sono esattamente i coefficienti che servono per calcolare l'inverso modulare. È la base computazionale di RSA, dove l'esponente privato $d$ è l'inverso di $e$ modulo $\phi(n)$.

2. **Non tutti gli interi sono invertibili modulo $n$:** in $\mathbb{Z}/n\mathbb{Z}$ gli elementi invertibili formano il **gruppo moltiplicativo** $(\mathbb{Z}/n\mathbb{Z})^*$, di ordine $\phi(n)$ (funzione di Eulero). Se $n$ è primo, ogni elemento non nullo è invertibile e $\mathbb{Z}/n\mathbb{Z}$ è un **campo**.

3. **La congruenza si preserva per divisori del modulo:** se $a \equiv b \pmod{n}$ e $d \mid n$ allora $a \equiv b \pmod{d}$. Questa proprietà è usata continuamente nelle dimostrazioni crittografiche per "ridurre" il modulo e semplificare i calcoli.