# There Is No Spoon

**Competizione:** ITSCyberGame<br>
**Categoria:** Web<br>

---

## Descrizione

> Neo ha ricevuto un messaggio segreto dal mondo reale ma gli Agenti lo hanno nascosto nel codice della simulazione. Solo chi sa dove guardare potrà trovarlo.

---

## Soluzione

Il titolo è già un hint: *"There Is No Spoon"*, non cercare l'ovvio. La pagina mostra solo un canvas animato con caratteri verdi che cadono e un messaggio generico. La flag non è visibile a schermo.

### Passo 1 — Ispezionare il Sorgente

La prima mossa in qualsiasi challenge web/misc è ispezionare il codice sorgente della pagina (`Ctrl+U` o DevTools). Scorrendo verso il basso, si trova un lungo commento HTML nascosto:

```html
<!--
Neo, the answer you seek is hidden within the code.
The Matrix has many secrets, but only the true chosen one will find it.

filo di codice scorre nel buio,
luci verdi danzano in un flusso continuo.
aspetti risposte, cerchi un motivo,
...
-->
```

Il commento contiene una poesia in italiano di 30 righe. Alcune righe iniziano con caratteri insoliti: lettere maiuscole nel mezzo di una frase, cifre numeriche, underscore e parentesi graffe `{` `}`. Questo è sospetto.

### Passo 2 — Leggere l'Acrostico

Estraendo il **primo carattere di ogni riga** della poesia, ricaviamo la flag:

```python
poem = """filo di codice scorre nel buio,
luci verdi danzano in un flusso continuo.
aspetti risposte, cerchi un motivo,
guarda più a fondo, segui l'istinto.
{Il mondo si piega, il codice è chiave,
...
}Ora decidi: pillola o cammino?"""

first_chars = [line[0] for line in poem.strip().split('\n')]
print(''.join(first_chars))
```

```
flag{...}
```

Si tratta di un **acrostico**: la flag è codificata verticalmente, nascosta nelle iniziali di ogni verso, una tecnica steganografica elementare ma efficace, resa invisibile dalla lunghezza del testo e dal contesto.