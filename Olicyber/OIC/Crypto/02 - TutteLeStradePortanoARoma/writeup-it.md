# Tutte le strade portano a Roma

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione

> Su un'antica pergamena è stata trovata questa citazione. Prova a decriptarla:
> `cixd{xsb_zxbpxo_jlofqrof_qb_pxirqxkq}`

Un testo cifrato da decrittare. La hint è anche nel titolo: *"Tutte le strade portano a Roma"*, chiaro riferimento diretto all'antica Roma e, di conseguenza, al **Cifrario di Cesare**.

---

## Soluzione

### Step 1 - Il Cifrario di Cesare

Ogni lettera del testo in chiaro viene sostituita dalla lettera che si trova `n` posizioni più avanti nell'alfabeto.

Formula di decifratura:
```
P = (C + shift) mod 26
```

---

### Step 2 — Decifratura

Applicando lo shift + 3 a ogni lettera del testo cifrato:

```
Cifrato:    c  i  x  d  {  x  s  b  _  z  x  b  p  x  o  _  j  l  o  f  q  r  o  f  _  q  b  _  p  x  i  r  q  x  k  q  }
Decifrato:  f  l  a  g  { ... }
```

---

### Step 3 — Script di decifratura

```python
def caesar_decrypt(text, shift=3):
    result = ""
    for c in text:
        if c.isalpha():
            result += chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += c
    return result

ciphertext = "cixd{xsb_zxbpxo_jlofqrof_qb_pxirqxkq}"
print(caesar_decrypt(ciphertext))
# Output: flag{...}
```

---

### Flag

flag{...}

---

## Conclusioni

Questa challenge dimostra che:
1. **Il formato della flag è un ancoraggio**: riconoscere `cixd{` → `flag{` permette di ricavare lo shift immediatamente
2. **Il Cifrario di Cesare è insicuro**: con sole 25 chiavi possibili, un attacco a forza bruta è banale