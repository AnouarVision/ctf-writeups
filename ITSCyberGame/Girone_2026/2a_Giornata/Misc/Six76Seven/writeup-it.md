# six76seven

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** six76seven.tar.gz

---

## Descrizione

> git gud

Viene fornito un archivio contenente una repository git. L'obiettivo è trovare la flag analizzando la storia dei commit.

---

## Soluzione

### 1. Estrazione dell'archivio

```bash
tar -xf six76seven.tar.gz
cd six76seven
```

La directory contiene una repository git con un solo file: `README.md`.

### 2. Analisi della storia dei commit

```bash
git log --oneline --all
```

```
9c478bc Ritocca ritmo e punteggiatura
c4d5e20 Aggiungi una nota di energia
f841ba4 Semplifica la chiusura
744bc94 Rendi "memorabilli" più evocativo
d681c47 Espandi la comunità
d09e666 Rafforza collaborazione
03c32d5 Cambio forme verbali
5e9d8e1 Dettagli sul quartiere
28652c4 Incipit più scorrevole
44b5dbe Primo Commit
```

10 commit, tutti modifiche minori al `README.md`. Nessun branch nascosto, nessun tag.

### 3. Enumerazione di tutti gli oggetti git

La storia dei commit non contiene nulla di sospetto, ma git conserva nell'object store **tutti gli oggetti mai creati**, anche quelli non raggiunti da nessun commit. Si elencano tutti:

```bash
git cat-file --batch-all-objects --batch-check
```

```
03c32d57... commit 243
0a81b8ab... blob 474       ← dimensione anomala!
1622734c... blob 447
...
ee234aac... blob 373
ff0f62b9... blob 447
```

Ci sono **11 blob** ma solo **10 commit**, uno in più del necessario. Il blob `0a81b8ab` ha dimensione `474`, leggermente superiore agli altri. Si ispeziona il suo contenuto:

```bash
git cat-file blob 0a81b8ab8a3c8906ea433503ec60cec1d29c2dd3
```

```
# six76seven

nel cuore della città prende forma un progetto culturale che unisce persone
diverse e racconta sogni condivisi, tra strade e piazze vive. Forte Umanità
Costruisce Kermesse flag{...} Inclusive Creative
Elettrizzanti è il motto di volontari, artisti e studenti: lavorano fianco
a fianco con entusiasmo, coinvolgono anche i bambini e trasformano idee
semplici in momenti che restano, ogni anno, per tutta la comunità, con
energia contagiosa.
```

La flag è nascosta nel testo del blob orfano, tra le parole del paragrafo.

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge insegna che in git **nulla viene davvero eliminato** finché non si esegue un garbage collection (`git gc`). Un blob creato ma mai committato rimane nell'object store e può essere recuperato con `git cat-file`. Il titolo `six76seven` e l'hint `git gud` suggerivano di approfondire la conoscenza degli internals di git, andando oltre la semplice storia dei commit visibile con `git log`.