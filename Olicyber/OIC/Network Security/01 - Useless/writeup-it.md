# Useless

**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** capture.pcapng

---

## Descrizione

> Ho rubato questo file da un server molto importante, ma non riesco a trovare nulla di utile in questi pacchetti, la loro sicurezza è impenetrabile.

---

## Soluzione

Il nome della challenge è già un indizio: **Useless** (Inutile). Quando il contenuto ovvio non funziona, bisogna pensare lateralmente e controllare livelli più astratti dei dati.

### Passo 1 — Analisi Iniziale del File PCAP

Aprendo il file in Wireshark e osservando il traffico, sembra non contenere nulla di particolare:
- Pacchetti standard di rete
- Nessun traffico HTTP/HTTPS sospetto
- Nessun payload interessante a primo sguardo

```
File: capture.pcapng
Dimensione: 2714 KB
Formato: Wireshark/pcapng
Incapsulamento: Ethernet
Numero Pacchetti: 3438
Durata: 31.314 secondi
```

### Passo 2 — Controllare I Metadati Del File

Poiché il contenuto dei pacchetti sembra "inutile", la vera informazione potrebbe trovarsi nei metadati del file stesso. Utilizziamo lo strumento `capinfos` (parte di Wireshark):

```bash
$ capinfos capture.pcapng
```

### Passo 3 — Scoperta Della Flag Nei Commenti

L'output di `capinfos` rivela il campo cruciale:

```
Capture comment: flag{...}
```

---

## Conclusioni

1. **I Metadati Sono Importanti**: Non cercare solo nei dati dei pacchetti; i commenti nel file possono contenere informazioni critiche
2. **Strumenti Alternativi**: `capinfos` permette un'analisi rapida senza interfaccia grafica
3. **Thinking Outside The Box**: Una challenge intitolato "Useless" suggerisce di ripensare l'approccio
4. **Verifica Tutti I Livelli**: Se il contenuto ovvio non funziona, controllare header, commenti e metadati