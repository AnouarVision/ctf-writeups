# A l'envers

**Competizione:** FCSC 2022 (intro)<br>
**Categoria:** Misc <br>
**Servizio:** localhost:4000

---

## Descrizione

>Connectez-vous au service distant et pour chaque chaîne de caractères reçue, vous devez renvoyer la chaîne de caractères contenant les caractères dans l’ordre inverse. Exemple : pour la chaîne ANSSI, vous devez renvoyer ISSNA (note : le respect de la casse est important).

Il server invia stringhe di caratteri precedute da `>>> ` e richiede di rispedirle invertite (rispettando la casse). I round aumentano progressivamente: si parte da parole brevi (es. `ANSSI`) fino a stringhe casuali da 32+ caratteri. Impossibile completare manualmente per via della latenza e del numero di round richiesti.

---

## Soluzione

### 1. Ricognizione iniziale

Connessione manuale con `nc` per fingerprinting del protocollo:

```
$ nc localhost 4000
>>> ANSSI
ISSNA
Well done, continue!
>>> Agence
ecnegA
Well done, continue!
...
Ooops. Bye bye.
```

**Protocollo identificato:**
- Il server invia `>>> <stringa>`
- Il client deve rispondere con `<stringa[::-1]>`
- Il server risponde `Well done, continue!` e passa al round successivo
- Risposta errata o troppo lenta → `Ooops. Bye bye.`
- Dopo N round corretti → flag

### 2. Meccanismo

Nessuna vulnerabilità: è una challenge di **scripting/automazione**. Il server richiede la gestione di decine di round in rapidissima successione, unica difesa contro soluzioni manuali.

Operazione chiave: inversione stringa in Python → `s[::-1]`

### 3. Exploit

```python
#!/usr/bin/env python3
from pwn import *

conn = remote("localhost", 4000)

while True:
    line = conn.recvline().decode().strip()
    if line.startswith(">>> "):
        conn.sendline(line[4:][::-1].encode())
    elif "FCSC{" in line:
        print(line)
        break
    elif "Bye" in line:
        break

conn.close()
```

**Output dell'exploit:**

```
[+] Opening connection to localhost on port 4000: Done
FCSC{...}
[*] Closed connection to localhost port 4000
```

---

## Flag

```
FCSC{...}
```

---

## Conclusioni

- `pwntools` è lo strumento ideale per interazioni socket in CTF: `remote()`, `recvline()`, `sendline()` coprono il 90% dei casi
- La slice inversa Python `s[::-1]` è O(n) e case-preserving, nessuna necessità di logica aggiuntiva
- Scalare la difficoltà con stringhe più lunghe è una tecnica classica per scoraggiare soluzioni manuali senza aggiungere complessità crittografica