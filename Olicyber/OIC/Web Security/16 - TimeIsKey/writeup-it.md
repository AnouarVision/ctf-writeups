# Time is Key

**Competizione:** OliCyber<br>
**Categoria:** Web / Timing Attack<br>
**URL:** http://time-is-key.challs.olicyber.it

---

## Descrizione

> Non c'è tempo! Veloce! Prendi la flag ora!

Una challenge basata su **timing attack**: la risposta del server rivela quanti caratteri della flag sono corretti in base al tempo impiegato.

**Note:**
- La flag contiene solo lettere minuscole e numeri
- La flag NON è nel formato standard → va racchiusa manualmente in `flag{...}`

---

## Soluzione

### Step 1 — Analisi del sorgente

Il primo passo è recuperare il codice sorgente della pagina vulnerabile:

```bash
curl -s 'http://time-is-key.challs.olicyber.it/index.php?show_source'
```

```php
<?php
    $flag = getenv("flag");
    if (isset($_POST["flag"]) && !is_array($_POST["flag"])){
        $your_flag = $_POST["flag"];
        $flag_len = 6;
        if (strlen($your_flag) !== $flag_len){
            die("Sbagliato! :(");
        }
        for ($i = 0; $i < $flag_len; $i++){
            if ($your_flag[$i] !== $flag[$i]){
                die("Sbagliato! :(");    // si ferma subito
            }
            usleep(1000000);             // +1 secondo per ogni carattere corretto
        }
        die("Che stai aspettando? Invia la flag!");
    }
?>
```

---

### Step 2 — Comprensione della vulnerabilità

Il server confronta la flag inviata **carattere per carattere** e per ogni carattere **corretto** aspetta `1.000.000 µs` = **1 secondo** prima di passare al successivo. Al primo carattere sbagliato termina immediatamente.

Questo crea un **oracolo temporale** misurabile:

| Caratteri corretti | Tempo di risposta atteso |
|---|---|
| 0 | ~0.2s |
| 1 | ~1.2s |
| 2 | ~2.2s |
| 3 | ~3.2s |
| 4 | ~4.2s |
| 5 | ~5.2s |
| 6 | ~6.2s |

---

### Step 3 — Timing Attack

Invece di dover provare tutte le combinazioni possibili (`36^6 ≈ 2 miliardi`), il timing attack riduce il problema a `36 × 6 = 216 tentativi` — uno per carattere per posizione.

Per ogni posizione, testiamo tutti i caratteri possibili e misuriamo il tempo di risposta. Il carattere che produce il tempo più lungo è quello corretto.

---

### Step 4 — Automazione del Timing Attack

Per automatizzare il timing attack, uno script Python testa tutti i caratteri possibili per ogni posizione e identifica quale produce il tempo di risposta più lungo.

La strategia è:
1. Per ogni posizione della flag (0-5)
2. Testare tutti i caratteri possibili (a-z, 0-9)
3. Misurare il tempo di risposta
4. Il carattere con il tempo più lungo è quello corretto
5. Ripetere fino a completare la flag

**Lo script Python per l'exploit è disponibile in questa cartella → [`timeiskey.py`](timeiskey.py)**

---

### Step 5 — Output atteso

Lo script testa tutti e 36 i caratteri per ogni posizione. Per la prima posizione, ad esempio:

```
  [1/6] aaaaaa → 0.19s
  [1/6] baaaaa → 0.18s
  [1/6] caaaaa → 0.20s
  ...
  [1/6] 7aaaaa → 1.21s       ← picco di tempo! Il carattere corretto è '7'
  ...
  [1/6] 9aaaaa → 0.19s

[+] Flag finora: 7 (tempo: 1.21s)

  [2/6] 7aaaaa → 1.20s
  [2/6] 7baaaa → 1.19s
  ...
  [2/6] 71aaaa → 2.22s       ← picco di tempo! Il carattere corretto è '1'
  ...

[+] Flag finora: 71 (tempo: 2.22s)

  ...

[+] Flag finora: 71m1n6 (tempo: 6.21s)

flag{71m1n6}
```

Il pattern è netto: un tentativo sbagliato impiega ~0.2s, mentre ogni carattere corretto aggiunge esattamente **~1 secondo** al tempo di risposta, rendendo il picco facilmente identificabile.

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | Timing Attack (Time-Based Oracle) |
| **Causa** | `usleep()` eseguito solo dopo un carattere corretto |
| **Effetto** | Il tempo di risposta rivela quanti caratteri sono giusti |
| **Impatto** | Enumerazione della flag carattere per carattere |

---

## Conclusioni

- I timing attack sono reali e difficili da mitigare completamente
- Non usare `usleep()` o delay a livello di logica di business per misure di sicurezza
- Implementare **constant-time comparison** (es. `hash_equals()` in PHP)
- Aggiungere **jitter casuale** ai tempi di risposta per nascondere i pattern
- Implementare **rate limiting** per prevenire test automatizzati
- Loggare i tentativi falliti e bloccare client con troppi errori