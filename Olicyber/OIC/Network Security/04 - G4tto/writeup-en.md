# G4tto

**Competition:** OliCyber<br>
**Category:** Network Forensics<br>
**File:** G4tt0.pcapng

---

## Description

> Will you be able to find the cat?

---

## Solution

The challenge revolves around finding a "cat" hidden inside captured network traffic.

### Step 1 — Analyzing the HTTP Traffic

Examining the PCAP file, an HTTP request is visible:

```
GET /HttpEcho/Gatto.jpeg HTTP/1.1
```

The server responds with a 66,182-byte JPEG file containing an image.

### Step 2 — Extracting the JPEG Image

Wireshark can automatically reassemble HTTP streams and save the transferred files. To do so:

1. Go to **File → Export Objects → HTTP...**
2. In the dialog that appears, look for the entry `Gatto.jpeg`
3. Select it and click **Save**

Opening the saved JPEG file reveals a cat image; the flag is visible directly in the image:

```
flag{...}
```

---

## Conclusions

1. **Binary File Extraction**: Wireshark's "Export Objects" feature reassembles and saves files transported over HTTP without manual effort.
2. **HTTP Payload Analysis**: HTTP responses often carry files that are key to solving the challenge.
3. **Lateral Thinking**: Sometimes the solution is not a hidden string but the object itself (the cat).
