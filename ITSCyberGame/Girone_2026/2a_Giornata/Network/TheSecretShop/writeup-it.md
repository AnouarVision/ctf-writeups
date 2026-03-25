# The Secret Shop

**Competizione:** ITSCyberGame<br>
**Categoria:** Network<br>
**File:** data_dev.pcap<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Questo shop online ha un'aria familiare... Cerca le credenziali d'accesso nel file .pcap e trova la flag tra questi ricordi nostalgici! Ma mi raccomando... quel file potrebbe servirti anche ad altro.

Viene fornito un file `.pcap` da analizzare per trovare credenziali e una flag nascosta in un endpoint di sviluppo.

---

## Soluzione

### 1. Analisi del traffico HTTP

Aprendo il pcap in **Wireshark** e filtrando per HTTP si vedono subito richieste interessanti:

```
http
```

Tra le richieste si notano:
- 80 GET per `/assets/img0.png` ... `/assets/img79.png`
- 1 POST a `/index.php` (login)
- Richieste GET a `/games?id=X`
- 1 POST a `/shop_action.php`

### 2. Estrazione delle credenziali — il trabocchetto TCP

Filtrando per il POST di login:

```
http.request.method == "POST" && http.request.uri == "/index.php"
```

Seguendo lo stream TCP (`tasto destro → Follow → TCP Stream`) si vede il payload del login. Apparentemente la password sembra `Hdk8@`, ma il campo `Content-Length: 29` rivela che il corpo ha più byte.

La password è spezzata su **due segmenti TCP** separati. In Wireshark questo si vede guardando i frame raw del reassembling:

- Segmento 1 termina con: `...username=admin&pas`
- Segmento 2 inizia con: `sword=Hdk8@md1`

Il byte successivo al `@` non è l'inizio del frame successivo ma fa ancora parte della password. La password completa è quindi **`Hdk8@md1`**.

Per vederlo chiaramente in Wireshark: selezionare il frame contenente il corpo del POST → nel pannello inferiore espandere **"Reassembled TCP"** → si legge `password=Hdk8@md1`.

### 3. Endpoint nascosto nel POST di shop_action.php

Analizzando il POST a `/shop_action.php`:

```
http.request.uri contains "shop_action"
```

Seguendo il TCP stream si trovano i dati del POST con un commento rivelatore:

```
# DEV NOTE: remove direct flag access in dev version
action=download&idx=42
```

Questo indica che nella versione di sviluppo esiste un accesso diretto alla flag tramite `action=download&idx=42`.

### 4. Login e recupero della flag

Con le credenziali corrette si effettua il login:

```bash
curl -s -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/index.php" \
  -d "username=admin&password=Hdk8@md1"
```

Poi si chiama l'endpoint di sviluppo:

```bash
curl -s -b cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/shop_action.php" \
  -d "action=download&idx=42"
```

Risposta:

```json
{"success":true,"points":200,"message":"<b>FLAG: flag{...}<\/b>"}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge combina due vulnerabilità. La prima è una **password nascosta nel TCP reassembling**: la password era spezzata su due segmenti TCP e una lettura superficiale del pcap mostrava solo una parte (`Hdk8@`), mentre quella completa era `Hdk8@md1`. La seconda è un **endpoint di sviluppo esposto**: il commento `# DEV NOTE` nel POST rivela un accesso diretto alla flag rimasto attivo in produzione. Il messaggio del flag è chiaro: le build di sviluppo non devono mai andare in produzione.