# Very Strong Vigenere

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Da quando ho scoperto vigenere mi sento completamente al sicuro!
> `fzau{ncn_isors_cviovw_pwcqoze}`

La flag è cifrata con il cifrario di Vigenère. L'obiettivo è recuperare la chiave e decifrare il messaggio.

---

## Il Cifrario di Vigenère

Il cifrario di Vigenère opera sull'alfabeto $\mathbb{Z}_{26}$, identificando ogni lettera con il suo indice: $\texttt{a} \mapsto 0,\ \texttt{b} \mapsto 1,\ \ldots,\ \texttt{z} \mapsto 25$.

Sia $P = (P_0, P_1, \ldots, P_{n-1}) \in \mathbb{Z}_{26}^n$ il plaintext, $K = (K_0, K_1, \ldots, K_{m-1}) \in \mathbb{Z}_{26}^m$ la chiave di lunghezza $m$, e $C = (C_0, C_1, \ldots, C_{n-1}) \in \mathbb{Z}_{26}^n$ il ciphertext. La cifratura è definita dalla mappa:

$$C_i = (P_i + K_{i \bmod m}) \bmod 26 \qquad \forall i \in \{0, \ldots, n-1\}$$

La decifratura è l'operazione inversa, ottenuta sottraendo la chiave in $\mathbb{Z}_{26}$:

$$P_i = (C_i - K_{i \bmod m}) \bmod 26 \qquad \forall i \in \{0, \ldots, n-1\}$$

I caratteri non alfabetici (simboli, punteggiatura) vengono trasmessi invariati e **non avanzano l'indice** della chiave.

---

## Soluzione

### Step 1 — Known Plaintext Attack

Il formato della flag è noto: i primi cinque caratteri del plaintext sono $P = (\texttt{f}, \texttt{l}, \texttt{a}, \texttt{g}, \texttt{\{})$, corrispondenti ai valori $(5, 11, 0, 6)$ in $\mathbb{Z}_{26}$ (la parentesi graffa non è alfabetica e viene ignorata).

Il ciphertext corrispondente è $C = (\texttt{f}, \texttt{z}, \texttt{a}, \texttt{u}, \texttt{\{})$, ovvero $(5, 25, 0, 20)$.

Applicando la formula di inversione per ciascuna posizione:

$$K_{i \bmod m} = (C_i - P_i) \bmod 26$$

$$K_0 = (5 - 5) \bmod 26 = 0 \quad \longrightarrow \quad \texttt{a}$$
$$K_1 = (25 - 11) \bmod 26 = 14 \quad \longrightarrow \quad \texttt{o}$$
$$K_2 = (0 - 0) \bmod 26 = 0 \quad \longrightarrow \quad \texttt{a}$$
$$K_3 = (20 - 6) \bmod 26 = 14 \quad \longrightarrow \quad \texttt{o}$$

La sequenza ottenuta è $\texttt{aoao}$, che rivela immediatamente una chiave di periodo $m = 2$:

$$K = (\texttt{a}, \texttt{o}) \quad \Longrightarrow \quad K = (0,\ 14)$$

---

### Step 2 — Decifratura completa

Con $K = (0, 14)$ e $m = 2$, si applica la decifratura a ogni carattere alfabetico del ciphertext:

$$P_i = (C_i - K_{i \bmod 2}) \bmod 26$$

| $i$ | $C_i$ | $K_{i \bmod 2}$ | $P_i$ | Lettera |
|-----|--------|-----------------|--------|---------|
| 0 | $\texttt{f}=5$ | $K_0=0$ | $5$ | f |
| 1 | $\texttt{z}=25$ | $K_1=14$ | $11$ | l |
| 2 | $\texttt{a}=0$ | $K_0=0$ | $0$ | a |
| 3 | $\texttt{u}=20$ | $K_1=14$ | $6$ | g |
| 4 | $\texttt{n}=13$ | $K_0=0$ | $13$ | n |
| 5 | $\texttt{c}=2$ | $K_1=14$ | $(2-14) \bmod 26 = 14$ | o |
| $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ |

---

### Step 3 — Script di decifratura

```python
def vigenere_decrypt(ciphertext, key):
    result = ""
    ki = 0
    for c in ciphertext:
        if c.isalpha():
            k = ord(key[ki % len(key)]) - ord('a')
            p = (ord(c.lower()) - ord('a') - k) % 26
            result += chr(p + ord('a'))
            ki += 1
        else:
            result += c
    return result

ciphertext = "fzau{ncn_isors_cviovw_pwcqoze}"
key = "ao"
print(vigenere_decrypt(ciphertext, key))
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge illustra la debolezza strutturale del cifrario di Vigenère quando la chiave è corta.

1. **Il Known Plaintext Attack annulla la sicurezza**: la struttura additiva in $\mathbb{Z}_{26}$ rende la chiave immediatamente recuperabile da una singola coppia $(P_i, C_i)$ nota. Con il formato della flag noto, bastano 4 caratteri per ricostruire l'intera chiave.

2. **La lunghezza della chiave è il parametro critico**: una chiave di periodo $m$ riduce il problema a $m$ istanze indipendenti del cifrario di Cesare, ciascuna attaccabile separatamente. Nel caso limite $m = n$ (chiave lunga quanto il messaggio, usata una sola volta) si ottiene il **One-Time Pad**, che è l'unico sistema di cifratura dimostrabilmente sicuro per il teorema di Shannon. Con $m = 2$ la sicurezza è pari a quella di due cifrari di Cesare sovrapposti.