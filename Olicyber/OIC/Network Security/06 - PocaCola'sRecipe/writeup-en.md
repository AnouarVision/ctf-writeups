# Poca Cola's Recipe

**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** intercepted.pcap

---

## Description

> I've been hiding under a table at Poca Cola headquarters for 3 days, I've captured all their communications! Please find the secret recipe so I can get out of here...

---

## Solution

### Step 1 — Filtering POST Requests Containing "ricetta"

Apply the following Wireshark filter:

```
http && http.request.method == POST && frame contains "ricetta"
```

This isolates exactly the POST packets containing the word "ricetta" (recipe), where the malware is transmitting the secret recipe file.

### Step 2 — Extracting the HTTP Payload

From the filtered POST frames, extract the binary payload. The payload contains multipart/form-data with the recipe ZIP file. The data starts with the magic bytes `PK` (0x504B) right after the HTTP header.

**Extraction with Python:**

```python
import dpkt

with open('intercepted.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)

    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        payload = bytes(tcp.data)

        if b'POST' in payload and b'ricetta' in payload:
            split_idx = payload.find(b'\r\n\r\n')
            http_body = payload[split_idx + 4:]

            with open('recipe.txt.zip', 'wb') as f:
                f.write(http_body)
```

### Step 3 — Finding the Password

Apply a filter to find packets containing the word "password":

```
frame contains "password"
```

Inspecting the TCP packets that match, the following message is found:

```
Damn it Rick, you need to be more careful, write it down somewhere,
the password is "qhcdpoktbjdsujbsrpjwr"
```

**Password:** `qhcdpoktbjdsujbsrpjwr`

### Step 4 — Extracting the ZIP File

The HTTP payload contains multipart/form-data. The `PK` magic bytes are located 118 bytes from the start of the body. After extracting the correct binary data, the resulting ZIP file is AES-encrypted (method 99).

To decompress it, use a library that supports AES:

```python
import pyzipper

with pyzipper.AESZipFile('recipe_extracted.zip', 'r') as z:
    z.extractall(pwd='qhcdpoktbjdsujbsrpjwr'.encode())
```

### Step 5 — Reading the Secret Recipe

Decompressing the archive yields `ricetta.txt`, which contains the flag:

```
flag{...}
```

---

## Conclusions

1. **Wireshark Filtering**: Use specific HTTP filters to isolate relevant traffic (`http.request.method == POST && frame contains "keyword"`).
2. **Multipart Payload Extraction**: Files transmitted via HTTP multipart/form-data have header overhead that must be stripped before the binary file can be used.
3. **AES Encryption in ZIP**: Modern ZIP files support AES (method 99), which requires libraries like `pyzipper` in Python — the standard `zipfile` module does not support it.
4. **Credentials in Plaintext**: Sensitive information like passwords is often transmitted in cleartext TCP traffic; a simple `frame contains "password"` filter is enough to expose it.

