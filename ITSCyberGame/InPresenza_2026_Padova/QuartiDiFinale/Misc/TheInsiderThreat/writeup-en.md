# The Insider Threat

**Competition:** ITSCyberGame <br>
**Category:** Misc <br>
**Artifact:** `datavault_incident.db`

---

## Description

On the night of 15 March 2024, DataVault Inc. (Milan) suffered a massive data exfiltration of roughly 2.3 TB of customer data. The CISO suspects an insider threat. A forensic database `datavault_incident.db` was provided containing seven days of logs (9–15 March 2024) organized into six tables:

- `employees`: registry of 50 employees
- `auth_logs`: authentication logs
- `vpn_logs`: VPN sessions
- `database_queries`: queries run against production DB
- `file_transfers`: file transfer records
- `security_alerts`: SIEM/DLP/EDR alerts

**Goal:** identify the perpetrator and reconstruct the timestamp and method of the exfiltration.
**Flag format:** `flag{first_last_YYYYMMDD_HHMM_protocol_last-octet-ip}`

---

## Solution

### 1. Initial reconnaissance

First, inspect the largest transfers in `file_transfers`:

```sql
SELECT * FROM file_transfers ORDER BY file_size_mb DESC LIMIT 10;
```

Two clearly anomalous records appear:

| id  | employee_id | timestamp           | filename                      | file_size_mb | destination_ip    | protocol | proxy_used |
|-----|-------------|---------------------|-------------------------------|--------------|-------------------|----------|------------|
| 268 | 9           | 2024-03-15 03:47:22 | customer_database_dump.sql    | 1250.5       | 45.142.212.98     | api      | 0          |
| 269 | 9           | 2024-03-15 03:52:10 | customer_files_archive.tar.gz | 980.3        | 45.142.212.98     | api      | 0          |

Suspicious traits:
- External destination IP hardcoded (`45.142.212.98`) — other transfers have `destination_ip = NULL`.
- `proxy_used = 0`: corporate proxy bypassed.
- Night hours (03:47–03:52).
- Massive sizes: 1250.5 + 980.3 ≈ 2230.8 MB (~2.3 TB).

`employee_id = 9` corresponds to Matteo Marino, Database Administrator, Engineering, Milan, `access_level = 4`.

---

### 2. Analysis of the malicious session

Auth logs for 15 March:

```sql
SELECT * FROM auth_logs WHERE employee_id=9 AND timestamp LIKE '2024-03-15%';
```

| timestamp           | action | ip_address      | user_agent    | success | session_id      | mfa_verified |
|---------------------|--------|-----------------|---------------|---------|-----------------|--------------|
| 2024-03-15 02:15:23 | login  | 87.12.234.156   | curl/7.68.0   | 1       | sess_malicious  | 0            |
| 2024-03-15 04:58:12 | logout | 87.12.234.156   | curl/7.68.0   | 1       | sess_malicious  | 0            |
| 2024-03-15 09:06:00 | login  | 192.168.10.131  | Mozilla/5.0…  | 1       | sess_676038     | 1            |

The `sess_malicious` session is conclusive:
- Source IP `87.12.234.156` (Romania): never seen previously in the 7-day window.
- User-agent `curl/7.68.0`: programmatic access, not a browser.
- MFA not verified (`mfa_verified = 0`): the only session in the period without MFA.

VPN logs show a matching connection:

```sql
SELECT * FROM vpn_logs WHERE employee_id=9 AND connect_time LIKE '2024-03-15%';
```

| connect_time        | disconnect_time     | ip_address     | location          | bytes_sent    | bytes_received | protocol |
|---------------------|---------------------|----------------|-------------------|---------------|----------------|----------|
| 2024-03-15 02:15:23 | 2024-03-15 04:58:12 | 87.12.234.156  | Bucharest, Romania| 2,456,231,936 | 15,728,640     | OpenVPN  |

`bytes_sent ≈ 2.456 GB` outbound, matching the exfiltrated volume.

---

### 3. Database queries — kill chain

Examining database activity around the window:

```sql
SELECT * FROM database_queries WHERE employee_id=9 AND timestamp LIKE '2024-03-15 0%' ORDER BY timestamp;
```

| timestamp           | query_type | table_name     | rows_affected | execution_time_ms |
|---------------------|------------|----------------|---------------|-------------------|
| 2024-03-15 02:45:30 | SELECT     | customers      | 50,000        | 1,230             |
| 2024-03-15 02:47:15 | SELECT     | customer_files | 125,000       | 4,567             |
| 2024-03-15 03:12:45 | DUMP       | customers      | 50,000        | 23,450            |
| 2024-03-15 03:47:22 | DUMP       | customer_files | 125,000       | 87,650            |

Classic pattern: reconnaissance `SELECT` followed by full `DUMP`. The `approved_by` field is `NULL` for these queries, indicating no out-of-band approval.

---

### 4. Security alerts

Relevant alerts:

| timestamp           | severity | alert_type          | source  | description                                      |
|---------------------|----------|---------------------|---------|--------------------------------------------------|
| 2024-03-15 01:44:00 | low      | failed_login        | DLP     | Generic failed_login detected                    |
| 2024-03-15 02:15:50 | medium   | anomaly             | SIEM    | Unusual login time for user matteo.marino        |
| 2024-03-15 02:16:10 | high     | policy_violation    | EDR     | MFA bypass detected during authentication        |
| 2024-03-15 03:12:55 | high     | threshold_exceeded  | DLP     | Large DB query: 50,000 rows from customers       |
| 2024-03-15 03:47:30 | critical | suspicious_activity | DLP     | Data exfiltration: 1250.5 MB to external IP     |
| 2024-03-15 03:52:15 | critical | suspicious_activity | DLP     | Data exfiltration: 980.3 MB to external IP      |

All alerts remained `resolved = 0`; SOC did not respond in real time.

---

### 5. Exploit / reconstruction

The helper script [the_insider_threat.py](/ITSCyberGame/InPresenza_2026_Padova/QuartiDiFinale/Misc/TheInsiderThreat/the_insider_threat.py) in the challenge folder contains the Python used to compute the flag from `datavault_incident.db`.

Run it as follows:

```bash
python3 the_insider_threat.py datavault_incident.db
```

The script prints the flag to stdout.

---

## Flag

```
flag{...}
```

**Decoding:**
- `matteo_marino`: Database Administrator, employee_id 9
- `20240315`: 15 March 2024
- `0352`: timestamp of the last file transfer completed (`customer_files_archive.tar.gz`, 03:52:10)
- `api`: protocol used for exfiltration
- `98`: last octet of destination IP (`45.142.212.98`)

---

## Conclusions

**Vector:** Credential compromise with MFA bypass. Matteo Marino's (DBA, access_level 4) credentials had been previously compromised. The attacker operated from Romania via `curl`, bypassing MFA, in the window 02:15–04:58.

**Initial investigative mistake:** in the first analysis I used the timestamp of the *first* DUMP (03:47) instead of the *last* completed file transfer (03:52); the flag format required the terminal event of the exfiltration chain.

1. **JIT Privilege**: a DBA should not be able to run `DUMP` on production without an `approved_by` non-NULL
2. **Alert fatigue**: 5 alerts escalated from `low` to `CRITICAL` in 2 hours with no SOC response
3. **Geo-blocking**: no control on access from Bucharest for a user based in Milan
4. **MFA enforcement**: an MFA bypass should have automatically blocked the session, not only logged an alert


