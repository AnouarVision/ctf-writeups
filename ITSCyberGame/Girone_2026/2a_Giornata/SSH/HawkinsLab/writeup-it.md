# Hawkins Lab

**Competizione:** ITSCyberGame<br>
**Categoria:** SSH<br>
**File:** key2<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Hey Dustin, sono Lucas, ho trovato questa private key per accedere ad un server del laboratorio di hawkins, ma c'è qualcosa che non va con il contenuto... credo che le minuscole si siano capovolte...
>
> `pnsʇᴉu ɟɐ ɾoƃƃᴉuƃ ɐ ɥɐʍʞᴉus ɔou bnǝllɐ qopʎɔɐɯ ǝxʇɹɐ dǝɹ sodɹɐʌʌᴉʌǝuzɐ`

Il tema è Stranger Things: bisogna decodificare una chiave SSH con caratteri upside-down, connettersi al server e trovare la flag nascosta.

---

## Soluzione

### 1. Decodifica del messaggio hint

Il testo hint è scritto in "upside-down text" — i caratteri vengono letti anche al contrario. Decodificandolo si ottiene:

```
dustin fa jogging a hawkins con quella bodycam extra per sopravvivenza
```

### 2. Decodifica della chiave SSH

La chiave `key2` contiene caratteri Unicode upside-down al posto delle minuscole. La mappa di sostituzione ha due categorie:

**Caratteri Unicode speciali:**

| Upside-down | Normale |
|---|---|
| `ɐ` | a |
| `ɔ` | c |
| `ǝ` | e |
| `ɟ` | f |
| `ƃ` | g |
| `ɥ` | h |
| `ᴉ` | i |
| `ɾ` | j |
| `ʞ` | k |
| `ɯ` | m |
| `ɹ` | r |
| `ʇ` | t |
| `ʌ` | v |
| `ʍ` | w |
| `ʎ` | y |

**Lettere ASCII che si invertono a vicenda** (il punto critico):

| Upside-down | Normale |
|---|---|
| `n` | u |
| `u` | n |
| `b` | q |
| `q` | b |
| `p` | d |
| `d` | p |

Questo secondo gruppo è il trabocchetto: `n`, `b`, `p` sono caratteri base64 validi, quindi una decodifica parziale che li ignora produce una chiave con check bytes errati e KDF corrotto.

Script di decodifica:

```python
full_flip = {
    'ƃ': 'g', 'ǝ': 'e', 'ɐ': 'a', 'ɔ': 'c', 'ɟ': 'f',
    'ɥ': 'h', 'ᴉ': 'i', 'ɯ': 'm', 'ɹ': 'r', 'ɾ': 'j',
    'ʇ': 't', 'ʌ': 'v', 'ʍ': 'w', 'ʎ': 'y', 'ʞ': 'k',
    'n': 'u', 'u': 'n', 'b': 'q', 'q': 'b', 'p': 'd', 'd': 'p',
}

with open('key2', 'r') as f:
    original = f.read()

lines = original.strip().split('\n')
fixed_lines = []
for line in lines:
    if line.startswith('-----'):
        fixed_lines.append(line)
    else:
        fixed_line = ''.join(full_flip.get(ch, ch) for ch in line)
        fixed_lines.append(fixed_line)

with open('key2_fixed', 'w') as f:
    f.write('\n'.join(fixed_lines) + '\n')
```

### 3. Connessione SSH

```bash
chmod 600 key2_fixed
ssh -i key2_fixed -p <port_number> hawkins-lab@sfide.itscybergame.it
```

Il server risponde con `Welcome to the Upside Down` e tutto l'output è in upside-down.

### 4. Esplorazione del server

Una volta connessi, il server risponde con `Welcome to the Upside Down` e tutto l'output è in upside-down. I comandi si inviano normalmente ma l'output va decodificato.

Il comando `ls -la` mostra una serie di file a tema Stranger Things nella home directory:

```
EMERGENCY_PROCEDURES.txt        gate
FACILITY_FLOOR_PLAN.txt         gate_cctv
MKULTRA_PROJECT_INDIGO.txt      internal_memo_containment.txt
SUBJECT_011_PROFILE.txt         meeting_minutes_19831105.txt
autopsy_report_DR_ELLIS.txt     personnel_directory.txt
camera_log_831106.txt           psychological_evaluation_011.txt
classified_access_codes.txt     security_incident_report_831106.txt
dimensional_research_notes.txt  sys_log_november_1983.log
experiment_log_19831102.txt
```

Sono presenti anche due binari: `gate` (eseguibile) e `gate_cctv` (formato non compatibile con l'architettura del server).

Eseguendo `./gate` il server risponde con un messaggio a tema:

```
╔══════════════════════════════════════╗
║  Reality Stabilized - Welcome Back!  ║
╚══════════════════════════════════════╝
The Upside Down fades away... You're back in Hawkins!
```

I file `.txt` contengono documenti fittizi ambientati nell'universo di Stranger Things (log di sistema del laboratorio, profili dei soggetti, memo interni, rapporti di sicurezza), nessuno contenente la flag.

L'output upside-down rende difficile la lettura manuale. Tra i file analizzati:

- `classified_access_codes.txt`: codici di accesso alle varie aree del laboratorio, combinazioni di casseforti
- `internal_memo_containment.txt`: memo interno sulla fuga del Soggetto 011
- `sys_log_november_1983.log`: log di sistema con la cronologia degli eventi del novembre 1983
- `camera_log_831106.txt`: footage delle telecamere durante la fuga
- `SUBJECT_011_PROFILE.txt`: profilo classificato del Soggetto 011

### 5. Ricerca della flag

Poiché la navigazione manuale dell'output upside-down è complessa, si usa `grep -r` per cercare direttamente il pattern della flag in modo ricorsivo su tutta la home:

```bash
grep -r "flag{" ~
```

Output:

```
/home/hawkins-lab/.nuclear_password:flag{...}
```

Il file `.nuclear_password` è un file nascosto che non era immediatamente evidente tra i file elencati. `grep -r` ha trovato la flag cercando direttamente il contenuto invece di navigare manualmente la struttura delle directory.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge richiede di riconoscere e invertire correttamente l'upside-down text applicato a una chiave SSH. Il punto critico è che alcune lettere ASCII (`n↔u`, `b↔q`, `d↔p`) si invertono a vicenda e sono anche caratteri base64 validi, ignorarle produce una chiave con struttura interna corrotta. Una volta connessi, il server risponde in upside-down ma i comandi si inviano normalmente; `grep -r` permette di trovare la flag nel file nascosto `.nuclear_password`.