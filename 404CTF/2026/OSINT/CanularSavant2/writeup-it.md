# Canular savant (2/3)

**Competizione:** 404CTF 2026 <br>
**Categoria:** OSINT

<img src="canular2.png">

---

## Soluzione
### Ricerca delle band alternative di Columbus
La prima cosa che ho fatto è stata chiedermi quali band alternative note provengano da Columbus. Una rapida ricerca su Google mi ha dato qualche nome interessante.
<img src="bands.png">

Per completezza, ho aperto anche la pagina Wikipedia dedicata agli artisti musicali della città, così da avere una lista più ampia.

<img src="colombus.png">

Onestamente non ne conoscevo quasi nessuno, quindi ho deciso di partire dai più famosi: i **Twenty One Pilots**.

### Cercare riferimenti nelle lyrics dei Twenty One Pilots

Dopo aver individuato i Twenty One Pilots come la band più famosa di Columbus, ho provato a verificare se nelle loro canzoni comparisse qualche riferimento a scienziati francesi. Ho iniziato con una ricerca mirata:

```
Twenty One Pilots lyrics french scientists group
```
<img src="query_lyrics.png">

Il primo risultato rimanda alle lyrics di **Morph** dall'album *Trench* (2018).

<img src="genius.png">

Nel secondo verse compare un riferimento esplicito a **Nicolas Bourbaki**.

Primo momento "aspetta, cosa?", non avevo mai sentito parlare di Bourbaki in un contesto musicale.


### Chi diavolo è Nicolas Bourbaki

Per capire il riferimento, ho aperto la pagina Wikipedia dedicata e ho iniziato a leggere.

<img src="nicolas_bourbaki.png">

Scopro subito che Nicolas Bourbaki **non è una persona reale**, ma lo pseudonimo collettivo di un gruppo di matematici (quasi tutti francesi) fondato a Parigi negli anni ’30.

Tra i membri fondatori compaiono Henri Cartan, Claude Chevalley, Jean Delsarte, Jean Dieudonné e André Weil, tutti ex studenti dell’École Normale Supérieure.

Poi ho notato una cosa che mi ha fatto ridere: il nome "Bourbaki" fu scelto per via di un **canular**, uno scherzo accademico degli anni ’20.
Un tizio si era travestito da professore con la barba finta e aveva tenuto una conferenza di matematica volutamente incomprensibile e piena di errori, firmandosi "Bourbaki".

La challenge si chiama **"Canular savant"**. Il titolo era già l’indizio, solo che non lo avevo ancora collegato.

---


## Flag

<img src="bourbaki.png">

```
404CTF{nicolas-bourbaki}
```