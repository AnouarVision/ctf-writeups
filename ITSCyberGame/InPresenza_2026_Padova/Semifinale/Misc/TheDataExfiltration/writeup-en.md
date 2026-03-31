# The Data Exfiltration
**Competition:** ITSCyberGame
**Category:** Misc
**Service:** cloudbank_exfiltration.db (SQLite)

---

## Description
> "On March 20, 2024 the CloudBank security team detected an anomalous API traffic spike and AWS costs: over 20 GB of customer data were exported to suspicious destinations within 48 hours. Preliminary analysis indicates a compromised API key was used for large-scale exfiltration. The CISO suspects the key was accidentally committed to a Git repository and then exploited by an insider. Flag format: flag{firstname_lastname_apikey_first12chars_total_gb}"

---

## Solution

### 1. Initial reconnaissance
The SQLite database contains 8 tables:

| Table | Rows | Content |
| `employees` | 100 | CloudBank employees |
| `git_commits` | 377 | Commits annotated with `contains_secret` |
| `authorized_api_keys` | 9 | API keys with hashes |
| `api_access_logs` | 2113 | API access logs |
| `s3_operations` | 1404 | S3 operations |
| `billing_records` | 105 | AWS billing records |
| `slack_messages` | 403 | Internal messages |
| `threat_intel` | 4 | Known IOCs |

**IOCs from `threat_intel`:**
```
45.142.215.89   → known data exfiltration destination (HIGH)
185.220.101.42  → Tor exit node (MEDIUM)
exfil-data-store-2024 → unauthorized S3 bucket (CRITICAL)
customers/export/all  → suspicious bulk export endpoint (HIGH)
```

### 2. Identify the malicious commit

SQL used to find commits with embedded secrets and their authors:
```sql
SELECT gc.timestamp, gc.secret_value, gc.repository,
	   e.first_name, e.last_name, e.email, e.department
FROM git_commits gc JOIN employees e ON gc.employee_id = e.id
WHERE gc.contains_secret = 1
ORDER BY gc.timestamp;
```

Four commits with secrets were found; the relevant one is:

| Date | Author | Repo | Key (truncated) |
|------|--------|------|-----------------|
| **2024-03-18 16:47** | **Marco Santoro** | **backend-api** | **`sk_live_a8f2d9...`** |
This key remained active (not revoked) and had scopes `read:customers,read:orders,write:logs`.

### 3. Correlate API logs with IOCs
Query to aggregate calls and transferred bytes from suspicious IPs for the compromised key hash:

```sql
SELECT COUNT(*), SUM(bytes_transferred),
	   MIN(timestamp), MAX(timestamp)
FROM api_access_logs
WHERE api_key_hash = 'c3f87a7b8b74c38a17fe62c1e3ce92471eea2dc0de73a8b410a242bd7c3c81c8'
	AND source_ip IN ('45.142.215.89','185.220.101.42');
```

Result:
- Calls: **183**
- Total bytes: **24,238,636,678** (~22.57 GB)
- Endpoint: `/api/v1/customers/export/all`
- Window: `2024-03-18 19:58` → `2024-03-20 19:49`

S3 confirms 183 PutObject operations to `exfil-data-store-2024` ≈ 22.16 GB. Billing shows API-Gateway cost spikes on 18/03 and 20/03.

### 4. Timeline

```
2024-03-18 16:47  Marco Santoro commits sk_live_a8f2... to repo backend-api
				 commit: d8c509b1f2a451b1ae2336436006277fd27998c2
				 msg: "Update API configuration"

2024-03-18 19:58  First request from 45.142.215.89 (IOC) using the compromised key
				 → GET /api/v1/customers/export/all → 148 MB
	↕ 48h of mass exfiltration

2024-03-20 19:49  Last request from 45.142.215.89
				 183 total requests, 22.57 GB transferred
### 5. Extract the flag

Example Python extraction:

```python
import sqlite3
conn = sqlite3.connect("cloudbank_exfiltration.db")
cur = conn.cursor()

cur.execute("""
		SELECT e.first_name, e.last_name, gc.secret_value
		FROM git_commits gc JOIN employees e ON gc.employee_id = e.id
		WHERE gc.contains_secret = 1
			AND gc.secret_value LIKE 'sk_live_a8f2%'
""")
row = cur.fetchone()

nome, cognome, api_key = row[0].lower(), row[1].lower(), row[2]
first12 = api_key[:12]   # "sk_live_a8f2"

cur.execute("""
		SELECT SUM(bytes_transferred) FROM api_access_logs
		WHERE api_key_hash = 'c3f87a7b8b74c38a17fe62c1e3ce92471eea2dc0de73a8b410a242bd7c3c81c8'
			AND source_ip IN ('45.142.215.89','185.220.101.42')
""")
total_gb = round(cur.fetchone()[0] / 1024**3)  # 23

print(f"flag{{{nome}_{cognome}_{first12}_{total_gb}}}")
```

---

## Flag

```
flag{...}
```

---

## Conclusions & Recommendations

The investigation demonstrates how a single accidental commit of a live API key can lead to large-scale data leakage and substantial financial impact if not detected quickly. Recommended mitigations:

- **Preventive controls:** enforce pre-commit and CI scans for secrets, and store credentials in a secrets manager instead of repositories.
- **Containment:** immediately revoke and rotate exposed keys; implement short-lived credentials where possible.
- **Least-privilege:** restrict API key scopes to minimum required permissions.
- **Detection:** centralize logs and create alerts for anomalous patterns (large bulk exports, sudden spikes, known IOC IPs).
- **Post-incident:** preserve timelines and evidence for forensic analysis and legal needs, run a post-mortem to update policies, and train teams on secure secret handling.

These controls reduce both the probability and impact of accidental key exposure and speed up incident response.

