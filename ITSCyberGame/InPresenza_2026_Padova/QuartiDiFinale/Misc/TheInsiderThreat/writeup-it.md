# The Insider Threat

**Competizione:** ITSCyberGame
**Categoria:** Misc
**Servizio:** `datavault_incident.db`

---

## Descrizione

Nella notte del 15 marzo 2024, DataVault Inc. (Milano) ha subito un'esfiltrazione massiva di circa 2.3 TB di dati clienti. Il CISO sospetta un insider threat. Viene fornito il database forense `datavault_incident.db` contenente 7 giorni di log (9–15 marzo 2024) strutturati in 6 tabelle:

- `employees`: anagrafica 50 dipendenti
- `auth_logs`: log di autenticazione
- `vpn_logs`: sessioni VPN
- `database_queries`: query eseguite sul DB di produzione
- `file_transfers`: trasferimenti file
- `security_alerts`: alert SIEM/DLP/EDR

**Obiettivo:** identificare il colpevole e ricostruire il timestamp e le modalità dell'esfiltrazione.
**Flag format:** `flag{nome_cognome_YYYYMMDD_HHMM_protocollo_ultimo-ottetto-ip}`

---

## Soluzione

### 1. Ricognizione iniziale

Prima query esplorativa sulla tabella `file_transfers` ordinata per dimensione decrescente:

```sql
SELECT * FROM file_transfers ORDER BY file_size_mb DESC LIMIT 10;
```

Emergono immediatamente due record anomali:

| id  | employee_id | timestamp           | filename                      | file_size_mb | destination_ip  | protocol | proxy_used |
|-----|-------------|---------------------|-------------------------------|--------------|-----------------|----------|------------|
| 268 | 9           | 2024-03-15 03:47:22 | customer_database_dump.sql    | 1250.5       | 45.142.212.98   | api      | 0          |
| 269 | 9           | 2024-03-15 03:52:10 | customer_files_archive.tar.gz | 980.3        | 45.142.212.98   | api      | 0          |

Caratteristiche sospette:
- **IP esterno** hardcoded (`45.142.212.98`): tutti gli altri trasferimenti hanno `destination_ip = NULL`
- **`proxy_used = 0`**: bypass del proxy aziendale
- **Orario notturno** (03:47–03:52)
- **Dimensioni massive**: 1250.5 + 980.3 = **2230.8 MB ≈ 2.3 TB** combinate

`employee_id = 9` → **Matteo Marino**, Database Administrator, Engineering, Milano, `access_level = 4`.

---

### 2. Analisi della sessione malevola

#### Auth Logs — 15 marzo

```sql
SELECT * FROM auth_logs WHERE employee_id=9 AND timestamp LIKE '2024-03-15%';
```

| timestamp           | action | ip_address      | user_agent    | success | session_id      | mfa_verified |
|---------------------|--------|-----------------|---------------|---------|-----------------|--------------|
| 2024-03-15 02:15:23 | login  | 87.12.234.156   | curl/7.68.0   | 1       | sess_malicious  | **0**        |
| 2024-03-15 04:58:12 | logout | 87.12.234.156   | curl/7.68.0   | 1       | sess_malicious  | **0**        |
| 2024-03-15 09:06:00 | login  | 192.168.10.131  | Mozilla/5.0…  | 1       | sess_676038     | 1            |

La sessione `sess_malicious` è inequivocabile:
- IP sorgente **87.12.234.156** (Romania): mai visto nei giorni precedenti
- User-agent **`curl/7.68.0`**: accesso programmatico, non browser
- **MFA bypassato** (`mfa_verified = 0`): unica sessione su tutti i 7 giorni senza MFA

#### VPN Logs

```sql
SELECT * FROM vpn_logs WHERE employee_id=9 AND connect_time LIKE '2024-03-15%';
```

| connect_time        | disconnect_time     | ip_address     | location          | bytes_sent    | bytes_received | protocol |
|---------------------|---------------------|----------------|-------------------|---------------|----------------|----------|
| 2024-03-15 02:15:23 | 2024-03-15 04:58:12 | 87.12.234.156  | Bucharest, Romania| 2.456.231.936 | 15.728.640     | OpenVPN  |

`bytes_sent = 2.456.231.936` (~2.3 GB outbound): corrisponde esattamente ai dati esfiltrati.

