# Greatest Common Divisor

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Calcolare $\gcd(a, b)$ per $a = 66528,\ b = 52920$.

La challenge introduce il concetto di Massimo Comune Divisore, chiede di implementare l'Algoritmo di Euclide e di applicarlo alla coppia di interi fornita.

---

## Fondamenti teorici

### Definizione

Dati due interi positivi $a, b \in \mathbb{Z}^+$, il loro **Massimo Comune Divisore** è definito come:

$$\gcd(a, b) = \max\{d \in \mathbb{Z}^+ : d \mid a \text{ e } d \mid b\}$$

Ovvero, il più grande intero $d$ che divide sia $a$ che $b$ senza resto.

### Coprimalità

Due interi $a, b$ si dicono **coprimi** (o primi tra loro) se:

$$\gcd(a, b) = 1$$

Ciò non richiede che uno dei due sia primo; è sufficiente che non abbiano fattori comuni maggiori di 1. Alcuni casi notevoli:

- Se $a$ e $b$ sono entrambi primi e $a \neq b$, allora $\gcd(a, b) = 1$.
- Se $a$ è primo e $b < a$, allora $a \nmid b$, quindi $\gcd(a, b) = 1$.
- Se $a$ è primo e $b > a$, è possibile che $a \mid b$ (ad esempio $a = 3,\ b = 6$), quindi $\gcd(a, b) = a \neq 1$. La coprimalità non è pertanto garantita.

La coprimalità è un concetto fondamentale in RSA: l'esponente pubblico $e$ deve soddisfare $\gcd(e, \lambda(n)) = 1$, dove $\lambda(n)$ è il totiente di Carmichael del modulo.

---

## L'algoritmo di Euclide

### Il teorema fondamentale

L'algoritmo si basa sulla seguente identità, valida per ogni $a, b \in \mathbb{Z}^+$ con $b \neq 0$:

$$\gcd(a, b) = \gcd(b,\ a \bmod b)$$

**Dimostrazione:**
sia $r = a \bmod b$, così $a = qb + r$ per qualche $q \in \mathbb{Z}$. Ogni divisore comune di $a$ e $b$ divide necessariamente $r = a - qb$, e ogni divisore comune di $b$ e $r$ divide necessariamente $a = qb + r$. L'insieme dei divisori comuni di $(a, b)$ coincide quindi con l'insieme dei divisori comuni di $(b, r)$ e in particolare i rispettivi massimi coincidono.

### L'algoritmo

Applicando ripetutamente l'identità:

$$\gcd(a, b) = \gcd(b, r_1) = \gcd(r_1, r_2) = \cdots = \gcd(r_{k-1}, 0) = r_{k-1}$$

dove $r_i = r_{i-2} \bmod r_{i-1}$. La sequenza dei resti è strettamente decrescente ($b > r_1 > r_2 > \cdots \geq 0$), quindi la terminazione è garantita. Quando il resto raggiunge zero, l'ultimo resto non nullo è $\gcd(a, b)$.

---

## Soluzione

### Calcolo svolto: $\gcd(66528,\ 52920)$

L'algoritmo procede come segue, sostituendo ad ogni passo $(a, b)$ con $(b,\ a \bmod b)$:

**Passo 1.**

$$66528 = 52920 \cdot 1 + 13608 \implies \gcd(66528,\ 52920) = \gcd(52920,\ 13608)$$

**Passo 2.**

$$52920 = 13608 \cdot 3 + 12096 \quad (13608 \cdot 3 = 40824,\ 52920 - 40824 = 12096)$$

$$\implies \gcd(52920,\ 13608) = \gcd(13608,\ 12096)$$

**Passo 3.**

$$13608 = 12096 \cdot 1 + 1512 \quad (13608 - 12096 = 1512)$$

$$\implies \gcd(13608,\ 12096) = \gcd(12096,\ 1512)$$

**Passo 4.**

$$12096 = 1512 \cdot 8 + 0 \quad (1512 \cdot 8 = 12096)$$

$$\implies \gcd(12096,\ 1512) = \gcd(1512,\ 0) = 1512$$

Il resto ha raggiunto lo zero. L'ultimo resto non nullo è $\boxed{1512}$.

### Tabella

| Passo | $a$ | $b$ | $q = \lfloor a/b \rfloor$ | $r = a \bmod b$ |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 66528 | 52920 | 1 | 13608 |
| 2 | 52920 | 13608 | 3 | 12096 |
| 3 | 13608 | 12096 | 1 | 1512 |
| 4 | 12096 | 1512 | 8 | **0** |

### Script

```python
#!/usr/bin/env python3

a = 66528
b = 52920

while b > 0:
    r = a % b
    a = b
    b = r

print(f"gcd = {a}")
```

Il ciclo implementa direttamente la ricorrenza $\gcd(a, b) = \gcd(b, a \bmod b)$: ad ogni iterazione `a` assume il valore di `b` e `b` assume il valore del resto `r = a % b`. Quando `b` raggiunge zero, `a` contiene il MCD.

---

### Risposta

$$\gcd(66528,\ 52920) = 1512$$

---

## Conclusioni

In Python, l'MCD è disponibile come `math.gcd(a, b)` nella libreria standard (da Python 3.5) senza richiedere dipendenze esterne. Tuttavia, implementare l'algoritmo da zero, come richiede questa challenge, è il modo più sicuro per interiorizzare la ricorrenza $\gcd(a, b) = \gcd(b, a \bmod b)$.

Questa ricorrenza ricomparirà in contesti più avanzati: l'**Algoritmo di Euclide Esteso** la arricchisce per calcolare gli interi $x, y$ tali che $ax + by = \gcd(a, b)$ (identità di Bézout), che costituisce il fondamento per il calcolo degli inversi modulari, operazione centrale nella generazione delle chiavi RSA e nella decifratura.