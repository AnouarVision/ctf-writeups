# Papioutai

**Competition:** 404CTF 2026 <br>
**Category:** OSINT

<img src="papioutai.png">

---

## Soluzione

### L'annuario ENS

Ammetto che, appena ho visto il titolo "Papioutai", il mio cervello ha fatto immediatamente partire Stromae in autoplay: “Papa où t’es?”. Scherzi a parte, l'idea della challenge è quella di cercare il bisnonno di qualcuno.

La prima cosa ovvia è trovare l’anno di promozione dell’“Ulmien” citato. “Ulmien” infatti indica un ex‑studente dell’École Normale Supérieure di Parigi (ENS Ulm) e per fortuna esiste un annuario online degli ex‑alunni su archicubes.ens.fr.

Sono andato su: https://www.archicubes.ens.fr/lannuaire e ho cercato `Roux Jean`.
Il risultato è questo:

<img src="annuaire.png">


La lettera `l` indica la promotion littéraire del concorso Ulm. Il candidato corretto è chiaramente **Jean Roux, 1912 l**.

L’unico problema è che la città di nascita non è riportata nell’annuario. Quindi si avanti con l’indagine.

## Ragionamento sull'anno di nascita

Ho cercato di ragionare sull'età. Un normalien della **promozione 1912**, quanti anni poteva avere? All’ENS si entra di solito intorno ai **19–20 anni**, dopo due anni di prépa. Quindi il nostro Jean Roux dovrebbe essere nato più o meno tra il **1891 e 1893**.

Per verificare, ho aperto la ricerca su Mémoire des Hommes (https://www.memoiredeshommes.defense.gouv.fr/recherche-globale/rechercher-dans-les-bases-nominatives?arko_default_66fa612acbc0d--ficheFocus=) e ho cercato semplicemente `Roux` e `Jean`, senza filtri sul luogo di morte. Poi mi sono messo a scorrere tutta la lista filtrando **a mano** per anno di nascita.
Spoiler: erano tipo una trentina. La Grande Guerra non ha risparmiato i Jean Roux.

<img src="jeanrouxmemoire.png">

I candidati che rientrano nel range giusto sono:

```
Jean    31/3/1891   dep. 17 (Charente-Maritime)   morto 18/10/1914
Jean    22/4/1893   dep. 33 (Gironde)              morto 15/10/1914
Jean    30/6/1892   dep. 19 (Corrèze)              morto 19/6/1916
```

I primi due sono morti nell’ottobre 1914, cioè nei **primissimi mesi della guerra**: perfettamente plausibile per uno studente ENS appena mobilitato.

## Apertura dei permalink uno per uno

Ogni risultato su Mémoire des Hommes aveva un permalink ARK del tipo:
```
https://www.memoiredeshommes.defense.gouv.fr:443/ark:40699/m005239ff9658531.moteur=...
```

Ne ho aperti diversi a mano. I primi erano soldati normali, morti in posti che non c'entravano nulla. In realtà, stavo già per mollare e cercare in un altro database quando ho aperto quello del Jean nato il 22/4/1893 in Gironde:
https://www.memoiredeshommes.defense.gouv.fr/conflits-et-operations-2/premiere-guerre-mondiale/morts-pour-la-france-de-la-premiere-guerre-mondiale/faire-une-recherche?detail=4309972

<img src="realjeanroux.png">

E lì… bingo.

**Courdemanges**, il nome **finisce con "demanges"**.

Reclutato a Bordeaux, morto a 21 anni nell’ottobre 1914. Mi torna tutto: nato nel 1893, promozione ENS 1912 (a 19 anni) e cade a Courdemanges durante i combattimenti dell’autunno 1914 sulla Marna.

Saint-Estèphe peraltro è il famoso paese dei vini di Bordeaux, zona dello Médoc. Dettaglio inutile ma mi ha fatto sorridere.

## Flag

<img src="saint-estephe.png">

```
404CTF{1912_saint-estèphe}
```
