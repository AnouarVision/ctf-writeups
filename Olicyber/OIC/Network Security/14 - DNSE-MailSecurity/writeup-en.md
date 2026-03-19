# DNS e-mail security
**Competition:** OliCyber<br>
**Category:** Network / DNS<br>
**Command:** `dig -p10502 @emailsec.challs.olicyber.it dns-email.localhost`

---

## Description

> More than 75% of companies suffer from phishing via e-mail, maybe I should make sure my recipients can verify my e-mail address.

---

## Solution

### Step 1 — Initial reconnaissance

The command provided by the challenge performs a DNS query of type **A** (default) on the domain `dns-email.localhost`:

```bash
dig -p10502 @emailsec.challs.olicyber.it dns-email.localhost
```

The server replies with:
```
dns-email.localhost.    3600    IN      A       13.37.13.37
```

The domain exists and resolves to `13.37.13.37`. The challenge is about e-mail security; the three main DNS standards are **SPF**, **DKIM**, and **DMARC**, all published as TXT records.

---

### Step 2 — Check standard e-mail records

The first approach is to check if the e-mail security records are already configured:

```bash
# SPF
dig -p10502 @emailsec.challs.olicyber.it dns-email.localhost TXT

# DKIM (default selector)
dig -p10502 @emailsec.challs.olicyber.it default._domainkey.dns-email.localhost TXT

# DMARC
dig -p10502 @emailsec.challs.olicyber.it _dmarc.dns-email.localhost TXT
```

All three return `ANSWER: 0`, the records do not exist. This confirms the challenge premise: the domain **does not have** e-mail security configured.

---

### Step 3 — Reasoning about the elements

The key point is **"this server"**: the server sends e-mails from `dns-email.localhost` which resolves to `13.37.13.37`. SPF authorizes sender IPs via TXT records, but can also do so via **inclusion mechanisms** that point to other DNS records.

In particular, SPF supports the `include:` and `redirect=` mechanisms, which can point to subdomains such as:
- `_spf.dns-email.localhost`
- `_netblocks.mail.dns-email.localhost`

These second-level SPF subdomains are often published as **CNAME records** pointing to lists of authorized IPs, a common structure among large e-mail providers (e.g., Google, SendGrid).

---

### Step 4 — Enumerate SPF subdomains with CNAME

Following the SPF hierarchy logic, the most likely subdomain to query is:

```bash
dig -p10502 @emailsec.challs.olicyber.it _netblocks.mail.dns-email.localhost CNAME
```

The record type to use is **CNAME**, not TXT, because SPF netblocks are typically published as aliases pointing to the final answer.

The response contains the flag in the CNAME value.

---

## Flag

flag{...}

---

## Conclusions

1. **SPF is not just TXT**: The SPF infrastructure can use CNAME records to delegate the list of authorized IPs to dedicated subdomains like `_netblocks.mail.<domain>`.

2. **Record type enumeration**: It's not enough to query TXT, MX, and A records. Records like CNAME, SRV, and PTR can contain hidden information, in a CTF it's essential to try all record types on all plausible subdomains.

3. **SPF hierarchy**: The standard structure of SPF subdomains follows the pattern `_spf.<domain>` → `_netblocks.mail.<domain>` → CNAME pointing to the actual netblock. Knowing this hierarchy allows you to find non-obvious records.
