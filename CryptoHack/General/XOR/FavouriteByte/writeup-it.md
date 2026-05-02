# Favourite Byte

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Alcuni dati sono stati nascosti applicando lo XOR con un singolo byte segreto. Decodificare la seguente stringa hex e recuperare la flag.
> `73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d`

Non viene fornita alcuna chiave. Il testo cifrato è stato ottenuto con un singolo byte sconosciuto, che deve essere recuperato.

---

## Fondamenti teorici

### Cifrario XOR a byte singolo

Sia $C = (c_0, c_1, \dots, c_{n-1})$ una sequenza di byte cifrati ottenuta applicando lo XOR tra ogni byte del testo in chiaro $P = (p_0, p_1, \dots, p_{n-1})$ e una chiave segreta fissa $k \in \{0, \dots, 255\}$:

$$c_i = p_i \oplus k \qquad \forall\, i \in \{0, \dots, n-1\}$$

### Attacco a forza bruta

Poiché lo spazio delle chiavi è $\{0, 1, \dots, 255\}$, soltanto 256 valori possibili: una ricerca esaustiva è computazionalmente banale. Per ogni chiave candidata $k' \in \{0, \dots, 255\}$, si calcola:

$$p'_i = c_i \oplus k' \qquad \forall\, i$$

e si verifica se la sequenza di byte risultante $P'$ è una stringa ASCII valida e stampabile. In questa challenge, sappiamo inoltre che il testo in chiaro inizia con il prefisso `crypto{`, che fornisce un ulteriore filtro.

Questo attacco è noto come **attacco a prefisso in chiaro noto** combinato con la forza bruta. Anche senza il prefisso, l'analisi delle frequenze sui testi candidati identificherebbe rapidamente la chiave corretta confrontando la distribuzione delle frequenze dei caratteri di $P'$ con quella attesa per il testo in inglese.

---

## Soluzione

### Script

```python
#!/usr/bin/env python3

hex_ciphertext = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

ciphertext = bytes.fromhex(hex_ciphertext)

for key in range(256):
    candidate = bytes([b ^ key for b in ciphertext])
    try:
        plaintext = candidate
        if plaintext.startswith("crypto{"):
            print(f"key = {key} ({hex(key)}): {plaintext}")
    except Exception:
        pass
```

Il ciclo itera su tutti i 256 valori di chiave possibili. Per ogni candidata $k'$, ogni byte di `ciphertext` viene messo in XOR con $k'$. Se il risultato si decodifica come ASCII valido e inizia con `crypto{`, la chiave corretta è stata trovata.

### Risultato

| Chiave (decimale) | Chiave (hex) | Testo in chiaro |
|:---:|:---:|:---|
| 16 | `0x10` | `crypto{...}` |

La chiave è $k = 16 = \texttt{0x10}_{16} = 00010000_2$.

### Verifica sul primo byte

$$c_0 = \texttt{73}_{16} = 115_{10}, \qquad k = \texttt{10}_{16} = 16_{10}$$

$$p_0 = 115 \oplus 16 = 99_{10} = \texttt{63}_{16} \implies \text{chr}(99) = \texttt{c} \checkmark$$

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge illustra la debolezza fondamentale della cifratura XOR a byte singolo: lo spazio delle chiavi è così piccolo ($2^8 = 256$ valori) che la ricerca esaustiva richiede al massimo 256 tentativi di decifratura, un'operazione che si completa in microsecondi su qualsiasi macchina moderna. Anche senza un filtro sul prefisso noto, la chiave corretta viene identificata banalmente per ispezione visiva o tramite analisi automatica delle frequenze.