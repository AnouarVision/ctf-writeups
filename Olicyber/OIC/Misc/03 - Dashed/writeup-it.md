# Dashed

**Competizione:** OliCyber
**Categoria:** Misc
**File:** `dashed.txt`

---

## Descrizione

> *"Questa mattina mi è arrivata una e-mail che conteneva questo messaggio, ma non riesco a capire di cosa si tratti. Puoi aiutarmi a decifrarlo?"*

Un file di testo contenente una sequenza di punti e trattini. L'obiettivo è decodificare il messaggio e trovare la flag.

---

## Soluzione

### 1. Ricognizione iniziale

Il file contiene esclusivamente `.`, `-` e `,` separati da spazi. Riconoscimento immediato: **codice Morse**. Il titolo "Dashed" è un ulteriore hint (dash = trattino).

### 2. Layer di codifica

Il messaggio è codificato su **4 layer** annidati:

```
Morse → Hex (0x30/0x31) → Binario → Base64 → ROT13
```

**Layer 1 — Morse:**
Decodificando il Morse si ottiene una sequenza di valori esadecimali separati da virgole:
```
0X30,0X31,0X31,0X30,0X30,0X30,0X31,0X31,...
```

**Layer 2 — Hex → Binario:**
`0x30` = `'0'`, `0x31` = `'1'`. La sequenza hex rappresenta una stringa binaria:
```
011000110011001101101100...
```

**Layer 3 — Binario → Base64:**
Convertendo i bit in ASCII (gruppi da 8) si ottiene una stringa Base64:
```
c3ludHtDQUVTQVJfTUUhLWwwaF9UMDdfdkdfZTF0dUchfQo=
```

**Layer 4 — Base64 → ROT13:**
Decodificando il Base64 si ottiene testo ROT13:
```
synt{CAESAR_ME!-l0h_T07_vG_e1tuG!}
```

Applicando ROT13 si ottiene la flag.

### 3. Script Python

```python
import re, base64, codecs

MORSE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '--..--': ',', '.-.-.-': '.', '..--..': '?',
}

# Layer 1: Morse → stringa hex
text = open('dashed.txt').read().strip()
tokens = text.split(' ')
morse_decoded = ''.join(MORSE.get(t, '') for t in tokens)

# Layer 2: hex (0X30/0X31) → stringa binaria
hex_vals = re.findall(r'0X([0-9A-F]{2})', morse_decoded)
binary_str = ''.join(chr(int(h, 16)) for h in hex_vals)

# Layer 3: binario → Base64 string
b64 = ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str)-7, 8))

# Layer 4: Base64 → ROT13 → flag
rot13 = base64.b64decode(b64).decode()
flag = codecs.decode(rot13.strip(), 'rot13')
print(flag)
```

---

## Flag

`flag{...}`

---

## Conclusioni

Challenge di encoding multi-layer classica. La parola chiave è riconoscere ogni strato nell'ordine corretto: il titolo "Dashed" suggerisce Morse, i valori `0x30`/`0x31` suggeriscono binario mascherato da hex, il padding `=` finale tradisce il Base64, e il prefisso `synt{` è il signature tipico di ROT13 su `flag{`.