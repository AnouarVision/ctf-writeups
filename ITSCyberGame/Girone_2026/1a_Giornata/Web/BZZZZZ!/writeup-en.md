# BZZZZZ!

**Competition:** ITSCyberGame  
**Category:** Web  
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> I hope you really like APIs :)

This challenge is a chain of HTTP endpoints. Start at `/api/start` and follow the instructions at each step until `/api/flag`.

---

## Solution

### 1. Start the session

```bash
curl -v -L -c cookies.txt -b cookies.txt "http://sfide.itscybergame.it:<port_number>/api/start"
```

Explanation of the flags used:

- `-v`: enable verbose mode; prints debugging info including request and response headers.
- `-L`: follow HTTP redirects (3xx); useful when the server responds with `302`.
- `-c cookies.txt`: write cookies received from the server to a cookie jar (`cookies.txt`) for use in later requests.

Note: `-b cookies.txt` reads cookies from the jar and sends them with the request.

The server responds with a **302 redirect** to `/api/check` and sets two session cookies:

```
Set-Cookie: PHPSESSID=<session_id>
Set-Cookie: SID=<sid_value>
```

Following the redirect with `-L` and saving cookies with `-c cookies.txt` leads to `/api/check`, which returns:

```json
{"ok":true,"next":"/api/token","note":"Requires a specific Accept header."}
```

### 2. Custom Accept header

The next endpoint `/api/token` requires a specific `Accept` header. If you try `application/json`, the server replies `406 Not Acceptable` and indicates the correct value:

```json
{"error":"bad_accept","need":"Accept: application/vnd.energyhub+json"}
```

Try again with the correct header:

```bash
curl -v -b cookies.txt \
  -H "Accept: application/vnd.energyhub+json" \
  "http://sfide.itscybergame.it:<port_number>/api/token"
```

Response:

```json
{
  "ok": true,
  "next": "/api/submit",
  "token": "<token_value>",
  "rule": "Send POST x-www-form-urlencoded with token and message containing spaces and a +"
}
```

### 3. POST with correct encoding

The next step requires an `x-www-form-urlencoded` POST with a `message` field that contains both spaces and a literal `+`.

Important: in `x-www-form-urlencoded` a `+` is interpreted as a space. To send a literal `+` you must encode it as `%2B`. The server expects the string `hello world+plus`, so the body should be:

```
message=hello+world%2Bplus
```

where `+` denotes a space and `%2B` is a literal plus sign.

```bash
curl -v -b cookies.txt \
  -H "Accept: application/vnd.energyhub+json" \
  --data-urlencode "token=<token_value>" \
  -d "message=hello+world%2Bplus" \
  "http://sfide.itscybergame.it:<port_number>/api/submit"
```

Response:

```json
{"ok":true,"next":"/api/flag","note":"Final step: simple header."}
```

### 4. Final header and flag

The final endpoint `/api/flag` requires a custom header:

```json
{"error":"missing_header","need":"X-API-Mode: curl"}
```

```bash
curl -v -b cookies.txt \
  -H "Accept: application/vnd.energyhub+json" \
  -H "X-API-Mode: curl" \
  "http://sfide.itscybergame.it:<port_number>/api/flag"
```

Response:

```json
{"flag":"flag{...}"}
```

---

## Flag

```
flag{...}
```

---

## Conclusion

This challenge teaches practical `curl` usage for interacting with HTTP APIs: managing session cookies (`-c`/`-b`), custom headers (`-H`), performing `x-www-form-urlencoded` POSTs, and understanding that `+` represents a space while `%2B` represents a literal plus sign in URL encoding.
