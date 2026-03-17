# G4tto

**Competizione:** OliCyber<br>
**Categoria:** Network Forensics<br>
**File:** G4tt0.pcapng

---

## Descrizione

> Riuscirai a trovare il gatto?

---

## Soluzione

La challenge è incentrata sulla ricerca di un "gatto" all'interno del traffico di rete catturato.

### Passo 1 — Analizzare Il Traffico HTTP

Esaminando il file PCAP, si osserva una richiesta HTTP verso:

```
GET /HttpEcho/Gatto.jpeg HTTP/1.1
```

Il server risponde con un file JPEG di 66.182 byte contenente un'immagine.

### Passo 2 — Estrarre L'Immagine JPEG

Wireshark è in grado di riassemblare automaticamente i flussi HTTP e salvare i file trasportati. Per farlo:

1. Andare su **File → Esporta Oggetti → HTTP...**
2. Nella finestra che appare, cercare la voce `Gatto.jpeg`
3. Selezionarla e cliccare su **Salva**

Aprendo il file JPEG salvato si vedrà l'immagine di un gatto; la flag è visibile direttamente nell'immagine:

```
flag{...}
```
---

## Conclusioni

1. **Estrazione Di File Binari**: I file binari come JPEG possono essere estratti dai pacchetti TCP cercando i marker del formato
2. **Analisi Di Payload HTTP**: Le risposte HTTP trasportano spesso file che sono la chiave per risolvere la challenge
3. **Interpretazione Laterale**: A volte la soluzione non è una stringa nascosta, ma l'oggetto stesso (il gatto)