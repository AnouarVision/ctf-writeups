# Wi-Fi

**Competition:** FCSC 2022 (intro) <br>
**Category:** Misc <br>
**File:** `intro-wifi_pcap.xz`<br>
**Network password:** `FCSC p0w3r is the answer`

---

## Description
> Saurez-vous déchiffrer cette capture Wi-Fi ? Le mot de passe du réseau est FCSC p0w3r is the answer.

A Wi‑Fi network capture is provided (pcapng, compressed with xz). Traffic is protected with WPA2. The network password is given — decrypt the capture and find the flag in cleartext traffic.

---

## Solution

### 1. Recon

Decompress the `.xz` archive and open the pcapng file with Wireshark.

The first frames are Beacon frames from the `FCSC-WiFi` network. Scrolling through the capture shows four EAPOL frames — the complete WPA2 4‑way handshake:

| Frame | Type |
|-------|------|
| 162 | EAPOL Key — Message 1 of 4 |
| 164 | EAPOL Key — Message 2 of 4 |
| 166 | EAPOL Key — Message 3 of 4 |
| 168 | EAPOL Key — Message 4 of 4 |

Complete handshake = we can decrypt the WPA2 traffic.

---

### 2. Decrypt WPA2 traffic

#### Step 1 — Open IEEE 802.11 preferences

Go to:

```
Edit → Preferences → Protocols → IEEE 802.11
```

or open `Edit → Preferences` and search for `802.11`.

#### Step 2 — Enable decryption

In **IEEE 802.11**, ensure:

```
☑ Enable decryption
```

is checked.

#### Step 3 — Add the WPA2 key

Click the `Edit...` button next to *Decryption keys*.
Click the **+** to add a new key and fill fields as:

| Field | Value |
|-------|-------|
| **Key type** | `wpa-pwd` |
| **Key** | `FCSC p0w3r is the answer:FCSC-WiFi` |

Format is `password:SSID` (colon separator). The SSID is `FCSC-WiFi`.

Click **OK** to close the keys window, then **OK** again to close Preferences.

#### Step 4 — Verify decryption

Wireshark will re-dissect the capture. Frames that previously showed encrypted `Data` should now show clear protocols like **DHCP, DNS, ARP, HTTP**.

---

### 3. Find the flag — Follow HTTP Stream

In the display filter, enter:

```
http
```

and press Enter. Two HTTP frames appear:

- `GET /my_precious HTTP/1.1` — the client request
- `HTTP/1.0 200 OK` — the server response containing the flag

Right‑click the response frame (`HTTP/1.0 200 OK`) → **Follow → TCP Stream**.
The TCP stream window shows the full session; the response body contains the flag:

```
HTTP/1.0 200 OK
...

FCSC{...}
```

---

## Flag

```
FCSC{...}
```

---

## Conclusion

Classic WPA2 decryption with Wireshark. Key points:

- The 4‑way EAPOL handshake is present in the capture, allowing decryption.
- Wireshark accepts WPA2 keys under `Edit → Preferences → IEEE 802.11` using `password:SSID` format.
- The flag was transported in cleartext HTTP at `/my_precious`.
