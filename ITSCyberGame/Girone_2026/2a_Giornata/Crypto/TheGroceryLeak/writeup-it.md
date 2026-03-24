# the_grocery_leak

**Competizione:** ITSCyberGame<br>
**Categoria:** Crypto<br>
**File:** Lista_Spesa.ods, secure_encryptor.py, grocery.txt

---

## Descrizione

> Abbiamo intercettato le comunicazioni di un gruppo di contrabbandieri digitali. Si scambiano messaggi cifrati, ma la chiave esadecimale per decifrarli sembra essere nascosta in bella vista: dentro una banale lista della spesa... ma i conti non tornano.

Vengono forniti tre file: un foglio di calcolo ODS, lo script Python usato per cifrare e un file di testo con il messaggio cifrato.

---

## Analisi dei file

### secure_encryptor.py

Lo script rivela l'algoritmo di cifratura: uno **XOR a chiave ripetuta** di esattamente 6 byte.

```python
def secure_algorithm(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
```

La chiave deve essere da esattamente 6 byte (12 caratteri hex).

### grocery2.txt

Il messaggio cifrato in esadecimale:

```
7458371fe1db6004354be8c54d473e48eacc235a3127f288715f650ae7
```

### Lista_Spesa1.ods

Il foglio contiene 20 righe di lista della spesa con 6 prodotti ciascuna. Ogni riga ha: `Prodotto`, `Qty`, `Prezzo`, `TOTALE`. La colonna `TOTALE` dovrebbe essere `Qty × Prezzo`, ma in molte righe vale `Prezzo + Qty`, i conti non tornano, esattamente come da hint.

---

## Soluzione

### Identificazione delle righe anomale

Analizzando il foglio si nota che alcune righe hanno tutti i prodotti con `Qty = 1` e `TOTALE = Prezzo + 1`. In queste righe i **prezzi letti in esadecimale** formano pattern riconoscibili:

| ID | Prezzi decimali | Prezzi esadecimali |
|---|---|---|
| 5  | 26, 43, 60, 77, 94, 111   | `1a 2b 3c 4d 5e 6f` |
| 7  | 18, 52, 86, 120, 154, 188 | `12 34 56 78 9a bc` |
| 10 | 161, 178, 195, 212, 229, 246 | `a1 b2 c3 d4 e5 f6` |
| 12 | 222, 173, 190, 239, 32, 37 | `de ad be ef 20 25` |
| 16 | 186, 220, 31, 254, 224, 31 | `ba dc 1f fe e0 1f` |
| 18 | 31, 31, 31, 31, 31, 31    | `1f 1f 1f 1f 1f 1f` |
| 19 | 192, 255, 238, 136, 153, 170 | `c0 ff ee 88 99 aa` |

Ogni riga speciale è una chiave candidata da 6 byte.

### Brute force delle chiavi candidate

```python
ciphertext = bytes.fromhex("7458371fe1db6004354be8c54d473e48eacc235a3127f288715f650ae7" + "0")

candidates = {
    "ID5":  "1a2b3c4d5e6f",
    "ID7":  "123456789abc",
    "ID10": "a1b2c3d4e5f6",
    "ID12": "deadbeef2025",
    "ID16": "badc1ffee01f",
    "ID18": "1f1f1f1f1f1f",
    "ID19": "c0ffee8899aa",
}

for name, key_hex in candidates.items():
    key = bytes.fromhex(key_hex)
    decrypted = bytes([ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))])
    print(f"{name}: {decrypted.decode('utf-8', errors='replace')}")
```

Output:

```
ID5  (1a2b3c4d5e6f): ns\x0bR...  (non leggibile)
ID7  (123456789abc): flag{...}
ID10 (a1b2c3d4e5f6): ...         (non leggibile)
...
```

La chiave corretta è quella della riga 7: `123456789abc`.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La chiave era nascosta nei prezzi della lista della spesa: leggendoli in esadecimale, i prezzi della riga 7 formano la sequenza `12 34 56 78 9a bc`. I "conti che non tornano" erano l'indizio per cercare righe anomale, quelle con `Qty = 1` e `TOTALE = Prezzo + 1` e interpretare i prezzi come valori esadecimali invece che decimali. L'algoritmo di cifratura era un semplice XOR con chiave ripetuta, reso vulnerabile dalla lunghezza fissa e breve della chiave (6 byte).