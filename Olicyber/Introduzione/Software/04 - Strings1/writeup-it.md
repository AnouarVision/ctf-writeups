# Software 04 - Strings 1

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Questi programmi chiedono in input la flag, o una stringa in generale, e ne verificano la correttezza. Un tool utile che permette di trovare tutte le stringhe contenute in un file è `strings`.

Viene fornito un binario `sw-04` che chiede in input la flag e ne verifica la correttezza. L'obiettivo è trovarla.

---

## Come funziona la verifica di una stringa in un programma

Quando un programma confronta l'input dell'utente con una stringa attesa, quella stringa deve esistere da qualche parte nel binario. Il compilatore la inserisce tipicamente nella sezione `.rodata`, *read-only data*, come sequenza di byte ASCII terminata da un byte nullo `\x00`. È dati statici, costanti, presenti nel file sin dal momento della compilazione.

Questo è il caso più semplice e più comune nelle challenge introduttive di reverse engineering: la flag è memorizzata in chiaro nel binario e viene confrontata direttamente con l'input tramite `strcmp`. Non c'è cifratura, non c'è offuscamento. La stringa è lì, in attesa di essere trovata.

---

## Soluzione

### Step 1 — Il comando `strings`

`strings` è uno strumento che scansiona un file binario alla ricerca di sequenze di caratteri ASCII stampabili di lunghezza minima (per default 4 caratteri) e le stampa una per riga. Non sa nulla di ELF, di sezioni, di codice macchina: legge i byte grezzi e riconosce i pattern di testo.

```bash
$ strings sw-04
```

Tra le centinaia di stringhe prodotte: nomi di librerie, simboli, stringhe di debug, nomi di sezioni; due righe spiccano immediatamente per rilevanza:

```
flag{0cca06f6}
 Qual' la flag? :
 Sbagliato! Prova ancora
 Giusto!
```

La flag è in chiaro. Il programma la memorizza nella sezione `.rodata` e la confronta con l'input usando `strcmp`, se le due stringhe coincidono, stampa `Giusto!`, altrimenti `Sbagliato! Prova ancora`.

### Step 2 — Perché funziona

La flag è una stringa costante nota al momento della compilazione. Il compilatore C, incontrandola nel sorgente, la inserisce nel segmento di dati in sola lettura del binario. `strings` non fa altro che trovarla lì, esattamente dove il compilatore l'ha messa.

Questo è il motivo per cui `strings` è **il primo strumento da eseguire** su qualsiasi binario di una challenge di reverse engineering. Costa zero sforzo e, nel caso più semplice, risolve la challenge in un secondo.

---

### Flag

```
flag{0cca06f6}
```

---

## Conclusioni

Questa challenge introduce il concetto fondamentale che guiderà le prossime challenge della serie: **la sicurezza per oscurità non è sicurezza**.

Memorizzare la flag in chiaro nel binario e confrontarla con `strcmp` è il metodo di verifica più ingenuo possibile. Chiunque abbia accesso al file può estrarre la flag con un singolo comando senza nemmeno eseguire il programma. Nelle challenge successive la verifica diventerà progressivamente più sofisticata: hash, trasformazioni, confronti distribuiti e `strings` da solo non sarà più sufficiente. Ma l'abitudine di eseguirlo come primo passo rimarrà sempre valida: anche quando la flag non è in chiaro, `strings` rivela i messaggi di errore, i nomi delle funzioni, le librerie usate e fornisce una mappa iniziale del comportamento del programma prima ancora di aprire un disassembler.