# Bosh

**Competizione:** ITSCyberGame<br>
**Categoria:** SSH<br>
**Connessione:** `sfide.itscybergame.it:<numero_porta>`

---

## Descrizione

> Per accedere alla macchina in ssh usa l'utente ITSCyberGame e password ITSCyberGame :)

---

## Soluzione

### Passo 1 — Connessione SSH

```bash
ssh -p 17520 ITSCyberGame@sfide.itscybergame.it
# password: ITSCyberGame
```

### Passo 2 — Ricognizione iniziale

I primi comandi sembrano non funzionare correttamente:

```bash
ITSCyberGame@aa2c28ad8dce:~$ ls        # mostra animazione del treno
ITSCyberGame@aa2c28ad8dce:~$ ls -la    # mostra animazione del treno
ITSCyberGame@aa2c28ad8dce:~$ cat /etc/passwd
rm: remove write-protected regular file '/etc/passwd'?
```

`cat` sta chiedendo di **rimuovere** il file invece di leggerlo. Qualcosa non va.

### Passo 3 — Analisi degli alias

```bash
ITSCyberGame@aa2c28ad8dce:~$ alias
alias cat='rm'
alias cd='hollywood'
alias find='sudo apt update && upgrade'
alias grep='cowsay'
alias ls='sl'
...
```

I comandi più comuni sono stati rimappati ad alias inutili o distruttivi:

| Comando | Alias | Effetto |
|---|---|---|
| `ls` | `sl` | Mostra un treno animato |
| `cat` | `rm` | Cancella il file invece di leggerlo |
| `cd` | `hollywood` | Apre animazione terminal fake |
| `find` | `sudo apt update && upgrade` | Aggiorna i pacchetti |
| `grep` | `cowsay` | Stampa testo con la mucca |

### Passo 4 — Bypass con path assoluti

Gli alias valgono solo per i nomi brevi dei comandi. Usando il **path assoluto** si esegue il binario reale, ignorando completamente l'alias:

```bash
ITSCyberGame@1697bd62f0e7:~$ /bin/ls -la
total 32
drwxr-x--- 1 ITSCyberGame ITSCyberGame 4096 Mar 23 22:16 .
drwxr-xr-x 1 root         root         4096 Feb  2 18:45 ..
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  220 Mar 31  2024 .bash_logout
-rw-r--r-- 1 ITSCyberGame ITSCyberGame 3913 Feb  2 18:45 .bashrc
drwx------ 2 ITSCyberGame ITSCyberGame 4096 Mar 23 22:16 .cache
-rw------- 1 ITSCyberGame ITSCyberGame   31 Mar 23 22:16 .flag.txt
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  807 Mar 31  2024 .profile
```

La flag è in `.flag.txt`, file nascosto (inizia con `.`), invisibile con `ls` normale.

```bash
ITSCyberGame@1697bd62f0e7:~$ /bin/cat .flag.txt
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge insegna due cose. La prima è che gli **alias bash** si applicano solo ai nomi brevi, usare il path assoluto (`/bin/ls`, `/bin/cat`) li aggira completamente. In alternativa si poteva usare `unalias cat ls find` per ripristinare i comandi nella sessione corrente. La seconda è che i **file nascosti** (dotfile, quelli che iniziano con `.`) non compaiono con `ls` senza il flag `-a` o `-la`, dettaglio fondamentale.