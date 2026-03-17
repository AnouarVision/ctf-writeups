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
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            payload = tcp.data

            if b'PK\x03\x04' in payload:
                print(f"ZIP file found! ({len(payload)} bytes)")

                pk_idx = payload.find(b'PK\x03\x04')
                zip_data = payload[pk_idx:]

                with open('recipe.txt.zip', 'wb') as f:
                    f.write(zip_data)
                print("Saved: recipe.txt.zip")
                break
        except:
            pass

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

### Passo 4 — Aprire Il File ZIP E Leggere La Flag

Aprire `recipe.txt.zip` con la password trovata. All'interno si trova `ricetta.txt` con la flag:

```
flag{...}
```

---

## Conclusioni

1. **Filtraggio Wireshark**: Usare filtri HTTP specifici per isolare il traffico pertinente (`http.request.method == POST && frame contains "keyword"`)
2. **Estrazione Di Magic Bytes**: I dati multipart/form-data contengono overhead di header; trovare i magic bytes `PK` nel payload permette di salvare correttamente il file ZIP.
3. **Credenziali In Chiaro**: Informazioni sensibili come le password vengono spesso trasmesse in chiaro nel traffico TCP; un semplice filtro `frame contains "password"` è sufficiente per trovarle.