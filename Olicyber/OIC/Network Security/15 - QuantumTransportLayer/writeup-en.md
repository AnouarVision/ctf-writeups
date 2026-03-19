# Quantum Transport Layer
**Competition:** OliCyber<br>
**Category:** Network / TLS<br>
**Command:** `gnutls-cli qtl.challs.olicyber.it:10503`

---

## Description

> Our sysadmin really cares about the company's security. Now he decided that we all have to use this new TLS Quantum protocol. Honestly, I have no idea how to use it, do you know anything about it?

---

## Background — How TLS works

**TLS** (Transport Layer Security) is the protocol that encrypts communications on the internet (HTTPS, etc.). During the initial handshake, client and server exchange some information before any real communication starts:

**X.509 Certificate**: the server identifies itself with a digital certificate that contains, among other things, the **Subject Alternative Names (SAN)**: the list of hostnames for which the certificate is valid.

**SNI (Server Name Indication)**: the client declares in the handshake which hostname it wants to connect to. This allows a single server to host multiple sites/services with different certificates on the same port.

**ALPN (Application-Layer Protocol Negotiation)**: the client declares in the handshake which application protocol it wants to use (e.g. `http/1.1`, `h2` for HTTP/2, `dot` for DNS-over-TLS). The server chooses among those it supports.

---

## Solution

### Step 1 — Initial connection

The command provided by the challenge attempts a standard TLS connection:

```bash
gnutls-cli qtl.challs.olicyber.it:10503
```

The client fails because the certificate is self-signed, expired, and the CN does not match the hostname. The server closes the connection showing only: `There is nothing here!`

---

### Step 2 — Ignore certificate verification and read the certificate

Reconnect ignoring certificate errors:

```bash
gnutls-cli --insecure qtl.challs.olicyber.it:10503
```

The server still replies with `There is nothing here!`, but now we have access to the full certificate. You can examine it with openssl to see its details:

```bash
openssl s_client -connect qtl.challs.olicyber.it:10503 -showcerts 2>/dev/null
```

In the certificate details, in the **X509v3 Subject Alternative Name** section, you find two hostnames:

```
DNS:quantum-transport-layer.test
DNS:fl4gg.quantum-transport-layer.test
```

The second SAN, `fl4gg`, is clearly a hint left on purpose in the challenge.

---

### Step 3 — Connect with the correct SNI

The server probably behaves differently depending on the hostname the client declares in the handshake via **SNI**. Use the `--sni-hostname` flag:

```bash
gnutls-cli --insecure \
  --sni-hostname=fl4gg.quantum-transport-layer.test \
  qtl.challs.olicyber.it:10503
```

This time the server replies with a different message:

```
Supported Protocols: default, flag
```

The server exposes two ALPN protocols: `default` (used so far) and `flag`.

---

### Step 4 — Select the correct ALPN protocol

Add the `--alpn=flag` flag to negotiate the `flag` protocol during the TLS handshake:

```bash
gnutls-cli --insecure \
  --sni-hostname=fl4gg.quantum-transport-layer.test \
  --alpn=flag \
  qtl.challs.olicyber.it:10503
```

The handshake shows:
```
- Application protocol: flag
- Handshake was completed
```

And the server returns the flag.

---

## Flag

```
flag{...}
```

---

## Conclusions

1. **X.509 certificates contain metadata**: Subject Alternative Names are not just for domain validation: in a CTF they can contain hidden hints. Always examine the full certificate.

2. **SNI changes server behavior**: a single TLS server can respond completely differently depending on the hostname declared by the client in the handshake. Without the correct SNI, the server reveals nothing.

3. **ALPN is an information vector**: the server uses ALPN to expose supported protocols. Selecting the wrong protocol (or not selecting one) gets you the default response. The `flag` protocol was only available to those who knew to look for it.
