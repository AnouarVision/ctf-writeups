# Click Me

**Competizione:** OliCyber<br>
**Categoria:** Web<br>
**URL:** http://click-me.challs.olicyber.it

---

## Descrizione

> Ho creato un clicker game, riesci ad arrivare a 10000000 biscotti?

Una semplice pagina con un gioco clicker dove bisogna raggiungere 10 milioni di biscotti. A prima vista, sembra richiedere 10 milioni di click manuali, ma il codice contiene un'evidente vulnerabilità.

---

## Soluzione

### Step 1 — Analisi del Codice HTML

Visitando il sito e ispezionando il codice sorgente (F12 → Sources/Elements), troviamo l'intera logica del gioco:

```javascript
var num = 0;
window.onload = function () {
    var name = prompt("Inserisci il tuo nome");
    var space = document.getElementById("space");
    space.innerHTML = "Pasticceria da: " + name;
}
var cookie = document.getElementById("cookie");
function cookieClick() {
    num += 1;
    var numbers = document.getElementById("numbers");
    document.cookie = "cookies="+num;
    numbers.innerHTML = num;
}
```

---

### Step 2 — Identificazione della Vulnerabilità

Il codice ha una vulnerabilità evidente: **la variabile `num` è accessibile e modificabile direttamente dalla console del browser**.

La funzione `cookieClick()` incrementa semplicemente `num` di 1, ma non c'è alcun controllo:
- Nessuna validazione lato server
- La variabile è globale e modificabile
- Il valore è salvato solo in un cookie non protetto

---

### Step 3 — Exploit via Console Browser

Aprire la console del browser (`F12` → Console) e eseguire il seguente comando:

```javascript
num = 10000000;
document.getElementById("numbers").innerHTML = num;
document.cookie = "cookies=10000000";
```

---

### Step 4 — Risultato

Dopo aver eseguito uno dei comandi precedenti, la pagina mostrerà `10000000` e rivelerà la flag della challenge.

## Conclusioni

Questo è un classico esempio di **insicurezza lato client**. I problemi principali sono:

1. **Nessuna validazione lato server**: il conteggio dei biscotti è gestito interamente dal client
2. **Variabili globali modificabili**: `num` è accessibile dalla console
3. **Nessuna autenticazione/autorizzazione**: non c'è controllo su chi modifica i dati
4. **Cookie non protetti**: il valore del cookie non è firmato o crittografato

In un gioco reale, il server dovrebbe:
- Gestire il conteggio lato server
- Validare ogni click con un token o session ID
- Proteggere i dati con firme crittografiche (HMAC)
- Implementare rate limiting per evitare abusi

---