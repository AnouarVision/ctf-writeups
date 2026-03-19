# Super Secret Agent 0x42
**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** intercepted.pcap

---

## Descrizione

> Sono riuscito ad intercettare una conversazione in uscita dalla sede del MI16. Credo contenga informazioni chiave sull'ultima missione dell'agente super segreto 0x42 ma è tutto cifrato, aiutami a scoprire la sua chiave e a catturarlo una volta per tutte.

---

## Soluzione

### Passo 1 — Analizzare il PCAP

Aprendo `intercepted.pcap` si vede traffico TCP verso la porta `12345`. Ci sono due sessioni distinte (stream 0 e stream 1), entrambe verso lo stesso server.

#### Con Wireshark

Aprire il file e applicare il filtro:
```
tcp.port == 12345
```

Wireshark assegna automaticamente un indice progressivo a ogni flusso TCP distinto (`tcp.stream eq 0`, `tcp.stream eq 1`, …). In questo pcap ci sono due connessioni separate verso la porta 12345, quindi due stream.

Per analizzarle singolarmente, cliccare con il tasto destro su un pacchetto → **Follow → TCP Stream**. Wireshark applicherà automaticamente il filtro:
```
tcp.stream eq 0
```
mostrando solo la sessione dell'**agente 0x00** (quella rifiutata dal server).

Per passare alla sessione dell'**agente 0x42**, modificare il filtro manualmente in:
```
tcp.stream eq 1
```

È necessario separare i due stream perché appartengono a connessioni TCP distinte (porte sorgente diverse: `37984` e `37986`). Mischiarli renderebbe impossibile distinguere quale challenge corrisponde a quale response. Analizzando lo stream `1` si trovano in sequenza la challenge del server e la response del client, da cui si ricava la chiave.

#### Con tshark

```bash
tshark -r intercepted.pcap -Y "tcp.payload" -T fields \
  -e frame.number -e ip.src -e tcp.payload 2>/dev/null
```

Decodificando i payload in ASCII emerge subito il protocollo applicativo.

---

### Passo 2 — Capire il protocollo challenge-response

Il server implementa un sistema di **autenticazione challenge-response con cifratura XOR**:

1. Il server invia un banner ASCII art (`MI16`) e un messaggio di benvenuto
2. Il server invia una **challenge**: 8 byte casuali in chiaro
3. Il client risponde con gli stessi 8 byte **cifrati con la propria chiave**
4. Se la chiave è corretta, il server invia il messaggio segreto cifrato

Nel pcap ci sono **due sessioni**:

| Stream | Agente | Esito |
|--------|--------|-------|
| 0 | `0x00` | Chiave errata: il server lo rifiuta |
| 1 | `0x42` | Autenticazione riuscita: riceve il messaggio |

Il messaggio del server all'agente `0x00` lo conferma esplicitamente:
```
Attenzione agente 0x00, sembra che la sua nuova chiave non funzioni
correttamente con il nostro algoritmo di cifratura!!
```

---

### Passo 3 — Estrarre la chiave dell'agente 0x42

Dalla sessione dell'agente `0x42` si estraggono:

- **Challenge** (inviata dal server, frame 20): `70 4e 34 bb ff 99 f3 fe`
- **Response** (inviata dal client, frame 22): `6c 00 fa d8 ae 0d 60 15`

Poiché la cifratura è XOR, la chiave si ricava semplicemente:

```
key = challenge XOR response
```

```python
challenge = bytes.fromhex("704e34bbff99f3fe")
response  = bytes.fromhex("6c00fad8ae0d6015")

key = bytes([c ^ r for c, r in zip(challenge, response)])
print(key.hex())  # 1c4ece63519493eb
```

**Chiave dell'agente 0x42:** `1c4ece63519493eb`

---

### Passo 4 — Decifrare il messaggio segreto

Il messaggio cifrato si trova nel frame 26. Gli ultimi 19 byte sono plaintext (`Fine comunicazione\n`), il resto è cifrato con la chiave a ripetizione (repeating-key XOR).

```python
key = bytes.fromhex("1c4ece63519493eb")

ciphertext = bytes.fromhex(
    "502fee1138e7e3846f3aaf4334b3b38a7a28ab113cf5e782"
    "6a2fe24330f3f685682bee5329a0a1c73c27a24322e1fccb"
    "6c27af0d3eb4e08e712cbc0271e4f6997a2bba173eb8b387"
    "7d6eaf1625fbe1826634a7023cfbb38a3c3ebc0c32f1f78e"
    "6e2be0695bf2ff8a7b35a6530ef8a7b46e7ffb1361a1a4df"
    "3011a3570ee5e6df7011fd3c3da0cc8f2c23fa0d35a0ac96"
    "1644"
)

plaintext = bytes([b ^ key[i % len(key)] for i, b in enumerate(ciphertext)])
print(plaintext.decode('utf-8'))
```

**Messaggio decifrato:**
```
La risposta e' affermativa, agente 0x42, il suo piano sembra perfetto,
la autorizziamo a procedere.

flag{...}
```

---

## Conclusioni

1. **Challenge-response vulnerabile**: Quando sia la challenge che la response sono visibili in rete, e la cifratura è XOR, la chiave si ricava banalmente con uno XOR tra i due valori.

2. **XOR a chiave ripetuta**: Con una chiave corta applicata a ripetizione su messaggi lunghi, conoscere la chiave permette di decifrare tutto il traffico passato e futuro.

3. **Known-plaintext attack**: Avere il plaintext (la challenge) e il ciphertext (la response) corrispondenti è sufficiente per rompere la cifratura XOR e recuperare la chiave.

4. **Lezione**: Una cifratura sicura non deve esporre sia il plaintext che il ciphertext della stessa operazione sullo stesso canale non protetto.