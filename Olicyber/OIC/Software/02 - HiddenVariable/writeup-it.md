# Hidden Variable

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Non trovo più la mia variabile :(, mi daresti una mano?

Viene fornito un binario ELF x86-64. All'esecuzione stampa una flag "corrotta" e un messaggio di errore. L'obiettivo è trovare la variabile nascosta contenente la flag reale.

---

## Analisi del binario

### Step 1 — Ricognizione iniziale

```bash
file hidden_variable
# ELF 64-bit LSB pie executable, x86-64, not stripped

strings hidden_variable
# "La tua flag"
# "f_ag{."          ← flag corrotta (depistaggio)
# "Accidenti, sembra corrotta! Dove avrò lasciato l'originale?"
# "fl4g"            ← simbolo sospetto nella symbol table
```

Il binario è **not stripped**: la symbol table è intatta e rivela un simbolo `fl4g` nella sezione `.data`. La flag mostrata a runtime è volutamente corrotta, un depistaggio.

---

### Step 2 — Ispezione della sezione `.rodata`

Il `main` stampa due stringhe tramite `puts`. Ispezionando `.rodata`:

```
2008: "La tua flag .. f_ag{...#[..."   ← flag corrotta con byte non-ASCII
2030: "Accidenti, sembra corrotta!..."
```

La stringa a `0x2008` contiene caratteri non-ASCII al posto dei caratteri corretti della flag, è un falso positivo inserito per confondere l'analisi statica superficiale.

---

### Step 3 — Ispezione della sezione `.data` e del simbolo `fl4g`

```bash
nm hidden_variable | grep fl
# 0000000000004020 D fl4g

objdump -s -j .data hidden_variable
```

A partire dall'indirizzo `0x4020` si trova:

```
4020: 66000000 6c000000 61000000 67000000   f...l...a...g...
4030: 7b000000 75000000 6e000000 75000000   {...u...n...u...
4040: 35000000 33000000 64000000 5f000000   5...3...d..._...
...
```

La variabile `fl4g` è un **array di interi a 32 bit** (`int[]`) in little-endian. Ogni elemento contiene un singolo carattere ASCII nel byte meno significativo, con i 3 byte superiori a zero. Questa è una tecnica comune per nascondere stringhe all'analisi con `strings`, che cerca sequenze di byte ASCII contigui, qui i caratteri sono separati da 3 byte nulli.

---

### Step 4 — Ricostruzione della flag

Per estrarre la flag si legge il primo byte di ogni gruppo da 4:

```python
data = bytes.fromhex(
    '66000000 6c000000 61000000 67000000'
    '7b000000 75000000 6e000000 75000000'
    '35000000 33000000 64000000 5f000000'
    '76000000 34000000 72000000 35000000'
    '5f000000 34000000 72000000 33000000'
    '5f000000 35000000 37000000 31000000'
    '31000000 5f000000 63000000 30000000'
    '6d000000 70000000 31000000 6c000000'
    '33000000 64000000 7d000000'.replace(' ', '')
)
flag = ''.join(chr(data[i]) for i in range(0, len(data), 4))
print(flag)
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

> Le variabili non usate nel codice sorgente possono comunque essere compilate nel binario e restare accessibili tramite analisi statica, soprattutto se il binario non è stripped.

Tre osservazioni fondamentali:

1. **`strings` non basta:** il tool `strings` cerca sequenze di byte ASCII contigui di lunghezza minima (default 4). Memorizzare una stringa come array di `int` con un carattere per elemento separa i byte ASCII con tre zeri, rendendo la stringa invisibile a `strings`. L'analisi della sezione `.data` con `objdump -s` o un disassembler come Ghidra è necessaria per trovare questo tipo di encoding.

2. **Not stripped = symbol table intatta:** quando un binario non è stripped, i simboli delle variabili globali (`D` nella symbol table di `nm`) sono ancora presenti. Il simbolo `fl4g` ha rivelato direttamente l'indirizzo della variabile nascosta. In produzione i binari vengono strippati con `strip` per rimuovere queste informazioni e rendere il reverse engineering più difficile.

3. **Il depistaggio nella `.rodata`:** la flag corrotta stampata a runtime è una tecnica di *anti-reversing* elementare, induce l'analista a pensare di aver trovato la flag e a smettere di cercare. Un'analisi sistematica di tutte le sezioni del binario è sempre necessaria prima di concludere.