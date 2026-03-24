# Orbital Decay

**Competizione:** ITSCyberGame<br>
**Categoria:** Software<br>
**File:** orbital_decay_5

---

## Descrizione

> Il sistema di dump del nostro satellite ha prodotto questo binario, ma non sembra che contenga nulla di utile. Chissà se è possibile recuperare qualche informazione...

---

## Soluzione

### Passo 1 — Analisi iniziale

```bash
$ file orbital_decay_5
orbital_decay_5: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
dynamically linked, not stripped

$ checksec --file=orbital_decay_5
Partial RELRO   No canary   NX enabled   PIE enabled   38 Symbols
```

Il binario è **not stripped**, i simboli sono presenti, il che aiuta l'analisi. NX è abilitato ma non ci interessa per questa challenge.

### Passo 2 — Analisi con strings

```bash
$ strings orbital_decay_5
--- SATELLITE MEMORY DUMP V4.0 ---
Showing dump diagnostics...
[ERROR] Buffer was captured, but no meaningful data was present.
[ERROR] Nothing to show. Bailing out, you're in your own - good luck.
main
show_diagnostics
SECRET_BEACON
```

`strings` rivela tre simboli interessanti: `main`, `show_diagnostics` e **`SECRET_BEACON`**. Quest'ultimo non appare mai come output del programma, è un simbolo presente ma che non viene mai chiamato.

### Passo 3 — Disassembly di main e show_diagnostics

```bash
$ objdump -d orbital_decay_5
```

```asm
000000000000117c <main>:
    117c:   push   %rbp
    117d:   mov    %rsp,%rbp
    1180:   call   1139 <show_diagnostics>
    1185:   mov    $0x0,%eax
    118a:   pop    %rbp
    118b:   ret

0000000000001139 <show_diagnostics>:
    1139:   push   %rbp
    113a:   mov    %rsp,%rbp
    113d:   lea    0xf0c(%rip),%rax   # 2050 <SECRET_BEACON+0x30>
    1147:   call   puts@plt           # stampa stringa di errore
    114c:   lea    0xf20(%rip),%rax   # 2073 <SECRET_BEACON+0x53>
    1156:   call   puts@plt
    115b:   lea    0xf2e(%rip),%rax   # 2090 <SECRET_BEACON+0x70>
    1165:   call   puts@plt
    116a:   lea    0xf67(%rip),%rax   # 20d8 <SECRET_BEACON+0xb8>
    1174:   call   puts@plt
    117b:   ret
```

`show_diagnostics` stampa solo messaggi di errore, tutti gli indirizzi puntano a offset **dentro** `SECRET_BEACON+0x30` e oltre, saltando completamente l'inizio della sezione.

### Passo 4 — Dump della sezione .rodata

```bash
$ objdump -s -j .rodata orbital_decay_5

Contents of section .rodata:
[raw bytes omitted]
```

All'offset `0x2020` (inizio di `SECRET_BEACON`) si trovano dati con un byte `\x00` dopo ogni carattere, è una stringa **UTF-16LE** (wide string). `strings` non l'ha rilevata perché cerca solo stringhe ASCII consecutive.

Decodificando i byte si ottiene una stringa UTF-16LE che corrisponde a una flag. Non riveliamo qui la flag completa: provate a estrarre e decodificare i byte dalla sezione `.rodata` per ricostruirla.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La flag era codificata come **wide string UTF-16LE** nella sezione `.rodata`, etichettata con il simbolo `SECRET_BEACON`, mai referenziata dalla logica del programma. `show_diagnostics` puntava deliberatamente a offset successivi, saltando il segreto nascosto all'inizio. `strings` non l'ha rilevata perché interpola solo sequenze ASCII, mentre `objdump -s -j .rodata` ha rivelato i byte grezzi e la codifica wide.