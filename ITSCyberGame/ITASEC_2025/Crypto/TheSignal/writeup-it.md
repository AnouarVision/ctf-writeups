# The Signal

**Competizione:** ITSCyberGame<br>
**Categoria:** Crypto<br>
**File**: the_signal.txt

---

## Descrizione

> Un gruppo ha intercettato un messaggio criptato dal gruppo alleato, dicono che contenga la chiave per abbattere le loro difese ma nessuno sa come leggerlo.
---

## Soluzione

Il messaggio è cifrato su **tre livelli** sovrapposti: Morse binario → Base64 → ROT47.

### Passo 1 — Morse Binario

I simboli non seguono l'alfabeto Morse standard: ci sono solo due valori distinti, `----- ` e `.----`, che ricordano immediatamente uno `0` e un `1`. Si tratta di **codifica binaria mascherata da Morse**.

Mappando ogni token:

```
-----  →  0
.----  →  1
```

Si ottiene una lunga stringa di bit. Raggruppandola in blocchi da 8 e convertendo ogni byte in ASCII:

```python
signal = "----- .---- ----- ----- .---- .---- .---- ----- ..."
tokens = signal.split()

bits = ""
for t in tokens:
    if t == "-----":
        bits += "0"
    elif t == ".----":
        bits += "1"

chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
result = "".join(chars)
# → Nz0yOExST1Q0Nz5jRDxkMD5fQ2IwZjljPzA9YkVFYkNkTg==
```

Il risultato è una stringa Base64 riconoscibile dal padding `==` finale.

### Passo 2 — Base64

Decodificando la stringa Base64:

```python
import base64
b64 = "Nz0yOExST1Q0Nz5jRDxkMD5fQ2IwZjljPzA9YkVFYkNkTg=="
decoded = base64.b64decode(b64).decode()
# → 7=28LROT47>cD<d0>_Cb0f9c?0=bEEbCdN
```

Il risultato è una stringa di caratteri ASCII apparentemente casuali. La presenza della sottostringa `LROT` è un indizio: **ROT**ation cipher.

### Passo 3 — ROT47

Osservando i primi 4 caratteri `7=28`, si nota che il formato `flag{...}` ha anch'esso 4 caratteri iniziali. Calcolando la differenza ASCII:

```
f (70) - 7 (55) = 15  X  (non è un Cesare standard)
```

Applicando invece una rotazione sull'intero set di caratteri ASCII stampabili (da `!` a `~`, 94 caratteri totali) con shift **47**, il classico **ROT47**:

```python
s = "7=28LROT47>cD<d0>_Cb0f9c?0=bEEbCdN"

result = ""
for c in s:
    if 33 <= ord(c) <= 126:
        result += chr((ord(c) - 33 + 47) % 94 + 33)

print(result)
# → flag{...}
```

---

## Script Completo

```python
import base64

# Passo 1: Morse binario → bits → ASCII (Base64)
signal = open("the_signal.txt").read().strip()
tokens = signal.split()

bits = "".join("0" if t == "-----" else "1" for t in tokens)
b64 = "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# Passo 2: Base64 → stringa cifrata
s = base64.b64decode(b64).decode()

# Passo 3: ROT47 → flag
flag = "".join(chr((ord(c) - 33 + 47) % 94 + 33) if 33 <= ord(c) <= 126 else c for c in s)
print(flag)
```