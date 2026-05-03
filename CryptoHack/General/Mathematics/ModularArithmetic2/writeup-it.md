# Modular Arithmetic 2

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Usando il primo $p = 65537$, calcolare $273246787654^{65536} \bmod 65537$.

La challenge introduce i campi finiti, il Piccolo Teorema di Fermat e chiede di calcolare un'esponenziazione modulare risolvibile per sola via ragionativa, senza calcolatrice.

---

## Fondamenti teorici

### Campi vs. anelli

Quando il modulo $m$ è **primo**, gli interi modulo $m$ formano un **campo**, denotato $\mathbb{F}_p$ o $\text{GF}(p)$. Un campo è un insieme dotato di addizione e moltiplicazione in cui ogni elemento non nullo possiede sia un inverso additivo $b^+$ che un inverso moltiplicativo $b^*$:

$$a + b^+ = 0, \qquad a \cdot b^* = 1$$

Quando $m$ **non è primo**, gli interi modulo $m$ formano solo un **anello**, gli inversi moltiplicativi non esistono per tutti gli elementi. Ad esempio, in $\mathbb{Z}_6$, l'elemento 2 non ha inverso moltiplicativo poiché $\gcd(2, 6) = 2 \neq 1$.

Il campo finito $\mathbb{F}_p = \{0, 1, \dots, p-1\}$ è la struttura matematica alla base di RSA, Diffie–Hellman e della crittografia su curve ellittiche.

### Il Piccolo Teorema di Fermat

**Teorema.** Sia $p$ primo e $a$ un intero con $p \nmid a$ (ovvero $a \not\equiv 0 \pmod{p}$). Allora:

$$a^{p-1} \equiv 1 \pmod{p}$$

**Intuizione.** Consideriamo l'insieme $\{1, 2, \dots, p-1\}$, gli elementi non nulli di $\mathbb{F}_p$. Moltiplicare ogni elemento per $a$ (modulo $p$) permuta l'insieme: produce gli stessi $p-1$ valori in ordine diverso. Quindi:

$$\prod_{k=1}^{p-1} (a \cdot k) \equiv \prod_{k=1}^{p-1} k \pmod{p}$$

$$a^{p-1} \cdot (p-1)! \equiv (p-1)! \pmod{p}$$

Poiché $\gcd((p-1)!, p) = 1$, possiamo dividere entrambi i membri per $(p-1)!$:

$$a^{p-1} \equiv 1 \pmod{p} \qquad \square$$

### Conseguenza: $a^p \equiv a \pmod{p}$

Moltiplicando entrambi i membri del teorema per $a$:

$$a^p \equiv a \pmod{p}$$

Questo vale anche quando $a \equiv 0 \pmod{p}$, rendendolo un enunciato universale su tutti gli interi.

---

## Soluzione

### Verifica su esempi piccoli

Prima di affrontare il problema principale, la challenge chiede di verificare il teorema su casi semplici:

| Espressione | Valore | Spiegazione |
|:---|:---:|:---|
| $3^{17} \bmod 17$ | $3$ | $a^p \equiv a \pmod{p}$ |
| $5^{17} \bmod 17$ | $5$ | $a^p \equiv a \pmod{p}$ |
| $7^{16} \bmod 17$ | $1$ | $a^{p-1} \equiv 1 \pmod{p}$ |

### Problema principale: $273246787654^{65536} \bmod 65537$

Osserviamo che $65537$ è primo (è il noto primo di Fermat $F_4 = 2^{2^4} + 1$) e che $65536 = 65537 - 1 = p - 1$. Per il Piccolo Teorema di Fermat, per qualsiasi $a$ con $p \nmid a$:

$$a^{p-1} \equiv 1 \pmod{p}$$

Poiché $273246787654$ non è divisibile per $65537$, concludiamo immediatamente:

$$273246787654^{65536} \equiv 1 \pmod{65537}$$

**Non è necessario alcun calcolo.** Il risultato segue direttamente dal teorema.

### Script

```python
#!/usr/bin/env python3

p = 65537

print(f"3^17 mod 17      = {pow(3, 17, 17)}")
print(f"5^17 mod 17      = {pow(5, 17, 17)}")
print(f"7^16 mod 17      = {pow(7, 16, 17)}")
print(f"273246787654^65536 mod 65537 = {pow(273246787654, p - 1, p)}")
```

Nota: `pow(a, e, m)` usa l'**esponenziazione modulare veloce** integrata in Python (square-and-multiply), che calcola $a^e \bmod m$ in $O(\log e)$ moltiplicazioni. Questo è essenziale in crittografia dove gli esponenti hanno centinaia di cifre.

---

### Flag

```
1
```

---

## Conclusioni

Il Piccolo Teorema di Fermat è uno dei pilastri della crittografia a chiave pubblica. Le sue generalizzazioni sono altrettanto fondamentali:

**Teorema di Eulero**:
per qualsiasi $a$ con $\gcd(a, n) = 1$:

$$a^{\phi(n)} \equiv 1 \pmod{n}$$

dove $\phi(n)$ è la funzione di Eulero. Quando $n = p*q$ (prodotto di due primi distinti, come in RSA), $\phi(n) = (p-1)(q-1)$.

**La correttezza di RSA** si basa direttamente su questo: l'esponente di decifratura $d$ soddisfa $ed \equiv 1 \pmod{\phi(n)}$, quindi:

$$c^d = (m^e)^d = m^{ed} = m^{1 + k\phi(n)} = m \cdot (m^{\phi(n)})^k \equiv m \cdot 1^k = m \pmod{n}$$

Comprendere il Teorema di Fermat, e perché funziona, è quindi il primo passo verso la comprensione di RSA.