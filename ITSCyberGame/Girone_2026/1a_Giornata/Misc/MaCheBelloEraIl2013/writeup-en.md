# What a great 2013 was...

**Competition:** ITSCyberGame
**Category:** Misc
**Zip:** segreti.zip

---

## Description

> The summer of 2013 was awesome; I saved everything in that secret folder, if only I could remember the password...

The provided file is a password-protected zip `segreti.zip`. Inside is a single hidden file: `.flag.txt`.

---

## Solution

### 1. Inspect the archive

List the archive contents:

```bash
unzip -l segreti.zip
```

```
Archive:  segreti.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        69  2026-02-02 15:12   .flag.txt
---------                     -------
        69                     1 file
```

The archive contains a single hidden file, `.flag.txt`, protected by a password.

### 2. Interpretation

The hint mentions the **summer of 2013** and a "secret folder". Use a password wordlist with common passwords from that era — `rockyou.txt` is a suitable choice.

### 3. Crack the zip password with John the Ripper

Extract the hash from the zip:

```bash
zip2john segreti.zip > hash.txt
```

If needed, decompress the `rockyou.txt` wordlist:

```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

Run John with the wordlist:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

Example output (password found quickly):

```
Loaded 1 password hash (PKZIP [32/64])
monkey           (segreti.zip/.flag.txt)
1g 0:00:00:00 DONE
```

Verify cracked password:

```bash
john --show hash.txt
# segreti.zip/.flag.txt:monkey:...
```

Password found: `monkey`.

### 4. Decode the flag

The `.flag.txt` contents are a hexadecimal string:

```
666c61677b546831735f5a31705f5734735f5072307433637433645f4234646c797d
```

You can decode it with Python:

```python
bytes.fromhex("666c61677b546831735f5a31705f5734735f5072307433637433645f4234646c797d").decode()
```

---

## Flag

```
flag{...}
```

---

## Conclusion

The challenge highlights that a weak password offers no real protection. Using a common password like `monkey` (even in 2013) makes the archive trivially crackable with a standard wordlist.
