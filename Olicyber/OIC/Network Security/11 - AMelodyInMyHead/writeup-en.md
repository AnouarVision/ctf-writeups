# A Melody in My Head
**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** a_melody_in_my_head.pcapng<br>
**Server:** `nc melody.challs.olicyber.it 10020`

---

## Description

> We are testing the implementation of a brand new super-secure authentication protocol for our brand new messaging app. What do you think? Can you find any hidden vulnerability that escaped our sophisticated checks?

---

## Background — What is a Nonce and Why is it Important

A **nonce** (Number used ONCE) is a random number used in authentication protocols to prevent **replay attacks**.

The principle is simple: every time a client wants to authenticate, the server sends a different random number. The client replies with `hash(password + nonce)`. This way, the response changes every session, and even if an attacker intercepts the communication, they cannot reuse it because the server will send a different nonce next time.

**The problem**: if the nonce is too small, the space of possible values is limited. Sooner or later, the server will send a nonce that has already been seen, and the attacker can reuse the intercepted response. This is called a **replay attack**.

---

## Solution

### Step 1 — Analyze the PCAP

Opening `a_melody_in_my_head.pcapng` and following the TCP streams, you can reconstruct the protocol:

```
Server → Client:  SERVER HELLO
Server → Client:  NONCE <number>
Client → Server:  <hash_hex_64_char>
Server → Client:  LOGIN SUCC / LOGIN FAIL
Server → Client:  FLAG <flag>   (only if LOGIN SUCC)
```

The client replies with a 64-character hexadecimal string, i.e., a **SHA256** of something that includes the password and the nonce.

#### With Wireshark

1. Open `a_melody_in_my_head.pcapng`
2. Right-click on a packet → **Follow → TCP Stream**
3. Wireshark shows the full conversation: **blue** text is the server, **red** is the client
4. Change session with the **Stream** dropdown menu at the bottom (from `tcp.stream eq 0` to `eq 1`, `eq 2`, etc.) to see all connections
5. At the bottom in the **Show data as** menu, select **ASCII** to read the messages in cleartext

Repeating this for each stream, you clearly see `SERVER HELLO`, `NONCE`, the hash responses, and the results `LOGIN SUCC` / `LOGIN FAIL`. To copy the exact hash values, change **Show data as** to **Hex Dump**.

#### With tshark

```bash
tshark -r a_melody_in_my_head.pcapng -Y "tcp.payload" -T fields \
  -e frame.number -e ip.src -e tcp.payload 2>/dev/null
```

There are 5 sessions in the pcap:

| Nonce | Hash sent | Result |
|-------|-----------|--------|
| 40 | `253b2b73...` | LOGIN FAIL |
| 33 | `cd01ef2a...` | LOGIN FAIL |
| 23 | `2a3a1630...` | **LOGIN SUCC** |
| 68 | `23c90a60...` | **LOGIN SUCC** |
|  2 | `0cce6bab...` | **LOGIN SUCC** |

The first two attempts fail (the user does not know the password), the last three succeed.

---

### Step 2 — Identify the Vulnerability

The nonce is a small decimal number. From the observed values (2, 23, 33, 40, 68), you can deduce that the nonce is a **1-byte integer: from 0 to 255**, only 256 possible values in total.

This is the problem: an attacker who has intercepted the traffic already has valid responses for nonces 2, 23, and 68. Since the server chooses the nonce randomly among only 256 values, the probability of receiving a previously seen nonce is **3/256 ≈ 1.2%** for each connection.

You don't need to know the password. You don't need to break SHA256. You just need to **wait** for the server to send a previously seen nonce and reply with the intercepted hash.

---

### Step 3 — Replay Attack

The valid responses extracted from the pcap:

```
NONCE  2  ->  0cce6bab87baa7031b69539ac1a211f202fc35cc8f3ac27fdb7e527527310f0e
NONCE 23  ->  2a3a1630446304ab588ef90f32b8d3db88933f9737016e60df5cb3a2dca19b74
NONCE 68  ->  23c90a60a0d2d24b53eca03ac2c4f4194c617f001fa1bf99b20cede152cc240f
```

For a ready-to-use script that automates the replay attack, see the `melody.py` file in the challenge folder.

---

### Step 4 — Result

Running the melody.py script, the server replies with LOGIN SUCC and the flag as soon as one of the previously seen nonces is sent:

```
Replay attack started. Looking for nonce 2, 23 or 68...
[  1] NONCE=  23 -> MATCH! Response sent
       Server: LOGIN SUCC\nFLAG flag{...}

[!] FLAG FOUND!
```

---

## Flag

```
flag{...}
```

---

## Conclusions

1. **The nonce must be unpredictable and large**: a 1-byte nonce (256 values) is too small. With just 3 intercepted responses, you already have a significant chance of success on each attempt. A secure nonce should be at least 128 bits (16 bytes) and cryptographically generated.

2. **The replay attack does not require breaking cryptography**: SHA256 is mathematically secure, but you don't need to break SHA256. You just need to reuse a previously valid response intercepted earlier.

3. **Nonce space size is critical**: with 256 possible values, after ~180 connections you are almost certain to have seen all possible nonces. With a 128-bit nonce, this would be computationally impossible.

4. **Moral**: a secure authentication protocol depends on all its components. Even if the hash is robust, a weak nonce compromises the entire system's security.
