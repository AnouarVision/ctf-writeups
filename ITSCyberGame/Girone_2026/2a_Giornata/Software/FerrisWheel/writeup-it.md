# ferris_wheel

**Competizione:** ITSCyberGame<br>
**Categoria:** Software<br>
**File:** ferris_wheel_2

---

## Descrizione

> Qualcuno ha avuto la fantastica idea di riscrivere il validatore dei biglietti in Rust per renderlo "memory safe", ma ora sembra che anche gli input facciano uno strano giro di giostra...

Il nome è un doppio riferimento: Ferris è la mascotte di Rust, e il "giro di giostra" è un hint sull'iteratore `.cycle()` usato internamente.

---

## Analisi del binario

```bash
file ferris_wheel_2
# ELF 64-bit LSB pie executable, x86-64, with debug_info, not stripped

checksec --file=ferris_wheel_2
# Full RELRO | No canary | NX enabled | PIE enabled | 1222 Symbols
```

Il binario è compilato in Rust con simboli di debug, il che rende l'analisi più semplice. Eseguendolo:

```
Please present your Ticket for the Ride:
AAAA
error[E6769]: Mismatched types. Expected 'Ticket', found 'Garbage'.
```

Dall'output delle stringhe si identificano subito le funzioni rilevanti:

```
_ZN12ferris_wheel10check_flag17he73db58859bcfe08E
_ZN12ferris_wheel4main17hb98cabaa180c18cfE
input
clean_input
```

E i tipi Rust significativi:

```
Bytes
cycle
next<core::iter::adapters::zip::Zip<core::str::iter::Bytes,
     core::iter::adapters::cycle::Cycle<core::slice::iter::Iter<u8>>>, ...>
```

La presenza di `Bytes`, `zip` e `cycle` suggerisce uno schema di cifratura con chiave ciclica.

---

## Reverse engineering di check_flag

Disassemblando la funzione `check_flag` (offset `0x19090`):

```
19090: sub $0x148, %rsp
190b1: call str::len              ; controlla lunghezza
190b6: cmp $0x1d, %rax            ; deve essere 29 (0x1d)
190ba: jne 19170                  ; se != 29 -> ritorna false

190ca: call str::bytes            ; input.bytes()
190e0: mov $0x6, %esi             ; chiave di 6 bytes
190d9: lea -0xf4b0(%rip), %rdi   ; puntatore alla chiave (0x9c30)
190f5: call Iterator::cycle       ; key.iter().cycle()

19114: call Iterator::zip         ; zip(input.bytes(), key.cycle())
19129: call Iterator::map         ; map(|(a,b)| a + b)

19135: mov $0x1d, %esi            ; 29 bytes attesi
1913a: lea -0xf522(%rip), %rdi   ; puntatore ai bytes attesi (0x9c13)
19159: call Iterator::zip         ; zip(mapped, expected)
19163: call Iterator::all         ; all(|(a,b)| a == b)
```

La seconda closure (offset `0x17c20`) implementa:

```rust
|(input_byte, key_byte)| (input_byte + key_byte) & 0xff
```

Quindi la logica è:

```
input[i] + key[i % 6] == expected[i]
```

---

## Estrazione di chiave e bytes attesi

Dalla sezione `.rodata` (VMA `0x8060`, file offset `0x8060`):

```python
with open('ferris_wheel_2', 'rb') as f:
    data = f.read()

expected = data[0x9c13:0x9c13+29]
key      = data[0x9c30:0x9c30+6]
```

Valori trovati:
- **Chiave** (6 bytes): `42 13 37 66 01 99`
- **Expected** (29 bytes): `a8 7f 98 cd 7c fc bb 76 68 97 64 f8 73 87 6a d8 35 0d 72 85 96 d3 35 fd b0 46 aa d9 7e`

---

## Decifratura

Invertendo la trasformazione:

```python
flag = bytes((expected[i] - key[i % 6]) % 256 for i in range(29))
print(flag.decode())
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge usa un cifrario additivo con chiave ciclica di 6 bytes implementato tramite gli iteratori Rust `.bytes()`, `.cycle()`, `.zip()` e `.map()`. La struttura è leggibile direttamente dal disassembly grazie ai simboli di debug lasciati nel binario. La decifratura si riduce a sottrarre la chiave modulare dai bytes attesi hardcoded nel binario.