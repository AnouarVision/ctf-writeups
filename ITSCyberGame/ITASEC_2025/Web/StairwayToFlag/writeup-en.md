# Stairway to Flag

**Competition:** ITSCyberGame
**Category:** Web
**File:** login_stairway_to_flag.html

---

## Description

> Only true rockers can access the backstage. Find the flag hidden in the login code and prove you have the right spirit to enter!

---

## Solution

The challenge provides the source code of a login page. In these cases, the first step is always to read the client-side JavaScript: all authentication logic runs in the browser and is fully exposed.

### Step 1 — Credentials check

The HTML contains the `checkLogin()` function:

```javascript
if (username === 'admin' && password === 'flag{r0ck_4nd_r0l1_...}') {
    message.innerHTML = 'Access Granted! Welcome to the backstage!<br>' + decryptString('iru3yhu');
```

The password is hardcoded in cleartext. This reveals the **first part of the flag**:

```
flag{r0ck_4nd_r0l1_...}
```

The `...` indicates the flag is incomplete; the remainder is produced dynamically by `decryptString('iru3yhu')`.

### Step 2 — Analysis of `decryptString`

The `decryptString` function runs client-side and is used by the page to build the final part of the flag during the login flow. We do not publish the decrypted suffix here: the page reveals that suffix automatically after a successful login, and we omit that part to avoid exposing it directly in the writeup.

### Step 3 — Reconstructing the flag

The first fragment of the flag is visible in the source (the hardcoded password). The second fragment is obtained dynamically by the page after login; we do not show it here. Combining the visible fragment with the suffix revealed by the site yields the complete flag.

---

## Flag

```
flag{r0ck_4nd_r0l1_...}
```
