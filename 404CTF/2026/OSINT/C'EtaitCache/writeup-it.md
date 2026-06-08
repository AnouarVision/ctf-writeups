# C'était caché

**Competizione:** 404CTF 2026 <br>
**Categoria:** OSINT

<img src="c'etaitcache.png">

---

## Soluzione
### Ricostruzione dell’immagine censurata
<img src="censure.png">

La challenge fornisce un’immagine che mostra lo screenshot di una repository pubblica, quasi interamente oscurata da grossi scarabocchi rossi. Ingrandendo però si distingue ancora qualcosa nella barra dell’URL: si leggono pezzi come `alice-reco...`, `...ileur-repo-pos...` e alla fine `FLAG.TXT`. Vediamo anche dei commit. Il resto viene coperto.

Ok, `alice-reco` + "grande dame française de l'informatique", ho cercato su Google:

```
alice reco informatique française
```
<img src="alice-recoque.png">

Primo risultato: **Alice Recoque**, pioniera dell'informatica francese, una delle prime donne a lavorare sui grandi calcolatori negli anni '60-'70.


Il pezzo di URL che si vedeva era chiaramente `alice-recoque` come username.

<img src="repo.png">

Il suo profilo GitHub contiene una sola repository pubblica: `le-meilleur-repo-possible` (esattamente ciò che si intravedeva nel pezzo `...ileur-repo-pos...`).

Nello screenshot compariva anche la lista dei commit, tutti con messaggi del tipo “gros ch…”, fatti da `alice-r...`, con uno effettuato circa 19 ore prima. Inoltre, nella barra dell’URL si intravedeva ancora `FLAG.TXT`, che rimandava chiaramente a un file presente all’interno della repository.

### Esplorazione della cronologia Git

```bash
git clone https://github.com/alice-recoque/le-meilleur-repo-possible.git
cd le-meilleur-repo-possible
```

Dopo aver clonato la repository, il primo passo è analizzare la cronologia completa dei commit. Per farlo utilizziamo:
```bash
git log --all --name-status
```
Questo comando mostra l’intera history della repo, includendo per ogni commit anche l’elenco dei file modificati, aggiunti o rimossi.

<img src="gitall.png">

L’output è enorme: compaiono tante rinominazioni, tutte con lo stesso pattern, da maiuscolo a minuscolo, ad esempio `R100 A/A/A.TXT a/a/a.txt`.

A questo punto decido di cercare la stringa 404CTF in tutta la history, includendo ogni commit:

```bash
git rev-list --all | xargs git grep -a "404CTF"
```

<img src="flag.png">

Tramite `git rev-list --all | xargs git grep`, abbiamo individuato il file `s/t/k/flag.txt` (S/T/K/FLAG.TXT nei commit più datati) come contenitore della flag. Osservando la cronologia, si nota che quasi tutti i commit successivi riportano il valore `CENSURÉ`.

Questo comportamento indica che Alice Recoque si è accorta di aver pubblicato accidentalmente la flag in chiaro su una repository pubblica. Per rimediare ha iniziato a sostituire il contenuto con `CENSURÉ` nei commit successivi, ma senza rimuovere le versioni precedenti dalla history. Di conseguenza, la flag originale rimane comunque recuperabile analizzando i commit più vecchi.

---

## Flag

<img src="evangelin.png">

```
404CTF{PLuT0T_FriTE5_0û_P0T@T03S?}
```
