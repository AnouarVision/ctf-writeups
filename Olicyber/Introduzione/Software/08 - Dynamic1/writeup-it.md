# Software 08 - Dynamic 1

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Questo binario esegue la chiamata a funzione `open(FLAG)`. Trova la flag provando con il comando `ltrace`, un tool che permette di tracciare le chiamate a funzione eseguite da un file binario.

Viene fornito un binario `sw-08`. L'obiettivo è trovare la flag tramite **analisi dinamica** cioè osservando il comportamento del programma mentre viene eseguito, senza aprire un disassembler.

---

## Analisi statica vs analisi dinamica

Fino a questa challenge abbiamo sempre usato strumenti di **analisi statica**: `strings`, `objdump`, `readelf`, Ghidra. Questi strumenti leggono il file binario senza eseguirlo, ispezionandone la struttura e il codice.

L'**analisi dinamica** è complementare: invece di leggere il binario, lo si esegue in un ambiente controllato e si osserva cosa fa a runtime: quali funzioni chiama, quali syscall invoca, quali file apre e quali dati scrive in memoria. Questa tecnica è indispensabile quando il codice è offuscato, cifrato, o produce risultati che dipendono dall'esecuzione.

La serie Dynamic introduce i due strumenti fondamentali per l'analisi dinamica su Linux: `ltrace` e `strace`.

---

## Il comando `ltrace`

`ltrace`: *library call tracer*, intercetta e registra tutte le chiamate alle funzioni di libreria effettuate dal programma durante l'esecuzione. Per ogni chiamata mostra il nome della funzione, gli argomenti passati e il valore di ritorno.

```bash
$ ltrace ./sw-08
puts("✨ Executing open(FLAG})..."✨ Executing open(FLAG})...
)                                                              = 29
open("flag{...}", 0, 024114303620)                        = -1
+++ exited (status 0) +++
```

L'output rivela due chiamate di libreria:

`puts(...)`: stampa il messaggio introduttivo a schermo. Il valore di ritorno `29` è il numero di caratteri scritti.

`open("flag{...}", 0, ...)`: tenta di aprire un file il cui nome è la flag. Il valore di ritorno `-1` indica che il file non esiste sul sistema (ovviamente, la challenge non lo fornisce), ma il percorso passato come primo argomento contiene la flag in chiaro. `ltrace` ce la mostra prima ancora che la chiamata venga eseguita dal kernel.

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge introduce tre concetti che torneranno in ogni sessione di analisi dinamica:

**`ltrace` intercetta prima dell'esecuzione**: gli argomenti vengono mostrati nel momento in cui la funzione viene chiamata, indipendentemente dal suo esito. Anche se `open()` fallisce con `-1`, il nome del file è già visibile. Questo è il punto di forza dell'analisi dinamica: non importa quanto sia offuscato il codice che costruisce un valore, `ltrace` lo cattura nel momento in cui viene usato.

**Il valore di ritorno è informativo**: `open()` restituisce `-1` perché il file `flag{...}` non esiste sul filesystem locale. In un contesto reale, ad esempio su un server CTF dove la flag è un file vero, la chiamata avrebbe successo e restituito un file descriptor. `ltrace` ci mostrerebbe comunque il percorso.

**L'analisi dinamica ha limiti**: `ltrace` intercetta le chiamate alle librerie condivise (come `libc`), ma non le syscall dirette né le funzioni interne al binario. Per le syscall esiste `strace` (prossime challenge). Per le funzioni interne al binario è necessario un debugger come `gdb`. I tre strumenti si completano a vicenda.