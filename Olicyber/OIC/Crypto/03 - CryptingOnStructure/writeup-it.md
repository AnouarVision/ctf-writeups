# Crypting on Structure

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>

---

## Descrizione

> Decodificami!
>
`AAAABAAAAAAAABAABBBAABBABABAAABAABABAABAABBBABAABBAAAAABAABABAABBBBAAA`
>
>La flag non è nel formato standard, per cui decripta ed inserisci il messaggio al posto dei puntini: `flag{...}`

---

## Soluzione

### Step 1 — Analisi del testo cifrato

Il testo è composto esclusivamente da due simboli: `A` e `B`. Questo suggerisce una codifica binaria. Il titolo *"Crypting on Structure"* è una hint: non è la sequenza dei simboli a portare informazione, ma la loro **struttura**, ovvero come vengono raggruppati.

Contando i caratteri: 70 totali, divisibili per 5 → **14 gruppi da 5 simboli**.

---

### Step 2 — Cifrario di Bacone

Il **Cifrario di Bacone** (Francis Bacon, 1605) è una delle prime forme di steganografia binaria. Ogni lettera dell'alfabeto viene codificata con una sequenza di 5 simboli scelti tra due valori (qui `A` e `B`):

```
A = AAAAA    (00000 = 0)
B = AAAAB    (00001 = 1)
C = AAABA    (00010 = 2)
D = AAABB    (00011 = 3)
...
Z = BBAAB    (11001 = 25)
```

Con `A = 0` e `B = 1`, ogni gruppo da 5 è semplicemente un numero binario a 5 bit che indica la posizione della lettera nell'alfabeto.

---

### Step 3 — Decifratura

Dividendo il testo in gruppi da 5:

```
AAAAB AAAAA AAABA ABBBA ABBAB ABAAA BAABA BAABA ABBBA BAABB AAAAA BAABA BAABB BBAAA
```

Convertendo ogni gruppo in decimale e poi in lettera:

```
AAAAB = 00001 =  1 → B
AAAAA = 00000 =  0 → A
AAABA = 00010 =  2 → C
ABBBA = 01110 = 14 → O
ABBAB = 01101 = 13 → N
ABAAA = 01000 =  8 → I
BAABA = 10010 = 18 → S
BAABA = 10010 = 18 → S
ABBBA = 01110 = 14 → O
BAABB = 10011 = 19 → T
AAAAA = 00000 =  0 → A
BAABA = 10010 = 18 → S
BAABB = 10011 = 19 → T
BBAAA = 11000 = 24 → Y
```

Risultato: **`BACONISSOTASTY`**

---

### Step 4 — Script di decifratura

```python
def bacon_decrypt(text):
    groups = [text[i:i+5] for i in range(0, len(text), 5)]
    result = ""
    for group in groups:
        val = int(group.replace('A', '0').replace('B', '1'), 2)
        result += chr(val + ord('A'))
    return result

ciphertext = "AAAABAAAAAAAABAABBBAABBABABAAABAABABAABAABBBABAABBAAAAABAABABAABBBBAAA"
print(bacon_decrypt(ciphertext))
# Output: BACONISSOTASTY
```

---

### Flag

```
flag{baconissotasty}
```

---

## Conclusioni

Questa challenge dimostra che:

1. **Due simboli in gruppi da 5 → Bacone**: è il pattern riconoscibile di questo cifrario classico
3. **Il cifrario di Bacone è steganografico**: storicamente usato per nascondere messaggi segreti dentro testi apparentemente innocui sostituendo due font tipografici diversi