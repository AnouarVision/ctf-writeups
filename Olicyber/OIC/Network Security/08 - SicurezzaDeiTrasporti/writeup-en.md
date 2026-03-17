# Sicurezza dei Trasporti

**Competition:** OliCyber<br>
**Category:** Network<br>
**Files:** capture.pcapng, keys.log

---

## Description

> Please help us find the content of the web pages from this traffic log. There's an additional file, it might be useful...

---

## Solution

### Step 1 — Analyzing the PCAP and Recognizing TLS 1.3

The file `capture.pcapng` contains traffic encrypted with TLS 1.3. The presence of the `keys.log` file (SSLKEYLOG format) indicates that it is possible to decrypt the traffic if the keys are configured correctly.

### Step 2 — Configuring Wireshark for TLS 1.3 Decryption

1. Open Wireshark
2. Go to **Edit → Preferences → Protocols → TLS**
3. In the **(Pre)-Master-Secret log filename** field, select the `keys.log` file
4. Click **Apply** and **OK**

The `keys.log` file contains the master secrets in the standard SSLKEYLOG format:

```
CLIENT_TRAFFIC_SECRET_0 <session_id> <secret_key>
SERVER_TRAFFIC_SECRET_0 <session_id> <secret_key>
```

### Step 3 — Opening the PCAP and Filtering HTTP Traffic

1. **File → Open** → Select `capture.pcapng`
2. Wireshark will automatically decrypt the TLS 1.3 traffic
3. Filter by `http` to display the decrypted HTTP packets
4. Look for DATA packets containing HTML responses

### Step 4 — Identifying the Response Containing the Flag

Analyzing the decrypted traffic, an HTTP GET request to an internal server (3.125.223.134) is found:

- **Request:** `GET /` (Stream ID 1)
- **Response:** Contains the HTML content with the flag

Expanding the packet under **Hypertext Transfer Protocol → Line-based text data**, the flag is clearly readable:

```
flag{...}
```

### Step 5 — Verification

The flag appears in the decrypted traffic as a response to an HTTP GET request to the internal host. The HTML content of the response contains the flag in plaintext.

---

## Conclusions

1. **TLS 1.3 Decryption**: Wireshark can decrypt TLS 1.3 traffic using an SSLKEYLOG file, which contains the session keys extracted during the handshake.
2. **SSLKEYLOG Format**: A standard for saving TLS master secrets, natively supported by browsers and capture tools for forensic and debugging purposes.
3. **Essential Configuration**: To analyze encrypted TLS traffic, you need to:
   - Have access to the session keys or master secrets
   - Correctly configure the keylog file path in Wireshark
   - Reload the PCAP after configuration
4. **The Security Paradox**: Even with TLS 1.3 (strong modern encryption), if an attacker has access to the master secrets, they can decrypt all traffic. Transport security depends on the secrecy of the keys, not the algorithm.
