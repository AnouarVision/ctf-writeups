# Canular savant (1/3)

**Competizione:** 404CTF 2026 <br>
**Categoria:** OSINT

<img src="canular_savant.png">

---

## Soluzione

Ho aperto Google e ho provato una ricerca del tipo:

```
paris rond-point plusieurs fontaines
```

Tra i primi risultati sono apparse subito le Champs‑Élysées. Era una scelta piuttosto intuitiva dati gli elementi forniti: Parigi, fontane e rond‑point, puntano direttamente al **rond‑point des Champs‑Élysées**, che è il più iconico e presenta sei fontane disposte in modo simmetrico.

<img src="fontaine.png">

Ho provato subito:
```
404CTF{rond-point_des_champs-elysees}
```

Cosa avrò sbagliato?

Forse serviva il nome completo. Ho aperto la pagina Wikipedia del rond‑point des Champs‑Élysées e ho scoperto che dal 1991 il nome ufficiale è **“Rond‑point des Champs‑Élysées‑Marcel‑Dassault”**. Ecco perché la mia flag non veniva accettata.

<img src="rond-point.png">


Ho fatto un nuovo tentativo:

```
404CTF{rond-point_des_champs-elysees-marcel-dassault}
```

Finalmente è corretta.

---

## Flag

```
404CTF{rond-point_des_champs-elysees-marcel-dassault}
```