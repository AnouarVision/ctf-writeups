# Encoding 3

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Spesso in crittografia si ha a che fare con numeri interi. Questi vengono usualmente trasmessi utilizzando svariati encoding delle sequenze di bit corrispondenti.

La flag è spezzata in due metà: la prima codificata in Base64, la seconda come intero in base 10 da convertire in bytes big-endian.

```
ZmxhZ3t3NDF0XzF0c19hbGxfYjE=
664813035583918006462745898431981286737635929725
```

---

## Soluzione

### Step 1 — Decodifica Base64

Base64 è un encoding che rappresenta sequenze di byte usando un alfabeto di 64 caratteri ASCII stampabili (`A-Z`, `a-z`, `0-9`, `+`, `/`). Ogni 3 byte di input (24 bit) vengono codificati in 4 caratteri Base64 (6 bit ciascuno):

$$3 \text{ byte} \xrightarrow{\text{Base64}} 4 \text{ caratteri}$$

Il padding `=` indica che l'ultimo gruppo di byte non era multiplo di 3.

```python
from base64 import b64decode
part1 = b64decode('ZmxhZ3t3NDF0XzF0c19hbGxfYjE=').decode()
```

**Output:** `flag{...`

---

### Step 2 — Intero in base 10 a bytes (big-endian)

Un intero $z$ può essere rappresentato come sequenza di byte in due ordini:

- **Big-endian:** il byte più significativo (MSB) è il primo, convenzione di rete, usata in crittografia
- **Little-endian:** il byte meno significativo (LSB) è il primo, convenzione x86

Il numero di byte necessari si calcola come $n = \lceil \log_{256} z \rceil = \lceil \text{bit\_length}(z) / 8 \rceil$.

```python
n = 664813035583918006462745898431981286737635929725
part2 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
```

**Output:** `...}`

---

### Script

```python
from base64 import b64decode

part1 = b64decode('ZmxhZ3t3NDF0XzF0c19hbGxfYjE=').decode()
n = 664813035583918006462745898431981286737635929725
part2 = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
print(part1 + part2)
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

> In crittografia i dati sono sempre sequenze di bit: Base64 e big-endian sono due dei tanti modi per rappresentarle in forma compatta e non ambigua.

Due osservazioni fondamentali:

1. **Base64 non è cifratura:** come Base16 (esadecimale), Base64 è un puro encoding, non fornisce alcuna segretezza. Il suo scopo è rendere dati binari arbitrari trasportabili in contesti che accettano solo caratteri ASCII, come le email o i certificati X.509 (formato PEM). Ogni stringa Base64 è decodificabile da chiunque senza chiave.

2. **Big-endian è la convenzione crittografica:** RSA, DSA, ECDSA e tutti i principali standard crittografici (PKCS, X.509, TLS) rappresentano i grandi interi in big-endian. Questo perché la matematica modulare tratta i numeri come valori assoluti, il byte più significativo viene scritto per primo, esattamente come si scrive un numero decimale da sinistra a destra. Confondere big-endian con little-endian è una fonte classica di bug nelle implementazioni crittografiche.