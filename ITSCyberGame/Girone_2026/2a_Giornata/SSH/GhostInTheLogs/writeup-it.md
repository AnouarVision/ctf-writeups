# Ghost in the Logs

**Competizione:** ITSCyberGame<br>
**Categoria:** SSH<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Ore 03:45 del mattino. Il server di produzione PROD-SEC-01 ha subito un arresto anomalo di un modulo critico di crittografia. Il watchdog di sistema ha terminato il processo prima che potesse completare l'invio dei dati, ma sospettiamo che una stringa sensibile sia rimasta intrappolata nei registri di sistema proprio prima del crash. Il processo, noto come `worker-node`, non è più attivo e non può essere riavviato.

Viene fornito accesso SSH a un server. L'obiettivo è trovare la flag nei log di sistema lasciati dal processo crashato.

---

## Soluzione

### 1. Connessione SSH

```bash
ssh -p <port_number> itscybergame@sfide.itscybergame.it
# password: itscybergame
```

La home directory è completamente vuota, nessun file rilevante.

### 2. Ricerca nei log di sistema

La hint parla del processo `worker-node` e di un crash. Si cercano le sue tracce in `/var/log/syslog`:

```bash
cat /var/log/syslog | grep worker-node
```

Output:

```
Mar 24 21:40:16 ctf-machine kernel: [ 1337.000] process 'worker-node' (pid 552) crashed.
Mar 24 21:40:16 ctf-machine worker-node[552]: Dumping environment strings...
Mar 24 21:40:16 ctf-machine worker-node[552]: ENV_DATA=ZmxhZ3tiNjRfaXNfbjB0X2VuY3J5cHRpMG5fanVzdF9lbmNvZGluZ30=
```

Il processo ha stampato una variabile d'ambiente `ENV_DATA` contenente una stringa in base64 prima di crashare.

### 3. Decodifica base64

```bash
echo "ZmxhZ3tiNjRfaXNfbjB0X2VuY3J5cHRpMG5fanVzdF9lbmNvZGluZ30=" | base64 -d
```

Output:

```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La flag era nascosta nei log di sistema: il processo `worker-node` al momento del crash aveva stampato la variabile `ENV_DATA` codificata in base64. Il messaggio del flag è anche un insegnamento: il base64 non è cifratura, è solo una codifica: chiunque possa leggere il log può decodificarlo immediatamente. I log di sistema non sono mai un posto sicuro dove conservare dati sensibili.