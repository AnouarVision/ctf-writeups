# 1337_XOR

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Ho cifrato la mia flag. La chiave è troppo lunga per essere trovata tramite bruteforce, mi dispiace ma non riuscirai decifrarla :D

Vengono forniti due file: `encrypt.py` (il codice di cifratura) e `output.txt` (il ciphertext in esadecimale).

---

## Analisi del codice

```python
key = os.urandom(6)
xor(FLAG, key * (len(FLAG)//len(key) + 1)).hex()
```

La chiave è generata casualmente come sequenza di **6 byte** (`os.urandom(6)`), poi ripetuta fino a coprire la lunghezza del plaintext. La cifratura avviene byte per byte tramite XOR:

```
C[i] = P[i] ⊕ K[i mod 6]
```

dove `P` è il plaintext, `K` la chiave di 6 byte, `C` il ciphertext.

---

## Soluzione

### Step 1 — Modello matematico

Sia $P \in \{0,\ldots,255\}^n$ il plaintext, $K \in \{0,\ldots,255\}^6$ la chiave, $C \in \{0,\ldots,255\}^n$ il ciphertext. La cifratura è definita dalla mappa:

$$C_i = P_i \oplus K_{i \bmod 6} \qquad \forall i \in \{0, \ldots, n-1\}$$

dove $\oplus$ denota l'operazione di XOR bit a bit, corrispondente all'addizione nel campo $\mathbb{F}_2^8$.

### Step 2 — Known Plaintext Attack

L'operazione XOR gode della seguente proprietà fondamentale: è la propria inversa. Formalmente, per ogni $a, b \in \{0,1\}^8$:

$$(a \oplus b) \oplus b = a$$

Ne segue immediatamente che, **noti** $P_i$ e $C_i$, è possibile ricavare $K_{i \bmod 6}$:

$$K_{i \bmod 6} = C_i \oplus P_i$$

Il formato della flag è noto: `flag{...}`. Questo ci fornisce **5 byte di plaintext noti** nelle posizioni $i = 0, 1, 2, 3, 4$:

$$P = [\texttt{0x66},\ \texttt{0x6c},\ \texttt{0x61},\ \texttt{0x67},\ \texttt{0x7b},\ \ldots]$$

Applicando la formula di inversione:

$$K_i = C_i \oplus P_i \qquad i = 0, 1, 2, 3, 4$$

Otteniamo 5 dei 6 byte della chiave. Per il sesto byte $K_5$, poiché lo spazio di ricerca è $|\{0,\ldots,255\}| = 256$, un attacco esaustivo sul solo byte mancante è computazionalmente banale, $O(256)$ operazioni contro un bruteforce sull'intera chiave che richiederebbe $O(256^6) \approx 2.8 \times 10^{14}$ operazioni.

### Step 3 — Verifica del candidato

Per ciascun valore $k \in \{0,\ldots,255\}$ del sesto byte, si completa la chiave $\hat{K} = (K_0, K_1, K_2, K_3, K_4, k)$ e si calcola il plaintext candidato:

$$\hat{P}_i = C_i \oplus \hat{K}_{i \bmod 6} \qquad \forall i$$

Il candidato corretto è quello per cui $\hat{P}$ è una stringa ASCII stampabile che termina con `}`.

### Step 4 — Script

```python
ciphertext = bytes.fromhex(
    "27893459dc8772d66261ff8633ba1e5097c10fba257293872fd2664690e975d2015fc4fd3c"
)

known = b"flag{"
key_partial = bytes([known[i] ^ ciphertext[i] for i in range(5)])

for b in range(256):
    key_candidate = key_partial + bytes([b])
    plaintext = bytes([ciphertext[i] ^ key_candidate[i % 6] for i in range(len(ciphertext))])
    try:
        s = plaintext.decode('ascii')
        if s.endswith('}') and all(32 <= c < 127 for c in plaintext):
            print(f"Key: {key_candidate.hex()}")
            print(f"Flag: {s}")
    except:
        pass
```

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge illustra due proprietà cruciali dello XOR come primitiva crittografica:

1. **L'involuzione di XOR**: $a \oplus b \oplus b = a$, rende immediatamente invertibile la cifratura se si conosce anche solo una porzione di plaintext. Questo è il cuore del **Known Plaintext Attack (KPA)**.
2. **Il riuso della chiave è fatale**, ripetere una chiave corta su un plaintext lungo riduce drasticamente la sicurezza: la periodicità della chiave espone ogni posizione $i \bmod 6$ come un problema indipendente e separato.
3. **La lunghezza della chiave non è sufficiente**: il sistema non è sicuro per il solo fatto che la chiave è "troppo lunga per il bruteforce". La struttura algebrica di XOR con chiave ripetuta permette di scomporre il problema e attaccarlo un byte alla volta.

La cifratura XOR con chiave ripetuta è sicura **solo** nel caso limite in cui $|K| = |P|$ e la chiave è usata una sola volta (**One-Time Pad**, dimostrato information-theoretically secure da Shannon nel 1949). In tutti gli altri casi, è vulnerabile.