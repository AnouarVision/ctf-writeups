# Software 09 - Dynamic 2

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Questo binario è identico a quello di Dynamic 1, compilato però questa volta staticamente. Non è quindi più possibile utilizzare il comando `ltrace`. Prova ad usare il comando `strace`.

Viene fornito un binario `sw-09`, stesso comportamento di `sw-08`, ma compilato staticamente. `ltrace` non funziona più: serve `strace`.

---

## Perché `ltrace` non funziona sui binari statici

`ltrace` intercetta le chiamate alle **funzioni di libreria condivisa** (come `libc.so`) agganciandosi al meccanismo del dynamic linker: quando il programma chiama `open()`, passa attraverso la PLT (*Procedure Linkage Table*) e `ltrace` si inserisce in quel punto di passaggio.

Un binario **staticamente linkato** non usa la PLT né il dynamic linker, tutto il codice di `libc` è incorporato direttamente nell'eseguibile al momento della compilazione. Non c'è alcun punto di aggancio esterno, quindi `ltrace` non ha modo di intercettare nulla.

La differenza è visibile già con `file`:

```
sw-08: ELF 64-bit, dynamically linked   <- ltrace funziona
sw-09: ELF 64-bit, statically linked    <- ltrace non funziona
```

---

## Il comando `strace`

`strace`: *system call tracer*, opera a un livello più basso di `ltrace`: intercetta le **syscall**, cioè le chiamate dirette al kernel Linux. Funziona su qualsiasi binario, statico o dinamico, perché le syscall passano sempre attraverso il kernel indipendentemente da come il programma è linkato.

```bash
$ strace ./sw-09
execve("./sw-09", ["./sw-09"], 0x7ffd021f1d80 /* 57 vars */) = 0
brk(NULL)                               = 0x4655000
brk(0x4655d80)                          = 0x4655d80
arch_prctl(ARCH_SET_FS, 0x4655380)      = 0
uname({sysname="Linux", nodename="kali", ...}) = 0
readlink("/proc/self/exe", "/home/<user>/Scaricati/sw-09", 4096) = 28
brk(0x4676d80)                          = 0x4676d80
brk(0x4677000)                          = 0x4677000
mprotect(0x4ab000, 4096, PROT_READ)     = 0
fstat(1, {st_mode=S_IFCHR|0600, st_rdev=makedev(0x88, 0), ...}) = 0
write(1, "\342\234\250 Executing open(FLAG})...\n", 29✨ Executing open(FLAG})...
) = 29
openat(AT_FDCWD, "flag{...}", O_RDONLY) = -1 ENOENT (File o directory non esistente)
exit_group(0)                           = ?
+++ exited with 0 +++
```

L'output è più verboso di `ltrace` perché mostra **tutte** le syscall, incluse quelle di inizializzazione (`brk`, `mprotect`, `arch_prctl`, ecc.) che normalmente non interessano. Le righe rilevanti sono due:

`write(1, "✨ Executing open(FLAG})...", 29)`: scrive il messaggio sullo stdout (file descriptor 1). Il valore `29` è il numero di byte scritti.

`openat(AT_FDCWD, "flag{...}", O_RDONLY) = -1 ENOENT`: tenta di aprire il file `flag{...}` in sola lettura. Fallisce con `ENOENT` (*No such file or directory*) perché il file non esiste, ma il percorso passato come secondo argomento contiene la flag in chiaro.

---

## `ltrace` vs `strace`: il livello di astrazione

| | `ltrace` | `strace` |
|---|---|---|
| Intercetta | Chiamate a funzioni di libreria | Syscall al kernel |
| Funziona su binari statici | No | Sì |
| Output | Più compatto, solo chiamate di libreria | Più verboso, tutte le syscall |
| Meccanismo | Si aggancia alla PLT | Usa `ptrace()` del kernel |

In questa challenge `open()` di `libc`, che `ltrace` avrebbe intercettato si traduce internamente nella syscall `openat()` che `strace` intercetta. Il risultato finale è lo stesso: la flag appare come argomento.

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge completa il quadro degli strumenti di analisi dinamica di base:

**`strace` è universale**: funziona su qualsiasi binario Linux perché le syscall sono l'unico punto di contatto tra qualsiasi programma e il kernel, indipendentemente da come il codice è compilato o linkato. È lo strumento da usare quando `ltrace` non produce output utile.

**Il linking statico non è una protezione**: cambiare da linking dinamico a statico rimuove un vettore di analisi (`ltrace`) ma non l'altro (`strace`). In entrambi i casi la flag emerge in chiaro come argomento di una chiamata. La vera protezione richiederebbe cifrare la flag e decodificarla solo in memoria, senza mai passarla come argomento a funzioni osservabili.

**L'output di `strace` va filtrato**: in un'analisi reale, un programma complesso produce centinaia di syscall prima di arrivare alla parte interessante. È buona pratica usare `strace -e trace=openat,read,write ./binario` per filtrare solo le syscall rilevanti, o reindirizzare l'output con `strace ./binario 2>&1 | grep open` per trovare rapidamente le chiamate di interesse.