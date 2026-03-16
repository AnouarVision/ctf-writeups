# Headache

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://headache.challs.olicyber.it

---

## Description

> When we load a web page we are communicating with a server, but what does it respond with?

---

## Solution

The HTML page says *"The flag is here... but not right here"*, hinting that the flag is not in the page body.

The challenge description asks what the server responds with: beyond the HTML content, every HTTP response includes **headers** — metadata sent by the server before the page body. That's where the flag is hidden.

### Step 1 — Inspect the HTTP headers

To view only the response headers, use `curl` with the `-I` flag:

```bash
curl -I http://headache.challs.olicyber.it
```

### Step 2 — Read the response

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Date: Sun, 15 Mar 2026 23:27:41 GMT
Flag: flag{...}
Server: Apache/2.4.56 (Debian)
X-Powered-By: PHP/8.0.30
```

Among the response headers there is a non-standard field: `Flag`, which contains the flag directly.