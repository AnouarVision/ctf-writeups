# Strange Packets

**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** net2.pcap

---

## Descrizione

> Oggi ho trovato uno strano dispositivo collegato al mio PC. Sono riuscito a catturare questi pacchetti, ma sembrano del tutto innocui.

---

## Soluzione

La challenge presenta un file PCAP con traffico apparentemente normale: connessioni HTTPS verso Google, Facebook, forum Kali e altri siti comuni. La chiave è nel suggerimento "That is a lot of F", un riferimento a `0xFFFF` in esadecimale.

### Passo 1 — Identificare i Pacchetti Anomali

Aprendo il PCAP in Wireshark, quasi tutto il traffico risulta essere TCP/HTTPS standard. Tuttavia, applicando il filtro:

```
eth.type == 0xFFFF
```

emergono **21 pacchetti** con un EtherType non valido. `0xFFFF` non corrisponde ad alcun protocollo Ethernet legittimo, questi sono i pacchetti "davvero strani" citati nella descrizione.

### Passo 2 — Analizzare la Struttura dei Pacchetti

Esaminando i 21 pacchetti anomali, si nota che il **MAC di destinazione cambia** in modo sospetto da un pacchetto all'altro. In particolare, il **primo byte** del MAC di destinazione è diverso in ciascuno:

| Pacchetto | MAC Destinazione      | Primo Byte | Carattere |
|----------:|-----------------------|:----------:|:---------:|
| 70        | `66:5d:64:16:ff:84`   | `0x66`     | `f`       |
| 71        | `6c:00:27:5c:65:26`   | `0x6c`     | `l`       |
| 256       | `61:00:27:5c:65:26`   | `0x61`     | `a`       |
| 452       | `67:5d:64:16:ff:84`   | `0x67`     | `g`       |
| 687       | `7b:5d:64:16:ff:84`   | `0x7b`     | `{`       |
| ...       | ...                   | ...        | ...       |
| 3055      | `7d:5d:64:16:ff:84`   | `0x7d`     | `}`       |

### Passo 3 — Estrarre il Flag

Per uno script già pronto che automatizza l'estrazione, vedi il file [`net2.py`](net2.py) nella cartella della challenge.

---

## Conclusioni

1. **EtherType come canale nascosto**: Il valore `0xFFFF` è un EtherType non valido che non corrisponde ad alcun protocollo reale, filtrare i pacchetti anomali per tipo di protocollo è sempre una buona pratica nell'analisi forense di rete.
2. **Steganografia nei campi MAC**: Il dato segreto era codificato nel primo byte del MAC di destinazione, un campo che Wireshark mostra chiaramente ma che è facile ignorare se si è concentrati sul payload.
3. **Mimetismo nel traffico legittimo**: I pacchetti malevoli erano disseminati tra migliaia di connessioni HTTPS innocue verso siti noti, rendendo l'anomalia difficile da notare senza filtrare per protocollo.