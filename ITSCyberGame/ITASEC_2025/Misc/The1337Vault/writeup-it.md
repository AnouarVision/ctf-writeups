# The 1337 Vault

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**File:** the_1337_vault.7z

---

## Descrizione

> Solo i veri hacker sanno cosa significa essere 1337.
> Davanti a te c'è una cassaforte digitale con 1337 strati di crittografia compressa. Ogni livello che sblocchi ti avvicina a un segreto custodito da chi parla la lingua del leet.
> Riuscirai a dimostrare di essere degno e trovare la flag nascosta?

---

## Soluzione

Il titolo e la descrizione fanno riferimento esplicito a **1337 strati di compressione**. La strategia è chiara: automatizzare la decompressione ricorsiva fino a raggiungere il contenuto finale.

### Passo 1 — Analisi iniziale del file

```bash
$ file the_1337_vault.7z
the_1337_vault.7z: 7-zip archive data, version 0.3

$ 7z l the_1337_vault.7z
Path = the_1337_vault.7z
Type = 7z
Method = LZMA:23

   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2025-02-03 ...                  167469       169287  layer_1336.7z
```

Il file contiene un archivio chiamato `layer_1336.7z`. Il nome suggerisce che ogni layer contiene quello precedente, fino al layer 1 dove si trova la flag.

### Passo 2 — Decompressione ricorsiva

Estrarre manualmente 1337 archivi non è praticabile. Invece si utilizza lo script Python fornito, salvato nella stessa cartella come [the_1337_vault.py](the_1337_vault.py). Lo script copia il primo archivio in una directory temporanea, estrae ricorsivamente i file .7z e stampa il contenuto del file finale.

### Passo 3 — Esecuzione

Esegui lo script dalla cartella che contiene gli archivi:

```bash
$ python3 the_1337_vault.py
Content of flag.txt:
flag{...}
```

Dopo 1337 estrazioni, il layer 1 contiene `flag.txt` con la flag in chiaro; il contenuto viene stampato direttamente.