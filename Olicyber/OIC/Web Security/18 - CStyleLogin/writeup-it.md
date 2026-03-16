# C Style Login

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://clogin.challs.olicyber.it

---

## Descrizione

> Riesci ad indovinare la mia password?

Un form di login che utilizza `strcmp()` per il confronto della password. La vulnerabilità è nel comportamento di `strcmp()` con il type juggling di PHP.

---

## Soluzione

### Step 1 — Analisi del codice sorgente

Visitando il sito, notiamo subito la presenza di un link al codice sorgente (`/?source`). Esaminandolo, troviamo il codice PHP vulnerabile:

```php
<?php
include_once('./secrets.php');
if (isset($_POST['password'])) {
  if (strcmp($_POST['password'], $password) == 0) {
    echo $FLAG;
  } else {
    echo '<br />Wrong Password<br /><br />';
  }
}
?>
```

La condizione di accesso è:

```php
if (strcmp($_POST['password'], $password) == 0)
```

Il flag viene stampato quando `strcmp()` restituisce `0`, ovvero quando i due argomenti sono **uguali**.

---

### Step 2 — Identificazione della vulnerabilità

La vulnerabilità risiede nel comportamento di `strcmp()` in PHP quando riceve argomenti di tipo non stringa:

- **PHP < 8:** `strcmp(array, string)` restituisce `NULL` invece di un intero.
- `NULL == 0` è **`true`** in PHP per via del confronto debole (`==`), detto anche *type juggling*.

Di conseguenza, il check diventa:

```
strcmp([], $password) → NULL
NULL == 0             → true
```

La flag viene restituita **senza conoscere la password reale**.

---

### Step 3 — Sfruttamento

Il form HTML invia sempre `password` come stringa. Per inviare un **array** al server, è necessario manipolare la richiesta HTTP direttamente.

**Metodo 1 — curl:**

```bash
curl -X POST http://clogin.challs.olicyber.it \
     -d "password[]="
```

**Metodo 2 — Burp Suite:**

1. Catturare una richiesta POST dal form
2. Modificare il body da `password=qualsiasi` a `password[]=`
3. Inviare la richiesta modificata

Il suffisso `[]` fa sì che PHP interpreti `password` come un array anziché come una stringa.

---

### Step 4 — Output

La risposta conterrà il flag:

```
flag{...}
```

Nota: PHP emetterà anche un warning:

```
Warning: strcmp() expects parameter 1 to be string, array given
```

Questo confirma esattamente il comportamento sfruttato: `strcmp()` ha ricevuto un array, ha restituito `NULL` e il confronto debole ha concesso l'accesso.

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | strcmp() Type Juggling |
| **Causa** | strcmp() con array restituisce NULL, non una eccezione |
| **Confronto** | Uso di `==` (loose) invece di `===` (strict) |
| **Impatto** | Bypass della password senza conoscerla |

---

Il confronto debole `==` (invece di `===`) è la radice del problema. Se il codice usasse `=== 0`, l'exploit non funzionerebbe, poiché `NULL !== 0`.

---

## Conclusioni

- Usare il confronto stretto `=== 0` anziché `== 0`
- Validare il tipo dell'input con `is_string($_POST['password'])` prima di passarlo a `strcmp()`
- Aggiornare a **PHP 8+**, dove `strcmp()` con argomenti non stringa genera un errore fatale
- Il type juggling di PHP può introdurre vulnerabilità non ovvie
- La flessibilità dei tipi dinamici richiede validazione esplicita