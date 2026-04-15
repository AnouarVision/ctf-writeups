# One More Time Please

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Utilizzando il cifrario di Vernam si ottiene segretezza perfetta. Un principio fondamentale in questi metodi di cifratura (detti non a caso One Time Pad) è quello di non riutilizzare mai una chiave più di una volta.

Viene fornito un file `output.txt` contenente 9 testi cifrati in esadecimale, tutti prodotti con la **stessa chiave** $K$ tramite XOR (cifrario di Vernam).

---

## Soluzione

### Step 1 — La chiave si cancella algebricamente

Il cifrario di Vernam cifra ogni messaggio $P_i$ con la stessa chiave $K$:

$$C_i = P_i \oplus K, \quad i = 1, \ldots, 9$$

XORando due qualsiasi testi cifrati la chiave scompare, poiché $K \oplus K = \mathbf{0}$:

$$C_i \oplus C_k = P_i \oplus P_k$$

Con $N = 9$ messaggi si ottengono $\binom{9}{2} = 36$ coppie, ognuna delle quali espone lo XOR di due plaintext, rendendo il sistema completamente vulnerabile.

---

### Step 2 — Recupero statistico della chiave tramite MTP

I messaggi sono testo ASCII. Lo XOR tra uno spazio (`0x20`) e una lettera produce ancora una lettera:

$$\texttt{0x20} \oplus \ell \in \texttt{[A-Za-z]}, \quad \forall\, \ell \in \texttt{[A-Za-z]}$$

Per ogni posizione $j$, si calcola $C_i[j] \oplus C_k[j]$ per tutte le 36 coppie. Se il risultato è un carattere alfabetico, uno dei due plaintext ha quasi certamente uno spazio in $j$, e si emette il voto:

$$\hat{K}[j] \leftarrow C_i[j] \oplus \texttt{0x20}$$

Il byte di chiave viene stimato per **massima verosimiglianza** tra tutti i voti raccolti per quella posizione:

$$\hat{K}[j] = \arg\max_{v} \;\#\{\text{voti per } v \text{ in posizione } j\}$$

Applicando questo su tutte le posizioni si ottiene una stima $\hat{K}$ e si decifrano parzialmente i messaggi con $P_i[j] = C_i[j] \oplus \hat{K}[j]$.

---

### Step 3 — Lettura dei plaintext parziali

Eseguendo il voto statistico sul file `output.txt` con il seguente script:

```python
from collections import Counter

ciphertexts = [bytes.fromhex(line.strip()) for line in open("output.txt") if line.strip()]

max_len = max(len(c) for c in ciphertexts)
key_votes = [[] for _ in range(max_len)]

for i, ct1 in enumerate(ciphertexts):
    for j, ct2 in enumerate(ciphertexts):
        if i == j:
            continue
        for pos in range(min(len(ct1), len(ct2))):
            xored = ct1[pos] ^ ct2[pos]
            if 65 <= xored <= 90 or 97 <= xored <= 122:
                key_votes[pos].append(ct1[pos] ^ 0x20)
                key_votes[pos].append(ct2[pos] ^ 0x20)

key = [Counter(v).most_common(1)[0][0] if v else 0 for v in key_votes]

for i, ct in enumerate(ciphertexts):
    print(f"ct{i+1}: {''.join(chr(ct[j] ^ key[j]) for j in range(len(ct)))}")
```

**Output:**
```
ct1: IL CRITTOSISTEMA CHE STO UTIL_ZZ__DO S_MB__ IND_STR_TT_B_LE
ct2: NON LEGGERAI MAI QUESTA SEGRETISSIMA FRASE
ct3: LA MIA PREZIOSA FLAG: flag{M4_y_71_3_P_D_N_gH_m_r_}
ct4: I MIEI AMICI CONTINUANO A DIR_I C__ NO_ D_VRE_ UT_LIZ_ARE P_U _NS_...
ct5: SONO SICURO CHE NON CI SARANNO PROBLE__, _ _IEI AM_CI S_ _BAGL_ANO...
ct6: HO AVUTO UNA BELLISSIMA IDEA PER C_SOL_ER_ IL PRO_LEM_ DE_ _ISA_...
ct7: POTREMMO LASCIARE TUTTI I FRIGORIFERI APERTI PER QUALCHE ANNO
ct8: QUANDO HO PARLATO DELLA MIA I_EA P_ MIE_ _MIC_ SON_ _COP_IAT_...
ct9: INVIERO SUBITO UNA LETTERA A _TEP_EN _U_KI_G, LUI _PRE_ZER_ SC_...
```

