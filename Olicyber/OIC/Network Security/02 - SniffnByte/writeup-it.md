# Sniff 'n' byte

**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** sniff_n_byte.pcapng

---

## Descrizione

> Oh no! Sembra che qualcuno abbia infettato il nostro server con uno spyware e stia esfiltrando dei dati sensibili! Annusa in giro e scopri quali informazioni il malware sta inviando ai malintenzionati!

---

## Soluzione

La challenge presenta un file PCAP contenente traffico di rete. Il testo descrive un'esfilrazione di dati tramite uno spyware, dunque dobbiamo cercare il traffico sospetto.

### Passo 1 — Analizzare Il File PCAP

Estraendo i metadati del file PCAP con `capinfos`:

```
File: sniff_n_byte.pcapng
Numero Pacchetti: 69
Durata: 32.529 secondi
Filtro Cattura: tcp dst port 10622 or src port 10622
```

Il filtro applicato durante la cattura rivela che il traffico sospetto passa per la **porta 10622 TCP**.

### Passo 2 — Identificare Il Flusso TCP

L'intestazione della captura contiene anche un easter egg nei commenti:

```
Capture comment: Congrats! You found an EASTER EGG ^-^ Now you are a REAL 1337 H4XX0R, but go back to the challenge!
```

Questo conferma che stiamo sulla strada giusta, ma la vera flag è nel flusso TCP stesso.

### Passo 3 — Decodificare Il Payload TCP

Analizzando i payload dei pacchetti TCP, il testo della challenge fornisce il flusso esfiltratto:

```
0x660x6c0x610x670x7b0x370x680x330x590x5f0x350x410x790x5f0x790x300x750x5f0x630x340x4e0x5f0x350x4e0x310x660x660x5f0x5e0x2d0x5e0x7d
```

Questo è in formato esadecimale con prefisso `0x` per ogni byte. Rimuovendo i separatori e convertendo:

```
Hex: 666c61677b376833595f3541795f7930755f63344e5f354e3166665f5e2d5e7d
```

Convertendo da esadecimale ad ASCII:

```
flag{...}
```

---

## Conclusioni

1. **Filtri Di Cattura**: I filtri TCPdump applicati al momento della cattura rivelano quali porte/protocolli sono sospetti
2. **Payload Analysis**: Il valore reale non è sempre nei metadati, ma nei dati effettivi trasmessi
3. **Encoding Detection**: Riconoscere il formato di codifica (hex-encoded string in questo caso)
4. **Network Forensics**: Quando il malware comunica, usa spesso protocolli comuni (TCP) su porte non standard