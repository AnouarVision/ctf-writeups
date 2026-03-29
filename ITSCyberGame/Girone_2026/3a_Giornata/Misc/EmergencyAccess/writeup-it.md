# Emergency Access

**Competizione:** ITSCyberGame
**Categoria:** Misc
**Servizio:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

Terminale legacy di emergenza con shell ristrittiva. Il sistema espone solo pochi comandi documentati, tutti bloccati da una modalità DEBUG. L'obiettivo è attivare la modalità di manutenzione nascosta e recuperare i log di sistema contenenti la flag.

---

## Soluzione

### 1. Ricognizione iniziale

Connessione via netcat al servizio:

```bash
ncat sfide.itscybergame.it <port_number>
```

Output del banner:

```
--- Benvenuto nel Terminale di Emergenza v1.0 ---
Digitare 'help' per i comandi disponibili.
restricted-sh> help
Comandi disponibili: ls, exit, status
```

Tutti i comandi documentati restituiscono:

```
ERRORE: Accesso negato. Modalita' DEBUG necessaria.
```

### 2. Enumerazione comandi nascosti

Il comando `help` lista solo `ls`, `exit`, `status`, ma la shell potrebbe accettare comandi non documentati. Si esegue fuzzing manuale su keyword comuni legate a modalità di debug/manutenzione:

```bash
debug       # nessuna risposta
debug on    # nessuna risposta
enable debug # nessuna risposta
maintenance  # nessuna risposta
mode debug   # nessuna risposta
DEBUG        # → ATTIVAZIONE
```

### 3. Bypass: attivazione modalità manutenzione

Il comando `DEBUG` (case-sensitive, tutto maiuscolo) non è documentato in `help` ma è presente nella shell:

```
restricted-sh> DEBUG
*** MODALITA' MANUTENZIONE ATTIVATA ***
Inserire codice di sblocco (Suggerimento: 2+2*2):
```

### 4. Risoluzione challenge matematica

Il sistema richiede un codice numerico. Il suggerimento `2+2*2` è un classico test di operator precedence:

```
2 + 2*2
= 2 + 4      # moltiplicazione prima (precedenza)
= 6
```

```
restricted-sh> 6
Codice accettato. Accesso ai log di sistema garantito.
Log 05/03/2026: Recupero flag di sistema... flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

Due vulnerabilità concatenate:

1. **Hidden command disclosure**: la shell restrittiva non espone tutti i comandi accettati tramite `help`. Il fuzzing su keyword comuni (`DEBUG`, `MAINTENANCE`, `ADMIN`, ecc.) è sufficiente a scoprire comandi nascosti non documentati.

2. **Weak authentication**: il "codice di sblocco" è un semplice calcolo matematico con operatori standard. Nessuna entropia reale, nessun meccanismo di lockout.