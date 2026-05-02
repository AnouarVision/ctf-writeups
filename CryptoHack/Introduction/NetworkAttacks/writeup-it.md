# Network Attacks

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Nella challenge viene richiesto di comunicare con un server TCP che parla esclusivamente JSON. L'obiettivo è inviare un oggetto con la chiave `buy` e valore `flag` per ottenere la flag. Il formato della flag è `crypto{...}`.

Viene fornito uno script Python di partenza da modificare. L'obiettivo è capire il protocollo del server e costruire la richiesta corretta.

---

## Il protocollo JSON su socket

Prima di analizzare la soluzione, vale la pena capire il contesto. Molte challenge crypto su CryptoHack e in generale nelle competizioni CTF usano server TCP che comunicano tramite oggetti **JSON** (*JavaScript Object Notation*).

Il flusso tipico è:

1. Il server invia un messaggio di benvenuto (o un prompt)
2. Il client risponde con un oggetto JSON
3. Il server elabora la richiesta e risponde con un altro oggetto JSON

---

## Soluzione

### Step 1 — Analisi dello script fornito

Lo script di partenza usa `pwntools`, una libreria Python pensata appositamente per il networking. Fornisce primitive comode come `r.readline()` e `r.sendline()`, che gestiscono la connessione TCP in modo trasparente.

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

Lo script fa già tutto il necessario: apre la connessione, legge i quattro messaggi iniziali del server e invia un oggetto JSON con chiave `buy`. Il valore di default è `"clothes"`, che è chiaramente un placeholder.

Il testo della challenge ci dice esplicitamente cosa fare: inviare `{"buy": "flag"}`. La soluzione è già davanti a noi.

---

### Step 2 — La modifica

L'unica modifica necessaria è cambiare il valore della chiave `buy` da `"clothes"` a `"flag"`:

```python
request = {
    "buy": "flag"
}
```

Nient'altro. Il resto dello script funziona già correttamente: `json_send` serializza il dizionario Python in una stringa JSON e lo invia al server, `json_recv` legge la risposta e la deserializza.

---

### Step 3 — Esecuzione e output

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

Il server risponde con un oggetto JSON contenente la chiave `flag` e il suo valore.

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge introduce due strumenti e un pattern che si ripeteranno in quasi tutte le challenge interattive di CryptoHack:

**`pwntools`** è la libreria fondamentale per il networking. Gestisce la connessione TCP, l'invio e la ricezione di dati e si integra naturalmente con Python. Va installata una volta sola con `pip install pwntools` e poi riutilizzata in ogni challenge di rete.

**Il pattern JSON su socket**: leggere, deserializzare, elaborare, serializzare, inviare, è lo scheletro di quasi tutte le challenge interattive della piattaforma.