# DH Helpline

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc crypto-12.challs.olicyber.it 30005`

---

## Descrizione

> Uno dei problemi più utilizzati in crittografia asimmetrica è quello del logaritmo discreto. Uno dei protocolli più semplici che ne fanno uso è quello di Diffie-Hellman.

Il server pone quattro quesiti sul logaritmo discreto e sul protocollo di Diffie-Hellman. Rispondere correttamente a tutti restituisce la flag.

---

## Background matematico

**Gruppo moltiplicativo modulo p.** Se $p$ è primo, ogni intero in $\{1, 2, \ldots, p-1\}$ è coprimo con $p$, quindi:

$$\phi(p) = p - 1$$

L'insieme $(\mathbb{Z}/p\mathbb{Z})^* = \{1, 2, \ldots, p-1\}$ forma un **gruppo ciclico** di ordine $p-1$: esiste un generatore $g$ tale che le potenze $g^0, g^1, \ldots, g^{p-2}$ producono tutti gli elementi del gruppo.

**Logaritmo discreto.** Dato un gruppo ciclico $\langle g \rangle$ di ordine $p-1$, il logaritmo discreto di $h$ in base $g$ modulo $p$ è l'unico intero $x \in [0, p-2]$ tale che:

$$g^x \equiv h \pmod{p}$$

Scritto $x = \log_g h \pmod{p}$. A differenza del logaritmo reale, non esiste un algoritmo efficiente noto per calcolarlo quando $p$ è grande, questo è il **problema del logaritmo discreto (DLP)**, su cui si fonda la sicurezza di Diffie-Hellman.

**Protocollo Diffie-Hellman.** Alice e Bob concordano pubblicamente su un primo $p$ e un generatore $g$. Poi:

1. Alice sceglie una chiave privata $a$, calcola e pubblica $A = g^a \bmod p$
2. Bob sceglie una chiave privata $b$, calcola e pubblica $B = g^b \bmod p$
3. Entrambi calcolano il segreto condiviso:

$$S = B^a \bmod p = A^b \bmod p = g^{ab} \bmod p$$

Un avversario che osserva $p, g, A, B$ dovrebbe risolvere il DLP per ricavare $a$ o $b$, computazionalmente intrattabile per $p$ sufficientemente grande.

---

## Soluzione

### Step 1 — Coprimi con un primo

Il server chiede quanti interi positivi minori di $p$ sono coprimi con $p$:

$$\phi(p) = p - 1$$

**Risposta:** `p-1`

---

### Step 2 — Logaritmo discreto di una potenza di 2

Il server chiede $\log_2(65536) \bmod p$ con $p = 295698861441889376682620757082475676757$:

$$65536 = 2^{16}$$

Poiché $2^{16} \equiv 2^{16} \pmod{p}$ (il valore è molto minore di $p$), la risposta è banalmente:

$$x = 16$$

**Risposta:** `16`

---

### Step 3 — Logaritmo discreto di 11 in base 2 modulo 29

Il server chiede $\log_2(11) \bmod 29$, ovvero $x$ tale che $2^x \equiv 11 \pmod{29}$.

Si enumera: $2^{25} \bmod 29 = 33554432 \bmod 29$. Tramite esponenziazione modulare `pow(2, 25, 29) = 11` ✓.

**Risposta:** `25`

---

### Step 4 — Scambio Diffie-Hellman

Il server fornisce $p = 61$, $g = 2$, chiave pubblica del server $B = 18$.

Si sceglie chiave privata $b = 5$, quindi la chiave pubblica da inviare è:

$$A = g^b \bmod p = 2^5 \bmod 61 = 32$$

Una volta ricevuta la chiave pubblica del server $B = 18$, si calcola il segreto condiviso:

$$S = B^b \bmod p = 18^5 \bmod 61 = \mathbf{32}$$

**Verifica:** il server calcola $A^a \bmod p = 32^a \bmod 61$, che deve coincidere con $S = 32$ ✓.

**Risposta:** chiave pubblica `32`, segreto condiviso `32`

---

### Script

```python
p, g = 61, 2
B_server = 18
b = 5

A_pub = pow(g, b, p)
shared = pow(B_server, b, p)

print(f"Chiave pubblica: {A_pub}")
print(f"Segreto condiviso: {shared}")

print(pow(2, 25, 29))
```

**Output:**
```
Chiave pubblica: 32
Segreto condiviso: 32
11
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> La sicurezza di Diffie-Hellman non risiede nella segretezza dei parametri pubblici $p$, $g$, $A$, $B$, ma nell'impossibilità computazionale di ricavare $a$ o $b$ a partire da essi.

Tre osservazioni fondamentali:

1. **Il DLP è asimmetrico:** calcolare $g^a \bmod p$ è efficiente in $O(\log a)$ operazioni tramite esponenziazione modulare; invertire l'operazione, cioè trovare $a$ dato $g^a \bmod p$, non ha algoritmi efficienti noti per $p$ grande. Questa asimmetria è il motore di tutta la crittografia a chiave pubblica basata su gruppi.

2. **Diffie-Hellman non cifra messaggi:** DH è un protocollo di **accordo su chiave** (*key agreement*), non un cifrario. Il segreto condiviso $S = g^{ab} \bmod p$ viene poi usato come chiave per un cifrario simmetrico (es. AES). DH da solo non fornisce autenticazione: è vulnerabile all'attacco man-in-the-middle senza un meccanismo di autenticazione aggiuntivo.

3. **La scelta del gruppo è critica:** $p$ deve essere un primo sicuro (ovvero $(p-1)/2$ deve essere anch'esso primo) e $g$ deve generare un sottogruppo di ordine grande. Parametri deboli rendono il DLP risolvibile con algoritmi come Baby-step Giant-step o Index Calculus in tempo sub-esponenziale.