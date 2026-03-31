# We Are Under Attack!

**Competizione:** ITSCyberGame<br>
**Categoria:** Network<br>
**File:** network_dump.pcap

---

## Descrizione

> Il nostro reparto IT ha rilevato un picco di traffico verso il nostro server interno di gestione dell'inventario. Il firewall non ha registrato trasferimenti di file in uscita di grandi dimensioni e il server web non si è bloccato, ma sospettavamo fortemente che un hacker sia riuscito a esfiltrare informazioni riservate dal database di backend. Riesci a dirci cosa?

---

## Soluzione

### Passo 1 — Panoramica del traffico

Si apre il file `.pcap` in Wireshark e si analizza la gerarchia dei protocolli tramite `Statistics` → `Protocol Hierarchy`:

```
eth → ip → tcp → http   (28063 frame, di cui 4671 HTTP)
```

Tutto il traffico è HTTP su TCP. Si filtra subito con:

```
http
```

Si notano immediatamente migliaia di richieste GET verso `/product?id=...`.

### Passo 2 — Identificazione dell'attacco

Si applica il filtro:

```
http.request.uri contains "SELECT"
```

Le URI decodificate rivelano query SQL iniettate nel parametro `id`:

```
/product?id=1 AND (SELECT substr((SELECT pin FROM users WHERE username='admin'), 1, 1)) = 'a'
```

Il pattern è inequivocabile: si tratta di una **Blind Boolean-Based SQL Injection**. L'attaccante testa un carattere alla volta su una posizione fissa, sfruttando la differenza di risposta HTTP:

- `200 OK` → condizione vera, carattere corretto
- `404 Not Found` → condizione falsa, carattere sbagliato

In totale sono presenti **2336 richieste GET** automatizzate.

### Passo 3 — Isolamento delle risposte positive

Per trovare i caratteri che hanno avuto successo, si filtrano le risposte `200 OK`:

```
http.response.code == 200
```

Si ottengono **53 frame** con risposta positiva. Per ciascuno, si risale alla richiesta corrispondente:

1. Click sul pacchetto di risposta `200`
2. Nel pannello **Hypertext Transfer Protocol**, si legge `Request in frame: N`
3. Ci si sposta al frame N (`Ctrl+G`) e si legge la URI

In alternativa, tramite `File` → `Export Packet Dissections` → `As CSV`, si esporta tutto e si filtra per codice `200` offline.

### Passo 4 — Ricostruzione dei dati esfiltrati

Correlando le 53 risposte `200 OK` con le rispettive richieste e ordinando per posizione (`substr(..., N, 1)`), si ricostruiscono i valori estratti dal database:

**Tabella `users` — campo `pin` (admin):**

| Pos | Char | Frame |
|-----|------|-------|
| 1 | `8` | 728 |
| 2 | `2` | 1388 |
| 3 | `9` | 2132 |
| 4 | `1` | 2780 |

**Tabella `users` — campo `password` (admin):**

| Pos | Char | Pos | Char |
|-----|------|-----|------|
| 1 | `a` | 9 | `s` |
| 2 | `d` | 10 | `s` |
| 3 | `m` | 11 | `_` |
| 4 | `i` | 12 | `8` |
| 5 | `n` | 13 | `3` |
| 6 | `_` | 14 | `7` |
| 7 | `p` | 15 | `2` |
| 8 | `4` | | |

**Tabella `backup_codes` — campo `code` (id=1):**

```
BKP-8922-A1B9-4002
```

(I separatori `-` in posizione 4, 9 e 14 non compaiono nel dump perché l'attaccante li ha saltati nella sua enumerazione.)

**Tabella `secrets` — campo `flag` (id=1):**

| Pos | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
|-----|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|-----|
| Char | `f` | `l` | `a` | `g` | `{` | `b` | `l` | `1` | `n` | `d` | `S` | `Q` | `L` | `_` | `H` | `e` | `l` | `l` | `0` |

### Passo 5 — Riepilogo dei dati esfiltrati

| Tabella | Campo | Valore |
|---------|-------|--------|
| `users` | `pin` | `8291` |
| `users` | `password` | `admin_p4ss_8372` |
| `backup_codes` | `code` | `BKP-8922-A1B9-4002` |
| `secrets` | `flag` | `flag{bl1ndSQL_Hell0}` |

---

## Flag

```
flag{bl1ndSQL_Hell0}
```

---

## Conclusioni

La challenge dimostra come una Blind Boolean-Based SQL Injection permetta di esfiltrare dati sensibili **senza alcun trasferimento di file** e senza far crashare il server, motivo per cui il firewall non ha rilevato nulla di anomalo. L'unico segnale era il volume di richieste HTTP (2336 GET in rapida successione verso lo stesso endpoint). La ricostruzione dei dati è stata possibile identificando le 53 risposte `200 OK` tra le 404, ognuna corrispondente a un carattere indovinato correttamente e riordinandole per posizione.