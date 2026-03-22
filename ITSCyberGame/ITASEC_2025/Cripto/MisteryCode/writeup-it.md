# Mystery Code

**Competizione:** ITSCyberGame<br>
**Categoria:** Crittografia<br>

---

## Descrizione

> Un partecipante di Squid Game ha trovato un piccolo biglietto nascosto sotto il suo letto scritto in un codice incomprensibile. Il biglietto sembra contenere un indizio segreto sul prossimo gioco che lui e gli altri partecipanti dovranno affrontare ma nessuno sa come leggerlo.
>
> Il messaggio nel biglietto è: `synt{7u3_134f7_p4a_j4gpu_7u3_s10j_j4ea3!}`

---

## Soluzione

La hint è nella descrizione: **"codice incomprensibile"**. La struttura `synt{...}` ricorda molto il formato `flag{...}`, il che suggerisce immediatamente una sostituzione alfabetica semplice.

### Passo 1 — Riconoscere il Cifrario

Osservando il testo cifrato `synt{...}`, si nota che:

- `synt` è lungo 4 caratteri, proprio come `flag`
- La struttura con le parentesi graffe è identica al formato della flag

Mappando lettera per lettera:

```
s → f
y → l
n → a
t → g
```

Lo shift tra `f→s`, `l→y`, `a→n`, `g→t` è sempre di **13 posizioni**. Si tratta di **ROT13**.

### Passo 2 — Decifrare il Messaggio

Applicando ROT13 all'intero testo cifrato otteniamo la flag:

```python
import codecs
cipher = "synt{7u3_134f7_p4a_j4gpu_7u3_s10j_j4ea3!}"
print(codecs.decode(cipher, 'rot_13')) #flag{...}
```