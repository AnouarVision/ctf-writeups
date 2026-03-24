# Deep Dive

**Competizione:** ITSCyberGame<br>
**Categoria:** OSINT<br>
**File:** deep_dive_1.db

---

## Descrizione

> Il SOC della CyberSolutions S.r.l. ha rilevato un'anomalia nei log di accesso ai file riservati. Sembra che un insider abbia violato le policy aziendali accedendo a documenti critici poco prima che diversi account venissero bloccati per attività sospette. Abbiamo acquisito un dump del database gestionale interno. Le prime informazioni indicano che il file sottratto è `sistemi_business.pdf`.

Viene fornito un database SQLite `deep_dive_1.db`.

---

## Soluzione

### 1. Analisi della struttura del database

Aprendo il database si trovano 4 tabelle:

| Tabella | Righe | Contenuto |
|---|---|---|
| `employees` | 100 | Dipendenti: username, status, chiave assegnata |
| `system_keys` | 1000 | Chiavi di sistema con ID e valore |
| `file_access_logs` | 1501 | Log degli accessi ai file |
| `session_data` | 2001 | Sessioni utente con token |

### 2. Identificazione dell'insider

Si cercano i record che coinvolgono `sistemi_business.pdf`:

```sql
SELECT * FROM file_access_logs WHERE file_name = 'sistemi_business.pdf';
```

```
access_id: 160 | emp_id: 4864 | file_name: sistemi_business.pdf
```

Un solo accesso, da parte dell'impiegato `emp_id = 4864`. Incrociando con la tabella `employees`:

```sql
SELECT * FROM employees WHERE emp_id = 4864;
```

```
emp_id: 4864 | username: g.benassuti | status: LOCKED | assigned_key: KEY_1542_SIG
```

L'account è **LOCKED**, confermando il blocco post-incidente descritto nella challenge. Tra gli altri file acceduti da questo utente: `passwords.old`, `config.bak`, `notes.txt`.

### 3. Prima metà della flag — chiave in esadecimale

Si recupera il valore della chiave assegnata a `g.benassuti`:

```sql
SELECT key_value FROM system_keys WHERE key_id = 'KEY_1542_SIG';
```

```
666c61677b64347461626173335f
```

Il valore è in esadecimale. Decodificandolo:

```python
bytes.fromhex('666c61677b64347461626173335f').decode()
# → flag{...
```

**Prima metà della flag trovata.**

### 4. Seconda metà della flag — token in base64

Si analizzano le sessioni di `g.benassuti`:

```sql
SELECT session_id, token FROM session_data WHERE emp_id = 4864;
```

I token sembrano base64. Decodificando ognuno, la sessione `650` restituisce testo leggibile:

```python
import base64
base64.b64decode('aXNfbm90X2FfY3IxbWV9').decode()
# → ...}
```

**Seconda metà della flag trovata.**

---

## Flag

```
flag{...}
```

---

## Conclusioni

La flag era nascosta in due posti diversi del database, con due codifiche differenti:

- **Prima parte** nella colonna `key_value` della tabella `system_keys`, codificata in **esadecimale**
- **Seconda parte** nella colonna `token` della tabella `session_data`, codificata in **base64**

La challenge insegna l'importanza dell'analisi forense sui database: ogni campo apparentemente innocuo può nascondere dati codificati con tecniche elementari.