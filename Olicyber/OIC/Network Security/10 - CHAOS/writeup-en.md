# CHAOS
**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** CHAOS.pcap

---

## Description

> HELLO MORTAL, THIS IS A MESSAGE FROM THE WORLD OF C-H-A-O-S (YES, WE HAVE COMPUTERS HERE TOO). CAN YOU DECRYPT IT?

---

## Solution

### Step 1 — Analyze the PCAP and recognize the chaotic structure

Opening `CHAOS.pcap`, you immediately notice something strange: packets have **negative timestamps**, are out of order, and the traffic is full of TCP anomalies:

- `[TCP Retransmission]`: retransmitted packets
- `[TCP Spurious Retransmission]`: spurious retransmissions
- `[TCP Previous segment not captured]`: missing segments

All communication happens on `127.0.0.1:42014 → 127.0.0.1:12345`. The challenge name, **CHAOS**, is not random: the traffic is intentionally chaotic.

---

### Step 2 — Filter data packets

The relevant packets are those with exactly **1 byte** of payload (`tcp.len == 1`): each packet carries a single ASCII character of the flag.

#### With Wireshark

Enter in the filter bar:

```
tcp.len == 1
```

You will see PSH, ACK packets with a single byte of payload, mixed with spurious retransmissions.

##### Where to find the byte (hex) in Wireshark

To see the **raw byte** carried by each packet:

1. Select a filtered packet (with `tcp.len == 1`).
2. In the central Wireshark panel (**Packet Details**), expand:
   - **Transmission Control Protocol**
   - then **TCP payload (1 byte)**
   - under this entry you will see the **raw byte** in hexadecimal (hex), which corresponds to the ASCII character carried.

This allows you to visually check, for each packet, which byte is transmitted.

#### With tshark

```bash
tshark -r CHAOS.pcap -Y "tcp.len==1" -T fields \
  -e frame.time_relative -e tcp.seq -e tcp.payload
```

Output:

```
 0.000000   1    48
-14.015736  4294967283  6c
 2.001499   3    30
-8.008697   8    30
...
-15.018163  1    66
```

You will notice that some sequence numbers appear **twice** with different bytes, one is the original transmission and the other is a retransmission. The TCP sequence number alone is not enough to reconstruct the message.

---

### Step 3 — Sort by timestamp

The key is to sort the data packets by **increasing timestamp** (real chronological order), ignoring the TCP sequence number.

#### With Wireshark

1. Apply the filter `tcp.len == 1`
2. Click on the **Time** column to sort packets by increasing timestamp
3. Read the **Info** column → the payload bytes appear in the correct order

> Warning! Make sure Wireshark shows timestamps relative to the first packet: **View → Time Display Format → Seconds Since Beginning of Capture**

#### With tshark

Use `frame.time_epoch` for absolute timestamps and sort with `sort`:

```bash
tshark -r CHAOS.pcap -Y "tcp.len==1" -T fields \
  -e frame.time_epoch -e tcp.seq -e tcp.payload \
  | sort -n
```

Or, all in one line with Python to directly decode the bytes as ASCII:

```bash
tshark -r CHAOS.pcap -Y "tcp.len==1" -T fields \
  -e frame.time_epoch -e tcp.payload \
  | sort -n \
  | awk '{print $2}' \
  | xxd -r -p
```

---

### Step 4 — Reconstruct the message

Sorting the bytes by increasing timestamp gives the following sequence:

| Timestamp | TCP Seq | Byte (hex) | Character |
|-----------|---------|------------|-----------|
| -15.018 | 1 | `0x66` | `f` |
| -14.016 | wrap | `0x6c` | `l` |
| -13.015 | 3 | `0x61` | `a` |
| -12.014 | 4 | `0x67` | `g` |
| -11.011 | 5 | `0x7b` | `{` |
| -10.010 | 6 | `0x54` | `T` |
| -9.009 | 7 | `0x30` | `0` |
| -8.009 | 8 | `0x30` | `0` |
| -7.008 | 9 | `0x5f` | `_` |
| -6.006 | 10 | `0x4d` | `M` |
| -5.005 | 11 | `0x55` | `U` |
| -4.003 | 12 | `0x43` | `C` |
| -3.002 | 13 | `0x48` | `H` |
| -2.002 | 14 | `0x5f` | `_` |
| -1.001 | 15 | `0x43` | `C` |
| 0.000 | 1 | `0x48` | `H` |
| +1.001 | 17 | `0x34` | `4` |
| +2.001 | 3 | `0x30` | `0` |
| +3.008 | 19 | `0x35` | `5` |
| +4.009 | 20 | `0x7d` | `}` |

---

## Flag

```
flag{...}
```

---

## Conclusions

1. **The chaos is intentional**: Negative timestamps and TCP anomalies (retransmission, spurious retransmission) were deliberately inserted to hide the correct order of the data.

2. **TCP sequence ≠ real order**: Sorting by sequence number is misleading, sequence numbers were manipulated. The timestamp reveals the correct chronological order.

3. **Steganography in the traffic**: Each packet with `tcp.len == 1` carries a single character. Spurious retransmissions with different bytes are an additional source of confusion.

4. **Solving approach**: Filter data packets, sort by timestamp, concatenate the bytes and the message emerges from the CHAOS.
