# Extraction d'ADNs

**Competizione:** 404CTF 2026 <br>
**Categoria:** Forensic

<img src="extraction_d'adns.png">

---

## Soluzione

### Analisi iniziale

Viene fornito un file di cattura `challenge.pcap`.

Per identificare rapidamente eventuali anomalie nel traffico DNS, filtriamo direttamente le **query DNS**:

```bash
tshark -r challenge.pcap -Y "dns.flags.response == 0"
```
<img src="queryDNS.png">

L’output mostra immediatamente un pattern abbastanza sospetto, numerose query DNS verso domini che imitano servizi legittimi ma contengono numeri al posto di lettere (**typosquatting**):

- goog1e.com
- y0utube.com
- faceb00k.com
- inst4gram.com
- vida1.fr

Ogni query DNS contiene un **sottodominio dall'aspetto casuale**, composto esclusivamente da caratteri dell’alfabeto Base32. nessuno dei sottodomini contiene cifre non ammesse in Base32 (0, 1, 8, 9) e la lunghezza dei frammenti è compatibile con blocchi Base32 tranne l'ultimo.

La presenza di questi frammenti suggerisce che stiano trasportando dati codificati, molto probabilmente come parte di un meccanismo di **DNS tunneling**.


### Ricostruzione dello stream Base32 via DNS tunneling

Poiché ogni query DNS contiene un frammento diverso ma con la stessa struttura, è ragionevole interpretarli come **parti consecutive di uno stream Base32 utilizzato per l’esfiltrazione**.

La strategia consiste nel **concatenare tutti i sottodomini nell’ordine delle query** e decodificarli come un unico payload Base32.

```python
import base64

subdomains = [
    "kjeumrrwaeaaav2fijif", "mubyjquqcaaaf4vucdaa", "b4yp74z777zr66ea4nwj",
    "xy2efotw5zyaw3qsi2cp", "mjyyfhhtxcr6ibtqapoj", "cz6h4eac5mz56qhd6fn7",
    "uvp5uent76iexcui7yzx", "bw2isglxsd26mf7sncf7", "yw2eyk4tp5xjdjxqoqi3",
    "23wwz5skdnfqrwf4azri", "ryz6cm2y2flg2zoqfc5k", "n6it5kgq27iu4eag27ac",
    "s2hnkm6brhjvdhlt46og", "unf7mp3fm4iakktpmr4p", "aqd44qancit2co42envh",
    "anss6yvquy6oovx6tnmp", "3vtonkmrdly6zsol5jvq", "pbjbjdqwi2utlopi3voy",
    "qgcjibzle4d4n236o5by", "a4zlvkvmvjye3ykkqzg6", "yyp6dgkrqzx2id4anvsf",
    "mjeoxsgqyxqrtr4f7u3j", "mxrexqn6uy7jgwcmx4tb", "gz6ckpyp6dddx4j2j7lj",
    "tjnx54keoutur6e5p3vi", "77j7i4aaa"
]

payload = "".join(subdomains).upper()
pad_len = (8 - len(payload) % 8) % 8
payload += "=" * pad_len

data = base64.b32decode(payload, casefold=True)

with open("flag.png", "wb") as f:
    f.write(data)
```

> **Nota:** l’ultimo chunk  (`77j7i4aaa`) è lungo 9 caratteri e non può essere decodificato singolarmente (Base32 richiede lunghezze multiple di 8). Per questo motivo è necessario trattare l’intera concatenazione come un unico stream Base32 e applicare il padding **solo alla fine**.

### Identificazione del file

<img src="extracted_flag.png">

L’header del file decodificato inizia con: `RIFF....WEBP`, la firma inconfondibile di un’immagine **WebP**.

E sì, lo so: nello script l’ho salvata come flag.png perché rinominare l’estensione richiedeva uno sforzo emotivo che in quel momento non ero pronto ad affrontare. Per fortuna display non giudica e apre tutto lo stesso.

---

## Flag

```
404CTF{CL4UD3_B3RN4RD_G0T_PWNED}
```


