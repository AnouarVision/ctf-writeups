# Easy Stream

**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** easystream.pcapng

---

## Descrizione

> Riesci a seguire lo stream?

---

## Soluzione

La challenge presenta un file PCAP con traffico HTTP. Come suggerisce il nome, basta "seguire" il flusso per trovare la flag.

### Passo 1 — Estrarre Gli Oggetti HTTP

Wireshark permette di ricostruire e salvare automaticamente gli oggetti trasferiti via HTTP:

1. Andare su **File → Esporta Oggetti → HTTP...**
2. Nella finestra che appare, selezionare il file chiamato `Echo`
3. Cliccare su **Salva**

### Passo 2 — Leggere Il Contenuto Del File

Il file `Echo` è una pagina HTML con il seguente contenuto:

```html
<!DOCTYPE html>
<html>
<head>
  <title>benvenuti nel server della flag</title>
</head>
<body>
  <h1>flag trovata flag{...}</h1>
</body>
</html>
```

La flag è direttamente visibile nel titolo `<h1>` della pagina.

---

## Conclusioni

1. **Esporta Oggetti HTTP**: La funzione di Wireshark "Esporta Oggetti" riassembla automaticamente i file trasportati su HTTP, evitando l'analisi manuale dei pacchetti.
2. **Traffico in Chiaro**: HTTP non cifra i dati; tutto il contenuto trasmesso è leggibile direttamente nel PCAP.
3. **Follow TCP Stream**: In alternativa a "Esporta Oggetti", si può fare clic destro su un pacchetto e scegliere **Segui → Flusso TCP** per leggere la risposta HTTP completa.

