# DNS e-mail security
**Competizione:** OliCyber<br>
**Categoria:** Network / DNS<br>
**Comando:** `dig -p10502 @emailsec.challs.olicyber.it dns-email.localhost`

---

## Descrizione

> Più del 75% delle aziende subisce phishing via e-mail, forse dovrei essere certo che i miei destinatari possano verificare il mio indirizzo e-mail.

---

## Soluzione

### Passo 1 — Prima ricognizione

Il comando fornito dalla challenge esegue una query DNS di tipo **A** (default) sul dominio `dns-email.localhost`:

```bash
dig -p10502 @emailsec.challs.olicyber.it dns-email.localhost
```

Il server risponde con:
```
dns-email.localhost.    3600    IN      A       13.37.13.37
```

Il dominio esiste e risolve a `13.37.13.37`. La challenge parla di sicurezza email, i tre standard DNS di riferimento sono **SPF**, **DKIM** e **DMARC**, tutti pubblicati come record TXT.

---

### Passo 2 — Verificare i record email standard

Il primo approccio è verificare se i record di sicurezza email sono già configurati:

```bash
# SPF
dig -p10502 @emailsec.challs.olicyber.it dns-email.localhost TXT

# DKIM (selettore default)
dig -p10502 @emailsec.challs.olicyber.it default._domainkey.dns-email.localhost TXT

# DMARC
dig -p10502 @emailsec.challs.olicyber.it _dmarc.dns-email.localhost TXT
```

Tutti e tre rispondono con `ANSWER: 0`, i record non esistono. Questo conferma la premessa della challenge: il dominio **non ha** la sicurezza email configurata.

---

### Passo 3 — Ragionare sugli elementi

Il punto chiave è **"questo server"**: il server invia email da `dns-email.localhost` che risolve a `13.37.13.37`. SPF autorizza gli IP mittenti tramite record TXT, ma può anche farlo tramite **meccanismi di inclusione** che puntano ad altri record DNS.

In particolare, SPF supporta il meccanismo `include:` e `redirect=`, che a loro volta possono puntare a sottodomini come:
- `_spf.dns-email.localhost`
- `_netblocks.mail.dns-email.localhost`

Questi sottodomini SPF di secondo livello vengono spesso pubblicati come **record CNAME** che puntano a liste di IP autorizzati, una struttura comune nei grandi provider email (es. Google, SendGrid).

---

### Passo 4 — Enumerare sottodomini SPF con CNAME

Seguendo la logica della gerarchia SPF, il sottodominio più probabile da interrogare è:

```bash
dig -p10502 @emailsec.challs.olicyber.it _netblocks.mail.dns-email.localhost CNAME
```

Il tipo di record da usare è **CNAME**, non TXT, perché i netblock SPF vengono tipicamente pubblicati come alias che puntano alla risposta finale.

La risposta contiene la flag nel valore del CNAME.

---

## Flag

```
flag{...}
```

---

## Conclusioni

1. **SPF non è solo TXT**: L'infrastruttura SPF può usare record CNAME per delegare la lista degli IP autorizzati a sottodomini dedicati come `_netblocks.mail.<dominio>`.

2. **Enumerazione dei tipi di record**: Non basta interrogare TXT, MX e A. Record come CNAME, SRV, e PTR possono contenere informazioni nascoste, in una CTF è fondamentale provare tutti i tipi di record su tutti i sottodomini plausibili.

3. **Gerarchia SPF**: La struttura standard dei sottodomini SPF segue il pattern `_spf.<dominio>` → `_netblocks.mail.<dominio>` → CNAME verso i netblock effettivi. Conoscere questa gerarchia permette di trovare record non ovvi.