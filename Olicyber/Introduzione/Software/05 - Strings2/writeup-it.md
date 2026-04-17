# Software 05 - Strings 2

**Competizione:** OliCyber<br>
**Categoria:** Reverse Engineering

---

## Descrizione

> Il programma di questa challenge è molto simile al precedente. Questa volta però il comando `strings` non ti aiuterà. Analizza il contenuto della funzione `main` con Ghidra.

Viene fornito un binario `sw-05` che verifica una stringa in input. A differenza di `sw-04`, la flag non è memorizzata in chiaro e `strings` non la rivela.

---

## Perché `strings` non funziona

In `sw-04` la flag era una sequenza contigua di byte ASCII, visibile direttamente nell'output di `strings`. Qui l'autore ha adottato un accorgimento: la flag è memorizzata in formato **UTF-16LE**, ogni carattere occupa 2 byte, il secondo dei quali è sempre `\x00`. Il risultato è che i caratteri sono separati da byte nulli e nessuna sequenza di 4+ caratteri contigui è presente nel file. `strings` non trova nulla di utile perché le sequenze leggibili sono troppo corte.

---

## Ghidra: disassembler e decompiler

Per analizzare il binario usiamo **Ghidra**, lo strumento di reverse engineering sviluppato dalla NSA e rilasciato open source. Ghidra offre due viste fondamentali:

**La vista Disassembly** mostra le istruzioni macchina del processore — il codice così come esiste nel file, tradotto da byte grezzi in mnemonici leggibili (`MOV`, `CMP`, `JZ`, ecc.).

**La vista Decompiler** è quella più potente per chi inizia: Ghidra analizza il flusso di controllo e ricostruisce un **codice C approssimato** che rappresenta la logica del programma. Non è il sorgente originale, è una ricostruzione euristica, ma è enormemente più leggibile dell'assembly grezzo.

Per attivarla: nel menu `Window` → `Decompiler`, oppure premendo il tasto destro su una funzione nell'albero delle funzioni e scegliendo `Decompile`.

### Rinominare le variabili

Ghidra assegna nomi automatici alle variabili locali come `local_218`, `local_118`, `iVar1`, nomi che non dicono nulla sul loro significato. Una volta capito il ruolo di una variabile, conviene rinominarla immediatamente per mantenere il codice leggibile.

Per farlo: tasto destro sulla variabile nel decompiler → **Rename Variable** (oppure tasto `L`). È una pratica fondamentale nel reverse engineering professionale: il 90% del lavoro è dare un nome alle cose.

---

## Analisi del codice decompilato

### Codice originale prodotto da Ghidra

Aprendo `sw-05` in Ghidra e selezionando la funzione `main` nel decompiler, si ottiene questo pseudocodice C:

```c
undefined8 main(void)
{
  int iVar1;
  long in_FS_OFFSET;
  ulong i;
  undefined8 local_220;
  char local_218 [256];
  char local_118 [264];
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_218,0,0x100);
  memset(local_118,0,0x100);
  do {
    printf(&DAT_0010202c);
    fgets(local_218,0x100,stdin);
    local_220 = strlen(local_218);
    if (local_220 != 0) {
      if (local_218[local_220 - 1] == '\n') {
        local_218[local_220 - 1] = '\0';
      }
      for (i = 0; i < 0xe; i = i + 1) {
        local_118[i] = flag[i * 2];
      }
      iVar1 = strcmp(local_218,local_118);
      if (iVar1 == 0) {
        puts(&DAT_00102061);
        if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
          /* WARNING: Subroutine does not return */
          __stack_chk_fail();
        }
        return 0;
      }
    }
    puts(&DAT_00102045);
  } while( true );
}
```

I nomi come `local_218`, `local_118`, `iVar1` non dicono nulla. Il primo passo è capire il ruolo di ogni variabile e rinominarla con **Rename Variable** (tasto destro → `Rename Variable`, oppure tasto `L`).

### Codice con variabili rinominate

Dopo aver analizzato il flusso e rinominato le variabili, il codice diventa immediatamente comprensibile:

```c
undefined8 main(void)
{
  int risultato_strcmp;
  long in_FS_OFFSET;
  ulong i;
  undefined8 lunghezza_input;
  char input_utente [256];
  char flag_ricostruita [264];
  long stack_canary;

  stack_canary = *(long *)(in_FS_OFFSET + 0x28);
  memset(input_utente, 0, 0x100);
  memset(flag_ricostruita, 0, 0x100);
  do {
    printf(&DAT_0010202c);                          // "Qual è la flag? : "
    fgets(input_utente, 0x100, stdin);              // legge l'input, più sicuro di gets
    lunghezza_input = strlen(input_utente);
    if (lunghezza_input != 0) {
      if (input_utente[lunghezza_input - 1] == '\n') {
        input_utente[lunghezza_input - 1] = '\0';   // rimuove il newline finale
      }
      for (i = 0; i < 0xe; i = i + 1) {
        flag_ricostruita[i] = flag[i * 2];          // prende un byte ogni due dal raw
      }
      risultato_strcmp = strcmp(input_utente, flag_ricostruita);
      if (risultato_strcmp == 0) {
        puts(&DAT_00102061);                        // "Giusto!"
        if (stack_canary != *(long *)(in_FS_OFFSET + 0x28)) {
          __stack_chk_fail();
        }
        return 0;
      }
    }
    puts(&DAT_00102045);                            // "Sbagliato! Prova ancora"
  } while( true );
}
```

La riga chiave è una sola:

```c
flag_ricostruita[i] = flag[i * 2];
```

Il ciclo itera 14 volte (`0xe = 14`) e ad ogni passo copia in `flag_ricostruita[i]` il byte all'indice `i * 2` dell'array `flag`, cioè gli indici `0, 2, 4, 6, 8, 10, ...`. Gli indici dispari `1, 3, 5, ...` vengono saltati. Questo è esattamente il comportamento di una stringa **UTF-16LE**: ogni carattere è codificato su 2 byte, il secondo dei quali è `\x00` per tutti i caratteri ASCII.

---

## Estrazione della flag

Conoscendo la trasformazione, possiamo estrarre la flag direttamente con `objdump -s` sulla sezione `.rodata`, leggendo un byte ogni due:

```bash
$ objdump -s -j .rodata sw-05

Contenuto della sezione .rodata:
 2000 01000200 00000000 00000000 00000000  ................
 2010 66006c00 61006700 7b003800 31003700  f.l.a.g.{.8.1.7.
 2020 35003000 65003600 33007d00 f09f9aa9  5.0.e.6.3.}.....
```

A partire dall'offset `0x2010`, i byte agli indici pari sono:

```
66 6c 61 67 7b 38 31 37 35 30 65 36 33 7d
f  l  a  g  {  8  1  7  5  0  e  6  3  }
```

I byte agli indici dispari sono tutti `\x00`, la firma del formato UTF-16LE.

---

### Flag

```
flag{81750e63}
```

---

## Conclusioni

Questa challenge introduce la tecnica di analisi statica con decompiler e mostra perché è più potente di `strings`:

**`strings` trova solo testo in chiaro contiguo**: qualsiasi trasformazione che spezza la contiguità dei caratteri (interleaving, XOR, codifiche multi-byte) lo rende cieco. È un ottimo primo passo, ma non un sostituto dell'analisi.

**Il decompiler traduce la logica, non i dati**: Ghidra non trova la flag direttamente, ma mostra *come viene costruita* a runtime. Capire la trasformazione (`flag[i * 2]`) è sufficiente per invertirla e recuperare il plaintext.