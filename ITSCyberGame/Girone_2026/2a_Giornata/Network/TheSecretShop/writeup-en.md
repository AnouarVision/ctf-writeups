# The Secret Shop

**Competition:** ITSCyberGame
**Category:** Network
**Files:** data_dev.pcap
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> This online shop looks familiar... Find the login credentials inside the provided `.pcap` and locate the flag on a development endpoint. That pcap might be useful for other things as well.

A `.pcap` file is provided to inspect for credentials and a hidden flag endpoint.

---

## Solution

### 1. Inspect HTTP traffic

Open the pcap in Wireshark and filter for HTTP traffic:

```
http
```

Notable requests include many `GET /assets/img0.png` ... `GET /assets/img79.png`, a `POST /index.php` (login), `GET /games?id=X` and a `POST /shop_action.php`.

### 2. Extract credentials — TCP reassembly trap

Filter for the login POST:

```
http.request.method == "POST" && http.request.uri == "/index.php"
```

Follow the TCP stream (right-click → Follow → TCP Stream) to view the login payload. At first glance the password looks like `Hdk8@`, but the `Content-Length: 29` header indicates the body spans more bytes.

The password is split across two TCP segments. In the reassembled stream the first segment ends with `...username=admin&pas` and the second starts with `sword=Hdk8@md1`. The byte after `@` is still part of the password. The full password is **`Hdk8@md1`**.

In Wireshark expand the "Reassembled TCP" section to see `password=Hdk8@md1` clearly.

### 3. Hidden endpoint in `shop_action.php` POST

Inspect the POST to `/shop_action.php` (follow its TCP stream). The POST body contains a comment revealing a dev-only access:

```
# DEV NOTE: remove direct flag access in dev version
action=download&idx=42
```

This indicates a development endpoint that returns the flag when `action=download&idx=42` is posted.

### 4. Login and retrieve flag

Use the extracted credentials to login and call the dev endpoint:

```bash
curl -s -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/index.php" \
  -d "username=admin&password=Hdk8@md1"

curl -s -b cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/shop_action.php" \
  -d "action=download&idx=42"
```

Example response:

```json
{"success":true,"points":200,"message":"<b>FLAG: flag{...}</b>"}
```

---

## Flag

```
flag{...}
```

---

## Conclusions

This challenge uses two pitfalls:

- A password split across TCP segments, only proper TCP reassembly reveals the full credential (`Hdk8@md1`).
- An exposed development endpoint, a `DEV NOTE` in the POST body hinted that `action=download&idx=42` returns the flag and should not be present in production.

Never trust developer artifacts in production captures.
