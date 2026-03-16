# Headache

**Competizione:** OliCyber
**Categoria:** Web
**URL:** http://headache.challs.olicyber.it

---

## Descrizione

> Quando carichiamo una pagina web stiamo comunicando con un server, ma cosa ci risponde?

---

## Soluzione

La pagina HTML del sito dice *"La flag è qui... ma non proprio qui qui"*, suggerendo che la flag non si trova nel corpo della pagina.

La descrizione della challenge chiede cosa risponde il server: oltre al contenuto HTML, ogni risposta HTTP include degli **header**, ovvero metadati inviati dal server prima del corpo della pagina. È lì che va cercata la flag.

### Passo 1 — Analizzare gli header HTTP

Per vedere solo gli header della risposta, si può usare `curl` con il flag `-I`:

```bash
curl -I http://headache.challs.olicyber.it
```

### Passo 2 — Leggere la risposta

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Date: Sun, 15 Mar 2026 23:27:41 GMT
Flag: flag{...}
Server: Apache/2.4.56 (Debian)
X-Powered-By: PHP/8.0.30
```

Tra gli header di risposta è presente un campo non standard: `Flag`, che contiene direttamente la flag.