# CHAOS
**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** CHAOS.pcap

---

## Descrizione

> CIAO MORTALE, QUESTA È UNA COMUNICAZIONE DAL MONDO DEL C-H-A-O-S (SI, ANCHE QUI ABBIAMO I COMPUTER). RIUSCIRAI A DECIFRARLA?

---

## Soluzione

### Passo 1 — Analizzare il PCAP e riconoscere la struttura caotica

Aprendo `CHAOS.pcap` si nota immediatamente qualcosa di strano: i pacchetti hanno **timestamp negativi**, sono fuori ordine e il traffico è pieno di anomalie TCP:

- `[TCP Retransmission]`: pacchetti ritrasmessi
- `[TCP Spurious Retransmission]`: ritrasmissioni spurie
- `[TCP Previous segment not captured]`: segmenti mancanti

Tutta la comunicazione avviene su `127.0.0.1:42014 → 127.0.0.1:12345`. Il nome della challenge, **CHAOS**, non è casuale: il traffico è volutamente caotico.

---

### Passo 2 — Filtrare i pacchetti dati

I pacchetti rilevanti sono quelli con payload di esattamente **1 byte** (`tcp.len == 1`): ogni pacchetto trasporta un singolo carattere ASCII della flag.

#### Con Wireshark

Inserire nella barra dei filtri:

```
tcp.len == 1
```

Si vedranno i pacchetti PSH, ACK con un byte di payload ciascuno, mescolati a ritrasmissioni spurie.

##### Dove trovare il byte (hex) in Wireshark

Per vedere il **byte grezzo** trasportato da ciascun pacchetto:

1. Seleziona un pacchetto filtrato (con `tcp.len == 1`).
2. Nel pannello centrale di Wireshark (**Packet Details**), espandi:
  - **Transmission Control Protocol**
  - poi **TCP payload (1 byte)**
  - sotto questa voce vedrai il **byte grezzo** in esadecimale (hex), che corrisponde al carattere ASCII trasportato.

Questo ti permette di verificare visivamente, per ogni pacchetto, quale byte viene trasmesso.

#### Con tshark

```bash
tshark -r CHAOS.pcap -Y "tcp.len==1" -T fields \
  -e frame.time_relative -e tcp.seq -e tcp.payload
```

Output:

```
 0.000000   1    48
-14.015736  4294967283  6c
 2.001499   3    30
-8.008697   8    30
...
-15.018163  1    66
```

Si nota che alcuni numeri di sequenza compaiono **due volte** con byte diversi, uno è la trasmissione originale mentre l'altro una ritrasmissione. Il numero di sequenza TCP da solo non basta a ricostruire il messaggio.

---

### Passo 3 — Riordinare per timestamp

La chiave è ordinare i pacchetti dati per **timestamp crescente** (ordine cronologico reale), ignorando il numero di sequenza TCP.

#### Con Wireshark

1. Applicare il filtro `tcp.len == 1`
2. Cliccare sulla colonna **Time** per ordinare i pacchetti per timestamp crescente
3. Leggere la colonna **Info** → i byte del payload compaiono nell'ordine corretto

> Attenzione! Assicurarsi che Wireshark mostri i timestamp relativi al primo pacchetto: **View → Time Display Format → Seconds Since Beginning of Capture**

#### Con tshark

Usare `frame.time_epoch` per i timestamp assoluti e ordinare con `sort`:

```bash
tshark -r CHAOS.pcap -Y "tcp.len==1" -T fields \
  -e frame.time_epoch -e tcp.seq -e tcp.payload \
  | sort -n
```

Oppure, tutto in una riga con Python per decodificare direttamente i byte in ASCII:

```bash
tshark -r CHAOS.pcap -Y "tcp.len==1" -T fields \
  -e frame.time_epoch -e tcp.payload \
  | sort -n \
  | awk '{print $2}' \
  | xxd -r -p
```

---

### Passo 4 — Ricostruire il messaggio

Ordinando i byte per timestamp crescente si ottiene la seguente sequenza:

| Timestamp | Seq TCP | Byte (hex) | Carattere |
|-----------|---------|------------|-----------|
| -15.018 | 1 | `0x66` | `f` |
| -14.016 | wrap | `0x6c` | `l` |
| -13.015 | 3 | `0x61` | `a` |
| -12.014 | 4 | `0x67` | `g` |
| -11.011 | 5 | `0x7b` | `{` |
| -10.010 | 6 | `0x54` | `T` |
| -9.009 | 7 | `0x30` | `0` |
| -8.009 | 8 | `0x30` | `0` |
| -7.008 | 9 | `0x5f` | `_` |
| -6.006 | 10 | `0x4d` | `M` |
| -5.005 | 11 | `0x55` | `U` |
| -4.003 | 12 | `0x43` | `C` |
| -3.002 | 13 | `0x48` | `H` |
| -2.002 | 14 | `0x5f` | `_` |
| -1.001 | 15 | `0x43` | `C` |
| 0.000 | 1 | `0x48` | `H` |
| +1.001 | 17 | `0x34` | `4` |
| +2.001 | 3 | `0x30` | `0` |
| +3.008 | 19 | `0x35` | `5` |
| +4.009 | 20 | `0x7d` | `}` |

---

## Flag

```
flag{...}
```

---

## Conclusioni

1. **Il caos è intenzionale**: I timestamp negativi e le anomalie TCP (retransmission, spurious retransmission) sono stati inseriti deliberatamente per nascondere l'ordine corretto dei dati.

2. **Sequenza TCP ≠ ordine reale**: Riordinare per numero di sequenza porta fuori strada, i numeri di sequenza sono stati manipolati. Il timestamp rivela l'ordine cronologico corretto.

3. **Steganografia nel traffico**: Ogni pacchetto con `tcp.len == 1` trasporta un singolo carattere. Le ritrasmissioni spurie con byte diversi sono un ulteriore elemento di confusione.

4. **Approccio risolutivo**: Filtrare i pacchetti dati, ordinarli per timestamp, concatenare i byte e il messaggio emerge dal CAOS.