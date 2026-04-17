# Software 02 - Librerie

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> I binari linkati dinamicamente hanno bisogno di cercare nel sistema le librerie di cui hanno bisogno. Può quindi tornare utile saper trovare le loro dipendenze. In particolare questo binario cerca di caricare delle librerie strane. Quali?

Viene fornito un file binario `sw-02`. L'obiettivo è trovare le librerie "strane" che tenta di caricare.

---

## Linking statico e dinamico

Quando un programma viene compilato, raramente è un'isola. Quasi sempre dipende da codice esterno: funzioni di libreria per la gestione della memoria, l'I/O, le stringhe e la rete. Questo codice esterno può essere incorporato nel binario al momento della compilazione (**linking statico**) oppure cercato e caricato a runtime (**linking dinamico**).

Il linking dinamico è la norma su Linux per una ragione precisa: se dieci programmi usano tutti `libc`, è sufficiente avere una sola copia di `libc.so` in memoria, condivisa tra tutti. Da qui il nome **shared library**, libreria condivisa. Il file `sw-01` della challenge precedente era `statically linked`; questo `sw-02` è linkato dinamicamente, e questo cambia tutto.

Quando il sistema operativo carica un binario dinamicamente linkato, prima di trasferire il controllo al `main` del programma, un componente chiamato **dynamic linker** (`ld-linux.so`) legge la lista delle dipendenze dichiarate nell'ELF e tenta di caricarle in memoria. Se una libreria non viene trovata, il programma non può partire.

---

## Soluzione

### Step 1 — Il comando `ldd`

`ldd`: *List Dynamic Dependencies* è lo strumento che interroga il dynamic linker per ottenere la lista completa delle shared libraries richieste da un binario, risolvendone i percorsi sul sistema corrente.

```bash
$ ldd sw-02
        linux-vdso.so.1 (0x00007f43be66e000)
        F => not found
        L => not found
        A => not found
        G => not found
        { => not found
        1 => not found
        d => not found
        8 => not found
        d => not found
        b => not found
        5 => not found
        5 => not found
        9 => not found
        } => not found
        libc.so.6 => /usr/lib/x86_64-linux-gnu/libc.so.6 (0x00007f43be43f000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f43be670000)
```

L'output merita una lettura attenta. Tra le dipendenze standard: `linux-vdso.so.1`, `libc.so.6`, `ld-linux-x86-64.so.2`, compaiono delle librerie del tutto inusuali: singoli caratteri come `F`, `L`, `A`, `G`, `{`, `1`, `d`, `8`, `d`, `b`, `5`, `5`, `9`, `}`. Nessuna di esse viene trovata sul sistema (`=> not found`), ovviamente, non sono librerie reali.

### Step 2 — Leggere tra le righe

Il dynamic linker legge i nomi delle dipendenze direttamente dall'ELF, dalla sezione `.dynamic`, campo `DT_NEEDED`. Lo sviluppatore di questa challenge ha popolato quella sezione con una sequenza di stringhe di un singolo carattere che, lette nell'ordine in cui appaiono nell'output di `ldd`, compongono la flag:

```
F L A G { 1 d 8 d b 5 5 9 }
```

---

### Flag

```
flag{1d8db559}
```

---

## Conclusioni

Questa challenge introduce due concetti che torneranno costantemente nel reverse engineering:

**`ldd` come strumento di ricognizione**: prima ancora di aprire un disassembler, `ldd` rivela le dipendenze di un binario e fornisce un primo profilo delle sue capacità. Un binario che importa `libssl.so` fa crittografia; uno che importa `libpthread.so` usa thread; uno che importa qualcosa di insolito merita attenzione immediata.

**I metadati ELF come vettore di informazioni**: la flag non era nel codice eseguibile, non era in una stringa nel segmento `.rodata`, era nei metadati di linking. Questo insegna una lezione metodologica: in un'analisi binaria, ogni sezione dell'ELF è potenzialmente rilevante. `.dynamic`, `.symtab`, `.strtab`, `.comment`, `.note`, tutto può contenere informazioni utili e tutto va esaminato prima di addentrarsi nel disassembly.

Vale anche la pena ricordare una nota di cautela su `ldd`: poiché il tool esegue effettivamente il dynamic linker sul binario, **non va mai usato su binari non fidati** in un ambiente di produzione. Su un sistema di analisi isolato è perfettamente appropriato, ma su un sistema reale potrebbe innescare codice malevolo. Per un'analisi sicura di binari sospetti, l'alternativa è `readelf -d` che legge la sezione `.dynamic` direttamente senza eseguire nulla.