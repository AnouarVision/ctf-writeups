# Poca Cola's Recipe

**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** intercepted.pcap

---

## Descrizione

> Sono nascosto sotto un tavolo nella sede centrale della Poca Cola da 3 giorni, ho tracciato tutte le loro comunicazioni! Ti prego trova la ricetta segreta così posso andarmene da qua...

---

## Soluzione

### Passo 1 — Filtrare Le Richieste POST Contenenti "ricetta"

Applicando il filtro Wireshark:

```
http && http.request.method == POST && frame contains "ricetta"
```

Questo isola esattamente i pacchetti POST che contengono la parola "ricetta", dove il malware sta trasmettendo il file della ricetta segreta.

### Passo 2 — Estrarre Il Payload HTTP

Dai frame POST filtrati, estrarre il payload binario. Il payload contiene dati multipart/form-data con il file ZIP della ricetta. I dati iniziano con i magic bytes `PK` (0x504B) dopo l'header HTTP.

**Estrazione con Python:**

```python
import dpkt

with open('intercepted.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)

    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        payload = bytes(tcp.data)

        if b'POST' in payload and b'ricetta' in payload:
            split_idx = payload.find(b'\r\n\r\n')
            http_body = payload[split_idx + 4:]

            with open('recipe.txt.zip', 'wb') as f:
                f.write(http_body)
```

### Passo 3 — Trovare La Password

Applicare un filtro per trovare i pacchetti contenenti la parola "password":

```
frame contains "password"
```

Analizzando i pacchetti TCP che contengono "password", si trova questo messaggio:

```
Dannazione Rick, devi stare più attento, scrivila da qualche parte,
la password è "qhcdpoktbjdsujbsrpjwr"
```

**Password:** `qhcdpoktbjdsujbsrpjwr`

### Passo 4 — Estrarre Il File ZIP

Il payload HTTP contiene i dati multipart/form-data. I magic bytes PK si trovano a offset 118 dal inizio. Dopo estrarre i dati corretti con i magic bytes, il file ZIP risultante è protetto con AES encryption (metodo 99).

Per decomprimere, usare una libreria che supporta AES:

```python
import pyzipper

with pyzipper.AESZipFile('recipe_extracted.zip', 'r') as z:
    z.extractall(pwd='qhcdpoktbjdsujbsrpjwr'.encode())
```

### Passo 5 — Leggere La Ricetta Segreta

Decomprimendo il file, si ottiene il file `ricetta.txt` con la flag:

```
flag{...}
```

---

## Conclusioni

1. **Filtraggio Wireshark**: Usare filtri HTTP specifici per isolare il traffico pertinente (`http.request.method == POST && frame contains "keyword"`)
2. **Estrazione Di Payload Multipart**: I file trasmessi tramite HTTP multipart/form-data hanno overhead di header che deve essere rimosso prima di usare il file binario
3. **Crittografia AES In ZIP**: I file ZIP moderni supportano AES (metodo 99), che richiede librerie come `pyzipper` in Python (il modulo `zipfile` standard non lo supporta)
4. **Credenziali In Chiaro**: Informazioni sensibili come le password vengono spesso trasmesse in chiaro nel traffico TCP; un semplice filtro `frame contains "password"` è sufficiente per trovarle