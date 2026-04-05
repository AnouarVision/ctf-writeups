# TrulyRandomSignature

**Competizione:** OliCyber <br>
**Categoria:** Web <br>
**URL:** http://trulyrandomsignature.challs.olicyber.it

---

## Descrizione
>Avere solo un cookie con l'username non è abbastanza sicuro, quindi abbiamo deciso di firmarlo! Ora è impossibile che qualcuno possa modificarlo senza invalidare la firma! Nota: se pensi di aver capito e non riesci ad ottenere la flag, controlla che la versione di python che usi sia la stessa di quella del server.

Il sito firma il cookie `user=not_admin` con HMAC-SHA256 usando una chiave generata casualmente al boot. L'obiettivo è forgiare un cookie `user=admin` con firma valida per accedere a `/admin` e ottenere la flag.

---

## Soluzione

### 1. Ricognizione iniziale

```bash
curl -si "http://trulyrandomsignature.challs.olicyber.it/"
```

Risposta:
```
X-Uptime: 7036909
Date: Sun, 05 Apr 2026 21:04:21 GMT
Set-Cookie: user=not_admin
Set-Cookie: signature=8df8d5bb43380b88a569bc4e601dca18ad18077a22e23f27e3f9e30c0c1ee819
```

### 2. Vulnerabilità — Seed prevedibile per `random`

Dal source `app.py`:

```python
seed = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
random.seed(seed)
SUPER_SECRET_KEY = get_random_string(32)
```

Il seed è il **timestamp UTC al secondo** del momento di avvio del server.
Dall'header `X-Uptime` sappiamo da quanti secondi è in esecuzione → possiamo ricostruire il boot time esatto e brutare i secondi vicini finché la firma generata corrisponde a quella nota.

### 3. Exploit

Exploit script: [trulyrandomsign.py](./trulyrandomsign.py)

Output:
```
Seed: 2026-01-14 10:22:31
Key: ukgsiftrxuqiachnbtsawzuglhtjykgm
Admin signature: 95848dbc4277a386606ee9ec39db126e66da72f64afd1ef6ac32c508109c4340
```

Accesso a `/admin` con cookie forgiato:

```bash
curl -si "http://trulyrandomsignature.challs.olicyber.it/admin" \
  --cookie "user=admin; signature=95848dbc4277a386606ee9ec39db126e66da72f64afd1ef6ac32c508109c4340"
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

`random` di Python **non è crittograficamente sicuro** e il suo stato è completamente determinato dal seed. Usare un timestamp al secondo come seed riduce lo spazio a poche centinaia di valori da bruteforare.

**Fix corretto:** usare `secrets` o `os.urandom()` per generare la chiave, che non dipendono da seed prevedibili.