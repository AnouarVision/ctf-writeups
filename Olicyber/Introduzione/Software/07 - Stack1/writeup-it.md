# Software 07 - Stack 1

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Questo programma salva la flag sullo stack, tramite delle istruzioni `mov`, e poi esce. Spesso conviene guardare anche il codice disassemblato e non solo il decompilato.

Viene fornito un binario `sw-07`. La flag non è in `.rodata` né in una variabile globale — viene costruita direttamente sullo stack a runtime con istruzioni `mov`.

---

## Perché il decompiler non basta

Ghidra e gli altri decompiler fanno un lavoro straordinario nel ricostruire la logica di alto livello di un programma. Tuttavia, la ricostruzione è un'operazione con perdita di informazioni: il decompiler decide come raggruppare le operazioni, quali tipi assegnare alle variabili, e come rappresentare sequenze di istruzioni elementari. In alcuni casi, come questo, guardare direttamente il disassembly rivela dettagli che il decompilato oscura o aggrega.

La regola pratica è: **il decompiler per capire la struttura, il disassembly per capire i dettagli**.

---

## Analisi del disassembly

Il comando per ottenere il disassembly della sezione `.text` è:

```bash
$ objdump -d -j .text sw-07
```

La funzione `main` inizia a `0x1145`. Dopo il prologo standard (`push rbp`, `mov rbp,rsp`, `sub rsp,0x110`) e il setup del **stack canary** (protezione contro i buffer overflow), appare una sequenza di istruzioni `movb`, move byte, che scrivono costanti immediate direttamente sullo stack:

```asm
115f:  c6 85 f0 fe ff ff 66    movb   $0x66,-0x110(%rbp)
1166:  c6 85 f1 fe ff ff 6c    movb   $0x6c,-0x10f(%rbp)
116d:  c6 85 f2 fe ff ff 61    movb   $0x61,-0x10e(%rbp)
1174:  c6 85 f3 fe ff ff 67    movb   $0x67,-0x10d(%rbp)
117b:  c6 85 f4 fe ff ff 7b    movb   $0x7b,-0x10c(%rbp)
1182:  c6 85 f5 fe ff ff 66    movb   $0x66,-0x10b(%rbp)
1189:  c6 85 f6 fe ff ff 63    movb   $0x63,-0x10a(%rbp)
1190:  c6 85 f7 fe ff ff 32    movb   $0x32,-0x109(%rbp)
1197:  c6 85 f8 fe ff ff 66    movb   $0x66,-0x108(%rbp)
119e:  c6 85 f9 fe ff ff 34    movb   $0x34,-0x107(%rbp)
11a5:  c6 85 fa fe ff ff 34    movb   $0x34,-0x106(%rbp)
11ac:  c6 85 fb fe ff ff 39    movb   $0x39,-0x105(%rbp)
11b3:  c6 85 fc fe ff ff 62    movb   $0x62,-0x104(%rbp)
11ba:  c6 85 fd fe ff ff 7d    movb   $0x7d,-0x103(%rbp)
11c1:  c6 85 fe fe ff ff 00    movb   $0x0, -0x102(%rbp)
```

Ogni istruzione scrive un singolo byte a un offset crescente rispetto a `rbp`. Gli offset partono da `-0x110` e avanzano di 1 a ogni istruzione, è esattamente una stringa ASCII costruita carattere per carattere sullo stack.

---

## Lettura della flag

Leggendo i valori immediati nell'ordine in cui vengono scritti:

| Offset      | Valore hex | Carattere ASCII |
|-------------|-----------|-----------------|
| -0x110(rbp) | `0x66`    | `f`             |
| -0x10f(rbp) | `0x6c`    | `l`             |
| -0x10e(rbp) | `0x61`    | `a`             |
| -0x10d(rbp) | `0x67`    | `g`             |
| -0x10c(rbp) | `0x7b`    | `{`             |
| -0x10b(rbp) | `0x66`    | .           |
| -0x10a(rbp) | `0x63`    | .           |
| -0x109(rbp) | `0x32`    | .           |
| -0x108(rbp) | `0x66`    | .          |
| -0x107(rbp) | `0x34`    | .          |
| -0x106(rbp) | `0x34`    | .           |
| -0x105(rbp) | `0x39`    | .           |
| -0x104(rbp) | `0x62`    | .           |
| -0x103(rbp) | `0x7d`    | `}`             |
| -0x102(rbp) | `0x00`    | terminatore     |

```python
bytes_seq = [0x66,0x6c,0x61,0x67,0x7b,0x66,0x63,0x32,0x66,0x34,0x34,0x39,0x62,0x7d]
print(bytes(bytes_seq).decode())
# flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge introduce due concetti fondamentali per il reverse engineering di binari:

**Lo stack come area di lavoro temporanea**: le variabili locali di una funzione non vivono in sezioni del file ELF come `.rodata` o `.data`, ma vengono allocate sullo stack a runtime, nell'area compresa tra `rbp` e `rsp`. Una stringa costruita con `movb` consecutivi non esiste nel file come sequenza contigua di byte, esiste solo durante l'esecuzione. È per questo che né `strings` né `objdump -s` la troverebbero: bisogna leggere il codice.

**Il valore del disassembly grezzo**: il decompiler di Ghidra avrebbe mostrato qualcosa come `local_110 = "flag{fc2f449b}"`, aggregando le `movb` in un'inizializzazione di stringa. Corretto nella semantica, ma opaco nella meccanica. Il disassembly mostra invece esattamente cosa succede a livello di CPU: ogni byte viene scritto individualmente, istruzione per istruzione. In situazioni più complesse: offuscamento, self-modifying code, shellcode. Questa visibilità a basso livello diventa indispensabile.