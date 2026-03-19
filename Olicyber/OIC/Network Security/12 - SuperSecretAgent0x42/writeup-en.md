# Super Secret Agent 0x42
**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** intercepted.pcap

---

## Description

> I managed to intercept an outgoing conversation from the MI16 headquarters. I believe it contains key information about the last mission of the super secret agent 0x42, but everything is encrypted. Help me discover his key and catch him once and for all.

---

## Solution

### Step 1 — Analyze the PCAP

Opening `intercepted.pcap`, you see TCP traffic to port `12345`. There are two distinct sessions (stream 0 and stream 1), both to the same server.

#### With Wireshark

Open the file and apply the filter:
```
tcp.port == 12345
```

Wireshark automatically assigns a progressive index to each distinct TCP stream (`tcp.stream eq 0`, `tcp.stream eq 1`, ...). In this pcap there are two separate connections to port 12345, so two streams.

To analyze them individually, right-click on a packet → **Follow → TCP Stream**. Wireshark will automatically apply the filter:
```
tcp.stream eq 0
```
showing only the session of **agent 0x00** (the one rejected by the server).

To switch to the session of **agent 0x42**, manually change the filter to:
```
tcp.stream eq 1
```

You need to separate the two streams because they belong to different TCP connections (different source ports: `37984` and `37986`). Mixing them would make it impossible to distinguish which challenge corresponds to which response. By analyzing stream `1`, you find in sequence the server's challenge and the client's response, from which you can derive the key.

#### With tshark

```bash
tshark -r intercepted.pcap -Y "tcp.payload" -T fields \
  -e frame.number -e ip.src -e tcp.payload 2>/dev/null
```

Decoding the payloads as ASCII immediately reveals the application protocol.

---

### Step 2 — Understand the challenge-response protocol

The server implements a **challenge-response authentication system with XOR encryption**:

1. The server sends an ASCII art banner (`MI16`) and a welcome message
2. The server sends a **challenge**: 8 random bytes in plaintext
3. The client replies with the same 8 bytes **encrypted with its key**
4. If the key is correct, the server sends the secret message (encrypted)

There are **two sessions** in the pcap:

| Stream | Agent | Result |
|--------|-------|--------|
| 0 | `0x00` | Wrong key: server rejects |
| 1 | `0x42` | Authentication successful: receives message |

The server's message to agent `0x00` confirms this explicitly:
```
Warning agent 0x00, it seems your new key does not work
properly with our encryption algorithm!!
```

---

### Step 3 — Extract the key of agent 0x42

From the session of agent `0x42` you extract:

- **Challenge** (sent by the server, frame 20): `70 4e 34 bb ff 99 f3 fe`
- **Response** (sent by the client, frame 22): `6c 00 fa d8 ae 0d 60 15`

Since the encryption is XOR, the key is simply:

```
key = challenge XOR response
```

```python
challenge = bytes.fromhex("704e34bbff99f3fe")
response  = bytes.fromhex("6c00fad8ae0d6015")

key = bytes([c ^ r for c, r in zip(challenge, response)])
print(key.hex())  # 1c4ece63519493eb
```

**Key of agent 0x42:** `1c4ece63519493eb`

---

### Step 4 — Decrypt the secret message

The encrypted message is in frame 26. The last 19 bytes are plaintext (`Fine comunicazione\n`), the rest is encrypted with the key in repetition (repeating-key XOR).

```python
key = bytes.fromhex("1c4ece63519493eb")

ciphertext = bytes.fromhex(
    "502fee1138e7e3846f3aaf4334b3b38a7a28ab113cf5e782"
    "6a2fe24330f3f685682bee5329a0a1c73c27a24322e1fccb"
    "6c27af0d3eb4e08e712cbc0271e4f6997a2bba173eb8b387"
    "7d6eaf1625fbe1826634a7023cfbb38a3c3ebc0c32f1f78e"
    "6e2be0695bf2ff8a7b35a6530ef8a7b46e7ffb1361a1a4df"
    "3011a3570ee5e6df7011fd3c3da0cc8f2c23fa0d35a0ac96"
    "1644"
)

plaintext = bytes([b ^ key[i % len(key)] for i, b in enumerate(ciphertext)])
print(plaintext.decode('utf-8'))
```

**Decrypted message:**
```
The answer is yes, agent 0x42, your plan seems perfect,
you are authorized to proceed.

flag{...}
```

---

## Conclusions

1. **Vulnerable challenge-response**: When both the challenge and the response are visible on the network, and the encryption is XOR, the key can be trivially obtained by XORing the two values.

2. **Repeating-key XOR**: With a short key applied repeatedly to long messages, knowing the key allows you to decrypt all past and future traffic.

3. **Known-plaintext attack**: Having the plaintext (the challenge) and the corresponding ciphertext (the response) is enough to break XOR encryption and recover the key.

4. **Lesson**: Secure encryption must not expose both the plaintext and ciphertext of the same operation on the same unprotected channel.
