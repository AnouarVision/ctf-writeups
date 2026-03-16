# Sito Vuoto

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://vuoto.challs.olicyber.it

---

## Descrizione

> Questo sito è vuoto, dove sarà mai la flag?

---

## Soluzione

Il titolo **"Sito Vuoto"** suggerisce che la pagina sembri vuota a prima vista. Tuttavia, il contenuto nascosto si trova spesso nei file statici del sito: **HTML, CSS e JavaScript**. L'approccio corretto è ispezionare tutti e tre.

### Passo 1 — Analizzare il sorgente HTML

```bash
curl http://vuoto.challs.olicyber.it/ | grep -i "flag"
```

Nel sorgente HTML è presente un commento con la **prima parte** della flag:

```html
<!-- Prima parte della flag: "flag{..." -->
```

### Passo 2 — Analizzare il file CSS

```bash
curl http://vuoto.challs.olicyber.it/css/style.css | grep -i "flag"
```

Nel file CSS è presente un commento con la **seconda parte** della flag:

```css
/* Seconda parte della flag: "..." */
```

### Passo 3 — Analizzare il file JavaScript

```bash
curl http://vuoto.challs.olicyber.it/js/script.js | grep -i "flag"
```

Nel file JavaScript è presente un commento con la **terza parte** della flag:

```js
/* Ecco la terza parte della flag: "...}" */
```

### Passo 4 — Assemblare la flag

Unendo le tre parti si ottiene la flag completa:

```
flag{...}
```

### Comando alternativo (tutto in uno)

Per automatizzare la ricerca su tutti e tre i file con un singolo blocco di comandi:

```bash
for url in "" "css/style.css" "js/script.js"; do
  echo "=== $url ==="
  curl -s "http://vuoto.challs.olicyber.it/$url" | grep -i "flag"
done
```