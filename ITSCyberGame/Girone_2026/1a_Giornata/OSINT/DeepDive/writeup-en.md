# Deep Dive

**Competition:** ITSCyberGame
**Category:** OSINT
**File:** deep_dive_1.db

---

## Description

> The SOC at CyberSolutions S.r.l. detected an anomaly in access logs for restricted files. It appears an insider accessed critical documents shortly before several accounts were locked for suspicious activity. We acquired a dump of the internal management database. Initial info indicates the stolen file is `sistemi_business.pdf`.

The provided artifact is a SQLite database `deep_dive_1.db`.

---

## Solution

### 1. Database structure analysis

Opening the database reveals four tables:

| Table | Rows | Content |
|---|---:|---|
| `employees` | 100 | Employees: username, status, assigned key |
| `system_keys` | 1000 | System keys with ID and value |
| `file_access_logs` | 1501 | File access logs |
| `session_data` | 2001 | User sessions with tokens |

### 2. Identify the insider

Search for records involving `sistemi_business.pdf`:

```sql
SELECT * FROM file_access_logs WHERE file_name = 'sistemi_business.pdf';
```

Result:

```
access_id: 160 | emp_id: 4864 | file_name: sistemi_business.pdf
```

Only one access, by `emp_id = 4864`. Cross-referencing with `employees`:

```sql
SELECT * FROM employees WHERE emp_id = 4864;
```

```
emp_id: 4864 | username: g.benassuti | status: LOCKED | assigned_key: KEY_1542_SIG
```

The account is **LOCKED**, matching the post-incident description. Other files accessed by this user include `passwords.old`, `config.bak`, and `notes.txt`.

### 3. First half of the flag — hex key

Retrieve the key value assigned to `g.benassuti`:

```sql
SELECT key_value FROM system_keys WHERE key_id = 'KEY_1542_SIG';
```

```
666c61677b64347461626173335f
```

The value is hexadecimal. Decoding it yields the beginning of the flag:

```python
bytes.fromhex('666c61677b64347461626173335f').decode()
# → flag{...
```

**First half of the flag found.**

### 4. Second half of the flag — base64 token

Inspect sessions for `g.benassuti`:

```sql
SELECT session_id, token FROM session_data WHERE emp_id = 4864;
```

Tokens appear Base64-encoded. Decoding session `650` returns readable text:

```python
import base64
base64.b64decode('aXNfbm90X2FfY3IxbWV9').decode()
# → ...}
```

**Second half of the flag found.**

---

## Flag

```
flag{...}
```

---

## Conclusion

The flag was split across two fields in the database using two simple encodings:

- **First part** in `system_keys.key_value`, encoded as **hexadecimal**
- **Second part** in `session_data.token`, encoded as **Base64**

This challenge highlights the importance of forensic analysis on databases: harmless-looking fields can contain encoded secrets.
