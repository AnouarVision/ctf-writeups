# Strange Packets

**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** net2.pcap

---

## Description

> Today I found a strange device connected to my PC. I managed to capture these packets, but they seem completely harmless.

---

## Solution

The challenge presents a PCAP file with seemingly normal traffic: HTTPS connections to Google, Facebook, Kali forums, and other common sites. The key is in the hint "That is a lot of F", a reference to `0xFFFF` in hexadecimal.

### Step 1 — Identify the Anomalous Packets

Opening the PCAP in Wireshark, almost all the traffic is standard TCP/HTTPS. However, applying the filter:

```
eth.type == 0xFFFF
```

reveals **21 packets** with an invalid EtherType. `0xFFFF` does not correspond to any legitimate Ethernet protocol; these are the "really strange" packets mentioned in the description.

### Step 2 — Analyze the Packet Structure

Examining the 21 anomalous packets, you notice that the **destination MAC** changes suspiciously from one packet to another. In particular, the **first byte** of the destination MAC is different in each:

| Packet | Destination MAC        | First Byte | Character |
|--------|------------------------|:----------:|:---------:|
| 70     | `66:5d:64:16:ff:84`    | `0x66`     | `f`       |
| 71     | `6c:00:27:5c:65:26`    | `0x6c`     | `l`       |
| 256    | `61:00:27:5c:65:26`    | `0x61`     | `a`       |
| 452    | `67:5d:64:16:ff:84`    | `0x67`     | `g`       |
| 687    | `7b:5d:64:16:ff:84`    | `0x7b`     | `{`       |
| ...    | ...                    | ...        | ...       |
| 3055   | `7d:5d:64:16:ff:84`    | `0x7d`     | `}`       |

### Step 3 — Extract the Flag

To automate the extraction, see the [`net2.py`](net2.py) script in the challenge folder.

---

## Flag

```
flag{...}
```

---

## Conclusions

The flag is hidden in the first byte of the destination MAC address of each packet with EtherType `0xFFFF`. This challenge demonstrates how protocol fields can be abused to covertly transmit information, even in what appears to be normal network traffic.

2. **EtherType as a covert channel**: Using a non-standard EtherType (`0xFFFF`) allows data to be hidden in plain sight, as most tools and analysts ignore unknown or invalid protocol types.

3. **Camouflage in legitimate traffic**: The malicious packets were scattered among thousands of innocuous HTTPS connections to well-known sites, making the anomaly hard to spot without filtering by protocol.
