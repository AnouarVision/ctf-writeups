# Protocollo Datagramma Utente

**Competition:** OliCyber<br>
**Category:** Network<br>
**Protocol:** UDP

---

## Description

> Can you reconstruct the flag among all these packets?

---

## Solution

The challenge is about analyzing UDP traffic. By inspecting the captured packets, it is possible to reconstruct the messages exchanged between client and server.

### Step 1 — Observing the UDP Exchange

Looking at the captured traffic, there is a UDP message exchange:

**Client → Server:**
```
Hello UDP Server, please s3nd me the s3cret
```

**Server → Client:**
```
Hello UDP Client, I will send you the s3cret fl4g, be ready, and listen till the end
```

### Step 2 — Reconstructing the Full Stream

Unlike TCP, UDP is a connectionless protocol. UDP packets arrive as independent datagrams. By concatenating the UDP payloads in arrival order, the full message is obtained:

```
flag{...}
```

---

## Conclusions

1. **UDP vs TCP**: TCP maintains a persistent connection; UDP sends independent datagrams
2. **Stream Reassembly**: UDP datagrams must be reassembled in timestamp order
3. **Stateless Analysis**: UDP provides no ordering guarantees, unlike TCP
