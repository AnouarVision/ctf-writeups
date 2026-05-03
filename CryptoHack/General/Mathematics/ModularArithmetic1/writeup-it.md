# Modular Arithmetic 1

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Calcolare i seguenti valori e inviare come flag il minore dei due risultati:
> $$11 \equiv x \pmod{6}$$
> $$8146798528947 \equiv y \pmod{17}$$

---

## Fondamenti teorici

### Congruenza e operazione modulo

Dati due interi $a, b$ e un intero positivo $m$, si dice che $a$ è **congruente a $b$ modulo $m$**, scritto:

$$a \equiv b \pmod{m}$$

se e solo se $m \mid (a - b)$, ovvero $m$ divide esattamente $a - b$. Equivalentemente, $b$ è il resto della divisione euclidea di $a$ per $m$:

$$a = q \cdot m + b, \qquad 0 \leq b < m, \quad q = \lfloor a / m \rfloor$$

L'insieme di tutti gli interi congruenti a $b$ modulo $m$ forma una **classe di equivalenza**:

$$[b]_m = \{\dots,\ b - 2m,\ b - m,\ b,\ b + m,\ b + 2m,\ \dots\}$$

L'insieme di tutte le classi $\{[0]_m, [1]_m, \dots, [m-1]_m\}$ forma l'**anello degli interi modulo $m$**, denotato $\mathbb{Z}/m\mathbb{Z}$ o $\mathbb{Z}_m$.

### L'analogia dell'orologio

Il modello più intuitivo è un orologio a 12 ore. Dopo le 12, il contatore riparte da 0: $13 \equiv 1 \pmod{12}$, $15 \equiv 3 \pmod{12}$. L'esempio del testo della challenge — $4 + 9 = 1$ — ha perfettamente senso sul quadrante di un orologio: partendo dalle 4 e aggiungendo 9 ore si arriva all'1.

### Proprietà chiave: indipendenza dalla dimensione

L'operazione modulo riduce qualsiasi intero, per quanto grande, a un valore in $\{0, 1, \dots, m-1\}$. È per questo che i sistemi crittografici possono lavorare con numeri enormi (centinaia di cifre) mantenendo tutti i risultati intermedi limitati: ogni operazione viene eseguita modulo un $m$ fisso.

---

## Soluzione

### Script

```python
#!/usr/bin/env python3

x = 11 % 6
y = 8146798528947 % 17

print(f"x = 11 mod 6 = {x}")
print(f"y = 8146798528947 mod 17 = {y}")
print(f"flag = {min(x, y)}")
```

### Calcolo svolto

**Prima riduzione: $11 \bmod 6$**

$$11 = 1 \cdot 6 + 5 \implies 11 \equiv 5 \pmod{6}$$

**Seconda riduzione: $8146798528947 \bmod 17$**

L'operatore `%` di Python gestisce nativamente interi di grandezza arbitraria, quindi non è necessaria alcuna divisione lunga manuale. Il risultato è:

$$8146798528947 = 479223442879 \cdot 17 + 4 \implies 8146798528947 \equiv 4 \pmod{17}$$

### Risultato

| Espressione | Valore |
|:---|:---:|
| $11 \bmod 6$ | $5$ |
| $8146798528947 \bmod 17$ | $4$ |
| $\min(x, y)$ | $4$ |

---

### Flag

```
4
```

---

## Conclusioni

L'aritmetica modulare è il fondamento matematico su cui è costruita praticamente ogni primitiva crittografica. In RSA, la cifratura è l'esponenziazione modulare $c = m^e \bmod n$; in Diffie–Hellman, il segreto condiviso deriva da $g^{ab} \bmod p$; nella crittografia su curve ellittiche, tutte le operazioni sui punti vengono eseguite modulo un primo $p$.

L'operatore `%` in Python calcola il resto non negativo per moduli positivi, che è la convenzione standard in crittografia. Per interi negativi, il comportamento di Python differisce da alcuni altri linguaggi (es. C), restituendo sempre un risultato in $\{0, \dots, m-1\}$.