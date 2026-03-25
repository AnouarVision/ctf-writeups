# backup_unlocker

**Competizione:** ITSCyberGame<br>
**Categoria:** Software<br>
**File:** `backup_unlocker_3`

---

## Descrizione

> Ho dimenticato la password del mio backup e questo sistema di autenticazione proprietario sembra offuscato a dovere. Riesci ad aiutarmi a recuperarla?

Viene fornito un eseguibile ELF 64-bit. L'obiettivo è analizzarlo staticamente per estrarre la password corretta.

---

## Soluzione

### 1. Riconoscimento del file

```bash
file backup_unlocker_3
```

```
ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
```

Il binario non è stripped, i nomi delle funzioni sono preservati. Una prima ispezione con `strings` rivela subito due simboli interessanti:

```
_TIG_EL_eTtb_1_stringEncoder
complex_function
```

Nessuna password in chiaro: le stringhe sono costruite a runtime dall'encoder.

---

### 2. Analisi statica: `_TIG_EL_eTtb_1_stringEncoder`

La funzione è un grande state machine che, a seconda di un ID passato come primo argomento (`edi`), scrive carattere per carattere una stringa in un buffer. La stringa non esiste mai in forma leggibile nel file binario, ogni `movb $0xNN, (%rax)` piazza un singolo byte nel buffer.

Nel `main`, prima del confronto con l'input utente, la funzione viene chiamata con `edi=2`:

```asm
mov $0x2, %edi
lea litStr2, %rsi
call _TIG_EL_eTtb_1_stringEncoder   ; costruisce la stringa di confronto
...
call strcmp@plt                      ; confronta input trasformato vs litStr2
```

Decodificando i `movb` del caso `id=2` si ottiene la stringa target hardcoded:

```
fogp{g3x0w3y_l0nn_n0ae_u4q4}
```

---

### 3. Analisi statica: `complex_function`

Prima del `strcmp`, ogni carattere dell'input utente viene passato a `complex_function(char, posizione)`. Il cuore della funzione (caso `0xb` della state machine) è:

```asm
movsbl -0x14(%rbp), %eax        ; char
lea    -0x61(%rax), %edx         ; char - 'a'
mov    -0x4(%rbp), %eax          ; costante = 3
imul   -0x18(%rbp), %eax         ; 3 * posizione
add    %eax, %edx                ; (char - 'a') + 3 * pos
; divisione modulare per 26 tramite moltiplicazione con magic number 0x4ec4ec4f
; risultato finale:
add    $0x61, %eax               ; + 'a'
```

In Python:

```python
char_enc = (ord(char) - ord('a') + 3 * posizione) % 26 + ord('a')
```

I caratteri non-lowercase (`_`, `{`, `}`, cifre) vengono restituiti invariati.

Si tratta di una **cifratura di Vigenère** con chiave posizionale fissa `k=3`.

---

### 4. Inversione e recupero della password

Per ottenere la password originale basta invertire la trasformazione:

```python
char_orig = (ord(char_enc) - ord('a') - 3 * posizione) % 26 + ord('a')
```

Script completo:

```python
encoded = 'fogp{g3x0w3y_l0nn_n0ae_u4q4}'

def invert(s):
    result = []
    pos = 0
    for c in s:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') - 3 * pos) % 26 + ord('a')))
            pos += 1
        else:
            result.append(c)
            pos += 1
    return ''.join(result)

print(invert(encoded))
```

```
flag{...}
```

**Verifica:**

```bash
echo "flag{...}" | ./backup_unlocker_3
# Backup unlocked!
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

Il binario usa due livelli di offuscamento combinati:

1. **String encoding a runtime**: nessuna stringa leggibile esiste nel file; `_TIG_EL_eTtb_1_stringEncoder` le assembla byte per byte durante l'esecuzione, rendendo inefficace una semplice analisi con `strings` o una ricerca nei segmenti `.rodata`.

2. **Trasformazione dell'input**: `complex_function` applica una variante di cifratura di Vigenere (shift posizionale `k=3`) su ogni lettera dell'input prima del confronto. Il confronto avviene quindi tra la password *trasformata* e la stringa target, non in chiaro.

La debolezza è che entrambe le trasformazioni sono deterministiche e invertibili: nota la stringa target nel binario e nota la legge di trasformazione, è possibile ricavare la password originale puramente per analisi statica, senza eseguire il programma.