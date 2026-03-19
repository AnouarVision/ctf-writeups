# Quantum Transport Layer
**Competizione:** OliCyber<br>
**Categoria:** Network / TLS<br>
**Comando:** `gnutls-cli qtl.challs.olicyber.it:10503`

---

## Descrizione

> Il nostro sysadmin tiene davvero alla sicurezza dell'azienda. Ora ha deciso che tutti dobbiamo usare questo nuovo TLS Quantum protocol. Onestamente, io non ho capito come si dovrebbe usare, tu ne sai qualcosa?

---

## Background — Come funziona TLS

**TLS** (Transport Layer Security) è il protocollo che cifra le comunicazioni su internet (HTTPS, ecc.). Durante l'handshake iniziale, client e server si scambiano alcune informazioni prima ancora di iniziare a comunicare:

**Certificato X.509**: il server si identifica con un certificato digitale che contiene, tra le altre cose, i **Subject Alternative Names (SAN)**: la lista di hostname per cui il certificato è valido.

**SNI (Server Name Indication)**: il client dichiara nell'handshake a quale hostname vuole connettersi. Questo permette a un singolo server di ospitare più siti/servizi con certificati diversi sulla stessa porta.

**ALPN (Application-Layer Protocol Negotiation)**: il client dichiara nell'handshake quale protocollo applicativo vuole usare (es. `http/1.1`, `h2` per HTTP/2, `dot` per DNS-over-TLS). Il server sceglie tra quelli che supporta.

---

## Soluzione

### Passo 1 — Connessione iniziale

Il comando fornito dalla challenge tenta una connessione TLS standard:

```bash
gnutls-cli qtl.challs.olicyber.it:10503
```

Il client fallisce perché il certificato è self-signed, scaduto e il CN non corrisponde all'hostname. Il server chiude la connessione mostrando solo: `There is nothing here!`

---

### Passo 2 — Ignorare la verifica del certificato e leggere il certificato

Si riconnette ignorando gli errori del certificato:

```bash
gnutls-cli --insecure qtl.challs.olicyber.it:10503
```

Il server risponde ancora con `There is nothing here!`, ma ora abbiamo accesso al certificato completo. Lo si esamina con openssl per vederne i dettagli:

```bash
openssl s_client -connect qtl.challs.olicyber.it:10503 -showcerts 2>/dev/null
```

Nei dettagli del certificato, nella sezione **X509v3 Subject Alternative Name**, si trovano due hostname:

```
DNS:quantum-transport-layer.test
DNS:fl4gg.quantum-transport-layer.test
```

Il secondo SAN, `fl4gg`, è chiaramente un hint lasciato apposta nella challenge.

---

### Passo 3 — Connettersi con il giusto SNI

Il server probabilmente si comporta diversamente a seconda dell'hostname che il client dichiara nell'handshake tramite **SNI**. Si usa la flag `--sni-hostname`:

```bash
gnutls-cli --insecure \
  --sni-hostname=fl4gg.quantum-transport-layer.test \
  qtl.challs.olicyber.it:10503
```

Questa volta il server risponde con un messaggio diverso:

```
Supported Protocols: default, flag
```

Il server espone due protocolli ALPN: `default` (quello usato finora) e `flag`.

---

### Passo 4 — Selezionare il protocollo ALPN corretto

Si aggiunge la flag `--alpn=flag` per negoziare il protocollo `flag` durante l'handshake TLS:

```bash
gnutls-cli --insecure \
  --sni-hostname=fl4gg.quantum-transport-layer.test \
  --alpn=flag \
  qtl.challs.olicyber.it:10503
```

L'handshake mostra:
```
- Application protocol: flag
- Handshake was completed
```

E il server restituisce la flag.

---

## Flag

```
flag{...}
```

---

## Conclusioni

1. **I certificati X.509 contengono metadati**: i Subject Alternative Names non sono solo per la validazione del dominio: in una CTF possono contenere hint nascosti. Esaminare sempre il certificato completo.

2. **SNI cambia il comportamento del server**: un singolo server TLS può rispondere in modo completamente diverso a seconda dell'hostname dichiarato dal client nell'handshake. Senza il giusto SNI il server non rivela nulla.

3. **ALPN è un vettore di informazioni**: il server usa ALPN per esporre i protocolli supportati. Selezionare il protocollo sbagliato (o non selezionarne uno) fa ricevere la risposta di default. Il protocollo `flag` era disponibile solo per chi sapeva cercarlo.