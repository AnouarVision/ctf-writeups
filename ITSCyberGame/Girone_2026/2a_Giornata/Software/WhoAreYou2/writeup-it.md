# who_are_you_2

**Competizione:** ITSCyberGame<br>
**Categoria:** Software<br>
**File:** who_are_you_2<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> OK, hai ragione, non ero stato molto attento nel dichiarare le variabili. Questa volta, però, ho ordinato tutto per benino...

Versione aggiornata di `who_are_you`. Il programma chiede ancora il nome e verifica se sei root, ma questa volta le variabili sono state riordinate.

---

## Analisi del binario

```bash
file who_are_you_2
# ELF 64-bit LSB executable, x86-64, stripped

checksec --file=who_are_you_2
# Partial RELRO | No canary | NX enabled | No PIE
```

### Differenza rispetto al v1

Dal disassembly si ricava il layout dello stack:

```
rbp-0xd0  →  USER   (buf+0x00, copiato da getenv con strcpy)
rbp-0x6c  →  input  (buf+0x64, letto da scanf("%s"))
```

Nel v1 era il contrario: USER a `buf+0x64`, input a `buf+0x00`. Questa volta:

- **strcmp1**: `strcmp(input, "root")`, l'input deve essere `"root"`
- **strcmp2**: `strcmp(USER, "root")`, USER del server è `"cybergame_contestant"`, non `"root"`

L'overflow dell'input non può sovrascrivere USER perché si trova a un indirizzo **inferiore** nel buffer rispetto all'area di input. Serve un approccio diverso.

---

## Soluzione

### Ret2win

L'exploit salta i controlli sovrascrivendo il **return address** con l'indirizzo del blocco che stampa la flag (`0x401214`):

```
0x401214: puts("Hi, root! Here's your flag")
0x401223: getenv("FLAG") + puts
```

**Calcolo del padding:**

```
input a rbp-0x6c
saved rbp a rbp
ret address a rbp+8

distanza da input a ret = 0x6c + 8 = 116 bytes
```

**Problema del primo strcmp:**

`strcmp(input, "root")` confronta l'intera stringa dell'input. Se il payload contiene `"rootAAA..."`, il confronto fallisce. La soluzione è inserire un **null byte** dopo `"root"`:

```python
payload = b"root\x00" + padding + ret_addr
```

`scanf("%s")` si ferma sui **whitespace** (spazio, tab, newline), **non** sui null byte quindi il null byte viene scritto nel buffer. `strcmp` invece si ferma al null byte, quindi vede solo `"root"` e il confronto passa.

### Script

Lo script è fornito separatamente nel file `who_are_you_2.py` presente nella cartella della challenge. Eseguire lo script con:

```
python3 who_are_you_2.py
```

Lo script connette al server, costruisce il payload con il null byte e l'overflow necessario e stampa l'output; il sorgente completo è disponibile in `who_are_you_2.py` per chi volesse eseguire o modificare l'automazione.

Il messaggio `"Liar!"` appare comunque perché il secondo strcmp fallisce, ma il ret2win fa sì che al `ret` finale il programma salti al blocco della flag invece di uscire.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge insegna due concetti fondamentali. Il primo è il **ret2win**: quando non si può sovrascrivere direttamente le variabili di controllo, si sovrascrive il return address per saltare al codice desiderato. Il secondo è il comportamento di `scanf("%s")`: si ferma sui whitespace ma **non** sui null byte, permettendo di inserire `\x00` nel payload per terminare anticipatamente la stringa che `strcmp` confronterà.