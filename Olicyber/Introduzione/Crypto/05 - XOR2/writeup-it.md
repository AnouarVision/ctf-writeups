# Xor 2

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Il metodo di cifratura utilizzato nella challenge precedente è detto One Time Pad. Un dettaglio fondamentale per ottenere sicurezza perfetta è che la chiave sia lunga tanto quanto il messaggio. Nel caso in cui la chiave sia molto corta (e ripetuta) potrebbe essere possibile un attacco a forza bruta.

Viene fornito un ciphertext cifrato con XOR a chiave di **un solo byte**. Il testo in chiaro non segue il formato `flag{...}`, la flag si costruisce come `'flag{' + plaintext + '}'`.

```
ciphertext = 104e137f425954137f74107f525511457f5468134d7f146c4c
```

---

## Soluzione

### Step 1 — Dimensione dello spazio delle chiavi

La chiave è un singolo byte, quindi lo spazio delle chiavi è:

$$|\mathcal{K}| = 2^8 = 256$$

Con soli 256 candidati, un attacco a forza bruta è computazionalmente banale: si prova ogni $k \in \{0, 1, \ldots, 255\}$ e si verifica se il plaintext risultante è testo ASCII leggibile.

### Step 2 — Decifratura

Per ogni candidato $k$, il plaintext è:

$$P = C \oplus k$$

dove l'operazione XOR viene applicata byte per byte con lo stesso $k$ (chiave ripetuta):

$$P[i] = C[i] \oplus k, \quad i = 0, \ldots, |C|-1$$

Un plaintext è considerato valido se tutti i suoi byte sono caratteri ASCII stampabili, ovvero $P[i] \in [32, 126]$ per ogni $i$.

### Step 3 — Script

```python
ct = bytes.fromhex('104e137f425954137f74107f525511457f5468134d7f146c4c')

for key in range(256):
    pt = bytes(b ^ key for b in ct)
    try:
        text = pt.decode('ascii')
        if all(32 <= ord(c) < 127 for c in text):
            print(f"key=0x{key:02x}: {text}")
    except:
        pass
```

**Output:**
```
key=0x20: ...
```

L'unico risultato leggibile si ottiene con $k = \texttt{0x20} = 32$.

---

## Flag

```
flag{...}
```

---

## Conclusioni

> Una chiave di un solo byte riduce la sicurezza perfetta dell'OTP a zero: lo spazio delle chiavi è così piccolo da essere esplorabile in microsecondi.

Due osservazioni fondamentali:

1. **La lunghezza della chiave è tutto:** il Teorema di Shannon garantisce segretezza perfetta solo se $|K| \geq |P|$. Con $|K| = 1$ byte e $|P| = 25$ byte, la chiave viene necessariamente ripetuta, riducendo il problema a un cifrario di Vigenère con periodo 1, equivalente al cifrario di Cesare sul dominio dei byte. Lo spazio delle chiavi crolla da $2^{200}$ a $2^8 = 256$.

2. **Il criterio di validità del plaintext è l'oracolo:** il brute force funziona perché il testo naturale occupa solo una piccola frazione dello spazio $\{0,\ldots,255\}^n$. Tra tutte le 256 decifrature possibili, una sola produce una stringa ASCII stampabile coerente, questo è sufficiente a identificare la chiave univocamente senza alcuna informazione aggiuntiva.