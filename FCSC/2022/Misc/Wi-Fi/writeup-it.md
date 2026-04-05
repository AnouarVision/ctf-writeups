# Wi-Fi

**Competizione:** FCSC 2022 (intro) <br>
**Categoria:** Misc <br>
**File:** `intro-wifi_pcap.xz`<br>
**Password rete:** `FCSC p0w3r is the answer`

---

## Descrizione
> Saurez-vous déchiffrer cette capture Wi-Fi ? Le mot de passe du réseau est FCSC p0w3r is the answer.

Viene fornita una cattura di rete Wi-Fi (formato pcapng, compresso xz). Il traffico è cifrato con WPA2. La password del network è fornita, bisogna decifrare la cattura e trovare la flag nascosta nel traffico in chiaro.

---

## Soluzione

### 1. Ricognizione iniziale

Si decomprime l'archivio `.xz` e si apre il file pcapng con Wireshark.

I primi frame sono tutti **Beacon** dalla rete `FCSC-WiFi`. Scorrendo si trovano 4 frame **EAPOL**, il WPA2 4-way handshake completo:

| Frame | Tipo |
|-------|------|
| 162 | EAPOL Key — Message 1 of 4 |
| 164 | EAPOL Key — Message 2 of 4 |
| 166 | EAPOL Key — Message 3 of 4 |
| 168 | EAPOL Key — Message 4 of 4 |

Handshake completo = possiamo decifrare tutto il traffico WPA2.

---

### 2. Decifrare il traffico WPA2

#### Passo 1 — Aprire le preferenze IEEE 802.11

Vai su:

```
Edit → Preferences → Protocols → IEEE 802.11
```

oppure in alternativa:

```
Edit → Preferences
```
poi cerca `802.11` nella barra di ricerca a sinistra.

#### Passo 2 — Abilitare il decryption

Nella sezione **IEEE 802.11**, assicurati che la voce:

```
☑ Enable decryption
```

sia **spuntata**.

#### Passo 3 — Aggiungere la chiave WPA2

Clicca sul pulsante **`Edit...`** accanto a *Decryption keys*.

Si apre una finestra. Clicca sul **`+`** in basso a sinistra per aggiungere una nuova chiave.

Compila i campi così:

| Campo | Valore |
|-------|--------|
| **Key type** | `wpa-pwd` |
| **Key** | `FCSC p0w3r is the answer:FCSC-WiFi` |

> **Formato:** `password:SSID`, il separatore è i due punti. L'SSID è `FCSC-WiFi`.

Clicca **OK** per chiudere la finestra delle chiavi, poi **OK** di nuovo per chiudere le Preferences.

#### Passo 4 — Verificare la decifratura

Wireshark ri-disseziona automaticamente la cattura. Ora i frame di dati che prima mostravano `Data` cifrato appaiono come protocolli leggibili: **DHCP, DNS, ARP, HTTP**.

---

### 3. Trovare la flag — Follow HTTP Stream

Nella barra dei filtri di Wireshark, digita:

```
http
```

e premi Invio. Appaiono 2 frame HTTP:

- `GET /my_precious HTTP/1.1`: il client chiede qualcosa di interessante
- `HTTP/1.0 200 OK`: la risposta del server con la flag

Fai **click destro** sul frame della risposta HTTP (`HTTP/1.0 200 OK`) →
**Follow → TCP Stream**

Si apre la finestra con il contenuto completo della sessione TCP. Il corpo della risposta contiene direttamente la flag:

```
HTTP/1.0 200 OK
...

FCSC{...}
```

---

## Flag

```
FCSC{...}
```

---

## Conclusioni

Challenge classica di **decifratura WPA2 con Wireshark**. I passaggi chiave:

- Handshake 4-way EAPOL completo presente nella cattura → decifratura possibile
- Wireshark supporta nativamente WPA2 tramite `Edit → Preferences → IEEE 802.11` con chiave in formato `password:SSID`
- Il traffico in chiaro conteneva una richiesta HTTP a `/my_precious` con il flag in chiaro nel body della risposta