# Extended GCD

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Usando i due primi $p = 26513,\ q = 32321$, trovare gli interi $x, y$ tali che $p \cdot x + q \cdot y = \gcd(p, q)$. Inviare come flag il minore tra $x$ e $y$.

---

## Fondamenti teorici

### Identità di Bézout

Per qualsiasi coppia di interi $a, b$ con $\gcd(a, b) = d$, esistono interi $x, y \in \mathbb{Z}$ detti **coefficienti di Bézout**, tali che:

$$a \cdot x + b \cdot y = d$$

Questa è nota come **Identità di Bézout**. I coefficienti $x$ e $y$ non sono unici: se $(x_0, y_0)$ è una soluzione, allora per qualsiasi $k \in \mathbb{Z}$:

$$\left(x_0 + k \cdot \frac{b}{d},\quad y_0 - k \cdot \frac{a}{d}\right)$$

è anch'essa una soluzione. L'Algoritmo di Euclide Esteso calcola efficientemente una particolare coppia $(x, y)$.

### GCD atteso di due primi distinti

Poiché $p = 26513$ e $q = 32321$ sono entrambi primi e $p \neq q$, nessuno dei due divide l'altro. L'unico divisore comune positivo è quindi 1:

$$\gcd(p, q) = 1$$

In questo caso l'Identità di Bézout diventa:

$$p \cdot x + q \cdot y = 1$$

Questa è esattamente l'equazione la cui soluzione fornisce l'**inverso modulare** di $p$ modulo $q$ (e di $q$ modulo $p$), un calcolo importante nella generazione delle chiavi RSA.

### L'Algoritmo di Euclide Esteso

L'Algoritmo di Euclide standard calcola $\gcd(a, b)$ tramite la ricorrenza $\gcd(a, b) = \gcd(b, a \bmod b)$. La versione **Estesa** lo arricchisce tenendo traccia dei coefficienti di Bézout ad ogni passo.

Ad ogni iterazione vengono mantenute due sequenze ausiliarie $\{x_i\}$ e $\{y_i\}$ tali che l'invariante:

$$r_i = a \cdot x_i + b \cdot y_i$$

sia valido lungo tutta l'esecuzione, dove $r_i$ è il resto corrente. Inizializzando con:

$$r_0 = a,\quad x_0 = 1,\quad y_0 = 0$$
$$r_1 = b,\quad x_1 = 0,\quad y_1 = 1$$

e applicando la ricorrenza con quoziente $q_i = \lfloor r_{i-1} / r_i \rfloor$:

$$r_{i+1} = r_{i-1} - q_i \cdot r_i$$
$$u_{i+1} = u_{i-1} - q_i \cdot x_i$$
$$v_{i+1} = v_{i-1} - q_i \cdot y_i$$

Quando $r_{i+1} = 0$, l'algoritmo termina: $r_i = \gcd(a, b)$ e $(x_i, y_i)$ sono i coefficienti di Bézout.

La formulazione ricorsiva è equivalente e più concisa: nel caso base $b = 0$ si restituisce $(a, 1, 0)$; altrimenti si ricorre su $(b, a \bmod b)$ e si effettua la back-substitution.

---

## Soluzione

### Script

```python
#!/usr/bin/env python3

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

p = 26513
q = 32321

gcd, x, y = extended_gcd(p, q)

print(f"gcd({p}, {q}) = {gcd}")
print(f"x = {x}")
print(f"y = {y}")
print(f"Verifica: {p}*{x} + {q}*{y} = {p*x + q*y}")
print(f"Flag: crypto{{{min(x, y)}}}")
```

### Back-substitution ricorsiva

La ricorsione si svolge come segue. Ad ogni chiamata ricorsiva, l'algoritmo risolve il sotto-problema per $(b, a \bmod b)$ e ottiene i coefficienti $(x_1, y_1)$ tali che:

$$b \cdot x_1 + (a \bmod b) \cdot y_1 = \gcd$$

Poiché $a \bmod b = a - \lfloor a/b \rfloor \cdot b$, sostituendo:

$$b \cdot x_1 + (a - \lfloor a/b \rfloor \cdot b) \cdot y_1 = \gcd$$

$$a \cdot y_1 + b \cdot (x_1 - \lfloor a/b \rfloor \cdot y_1) = \gcd$$

Pertanto:

$$x = y_1, \qquad y = x_1 - \lfloor a/b \rfloor \cdot y_1$$

### Risultato

| Grandezza | Valore |
|:---|:---:|
| $\gcd(p, q)$ | $1$ |
| $x$ | $10245$ |
| $y$ | $-8404$ |
| Verifica: $p \cdot x + q \cdot y$ | $26513 \cdot 10245 + 32321 \cdot (-8404) = 1$ ✓ |

Il minore tra i due coefficienti è $y = -8404$.

---

### Flag

```
-8404
```

---

## Conclusioni

L'Algoritmo di Euclide Esteso è uno degli algoritmi più importanti nella teoria computazionale dei numeri e nella crittografia applicata. La sua principale applicazione è il calcolo degli **inversi modulari**: dati $e$ e $\phi(n)$ con $\gcd(e, \phi(n)) = 1$, l'algoritmo trova $d$ tale che $e \cdot d \equiv 1 \pmod{\phi(n)}$, ovvero $e \cdot d + \phi(n) \cdot k = 1$ per qualche $k \in \mathbb{Z}$. Questo $d$ è l'esponente privato RSA.

In Python, l'inverso modulare può essere calcolato direttamente con `pow(e, -1, phi_n)` (da Python 3.8) oppure tramite `Crypto.Util.number.inverse()` di PyCryptodome, entrambi utilizzano internamente l'Algoritmo di Euclide Esteso.