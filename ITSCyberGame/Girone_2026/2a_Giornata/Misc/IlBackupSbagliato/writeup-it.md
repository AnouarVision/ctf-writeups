# Il backup sbagliato

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** backup_server.tar.gz

---

## Descrizione

> Un server di backup legacy ha avuto un restore incompleto. Ti forniamo un export del filesystem. Analizza la struttura e trova la flag.

Viene fornito un archivio contenente un export parziale di filesystem. L'obiettivo è analizzare la struttura e recuperare la flag.

---

## Soluzione

### 1. Estrazione e analisi del filesystem

```bash
tar -xzf backup_server.tar.gz
```

La struttura del filesystem estratto:

```
backup_server/
├── tmp/
│   ├── .backup.enc          ← file cifrato nascosto
│   └── restore.log
├── var/backups/
│   └── backup.sh            ← script con password hardcoded
├── etc/cron.d/
│   └── backup_job
└── home/sysadmin/
    ├── note.txt
    └── .hidden_backup/
        └── old_credentials.txt
```

### 2. Raccolta degli indizi

**`note.txt`** fornisce i primi hint:
```
- Lo script in /var/backups/backup.sh potrebbe avere credenziali obsolete.
- Controllare i log di restore in /tmp/restore.log.
```

**`restore.log`** conferma che c'è un file non rimosso:
```
[2024-08-02 03:10:45] Pulizia incompleta: encrypted dump non rimosso.
[2024-08-02 03:10:45] Suggerimento: cercare file nascosti in /tmp (nome simile a .backup.*)
```

**`old_credentials.txt`** rivela la password:
```
Servizio: backup_restore
Utente: backup-operator
Password storico restore: Summer2024!
Nota: rimuovere credenziali hardcoded dallo script backup.sh
```

**`backup.sh`** conferma la password e il comando per decifrare:
```bash
ARCHIVE_IN="/tmp/.backup.enc"
RESTORE_OUT="/tmp/restore_output.tar.gz"
PASS="Summer2024!"  # TODO: eliminare hardcoded password

openssl enc -d -aes-256-cbc -pbkdf2 -in "$ARCHIVE_IN" -out "$RESTORE_OUT" -pass pass:"$PASS"
```

### 3. Decifratura del backup

Con tutti gli elementi raccolti si esegue il comando di decrypt:

```bash
openssl enc -d -aes-256-cbc -pbkdf2 \
  -in backup_server/tmp/.backup.enc \
  -out restore_output.tar.gz \
  -pass pass:"Summer2024!"
```

Il file decifrato è un archivio tar.gz contenente `flag.txt`:

```bash
tar -xzf restore_output.tar.gz -O flag.txt
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge insegna tre lezioni fondamentali sulla sicurezza dei backup. Prima: le **credenziali hardcoded** negli script non vanno mai lasciate in produzione, la password `Summer2024!` era presente sia in `backup.sh` che in `old_credentials.txt`. Seconda: i **file temporanei cifrati** non rimossi correttamente possono esporre dati sensibili. Terza: i **log di sistema** non dovrebbero mai contenere suggerimenti su dove trovare file nascosti.