La stima non è perfetta, alcune posizioni con pochi voti rimangono errate o ambigue, ma è sufficiente a identificare chiaramente la struttura di ogni messaggio, in particolare il messaggio 3 che contiene visibilmente `LA MIA PREZIOSA FLAG: flag{`.

---

### Step 4 — Raffinamento tramite Known-Plaintext (KPA)

Riconoscendo le parole parziali si indovinano i plaintext completi e si applicano come testo in chiaro noto. Per ogni sottostringa $P_i[0:\ell]$ nota si ricavano i byte di chiave esatti:

$$K[t] = C_i[t] \oplus P_i[t], \quad t = 0, \ldots, \ell-1$$

sovrascrivendo la stima statistica con valori certi. Ogni byte di chiave corretto si propaga immediatamente a tutti gli altri $N-1$ messaggi in quella posizione, migliorando iterativamente la leggibilità di tutti i plaintext e permettendo di indovinare le parole successive.

---

### Step 5 — Exploit

```python
from collections import Counter

ciphertexts = [bytes.fromhex(line.strip()) for line in open("output.txt") if line.strip()]

max_len = max(len(c) for c in ciphertexts)
key_votes = [[] for _ in range(max_len)]

for i, ct1 in enumerate(ciphertexts):
    for j, ct2 in enumerate(ciphertexts):
        if i == j:
            continue
        for pos in range(min(len(ct1), len(ct2))):
            xored = ct1[pos] ^ ct2[pos]
            if 65 <= xored <= 90 or 97 <= xored <= 122:
                key_votes[pos].append(ct1[pos] ^ 0x20)
                key_votes[pos].append(ct2[pos] ^ 0x20)

key = [Counter(v).most_common(1)[0][0] if v else 0 for v in key_votes]

def set_key(ct, known, offset=0):
    for i, (c, p) in enumerate(zip(ct[offset:], known)):
        key[offset + i] = c ^ p

set_key(ciphertexts[2], b"LA MIA PREZIOSA FLAG: flag{")
set_key(ciphertexts[0], b"IL CRITTOSISTEMA CHE STO UTILIZZANDO SEMBRA INDISTRUTTIBILE")
set_key(ciphertexts[1], b"NON LEGGERAI MAI QUESTA SEGRETISSIMA FRASE")
set_key(ciphertexts[4], b"SONO SICURO CHE NON CI SARANNO PROBLEMI, I MIEI AMICI SI SBAGLIANO VI MORO")
set_key(ciphertexts[6], b"POTREMMO LASCIARE TUTTI I FRIGORIFERI APERTI PER QUALCHE ANNO")

ct3 = ciphertexts[2]
print(''.join(chr(ct3[i] ^ key[i]) for i in range(len(ct3))))
```

**Output:**
```
LA MIA PREZIOSA FLAG: flag{...}
```

---

## Conclusioni

> Una chiave OTP **non deve mai essere riutilizzata**: farlo annulla completamente la segretezza perfetta garantita dal teorema di Shannon.

Un sistema OTP sicuro deve rispettare tre condizioni:

- **Chiave fresca** per ogni messaggio: `key = os.urandom(len(plaintext))`
- **Chiave uniforme** e indipendente dal plaintext
- **Chiave mai riutilizzata**, nemmeno parzialmente

La vulnerabilità sfruttata è il **Many-Time Pad (MTP)**: con la stessa chiave su $N$ messaggi, lo XOR delle coppie espone $P_i \oplus P_k$, e la frequenza degli spazi nel testo naturale fornisce un oracolo statistico gratuito per stimare $K$ byte per byte. Ogni sottostringa di plaintext nota in uno qualsiasi dei messaggi propaga la conoscenza di $K$ a tutti gli altri $N-1$ testi cifrati.