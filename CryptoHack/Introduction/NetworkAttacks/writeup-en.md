# Network Attacks

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> The challenge requires communicating with a TCP server that speaks exclusively JSON. The goal is to send an object with the key `buy` and value `flag` to retrieve the flag. The flag format is `crypto{...}`.

A starter Python script is provided for us to modify. The objective is to understand the server's protocol and craft the correct request.

---

## The JSON-over-socket protocol

Before diving into the solution, it's worth understanding the context. Many crypto challenges on CryptoHack and CTF competitions in general, use TCP servers that communicate via **JSON** (*JavaScript Object Notation*) objects.

The typical flow is:

1. The server sends a welcome message (or a prompt)
2. The client replies with a JSON object
3. The server processes the request and responds with another JSON object

---

## Solution

### Step 1 — Analysing the provided script

The starter script uses `pwntools`, a Python library designed specifically for networking in CTF challenges. It provides convenient primitives such as `r.readline()` and `r.sendline()`, which handle the TCP connection transparently.

```python
#!/usr/bin/env python3

from pwn import *
import json

HOST = "socket.cryptohack.org"
PORT = 11112

r = remote(HOST, PORT)

def json_recv():
    line = r.readline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

print(r.readline())
print(r.readline())
print(r.readline())
print(r.readline())

request = {
    "buy": "clothes"
}
json_send(request)

response = json_recv()
print(response)
```

The script already does everything needed: it opens the connection, reads the four initial messages from the server, and sends a JSON object with the key `buy`. The default value is `"clothes"`, which is clearly a placeholder.

The challenge description tells us explicitly what to do: send `{"buy": "flag"}`. The solution is right in front of us.

---

### Step 2 — The fix

The only change needed is to replace the value of the `buy` key from `"clothes"` to `"flag"`:

```python
request = {
    "buy": "flag"
}
```

Nothing else. The rest of the script already works correctly: `json_send` serialises the Python dictionary into a JSON string and sends it to the server, while `json_recv` reads the response and deserialises it.

---

### Step 3 — Execution and output

```
[x] Opening connection to socket.cryptohack.org on port 11112
[+] Opening connection to socket.cryptohack.org on port 11112: Done
b"Welcome to netcat's flag shop!\n"
b'What would you like to buy?\n'
b"I only speak JSON, I hope that's ok.\n"
b'\n'
{'flag': 'crypto{...}'}
[*] Closed connection to socket.cryptohack.org port 11112
```

The server responds with a JSON object containing the key `flag` and its value.

---

### Flag

```
crypto{...}
```

---

## Conclusions

This challenge introduces two tools and a pattern that will recur in almost every interactive challenge on CryptoHack:

**`pwntools`** is the essential library for CTF networking. It handles the TCP connection, sending and receiving data, and integrates naturally with Python. Install it once with `pip install pwntools` and reuse it across every network challenge.

**The JSON-over-socket pattern**: receive, deserialise, process, serialise, send, is the skeleton of nearly every interactive challenge on the platform.