# Useless

**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** capture.pcapng

---

## Description

> I stole this file from a very important server, but I can't find anything useful in these packets — their security is impenetrable.

---

## Solution

The challenge name is already a hint: **Useless**. When the obvious content yields nothing, think laterally and check more abstract layers of the data.

### Step 1 — Initial PCAP Analysis

Opening the file in Wireshark and inspecting the traffic, it appears to contain nothing of interest:
- Standard network packets
- No suspicious HTTP/HTTPS traffic
- No interesting payload at first glance

```
File: capture.pcapng
Size: 2714 KB
Format: Wireshark/pcapng
Encapsulation: Ethernet
Number of Packets: 3438
Duration: 31.314 seconds
```

### Step 2 — Checking the File Metadata

Since the packet content seems "useless", the real information might be hidden in the file's own metadata. We use the `capinfos` tool (part of Wireshark):

```bash
$ capinfos capture.pcapng
```

### Step 3 — Discovering the Flag in the Comments

The `capinfos` output reveals the crucial field:

```
Capture comment: flag{...}
```

---

## Conclusions

1. **Metadata Matters**: Don't only look inside packet data; file comments can contain critical information.
2. **Alternative Tools**: `capinfos` allows quick analysis without a graphical interface.
3. **Think Outside the Box**: A challenge named "Useless" hints at rethinking the approach.
4. **Check All Layers**: If the obvious content yields nothing, inspect headers, comments, and metadata.
