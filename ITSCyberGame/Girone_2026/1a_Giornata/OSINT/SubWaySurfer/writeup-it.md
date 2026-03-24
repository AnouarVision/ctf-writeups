# SubWaySurfer

**Competizione:** ITSCyberGame<br>
**Categoria:** OSINT<br>
**Target:** `@alinacustoza65`

---

## Descrizione

> Questo profilo instagram mi ha scritto un messaggio strano @alinacustoza65

---

## Soluzione

### Passo 1 — Ricerca Google dei commenti indicizzati

Il punto di partenza è il profilo Instagram `@alinacustoza65`. Invece di analizzare manualmente il profilo, si cerca su Google il nome utente assieme alla parola chiave `commented` per trovare commenti pubblici indicizzati su altri siti:

```
"alinacustoza65" "commented"
```

Il primo risultato è un profilo Reddit:

```
https://www.reddit.com/user/alinacustoza65
What are your most essential PSP mods? alinacustoza65 commented 2 mo. ago.
Qualcuno è mai riuscito a mettere linux su una psp?
```

### Passo 2 — Analisi del profilo Reddit

Visitando `u/alinacustoza65` su Reddit si trova un post nella subreddit `r/itscybergame`:

> Ho ricevuto un messaggio strano, non capisco cosa ci sia scritto
> `c3ludHtFM3FxMWdfTnkxNGZfMWFfR3UzX1AwenozYWdmfQ==`

### Passo 3 — Decodifica Base64

La stringa è codificata in Base64:

```bash
$ echo "c3ludHtFM3FxMWdfTnkxNGZfMWFfR3UzX1AwenozYWdmfQ==" | base64 -d
synt{E3qq1g_Ny14f_1a_Gu3_P0zz3agf}
```

### Passo 4 — Decodifica ROT13

Il risultato è ancora cifrato, il pattern `synt{...}` è il classico indicatore di ROT13 applicato a `flag{...}`:

```bash
$ python3 -c "import codecs; print(codecs.decode('synt{E3qq1g_Ny14f_1a_Gu3_P0zz3agf}', 'rot13'))"
flag{...}
```

---

## Flag

```
flag{...}
```