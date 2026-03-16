# Just a Reminder...

**Competizione:** OliCyber
**Categoria:** Web
**URL:** http://just-a-reminder.challs.olicyber.it

---

## Descrizione

> Ho trovato un form di login su un sito senza nome, ma non ho idea di quali siano le credenziali... Proveresti a loggarti per me?

---

## Soluzione

Il sito presenta un semplice form di login. Poiché non abbiamo le credenziali, il primo passo è analizzare il codice sorgente della pagina, in particolare il file `default.js`, caricato dal frontend.

### Passo 1 — Analizzare il sorgente

Aprendo i DevTools del browser (`F12` → Sources) o visualizzando il file `default.js`, troviamo la funzione `login_check()` che gestisce il login lato client.

Dentro il codice troviamo subito due informazioni fondamentali:

**Username** — in chiaro nel codice:
```javascript
username_field.value === 'admin'
```

**Password** — cifrata con AES, ma la chiave è definita nello stesso file:
```javascript
var s3cr37 = 'ML4czctKUzigEeuR';
// ...
AES_decrypt('U2FsdGVkX1/JEKDXgPl2RqtEgj0LMdp8/Q1FQelH7whIP49sq+WvNOeNjjXwmdrl', s3cr37)
```

### Passo 2 — Decriptare la password

Poiché la libreria `CryptoJS` è già caricata nella pagina, possiamo decriptare la password direttamente dalla console del browser (`F12` → Console):

```javascript
var key = 'ML4czctKUzigEeuR';
var encrypted = 'U2FsdGVkX1/JEKDXgPl2RqtEgj0LMdp8/Q1FQelH7whIP49sq+WvNOeNjjXwmdrl';
CryptoJS.AES.decrypt(encrypted, key).toString(CryptoJS.enc.Utf8);
```

Il risultato è: `v3ry_l337_p455w0rd_!`

### Passo 3 — Login

Con le credenziali ottenute:

- **Username:** `admin`
- **Password:** `v3ry_l337_p455w0rd_!`

Effettuiamo il login e la pagina mostra la flag.