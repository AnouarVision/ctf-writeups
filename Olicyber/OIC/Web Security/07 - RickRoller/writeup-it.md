# Rick Roller

**Competizione:** OliCyber<br>
**Categoria:** Web / HTTP Response Interception<br>
**URL:** http://roller.challs.olicyber.it

---

## Descrizione

> Mi hanno mandato questo link ma vengo continuamente reindirizzato ad uno strano video. Sai dirmi come mai?

Una semplice pagina con un pulsante che promette di vincere una flag, ma reindirizza sempre verso un video di Rick Astley. La flag esiste ma il browser non la mostra.

---

## Soluzione

### Step 1 — Analisi del Comportamento HTTP

Visitando il sito, si accede a una pagina con un pulsante **"VINCI!"** che punta a `get_flag.php`. Cliccandolo, il browser reindirizza immediatamente verso:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Classico **Rick Roll**. La flag non è mai visibile (almeno non con il browser).

Il server PHP esegue essenzialmente questo:

```php
echo "flag{...}";
header("Location: https://www.youtube.com/watch?v=dQw4w9WgXcQ");
```

---

### Step 2 — Identificazione della vulnerabilità

L'output della flag viene inviato **prima** dell'header `Location`, ma il browser:

1. Riceve la risposta HTTP `302 Found`
2. Legge l'header `Location`
3. **Reindirizza immediatamente**, ignorando il corpo della risposta

Di conseguenza, la flag è presente nel body della risposta HTTP, ma il browser non la mostra mai all'utente.

Il server restituisce dati sensibili (la flag) nel **corpo di una risposta di redirect (302)**. Questo è un errore logico: il browser segue il redirect senza mostrare il body, ma strumenti che operano a livello di protocollo HTTP grezzo, come `curl`, leggono l'intera risposta, header **e** body.

---

### Step 3 — Exploit via curl

Basta usare `curl` con il flag `-i` per vedere sia gli header che il corpo della risposta, senza seguire automaticamente i redirect:

```bash
curl -i http://roller.challs.olicyber.it/get_flag.php
```

**Output:**

```
HTTP/1.1 302 Found
Content-Length: 30
Content-Type: text/html; charset=UTF-8
Date: Wed, 11 Mar 2026 21:10:47 GMT
Location: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Server: Apache/2.4.56 (Debian)
X-Powered-By: PHP/8.0.30

flag{...}
```

La flag appare nel body della risposta `302`, ignorata dal browser ma perfettamente leggibile con `curl`.

---

## Conclusioni

Non bisogna mai includere dati sensibili nel corpo di una risposta di redirect. Un browser segue il `Location` e scarta il body, ma questo **non equivale a nascondere i dati**: chiunque usi `curl`, Burp Suite o qualsiasi altro client HTTP può leggere la risposta completa.

Le best practice da seguire:

1. **Non inviare mai dati sensibili prima di un redirect**: il body di un `3xx` dovrebbe essere vuoto o contenere solo un messaggio HTML generico
2. **Eseguire il redirect prima di qualsiasi output**: in PHP, chiamare `header()` prima di ogni `echo`
3. **Separare la logica di autenticazione dalla consegna del contenuto**: la flag deve essere restituita solo dopo aver verificato tutte le condizioni, non nel mezzo di un flusso di redirect