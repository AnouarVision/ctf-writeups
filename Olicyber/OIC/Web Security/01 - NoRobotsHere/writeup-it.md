# No Robots Here

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://no-robots.challs.olicyber.it

---

## Descrizione

> Sei in grado di trovare i robots?

---

## Soluzione

Il nome della challenge è già un indizio: **No Robots Here** rimanda direttamente a `robots.txt`, un file standard usato dai siti web per comunicare ai crawler quali pagine indicizzare e quali no.

### Passo 1 — Controllare robots.txt

Naviga su:

```
http://no-robots.challs.olicyber.it/robots.txt
```

Il file contiene:

```
User-agent: *
Disallow: /I77p0mhKjr.html
```

La direttiva `Disallow` rivela una pagina nascosta che il sito cerca di tenere lontana dai motori di ricerca.

### Passo 2 — Visitare la pagina nascosta

Naviga sul percorso indicato:

```
http://no-robots.challs.olicyber.it/I77p0mhKjr.html
```

La pagina contiene la flag.