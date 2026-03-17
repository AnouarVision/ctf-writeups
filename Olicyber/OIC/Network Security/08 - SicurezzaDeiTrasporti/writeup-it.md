# Sicurezza dei Trasporti
**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** capture.pcapng, keys.log
---
## Descrizione
> Per favore aiutaci a trovare il contenuto delle pagine web da questo log del traffico. C'é un file aggiuntivo, ti può essere d'aiuto....

---
## Soluzione

### Passo 1 — Analizzare il PCAP e riconoscere il TLS 1.3

Il file `capture.pcapng` contiene traffico criptato con TLS 1.3. La presence del file `keys.log` (SSLKEYLOG format) indica che è possibile decodificare il traffico se si configurano correttamente le chiavi.

### Passo 2 — Configurare Wireshark per la decodifica TLS 1.3

1. Aprire Wireshark
2. Andare a **Edit → Preferences → Protocols → TLS**
3. Nel campo **(Pre)-Master-Secret log filename**, selezionare il file `keys.log`
4. Cliccare **Apply** e **OK**

Il file `keys.log` contiene le master secrets nel formato standard SSLKEYLOG:
```
CLIENT_TRAFFIC_SECRET_0 <session_id> <secret_key>
SERVER_TRAFFIC_SECRET_0 <session_id> <secret_key>
```

### Passo 3 — Aprire il PCAP e filtrare il traffico HTTP

1. **File → Open** → Selezionare `capture.pcapng`
2. Wireshark decodificherà automaticamente il traffico TLS 1.3
3. Filtrare per `http` per visualizzare i pacchetti HTTP decodificati
4. Cercare i pacchetti di tipo DATA che contengono le risposte HTML

### Passo 4 — Identificare la risposta con la flag

Analizzando il traffico decodificato, si trova una richiesta HTTP GET a un server interno (3.125.223.134):

- **Request:** `GET /` (Stream ID 1)
- **Response:** Contiene il contenuto HTML con la flag

Espandendo il pacchetto nella sezione **Hypertext Transfer Protocol → Line-based text data**, si legge chiaramente:

```
flag{...}
```

### Passo 5 — Verifica

La flag appare nel traffico decodificato come risposta a una richiesta HTTP GET verso l'host interno. Il contenuto HTML della risposta contiene il testo della flag in chiaro.

---
## Conclusioni

1. **TLS 1.3 Decryption**: Wireshark può decodificare il traffico TLS 1.3 usando il file SSLKEYLOG, che contiene le chiavi di sessione estratte durante l'handshake

2. **SSLKEYLOG Format**: Standard per salvare le master secrets di TLS, supportato nativamente da browser e tool di cattura per scopi forensici e debug

3. **Configurazione Essenziale**: Per analizzare traffico TLS criptato, è necessario:
   - Avere accesso alle session keys o master secrets
   - Configurare correttamente il percorso al keylog file in Wireshark
   - Ricaricare il PCAP dopo la configurazione

4. **Il Paradosso della Sicurezza**: Anche con TLS 1.3 (encryption forte e moderna), se un attaccante ha accesso alle master secrets, può decodificare tutto il traffico. La sicurezza del trasporto dipende dal segreto delle chiavi, non dall'algoritmo