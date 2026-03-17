# Sniff 'n' Byte

**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** sniff_n_byte.pcapng

---

## Description

> Oh no! It looks like someone has infected our server with spyware and is exfiltrating sensitive data! Sniff around and find out what information the malware is sending to the attackers!

---

## Solution

The challenge provides a PCAP file containing network traffic. The description mentions data exfiltration via spyware, so we need to look for suspicious traffic.

### Step 1 — Analyzing the PCAP File

Extracting the file metadata with `capinfos`:

```
File: sniff_n_byte.pcapng
Number of Packets: 69
Duration: 32.529 seconds
Capture Filter: tcp dst port 10622 or src port 10622
```

The capture filter reveals that the suspicious traffic flows through **TCP port 10622**.

### Step 2 — Identifying the TCP Stream

The capture header also hides an easter egg in the comments:

```
Capture comment: Congrats! You found an EASTER EGG ^-^ Now you are a REAL 1337 H4XX0R, but go back to the challenge!
```

This confirms we're on the right track, but the real flag is inside the TCP stream itself.

### Step 3 — Decoding the TCP Payload

Inspecting the TCP packet payloads, the exfiltrated stream is:

```
0x660x6c0x610x670x7b0x370x680x330x590x5f0x350x410x790x5f0x790x300x750x5f0x630x340x4e0x5f0x350x4e0x310x660x660x5f0x5e0x2d0x5e0x7d
```

This is hex-encoded with a `0x` prefix per byte. Stripping the separators and converting:

```
Hex: 666c61677b376833595f3541795f7930755f63344e5f354e3166665f5e2d5e7d
```

Converting from hex to ASCII yields:

```
flag{...}
```

---

## Conclusions

1. **Capture Filters**: TCPdump filters applied at capture time reveal which ports/protocols are suspicious.
2. **Payload Analysis**: The real value isn't always in the metadata, it's in the actual transmitted data.
3. **Encoding Detection**: Recognising the encoding format (hex-encoded string in this case) is key.
4. **Network Forensics**: When malware communicates, it often uses common protocols (TCP) on non-standard ports.
