# A l'envers

**Competition:** FCSC 2022 <br>
**Category:** Misc <br>
**Service:** localhost:4000

---

## Description

>Connectez-vous au service distant et pour chaque chaîne de caractères reçue, vous devez renvoyer la chaîne de caractères contenant les caractères dans l’ordre inverse. Exemple : pour la chaîne ANSSI, vous devez renvoyer ISSNA (note : le respect de la casse est important).

The server sends strings prefixed by `>>> ` and expects them back reversed (case-sensitive). Rounds increase progressively: short words (e.g. `ANSSI`) up to random 32+ character strings. Manual completion is infeasible due to latency and the number of required rounds.

---

## Solution

### 1. Initial reconnaissance

Manual connection with `nc` to fingerprint the protocol:

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

Protocol identified:
- Server sends `>>> <string>`
- Client must reply with `<string[::-1]>`
- Server replies `Well done, continue!` and advances to next round
- Wrong or too slow response → `Ooops. Bye bye.`
- After N correct rounds → flag

### 2. Approach

No vulnerability exists; this is an automation/scripting challenge. The server enforces many fast rounds to prevent manual solving.

Key operation: Python string reversal → `s[::-1]`

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

Example exploit output:

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

## Notes

- `pwntools` is convenient for socket interactions in CTFs: `remote()`, `recvline()`, `sendline()` cover most cases.
- Python slice `s[::-1]` is O(n) and preserves case; no additional logic required.
- Increasing input length is a simple way to force automation without adding cryptographic complexity.
