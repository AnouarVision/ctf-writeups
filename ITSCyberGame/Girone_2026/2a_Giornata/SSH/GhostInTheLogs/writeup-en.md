# Ghost in the Logs

**Competition:** ITSCyberGame
**Category:** SSH
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> 03:45 AM. The production server PROD-SEC-01 had an unexpected crash in a critical crypto module. The system watchdog killed the process before it could finish sending data, but we suspect a sensitive string was left in the system logs right before the crash. The process, called `worker-node`, is no longer running and cannot be restarted.

You are given SSH access to a server. The goal is to find the flag in the system logs produced by the crashed process.

---

## Solution

### 1. SSH connection

```bash
ssh -p <port_number> itscybergame@sfide.itscybergame.it
# password: itscybergame
```

The home directory is empty and contains no relevant files.

### 2. Search system logs

The hint mentions the `worker-node` process and a crash. Search `/var/log/syslog` for its traces:

```bash
cat /var/log/syslog | grep worker-node
```

Example output:

```
Mar 24 21:40:16 ctf-machine kernel: [ 1337.000] process 'worker-node' (pid 552) crashed.
Mar 24 21:40:16 ctf-machine worker-node[552]: Dumping environment strings...
Mar 24 21:40:16 ctf-machine worker-node[552]: ENV_DATA=ZmxhZ3tiNjRfaXNfbjB0X2VuY3J5cHRpMG5fanVzdF9lbmNvZGluZ30=
```

The process printed an environment variable `ENV_DATA` containing a base64 string before crashing.

### 3. Base64 decode

Decode the value with:

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

## Conclusions

The flag was left in the system logs: the `worker-node` process printed the `ENV_DATA` variable encoded in base64 just before the crash. This demonstrates that base64 is an encoding, not encryption: anyone who can read the logs can decode the secret.
