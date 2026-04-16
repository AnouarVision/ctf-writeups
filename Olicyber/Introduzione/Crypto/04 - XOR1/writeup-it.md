# Xor 1

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Un modo molto semplice ed efficace per offuscare un messaggio è utilizzare lo XOR con una chiave segreta. Lo XOR tra due sequenze binarie diventa lo XOR bit a bit.

Vengono forniti due messaggi in esadecimale. La flag si ottiene effettuando lo XOR tra i due.

```
m1 = 158bbd7ca876c60530ee0e0bb2de20ef8af95bc60bdf
m2 = 73e7dc1bd30ef6576f883e79edaa48dcd58e6aa82aa2
```

---

## Soluzione

### Step 1 — Definizione di XOR

Lo XOR (OR esclusivo) è un'operazione logica binaria definita dalla tabella di verità:

$$0 \oplus 0 = 0, \quad 0 \oplus 1 = 1, \quad 1 \oplus 0 = 1, \quad 1 \oplus 1 = 0$$

Estesa a stringhe di byte, l'operazione viene applicata bit a bit in corrispondenza di posizione. Per esempio:

$$\texttt{00110000} \oplus \texttt{01100001} = \texttt{01010001}$$

### Step 2 — Proprietà fondamentale

Lo XOR gode della proprietà di **involuzione**: applicato due volte con la stessa chiave restituisce il valore originale:

$$(A \oplus K) \oplus K = A$$

Questo è il principio alla base dell'OTP: cifrare è XOR con la chiave, decifrare è XOR con la stessa chiave.

### Step 3 — Script

```python
m1 = bytes.fromhex('158bbd7ca876c60530ee0e0bb2de20ef8af95bc60bdf')
m2 = bytes.fromhex('73e7dc1bd30ef6576f883e79edaa48dcd58e6aa82aa2')
print(bytes(x ^ y for x, y in zip(m1, m2)).decode())
```

**Output:**
```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> Lo XOR è l'operazione più semplice della crittografia simmetrica: reversibile, efficiente, e alla base dell'OTP e di tutti i cifrari a flusso moderni.

Due proprietà fondamentali dello XOR che tornano continuamente in crittografia:

1. **Involuzione:** $A \oplus K \oplus K = A$. Cifratura e decifratura sono la stessa operazione, basta applicare la chiave due volte. Questo è ciò che rende ChaCha20, AES-CTR e l'OTP così eleganti: non esistono due funzioni distinte per cifrare e decifrare.

2. **Linearità:** $\oplus$ è un'operazione lineare su $\mathbb{F}_2^n$, il campo di Galois a due elementi esteso a $n$ bit. Questa linearità è un'arma a doppio taglio: semplifica l'implementazione ma, se usata da sola senza sufficiente non-linearità (come in questo esercizio), rende il sistema banalmente attaccabile. I cifrari moderni introducono non-linearità tramite S-box (AES) o rotazioni non lineari (ChaCha20) proprio per rompere questa struttura.