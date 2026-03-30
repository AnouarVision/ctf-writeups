# labyrinth_protocol

**Competizione:** ITSCyberGame <br>
**Categoria:** Software <br>
**Servizio:** `./labyrinth_protocol <sync_key>`

---

## Descrizione

> Un vecchio terminale di una stazione di ricerca richiede una chiave di sincronizzazione per l'accesso al sistema, ma il disco su cui il programma di verifica è installato è corrotto ed è praticamente impossibile recuperare l'input corretto. Sarà difficile accedere ai dati necessari al nostro team...

Un terminale di una stazione di ricerca richiede una "sync key" come argomento. Il disco è corrotto: impossibile recuperare la chiave leggendo il codice sorgente. Obiettivo: ricostruire la chiave analizzando la logica di verifica nel binario.

---

## Soluzione

### 1. Ricognizione iniziale

```
file labyrinth_protocol
# ELF 64-bit LSB pie executable, x86-64, stripped

checksec --file=labyrinth_protocol
# Partial RELRO | No Canary | NX enabled | PIE enabled | No Symbols
```

**Strings rilevanti:**
```
[!] Initializing Labyrinth Protocol...
[-] Usage: %s <sync_key>
[!] Validating sync key...
CHUNK %d: 0x%x
[+] ACCESS GRANTED!
[-] ACCESS DENIED
```

Il programma: stampa i chunk della chiave, poi chiama una funzione di verifica.

### 2. Analisi della funzione di verifica (0x14cc)

La funzione riceve `(uint32_t x, uint32_t key, uint64_t magic)`.

Calcola:

```c
int64_t f = (int64_t)(int32_t)x * (int64_t)(int32_t)key;
```

**Dimostrazione algebrica:** denotando `A = x&k`, `B = x&~k`, `C = ~x&k`:

```
f = A(A+B+C) + BC = A² + AB + AC + BC = (A+B)(A+C) = x·k
```

Dopo la moltiplicazione viene applicata una catena di trasformazioni deterministiche:

```python
C1 = 0xffffffff21524111  # signed: -3715923183
C2 = 0xfffffffe42a48220  # signed: -7831831008
val1 = f + C1
val2 = (f * 2) | C2
r = val1 - val2 - 2
e = (r * 2 | 0x266f81bc) - (r ^ 0x1337c0de)
# verifica: e == magic
```

### 3. Exploit
Ogni chunk a 32-bit è indipendente: lo script di supporto [labyrinth_protocol.py](./labyrinth_protocol.py) nella stessa cartella effettua l'enumerazione vettorizzata (NumPy) e ricostruisce la chiave.

Eseguire:

```bash
python3 labyrinth_protocol.py
```
---

## Flag

```
flag{...}
```

---

## Conclusioni

**Vulnerabilità / tecnica:** White-box reversing di una funzione di verifica custom.

**Lezione:** La funzione booleana `(x&k)*(x|k) + (x&~k)*(~x&k)` sembra complessa ma si riduce a `x*k` per identità algebrica sulle partizioni di bit. Riconoscere questa semplificazione trasforma un problema apparentemente hard (invertire una funzione non-lineare a 64-bit) in un semplice enumerate a 32-bit, fattibile in pochi secondi con NumPy.

Protezioni come NX e PIE erano irrilevanti: la sfida era puramente logico-algoritmica, non un exploit di memoria.