# You either know, XOR you don't

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> La flag è stata cifrata con una chiave ripetuta segreta. Recuperarla.
> `0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104`

Non viene fornita alcuna chiave. Il testo cifrato è stato prodotto con una chiave XOR multi-byte ripetuta di lunghezza sconosciuta.

---

## Fondamenti teorici

### Cifrario XOR a chiave ripetuta

Siano $P = (p_0, p_1, \dots, p_{n-1})$ il testo in chiaro e $K = (k_0, k_1, \dots, k_{m-1})$ la chiave di lunghezza $m$. Il testo cifrato è:

$$c_i = p_i \oplus k_{i \bmod m} \qquad \forall\, i \in \{0, \dots, n-1\}$$

La chiave si ripete ciclicamente sul testo in chiaro. Per una chiave corta e un messaggio lungo, ogni byte della chiave cifra più byte del testo in chiaro, uno per ogni posizione $i$ in cui $i \equiv j \pmod{m}$ per il byte di chiave $j$.

### Attacco a prefisso in chiaro noto

Poiché tutte le flag di CryptoHack iniziano con il prefisso fisso `crypto{`, disponiamo di un **testo in chiaro noto** di almeno 7 byte. Dati i byte del testo cifrato $c_0, c_1, \dots, c_6$ e i corrispondenti byte noti $p_0 = \texttt{c},\ p_1 = \texttt{r},\ \dots,\ p_6 = \texttt{\{}$, possiamo recuperare direttamente i byte della chiave:

$$k_{i \bmod m} = c_i \oplus p_i \qquad \forall\, i \in \{0, \dots, 6\}$$

Questo produce fino a 7 byte di chiave, sufficienti a recuperare completamente una chiave di lunghezza $\leq 7$ o una chiave parziale per chiavi più lunghe.

---

## Soluzione

### Passo 1 — Recupero della chiave dal prefisso noto

Si esegue lo XOR tra i primi 7 byte del testo cifrato e la codifica ASCII di `crypto{`:

| $i$ | $c_i$ | $p_i$ | $c_i \oplus p_i$ | Byte di chiave |
|:---:|:---:|:---:|:---:|:---:|
| 0 | `0e` | `63` (`c`) | `6d` | `m` |
| 1 | `0b` | `72` (`r`) | `79` | `y` |
| 2 | `21` | `79` (`y`) | `58` | `X` |
| 3 | `3f` | `70` (`p`) | `4f` | `O` |
| 4 | `26` | `74` (`t`) | `52` | `R` |
| 5 | `04` | `6f` (`o`) | `6b` | `k` |
| 6 | `1e` | `7b` (`{`) | `65` | `e` |

I byte recuperati compongono la stringa `myXORke`. Poiché il byte successivo della chiave sarebbe `y` per completare la parola inglese, la chiave completa è:

$$K = \texttt{myXORkey} \quad (m = 8)$$

### Passo 2 — Decifratura del testo cifrato completo

```python
#!/usr/bin/env python3

hex_ciphertext = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

ciphertext = bytes.fromhex(hex_ciphertext)
key = b"myXORkey"

flag = bytes([c ^ key[i % len(key)] for i, c in enumerate(ciphertext)])
print(flag.decode())
```

Ogni byte del testo cifrato viene messo in XOR con il corrispondente byte della chiave alla posizione $i \bmod 8$, recuperando il testo in chiaro originale.

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge dimostra l'**attacco a testo in chiaro noto** sul cifrario XOR a chiave ripetuta. L'intuizione chiave è che un formato di flag fisso e pubblicamente noto rivela immediatamente i primi byte della chiave: poiché $c_i = p_i \oplus k_{i \bmod m}$, conoscere $c_i$ e $p_i$ fornisce direttamente $k_{i \bmod m}$.

Più in generale, qualsiasi cifrario XOR a chiave ripetuta è vulnerabile non appena la lunghezza della chiave è nota o stimata, a quel punto il testo cifrato può essere suddiviso in $m$ flussi XOR a byte singolo indipendenti, ciascuno attaccabile per forza bruta o analisi delle frequenze.