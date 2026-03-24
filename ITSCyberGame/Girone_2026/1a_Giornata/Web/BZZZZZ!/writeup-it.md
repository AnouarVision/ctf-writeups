# BZZZZZ!

**Competizione:** ITSCyberGame<br>
**Categoria:** Web<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Spero ti piacciano tanto le API :)

Una challenge a catena di endpoint HTTP. Si parte da `/api/start` e si arriva a `/api/flag` seguendo le indicazioni ad ogni step.

---

## Soluzione

### 1. Avvio della sessione

```bash
curl -v -L -c cookies.txt -b cookies.txt "http://sfide.itscybergame.it:<port_number>/api/start"
```
Spiegazione dei flag usati:

- `-v`: abilita la modalità verbose; stampa informazioni di debug, inclusi header di richiesta e risposta.
- `-L`: segue automaticamente redirect HTTP (3xx), utile quando il server risponde con `302`.
- `-c cookies.txt`: salva i cookie ricevuti dal server in un cookie-jar (`cookies.txt`) per usarli in richieste successive.

Nota: `-b cookies.txt` invece legge i cookie dal cookie-jar e li invia nella richiesta.

Il server risponde con un **302 redirect** verso `/api/check` e imposta due cookie di sessione:

```
Set-Cookie: PHPSESSID=<session_id>
Set-Cookie: SID=<sid_value>
```

Seguendo il redirect con `-L` e salvando i cookie con `-c cookies.txt`, si arriva a `/api/check` che risponde:

```json
{"ok":true,"next":"/api/token","note":"Serve header Accept specifico."}
```

### 2. Header Accept personalizzato

Il prossimo endpoint è `/api/token` e richiede un header `Accept` specifico. Tentando con `application/json` il server risponde con `406 Not Acceptable` e indica il valore corretto:

```json
{"error":"bad_accept","need":"Accept: application/vnd.energyhub+json"}
```

Si riprova con l'header corretto:

```bash
curl -v -b cookies.txt \
  -H "Accept: application/vnd.energyhub+json" \
  "http://sfide.itscybergame.it:<port_number>/api/token"
```

Risposta:

```json
{
  "ok": true,
  "next": "/api/submit",
  "token": "<token_value>",
  "rule": "Invia POST x-www-form-urlencoded con token e message che contiene spazi e un +"
}
```

### 3. POST con encoding corretto

Il prossimo step richiede una POST `x-www-form-urlencoded` con un campo `message` che contiene **spazi e un `+` letterale**.

Il punto critico: in `x-www-form-urlencoded` il `+` viene interpretato come spazio. Per inviare un `+` letterale bisogna codificarlo come `%2B`. Il server si aspetta `"hello world+plus"`, quindi il body deve essere:

```
message=hello+world%2Bplus
```

dove `+` = spazio e `%2B` = `+` letterale.

```bash
curl -v -b cookies.txt \
  -H "Accept: application/vnd.energyhub+json" \
  --data-urlencode "token=<token_value>" \
  -d "message=hello+world%2Bplus" \
  "http://sfide.itscybergame.it:<port_number>/api/submit"
```

Risposta:

```json
{"ok":true,"next":"/api/flag","note":"Ultimo step: header semplice."}
```

### 4. Header finale e flag

L'ultimo endpoint è `/api/flag`. Il server richiede un header custom:

```json
{"error":"missing_header","need":"X-API-Mode: curl"}
```

```bash
curl -v -b cookies.txt \
  -H "Accept: application/vnd.energyhub+json" \
  -H "X-API-Mode: curl" \
  "http://sfide.itscybergame.it:<port_number>/api/flag"
```

Risposta:

```json
{"flag":"flag{...}"}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge insegna l'uso pratico di `curl` per interagire con API HTTP: gestione dei cookie di sessione (`-c`/`-b`), header personalizzati (`-H`), POST con `x-www-form-urlencoded` e la differenza tra `+` (spazio) e `%2B` (plus letterale) nell'URL encoding.