---

### 3. Database Queries — Kill Chain

```sql
SELECT * FROM database_queries WHERE employee_id=9 AND timestamp LIKE '2024-03-15 0%' ORDER BY timestamp;
```

| timestamp           | query_type | table_name     | rows_affected | execution_time_ms |
|---------------------|------------|----------------|---------------|-------------------|
| 2024-03-15 02:45:30 | SELECT     | customers      | 50.000        | 1.230             |
| 2024-03-15 02:47:15 | SELECT     | customer_files | 125.000       | 4.567             |
| 2024-03-15 03:12:45 | **DUMP**   | customers      | 50.000        | 23.450            |
| 2024-03-15 03:47:22 | **DUMP**   | customer_files | 125.000       | 87.650            |

Pattern classico: `SELECT` di ricognizione → `DUMP` completo. Il campo `approved_by` è `NULL` su tutte le query: nessuna autorizzazione out-of-band.

---

### 4. Security Alerts

| timestamp           | severity | alert_type          | source  | description                                      |
|---------------------|----------|---------------------|---------|--------------------------------------------------|
| 2024-03-15 01:44:00 | low      | failed_login        | DLP     | Generic failed_login detected                    |
| 2024-03-15 02:15:50 | medium   | anomaly             | SIEM    | Unusual login time detected for user matteo.marino |
| 2024-03-15 02:16:10 | **high** | policy_violation    | EDR     | **MFA bypass detected during authentication**    |
| 2024-03-15 03:12:55 | **high** | threshold_exceeded  | DLP     | Large database query: 50000 rows from customers  |
| 2024-03-15 03:47:30 | **CRITICAL** | suspicious_activity | DLP | Data exfiltration: 1250.5 MB to external IP      |
| 2024-03-15 03:52:15 | **CRITICAL** | suspicious_activity | DLP | Data exfiltration: 980.3 MB to external IP       |

Tutti gli alert erano `resolved = 0`, il SOC non ha risposto in tempo reale.

---

### 5. Exploit / Ricostruzione

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('datavault_incident.db')
cur = conn.cursor()

cur.execute("""
    SELECT e.first_name, e.last_name, ft.timestamp, ft.protocol, ft.destination_ip
    FROM file_transfers ft
    JOIN employees e ON e.id = ft.employee_id
    WHERE ft.destination_ip IS NOT NULL
      AND ft.proxy_used = 0
      AND ft.file_size_mb > 500
    ORDER BY ft.timestamp DESC
    LIMIT 1
""")
row = cur.fetchone()
nome, cognome, ts, proto, ip = row

dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
last_octet = ip.split('.')[-1]

flag = f"flag{{{nome.lower()}_{cognome.lower()}_{dt.strftime('%Y%m%d_%H%M')}_{proto}_{last_octet}}}"
print(flag)
# Output: flag{...}
```

---

## Flag

```
flag{...}
```

**Decodifica:**
- `matteo_marino`: Database Administrator, employee_id 9
- `20240315`: 15 marzo 2024
- `0352`: timestamp dell'**ultimo** file transfer (`customer_files_archive.tar.gz`, 03:52:10)
- `api`: protocollo usato per l'esfiltrazione
- `98`: ultimo ottetto dell'IP di destinazione (`45.142.212.**98**`)

---

## Conclusioni

**Vettore:** Credential compromise con MFA bypass. Le credenziali di Matteo Marino (DBA, access_level 4) erano state compromesse in precedenza. L'attaccante ha operato dalla Romania via `curl`, bypassando MFA, nella finestra 02:15–04:58.

**Errore investigativo iniziale:** nella prima analisi avevo usato il timestamp del *primo* DUMP (03:47) invece dell'*ultimo* file transfer completato (03:52), il formato richiedeva l'evento terminale della catena esfiltrazione.

1. **JIT Privilege**: un DBA non dovrebbe poter eseguire `DUMP` su produzione senza approvazione `approved_by` non-NULL
2. **Alert fatigue**: 5 alert escalati da `low` a `CRITICAL` in 2 ore senza risposta SOC
3. **Geo-blocking**: nessun controllo su accessi da Bucharest per un utente basato a Milano
4. **MFA enforcement**: bypass MFA avrebbe dovuto bloccare la sessione automaticamente, non solo loggare un alert