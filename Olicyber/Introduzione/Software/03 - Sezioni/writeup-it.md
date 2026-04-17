# Software 03 - Sezioni

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Gli ELF sono composti da diverse sezioni. In particolare questo ELF ha una sezione misteriosa, cosa contiene?

Viene fornito un file binario `sw-03`. L'obiettivo è trovare il contenuto di una sezione insolita.

---

## La struttura a sezioni di un ELF

Un file ELF non è una sequenza monolitica di istruzioni macchina. È un contenitore organizzato in **sezioni**, ciascuna con un nome, una dimensione e uno scopo preciso. Il linker le assembla, il loader le mappa in memoria, il debugger le consulta. Conoscerle è il prerequisito per qualsiasi analisi binaria.

Le sezioni standard che si incontrano nella quasi totalità dei binari Linux sono:

- `.text`: il codice eseguibile del programma
- `.rodata`: dati in sola lettura, tipicamente stringhe costanti
- `.data`: variabili globali inizializzate con un valore
- `.bss`: variabili globali non inizializzate (non occupa spazio nel file, solo in memoria)
- `.plt` / `.got`: infrastruttura per il linking dinamico a runtime
- `.dynamic`: metadati per il dynamic linker
- `.debug_*`: informazioni di debug generate dal compilatore con `-g`

Nulla vieta tuttavia a un programmatore o a un autore di challenge di aggiungere sezioni con nomi arbitrari. L'ELF è uno standard flessibile: la section header table è semplicemente un array di descrittori e ciascuno può avere il nome che si vuole.

---

## Soluzione

### Step 1 — Enumerare le sezioni con `objdump -h`

`objdump` è uno strumento multifunzione per l'analisi di object files ed eseguibili. L'opzione `-h` (*headers*) elenca tutte le sezioni presenti nel binario con i loro attributi:

```bash
$ objdump -h sw-03
```

Scorrendo l'output tra le sezioni standard, una in particolare salta all'occhio:

```
25 .super-secret-section  0000001c  0000000000000000 ...
                           CONTENTS, READONLY
```

La sezione si chiama `.super-secret-section`, ha dimensione `0x1c` (28 byte), e non è mappata in memoria durante l'esecuzione (VMA = 0), è una sezione di soli dati statici, non caricata a runtime. Non è codice, non è una libreria: è un contenitore di informazioni nascosto nella struttura del file.

### Step 2 — Ispezionare il contenuto grezzo con `objdump -s`

L'opzione `-s` (*full-contents*) combinata con `-j` (*section*) mostra il contenuto raw di una sezione specifica in formato esadecimale + ASCII:

```bash
$ objdump -s -j .super-secret-section sw-03

Contenuto della sezione .super-secret-section:
 0000 46004c00 41004700 7b006400 30003300  F.L.A.G.{.d.0.3.
 0010 6c007600 6e003400 69007d00           l.v.n.4.i.}.
```

Il dump è immediato: ogni carattere significativo è separato da un byte nullo `\x00`. Si tratta di una stringa **UTF-16LE** (o più semplicemente di caratteri ASCII a 16 bit in little-endian), dove ogni carattere occupa 2 byte di cui il secondo è sempre zero.

Leggendo i byte non nulli nell'ordine:

```
46 4c 41 47 7b 64 30 33 6c 76 6e 34 69 7d
F  L  A  G  {  d  0  3  l  v  n  4  i  }
```

### Step 3 — Perché non usare `-d`?

L'opzione `-d` (*disassemble*) tenta di interpretare il contenuto della sezione come codice macchina x86-64. Il risultato è rumore:

```
0:   46 00 4c 00 41    add %r9b,0x41(%rax,%r8,1)
5:   00 47 00          add %al,0x0(%rdi)
...
```

Le istruzioni non hanno senso perché quei byte non sono codice, sono dati. Questo è un errore comune nell'analisi binaria: applicare lo strumento sbagliato alla sezione sbagliata. `objdump -d` ha senso sulla sezione `.text`; su una sezione dati produce disassembly senza significato. Lo strumento corretto per leggere dati grezzi è `-s`.

---

### Flag

```
flag{d03lvn4i}
```

---

## Conclusioni

Questa challenge insegna tre cose che resteranno valide in ogni analisi futura:

**Le sezioni ELF sono metadati esplorabili**: prima di entrare nel disassembly, vale sempre la pena fare `objdump -h` per avere il quadro completo di cosa contiene il binario. Una sezione con nome insolito, dimensione anomala o attributi particolari è sempre un punto di attenzione.

**`objdump -s` è il modo corretto per leggere dati grezzi**: il dump esadecimale affiancato alla rappresentazione ASCII permette di riconoscere stringhe, strutture dati e pattern a colpo d'occhio. È lo strumento da usare ogni volta che si vuole sapere *cosa c'è* in una sezione, prima ancora di interpretarlo.

**Non tutto il contenuto di un ELF viene eseguito**: sezioni con VMA pari a zero non vengono caricate in memoria durante l'esecuzione. Possono contenere informazioni di debug, metadati, commenti o come in questo caso dati nascosti che il programma non usa mai ma che esistono nel file. Un analista che esamina solo il codice eseguibile potrebbe non trovarle mai.