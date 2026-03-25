# But it was cheap!

**Competizione:** ITSCyberGame<br>
**Categoria:** Network<br>
**File:** `blindspot_3.pcap`

---

## Descrizione

> Ti contatto perché ho comprato questa telecamera estremamente economica, non è che nasconda qualcosa?

Viene fornita una cattura di traffico di rete. L'obiettivo è analizzarla e scoprire comportamenti sospetti della telecamera IP.

---

## Soluzione

### 1. Panoramica del traffico

Si apre il file in **Wireshark** (`File → Open`). Un primo sguardo alla barra di stato mostra 4795 pacchetti.

Per avere una panoramica dei protocolli presenti si usa:

> **Statistics → Protocol Hierarchy**

```
UDP  → 4662 pacchetti data  (traffico video RTP)
TCP  → HTTP / XML / RTSP
```

Per vedere le conversazioni attive e individuare flussi anomali:

> **Statistics → Conversations → scheda IPv4**

| Sorgente | Destinazione | Frames | Bytes |
|---|---|---|---|
| 192.168.1.10 ↔ 192.168.1.50 | (LAN) | 4672 | 6.7 MB |
| 192.168.1.50 → **203.0.113.77** | (**WAN**) | 5 | 3590 B |

Due flussi attirano l'attenzione:

- **192.168.1.10 ↔ 192.168.1.50**: streaming video RTSP/RTP interno, atteso e normale.
- **192.168.1.50 → 203.0.113.77:8080**: la telecamera (`192.168.1.50`) apre connessioni TCP verso un **IP pubblico esterno** su porta 8080. **Molto sospetto.**

### 2. Isolamento del traffico sospetto

Si filtra il traffico verso l'IP esterno nella barra dei filtri di Wireshark:

```
ip.addr == 203.0.113.77
```

Compaiono 5 pacchetti, tutti con info `HTTP/1.1 200 OK`. La telecamera sta **rispondendo a query ONVIF** provenienti dall'IP esterno, un server remoto non autorizzato sta interrogando il dispositivo tramite il protocollo **ONVIF** (Open Network Video Interface Forum), lo standard usato dalle telecamere IP per l'auto-scoperta e la configurazione.

### 3. Ispezione del payload XML

Si seleziona uno dei 5 pacchetti e nel pannello inferiore si espande:

> **Hypertext Transfer Protocol → Line-based text data: application/soap+xml**

Per leggere il payload completo in modo più comodo:

> Tasto destro sul pacchetto → **Follow → TCP Stream**

Il corpo della risposta è un `GetDeviceInformationResponse` ONVIF:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:tds="http://www.onvif.org/ver10/device/wsdl">
  <s:Body>
    <tds:GetDeviceInformationResponse>
      <tds:Manufacturer>HikvXion</tds:Manufacturer>
      <tds:Model>DS-2CD2143G2-I</tds:Model>
      <tds:FirmwareVersion>VEVMRU1FVFJZLU9LLTE3MDAwMDAwNDI=</tds:FirmwareVersion>
      <tds:SerialNumber>Wm14aFozdGtNSFZpYkROZllqUnpNMTl6TTJOeU0zUjk=</tds:SerialNumber>
      <tds:HardwareId>88</tds:HardwareId>
    </tds:GetDeviceInformationResponse>
  </s:Body>
</s:Envelope>
```

I campi `FirmwareVersion` e `SerialNumber` contengono valori che non assomigliano a versioni firmware o seriali reali, sono stringhe Base64.

### 4. Decodifica dei campi sospetti

**FirmwareVersion:**
```
VEVMRU1FVFJZLU9LLTE3MDAwMDAwNDI=
  → Base64 →
TELEMETRY-OK-1700000042
```

Un beacon di telemetria con un timestamp Unix (`1700000042` = 14 Nov 2023), inviato al server di comando e controllo per segnalare che il dispositivo è online. La telecamera fa **check-in** periodicamente verso l'esterno.

**SerialNumber (doppio Base64):**
```
Wm14aFozdGtNSFZpYkROZllqUnpNMTl6TTJOeU0zUjk=
  → Base64 (livello 1) →
ZmxhZ3tkMHVibDNfYjRzM19zM2NyM3R9
  → Base64 (livello 2) →
flag{...}
```

Il numero di serie è in realtà un payload esfiltrato codificato con **doppio strato Base64**, nascosto in un campo ONVIF apparentemente legittimo.

```python
import base64

serial = "Wm14aFozdGtNSFZpYkROZllqUnpNMTl6TTJOeU0zUjk="
layer1 = base64.b64decode(serial).decode()   # → ZmxhZ3tkMH...
layer2 = base64.b64decode(layer1).decode()   # → flag{...}
print(layer2)
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge simula un attacco reale documentato su telecamere IP economiche di produzione cinese (in particolare cloni/rebrand Hikvision): il firmware contiene un **backdoor C2** (Command & Control) che usa il protocollo ONVIF, legittimamente presente sul dispositivo, per esfiltrare dati verso un server remoto, nascondendo i payload nei campi metadata. Il doppio Base64 è un rudimentale tentativo di offuscamento per evitare ispezioni superficiali del traffico.

I segnali d'allarme nel PCAP erano:
1. **Connessioni TCP in uscita** dalla telecamera verso un IP pubblico su porta 8080.
2. **Risposte ONVIF non sollecitate** (la camera risponde a query provenienti dall'esterno, non dall'interno).
3. **Valori anomali** nei campi `FirmwareVersion` e `SerialNumber`, stringhe Base64 invece di identificatori standard.