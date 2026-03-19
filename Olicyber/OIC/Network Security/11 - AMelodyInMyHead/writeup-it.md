# A Melody in My Head
**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** a_melody_in_my_head.pcapng<br>
**Server:** `nc melody.challs.olicyber.it 10020`

---

## Descrizione

> Stiamo testando l'implementazione di un nuovo protocollo di autenticazione super-sicuro per la nostra nuovissima app di messaggistica. Che ne pensi? Riesci a trovare qualche vulnerabilità nascosta che è sfuggita ai nostri sofisticati controlli?

---

## Background — Cos'è un Nonce e perché è importante

Un **nonce** (Number used ONCE) è un numero casuale usato nei protocolli di autenticazione per evitare i **replay attack**.

Il principio è semplice: ogni volta che un client vuole autenticarsi, il server gli manda un numero casuale diverso. Il client risponde con `hash(password + nonce)`. Così la risposta cambia ad ogni sessione, anche se un attaccante intercetta la comunicazione, non può riusarla perché il server la volta dopo manderà un nonce diverso.

**Il problema**: se il nonce è troppo piccolo, lo spazio dei valori possibili è limitato. Prima o poi il server rimanda un nonce già visto e l'attaccante può riusare la risposta intercettata. Questo si chiama **replay attack**.

---

## Soluzione

### Passo 1 — Analizzare il PCAP

Aprendo `a_melody_in_my_head.pcapng` e seguendo i TCP stream si ricostruisce il protocollo:

```
Server → Client:  SERVER HELLO
Server → Client:  NONCE <numero>
Client → Server:  <hash_hex_64_char>
Server → Client:  LOGIN SUCC / LOGIN FAIL
Server → Client:  FLAG <flag>   (solo se LOGIN SUCC)
```

Il client risponde con una stringa esadecimale di 64 caratteri, ovvero un **SHA256** di qualcosa che include la password e il nonce.

#### Con Wireshark

1. Aprire `a_melody_in_my_head.pcapng`
2. Cliccare con tasto destro su un pacchetto → **Follow → TCP Stream**
3. Wireshark mostra la conversazione completa: il testo in **blu** è il server, in **rosso** il client
4. Cambiare sessione con il menu a tendina **Stream** in basso (da `tcp.stream eq 0` a `eq 1`, `eq 2`, ecc.) per vedere tutte le connessioni
5. In basso nel menu **Show data as** selezionare **ASCII** per leggere i messaggi in chiaro

Ripetendo questa operazione per ogni stream si vedono chiaramente `SERVER HELLO`, `NONCE`, le risposte hash e i risultati `LOGIN SUCC` / `LOGIN FAIL`. Per copiare il valore esatto degli hash, cambiare **Show data as** in **Hex Dump**.

#### Con tshark

```bash
tshark -r a_melody_in_my_head.pcapng -Y "tcp.payload" -T fields \
  -e frame.number -e ip.src -e tcp.payload 2>/dev/null
```

Si trovano 5 sessioni nel pcap:

| Nonce | Hash inviato | Esito |
|-------|-------------|-------|
| 40 | `253b2b73...` | LOGIN FAIL |
| 33 | `cd01ef2a...` | LOGIN FAIL |
| 23 | `2a3a1630...` | **LOGIN SUCC** |
| 68 | `23c90a60...` | **LOGIN SUCC** |
|  2 | `0cce6bab...` | **LOGIN SUCC** |

I primi due tentativi falliscono (l'utente non conosce la password), gli ultimi tre riescono.

---

### Passo 2 — Identificare la vulnerabilità

Il nonce è un numero decimale piccolo. Dai valori osservati (2, 23, 33, 40, 68) si deduce che il nonce è un **intero a 1 byte: da 0 a 255**, solo 256 valori possibili in tutto.

Questo è il problema: un attaccante che ha intercettato il traffico possiede già le risposte valide per i nonce 2, 23 e 68. Poiché il server sceglie il nonce a caso tra soli 256 valori, la probabilità di ricevere un nonce già visto è **3/256 ≈ 1.2%** per ogni connessione.

Non serve conoscere la password. Non serve rompere SHA256. Basta **aspettare** che il server mandi un nonce già visto e rispondere con l'hash intercettato.

---

### Passo 3 — Replay Attack

Le risposte valide estratte dal pcap:

```
NONCE  2  ->  0cce6bab87baa7031b69539ac1a211f202fc35cc8f3ac27fdb7e527527310f0e
NONCE 23  ->  2a3a1630446304ab588ef90f32b8d3db88933f9737016e60df5cb3a2dca19b74
NONCE 68  ->  23c90a60a0d2d24b53eca03ac2c4f4194c617f001fa1bf99b20cede152cc240f
```

Per uno script già pronto che automatizza l'attacco replay, vedi il file [`melody.py`](melody.py) nella cartella della challenge.

---

### Passo 4 — Risultato

Eseguendo lo script melody.py, il server risponde con LOGIN SUCC e la flag non appena viene inviato uno dei nonce già visti nel pcap:

```
Replay attack started. Looking for nonce 2, 23 or 68...
[  1] NONCE=  23 -> MATCH! Response sent
  Server: LOGIN SUCC\nFLAG flag{...}

[!] FLAG FOUND!
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

1. **Il nonce deve essere imprevedibile e grande**: un nonce a 1 byte (256 valori) è troppo piccolo. Con appena 3 risposte intercettate si ha già una probabilità significativa di successo ad ogni tentativo. Un nonce sicuro deve essere almeno 128 bit (16 byte) generato crittograficamente.

2. **Il replay attack non richiede di rompere la crittografia**: l'hash SHA256 è matematicamente sicuro, ma non serve rompere SHA256. Basta riusare una risposta già valida intercettata in precedenza.

3. **La dimensione dello spazio del nonce è critica**: con 256 valori possibili, dopo ~180 connessioni si è quasi certi di aver visto tutti i nonce possibili. Con un nonce a 128 bit questo sarebbe computazionalmente impossibile.

4. **Morale**: un protocollo di autenticazione sicuro dipende da tutti i suoi componenti. Anche se l'hash è robusto, un nonce debole compromette l'intera sicurezza del sistema.