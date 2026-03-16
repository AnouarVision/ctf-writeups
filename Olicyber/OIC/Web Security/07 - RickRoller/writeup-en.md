# Rick Roller

**Competition:** OliCyber<br>
**Category:** Web / HTTP Response Interception<br>
**URL:** http://roller.challs.olicyber.it

---

## Description

> Someone sent me this link but I keep getting redirected to a strange video. Can you tell me why?

A simple page with a button that promises to win a flag, but always redirects to a Rick Astley video. The flag exists but the browser doesn't show it.

---

## Solution

### Step 1 — HTTP Behavior Analysis

When visiting the site, you access a page with a **"WIN!"** button that points to `get_flag.php`. Clicking it, the browser immediately redirects to:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

A classic **Rick Roll**. The flag is never visible (at least not with the browser).

The PHP server essentially executes this:

```php
echo "flag{...}";
header("Location: https://www.youtube.com/watch?v=dQw4w9WgXcQ");
```

---

### Step 2 — Vulnerability Identification

The flag output is sent **before** the `Location` header, but the browser:

1. Receives the `302 Found` HTTP response
2. Reads the `Location` header
3. **Redirects immediately**, ignoring the response body

As a result, the flag is present in the HTTP response body, but the browser never shows it to the user.

The server returns sensitive data (the flag) in the **body of a redirect response (302)**. This is a logical error: the browser follows the redirect without showing the body, but tools that operate at the raw HTTP protocol level, like `curl`, read the entire response, headers **and** body.

---

### Step 3 — Exploit via curl

Simply use `curl` with the `-i` flag to see both headers and response body, without automatically following redirects:

```bash
curl -i http://roller.challs.olicyber.it/get_flag.php
```

**Output:**

```
HTTP/1.1 302 Found
Content-Length: 30
Content-Type: text/html; charset=UTF-8
Date: Wed, 11 Mar 2026 21:10:47 GMT
Location: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Server: Apache/2.4.56 (Debian)
X-Powered-By: PHP/8.0.30

flag{...}
```

The flag appears in the body of the `302` response, ignored by the browser but perfectly readable with `curl`.

---

## Conclusions

Never include sensitive data in the body of a redirect response. A browser follows the `Location` and discards the body, but this **doesn't mean the data is hidden**: anyone using `curl`, Burp Suite, or any other HTTP client can read the complete response.

Best practices to follow:

1. **Never send sensitive data before a redirect**: the body of a `3xx` response should be empty or contain only a generic HTML message
2. **Execute the redirect before any output**: in PHP, call `header()` before any `echo`
3. **Separate authentication logic from content delivery**: the flag should be returned only after verifying all conditions, not in the middle of a redirect flow