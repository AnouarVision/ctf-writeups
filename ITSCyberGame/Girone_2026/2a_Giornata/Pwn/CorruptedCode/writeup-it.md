# corrupted_code

**Competizione:** ITSCyberGame<br>
**Categoria:** Pwn<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Questo dannatissimo computer ha corrotto un'altra volta il contenuto della RAM. Riesci ad aiutarmi a decifrare i miei dati usando i dump prodotti dal mio software di recupero? Ti verranno fornite 100 stringhe che contengono diverse istanze di istruzioni `add(x,y)`, `sub(x,y)` e `mul(x,y)`; calcola il risultato di ciascuna ignorando il testo corrotto e rispondi di volta in volta con la somma cumulativa.

Il server invia 100 stringhe di testo corrotto. In ogni stringa bisogna identificare le istruzioni valide, calcolarne il risultato e rispondere con il valore corretto ad ogni round.

---

## Analisi del protocollo

Connettendosi al server si riceve un dump di esempio:

```
add(X,Y)*foradd( 34,56)=sub(12 ,34)defadd(X,Y)addd(90,12)add(52,45)mul(13,90)...
```

Il server risponde con `Invalid input! The correct answer was: 1524` se si sbaglia.

Analizzando manualmente il dump di esempio si capiscono le regole di validità:

| Istruzione | Valida? | Motivo |
|---|---|---|
| `add(52,45)` | SI | Forma corretta |
| `addd(90,12)` | NO | Suffisso extra (`addd`) |
| `add(X,Y)` | NO | Argomenti non interi |
| `add(12,34,56)` | NO | Tre argomenti |
| `add( 34,56)` | NO | Spazio nell'argomento |
| `add(56,78]` | NO | Parentesi errata |
| `fromsub(53,62)` | SI | Prefisso ok, nome corretto |
| `sub(78_90)` | NO | Underscore nell'argomento |

La regola chiave: il nome **non deve avere suffissi** letterali (`addd`, `subb`), ma può avere qualsiasi prefisso. Gli argomenti devono essere interi puri senza spazi.

---

## Soluzione

### Regex corretta

```python
PATTERN = r'(add|sub|mul)(?![a-zA-Z_])\((-?\d+),(-?\d+)\)'
```

- `(?![a-zA-Z_])`: lookahead negativo, blocca suffissi come `addd`, `subb`
- `(-?\d+)`: intero puro, senza spazi
- Nessun lookbehind: `fromsub(...)` è valido

Verifica sul dump di esempio:

```python
# Matches: add(52,45), mul(13,90), sub(53,62), add(25,2),
#          sub(93,57), add(6,48), sub(60,64), mul(1,4),
#          add(70,54), sub(72,47)
# Total: 1524
```

### Script

Lo script è fornito separatamente nel file `corrupted_code.py` presente nella cartella della challenge. Eseguire lo script con:

```
python3 corrupted_code.py
```

Lo script connette al server, applica la regex mostrata sopra e invia le risposte automaticamente; il sorgente completo è disponibile in `corrupted_code.py` per chi volesse eseguire o modificare l'automazione.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge testa la capacità di fare parsing robusto su testo rumoroso. Il punto critico era capire esattamente quali istruzioni considerare valide: il lookahead negativo `(?![a-zA-Z_])` blocca i suffissi extra (`addd`, `subb`), mentre i prefissi come `fromsub` o `computeadd` sono permessi perché il nome della funzione rimane corretto. Gli argomenti devono essere interi puri senza spazi o caratteri speciali.