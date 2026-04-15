# Congruenze Modulari

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc crypto-08.challs.olicyber.it 30001`

---

## Descrizione

> Come ormai potrai aver intuito, la crittografia fa un ampio uso di strumenti matematici. Le branche della matematica che hanno a che fare con il discreto si rivelano particolarmente utili.

Il server pone due quesiti sulle congruenze modulari. Rispondere correttamente a entrambi restituisce la flag.

---

## Background matematico

**Congruenza modulare.** Dati $a, b, n \in \mathbb{Z}$ con $n > 0$, si dice che $a$ è **congruente** a $b$ modulo $n$ se $n$ divide la loro differenza:

$$a \equiv b \pmod{n} \iff n \mid (a - b)$$

Intuitivamente, $a$ e $b$ lasciano lo stesso resto quando divisi per $n$. L'operazione $a \bmod n$ restituisce l'unico intero $r \in [0, n)$ tale che $a \equiv r \pmod{n}$.

**Struttura algebrica.** L'insieme delle classi di resto $\mathbb{Z}/n\mathbb{Z} = \{[0],[1],\ldots,[n-1]\}$ forma un **gruppo abeliano** rispetto alla somma modulare, ovvero soddisfa:

- **Chiusura**: $[a] + [b] = [a+b] \in \mathbb{Z}/n\mathbb{Z}$
- **Associatività**: $([a]+[b])+[c] = [a]+([b]+[c])$
- **Elemento neutro**: $[a] + [0] = [a]$
- **Inverso**: $\forall [a]\ \exists [-a] : [a]+[-a]=[0]$
- **Commutatività** (abeliano): $[a]+[b]=[b]+[a]$

Aggiungendo il prodotto modulare, $(\mathbb{Z}/n\mathbb{Z}, +, \cdot)$ diventa un **anello quoziente**, la struttura su cui poggiano RSA, Diffie-Hellman e la crittografia su curve ellittiche.

---

## Soluzione

### Step 1 — Riduzione modolare di un intero negativo

Il server chiede:

```
-45 % 73 = ?
```

$-45 \bmod 73$ è semplicemente il resto della divisione tra $-45$ e $73$. Poiché $-45$ è negativo ma $|-45| < 73$, basta sommare il modulo una volta:

$$-45 + 73 = \mathbf{28}$$

**Risposta:** `28`

---

### Step 2 — Verifica di congruenza tra due interi

Il server chiede:

```
323 == 615 (mod 100)? (si/no)
```

Si calcola il resto di ciascuno:

$$323 \bmod 100 = 23, \qquad 615 \bmod 100 = 15$$

Poiché $23 \neq 15$, si ha $323 \not\equiv 615 \pmod{100}$.

**Risposta:** `no`

---

## Flag

```
flag{...}
```

---

## Conclusioni

> L'aritmetica modulare è l'aritmetica dell'orologio: superato il modulo, si riparte da zero.

Due note importanti:

1. **Segno del resto in Python vs C:** in Python `%` restituisce sempre un risultato in $[0, n)$ per definizione. In C invece `(-45) % 73 = -45`, una fonte classica di bug crittografici.

2. **Perché $\mathbb{Z}/n\mathbb{Z}$ è fondamentale in crittografia:** lavorare in un anello quoziente consente di mantenere i numeri piccoli (sempre in $[0,n)$) pur eseguendo operazioni arbitrariamente complesse e di formulare problemi computazionalmente difficili, come il logaritmo discreto, che sono alla base della sicurezza dei moderni protocolli crittografici.