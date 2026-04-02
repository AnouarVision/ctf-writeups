# À l'aise

**Competizione:** FCSC 2022 (intro)
**Categoria:** Crypto

---

## Descrizione
>Cette épreuve vous propose de déchiffrer un message chiffré avec la méthode inventée par Blaise de Vigénère. La clé est FCSC et le message chiffré est : Gqfltwj emgj clgfv ! Aqltj rjqhjsksg ekxuaqs, ua xtwk
n'feuguvwb gkwp xwj, ujts f'npxkqvjgw nw tjuwcz
ugwygjtfkf qz uw efezg sqk gspwonu. Jgsfwb-aqmu f
Pspygk nj 29 cntnn hqzt dg igtwy fw xtvjg rkkunqf.

> Le flag est le nom de la ville mentionnée dans ce message.

Viene fornito un messaggio cifrato con il cifrario di Vigenère e la chiave nota `FCSC`. L'obiettivo è decifrare il testo e identificare il nome della città menzionata nel plaintext, da racchiudere nel formato `FCSC{...}`.

---

## Soluzione

### 1. Ricognizione iniziale

Il testo cifrato è:

```
Gqfltwj emgj clgfv ! Aqltj rjqhjsksg ekxuaqs, ua xtwk
n'feuguvwb gkwp xwj, ujts f'npxkqvjgw nw tjuwcz
ugwygjtfkf qz uw efezg sqk gspwonu. Jgsfwb-aqmu f
Pspygk nj 29 cntnn hqzt dg igtwy fw xtvjg rkkunqf.
```

Chiave nota: `FCSC`. Nessun cracking necessario → decifratura diretta.

### 2. Analisi del cifrario

Il cifrario di Vigenère cifra ogni carattere alfabetico con uno shift ciclico basato sulla chiave:

$$C_i = (P_i + K_{i \bmod |key|}) \bmod 26$$

La decifratura inverte l'operazione:

$$P_i = (C_i - K_{i \bmod |key|}) \bmod 26$$

**Attenzione**: i caratteri non alfabetici (`!`, `'`, spazi, newline) vengono saltati senza incrementare il contatore di chiave `ki`.

### 3. Exploit

```python
def vigenere_decrypt(ct, key):
    key = key.upper()
    pt = []
    ki = 0
    for c in ct:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - ord('A')
            base = ord('A') if c.isupper() else ord('a')
            pt.append(chr((ord(c) - base - shift) % 26 + base))
            ki += 1
        else:
            pt.append(c)
    return ''.join(pt)

ct = """Gqfltwj emgj clgfv ! Aqltj rjqhjsksg ekxuaqs, ua xtwk
n'feuguvwb gkwp xwj, ujts f'npxkqvjgw nw tjuwcz
ugwygjtfkf qz uw efezg sqk gspwonu. Jgsfwb-aqmu f
Pspygk nj 29 cntnn hqzt dg igtwy fw xtvjg rkkunqf."""

print(vigenere_decrypt(ct, "FCSC"))
```

**Output:**

```
Bonjour cher eleve ! Votre progression scolaire, au vu
d'elements bien sur, nous n'envisageons de changer
votre orientation ou de cycle que gracieux. Rendez-vous a
Nantes le 29 avril pour de feter de votre passion.
```

La città menzionata nel testo è **Nantes**.

---

## Flag

`Nantes`

---

## Conclusioni

Challenge introduttiva al cifrario di Vigenère. Con la chiave nota la soluzione è banale: basta implementare la decifratura standard prestando attenzione a saltare i caratteri non alfabetici nel conteggio dell'indice di chiave. Il plaintext è un testo in francese che menziona esplicitamente la città di **Nantes**.