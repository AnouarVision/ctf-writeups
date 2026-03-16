# Just a Reminder...

**Competition:** OliCyber
**Category:** Web
**URL:** http://just-a-reminder.challs.olicyber.it

---

## Description

> I found a login form on an unnamed site, but I have no idea what the credentials are... Would you try logging in for me?

---

## Solution

The site shows a simple login form. Since we don't have any credentials, the first step is to inspect the page source, specifically the `default.js` file loaded by the frontend.

### Step 1 — Analyze the source code

Opening the browser DevTools (`F12` → Sources) and reading `default.js`, we find the `login_check()` function that handles authentication entirely on the client side.

Two key pieces of information stand out immediately:

**Username** — hardcoded in plaintext:
```javascript
username_field.value === 'admin'
```

**Password** — AES-encrypted, but the key is defined in the same file:
```javascript
var s3cr37 = 'ML4czctKUzigEeuR';
// ...
AES_decrypt('U2FsdGVkX1/JEKDXgPl2RqtEgj0LMdp8/Q1FQelH7whIP49sq+WvNOeNjjXwmdrl', s3cr37)
```

### Step 2 — Decrypt the password

Since the `CryptoJS` library is already loaded on the page, we can decrypt the password directly from the browser console (`F12` → Console):

```javascript
var key = 'ML4czctKUzigEeuR';
var encrypted = 'U2FsdGVkX1/JEKDXgPl2RqtEgj0LMdp8/Q1FQelH7whIP49sq+WvNOeNjjXwmdrl';
CryptoJS.AES.decrypt(encrypted, key).toString(CryptoJS.enc.Utf8);
```

The result is: `v3ry_l337_p455w0rd_!`

### Step 3 — Login

Using the recovered credentials:

- **Username:** `admin`
- **Password:** `v3ry_l337_p455w0rd_!`

We log in and the page reveals the flag.