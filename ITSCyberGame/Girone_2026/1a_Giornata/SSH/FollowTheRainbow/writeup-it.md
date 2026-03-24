# Follow the rainbow

**Competizione:** ITSCyberGame<br>
**Categoria:** SSH<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Segui l'arcobaleno che ti porterà alla flag. Accedi via ssh con ITSCyberGame:rainbow.

Si accede a un server SSH con credenziali fornite. L'obiettivo è trovare la flag seguendo l'"arcobaleno".

---

## Soluzione

### 1. Connessione SSH

```bash
ssh -p <port_number> ITSCyberGame@sfide.itscybergame.it
# password: rainbow
```

La home directory è completamente vuota:

```bash
ITSCyberGame@5729c66040d4:~$ ls -la
total 28
drwxr-x--- 1 ITSCyberGame ITSCyberGame 4096 ...  .
drwxr-xr-x 1 root         root         4096 ...  ..
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  220 ...  .bash_logout
-rw-r--r-- 1 ITSCyberGame ITSCyberGame 3989 ...  .bashrc
drwx------ 2 ITSCyberGame ITSCyberGame 4096 ...  .cache
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  807 ...  .profile
```

### 2. Analisi del .bashrc

Leggendo `.bashrc`, in fondo al file si nota una funzione custom:

```bash
prompt_color() {
  color_code=$(/usr/local/bin/color-changer color 2>/dev/null || echo "\\[\\033[38;5;196m\\]")
  PS1="${color_code}\\u@\\h:\\w\\\$ \\[\\033[0m\\]"
}
PROMPT_COMMAND="prompt_color"
export PROMPT_COMMAND
```

Ad ogni comando eseguito, viene chiamato `/usr/local/bin/color-changer color` per cambiare il colore del prompt, questo è l'"arcobaleno" del titolo.

### 3. Ispezione del binario

```bash
ls -la /usr/local/bin/color-changer
# -rwxr-xr-x 1 root root 706768 Feb  4 12:06 /usr/local/bin/color-changer
```

È un binario custom installato da root. Proviamo a invocarlo con `--help`:

```bash
/usr/local/bin/color-changer --help
```

Output:

```
/usr/local/bin/color-changer
/usr/local/bin/color-changer list
/usr/local/bin/color-changer next
flag{...}
```

La flag era nascosta direttamente nell'help del binario.

---

## Flag

```
flag{...}
```

---

## Conclusioni

L'"arcobaleno" era il binario `color-changer` che cambiava colore al prompt ad ogni comando tramite `PROMPT_COMMAND` nel `.bashrc`. Ispezionando il binario con `--help`, la flag era stampata direttamente nell'output. La challenge insegna a leggere attentamente i file di configurazione della shell e a investigare i binari non standard presenti nel sistema.