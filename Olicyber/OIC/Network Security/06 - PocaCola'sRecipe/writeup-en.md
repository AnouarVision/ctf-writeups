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
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            payload = tcp.data

            if b'PK\x03\x04' in payload:
                print(f"ZIP file found! ({len(payload)} bytes)")

                pk_idx = payload.find(b'PK\x03\x04')
                zip_data = payload[pk_idx:]

                with open('recipe.txt.zip', 'wb') as f:
                    f.write(zip_data)
                print("Saved: recipe.txt.zip")
                break
        except:
            pass

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

### Step 4 — Opening the ZIP and Reading the Flag

Open `recipe.txt.zip` with the password found above. Inside is `ricetta.txt`, which contains the flag:

```
flag{...}
```

---

## Conclusions

1. **Wireshark Filtering**: Use specific HTTP filters to isolate relevant traffic (`http.request.method == POST && frame contains "keyword"`).
2. **Magic Bytes Extraction**: Multipart/form-data payloads contain header overhead; locating the `PK` magic bytes in the payload allows the ZIP file to be saved correctly.
3. **Credentials in Plaintext**: Sensitive information like passwords is often transmitted in cleartext TCP traffic; a simple `frame contains "password"` filter is enough to expose it.

