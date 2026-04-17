# Software 01 - Architetture

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Nella prima challenge viene richiesto di trovare l'architettura del file ELF. Il formato della flag è `flag{architettura}`.

Viene fornito un file binario `sw-01`. L'obiettivo è determinare per quale architettura hardware è stato compilato.

---

## Il formato ELF

Prima di rispondere alla domanda, vale la pena capire cosa stiamo guardando. Su Linux, i programmi eseguibili seguono il formato **ELF**, *Executable and Linkable Format*. Non è un semplice blob di codice macchina: è un file strutturato con una intestazione (*header*) che descrive tutto ciò che il sistema operativo ha bisogno di sapere per caricare ed eseguire il programma.

I primi 64 byte di ogni file ELF contengono l'*ELF header*, un manifesto che dichiara, tra le altre cose:

- se il file è a 32 o 64 bit
- se usa il formato little-endian o big-endian
- il **tipo di macchina** per cui è stato compilato
- l'indirizzo del punto di ingresso (`main`)
- dove si trovano le sezioni di codice e dati

Conoscere questa struttura è il prerequisito indispensabile per qualsiasi attività di reverse engineering.

---

## Soluzione

### Step 1 — Il comando `file`

Il primo strumento da impugnare di fronte a un binario sconosciuto è `file`. Il suo funzionamento è elegante nella sua semplicità: invece di fidarsi dell'estensione del file (che chiunque può cambiare), ispeziona i primi byte del contenuto (i cosiddetti **magic bytes**) e li confronta con un database di firme note.

```bash
$ file sw-01
sw-01: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV),
       statically linked, BuildID[sha1]=0073012c38af01374a53569a0d79290259d34d8d,
       not stripped
```

In una sola riga, `file` ci restituisce un'analisi straordinaria:

- `ELF 64-bit`: il formato è ELF, architettura a 64 bit
- `LSB`: *Least Significant Byte first*, ovvero little-endian
- `executable`: è un eseguibile, non una libreria o un object file
- **`ARM aarch64`**: compilato per processori ARM a 64 bit
- `statically linked`: non dipende da librerie esterne a runtime
- `not stripped`: i simboli di debug sono presenti, una manna per il reverse engineer

La risposta è già qui. Ma fermarsi a `file` sarebbe come ammirare la copertina di un libro senza aprirlo.

---

### Step 2 — Il comando `readelf`

`readelf` è lo strumento che permette di ispezionare la struttura interna di un file ELF con grande precisione. L'opzione `-h` (*header*) mostra l'intestazione completa:

```bash
$ readelf -h sw-01
Intestazione ELF:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Classe:                            ELF64
  Dati:                              complemento a 2, little endian
  Version:                           1 (current)
  SO/ABI:                            UNIX - System V
  Tipo:                              EXEC (file eseguibile)
  Macchina:                          AArch64
  Indirizzo punto d'ingresso:        0x40010c
  ...
```

Ogni campo merita attenzione:

**Magic bytes**: `7f 45 4c 46` sono i primi 4 byte di ogni file ELF. `0x45 0x4c 0x46` corrispondono alle lettere ASCII `E`, `L`, `F`. Il byte `0x7f` è il delimitatore. Questi 4 byte sono la firma che `file` riconosce.

**Classe: ELF64**: il byte in posizione 4 del magic (`02`) indica un binario a 64 bit. `01` sarebbe 32 bit.

**Dati: little endian**: il byte in posizione 5 (`01`) indica little-endian. `02` sarebbe big-endian. Questo determina come i valori multi-byte vengono memorizzati in memoria.

**Macchina: AArch64**: il campo `e_machine` dell'header, codificato come intero a 16 bit. Il valore corrispondente ad AArch64 è `0xB7` (183 decimale). Questo campo è la fonte autorevole sull'architettura target.

**Indirizzo punto d'ingresso: `0x40010c`**: l'indirizzo virtuale da cui inizia l'esecuzione. Per un reverse engineer, questo è il punto di partenza dell'analisi.

---

### Flag

```
flag{aarch64}
```

---

## Conclusioni

Questa challenge introduce due strumenti che accompagneranno ogni analisi di file binari:

`file` è il primo approccio: veloce, leggibile, immediato. Va usato **sempre** come primo passo davanti a qualsiasi file sconosciuto, non solo per gli ELF. Sa riconoscere centinaia di formati diversi: archivi, immagini, documenti, firmware.

`readelf` è lo strumento di precisione, permette di leggere ogni struttura interna dell'ELF: header (`-h`), sezioni (`-S`), segmenti (`-l`), simboli (`-s`), stringhe (`-p`), note (`-n`). Durante il reverse engineering e il pwn, questi dettagli diventano fondamentali: sapere dove si trovano le sezioni `.text`, `.data`, `.bss`, `.plt` e `.got` è la base su cui si costruisce qualsiasi analisi più approfondita.