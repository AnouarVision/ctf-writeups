# The Data Exfiltration

**Competizione:** ITSCyberGame <br>
**Categoria:** Misc <br>
**Servizio:** cloudbank_exfiltration.db (SQLite)

---

## Descrizione

> "Il 20 marzo 2024, il team Security di CloudBank ha rilevato un picco anomalo di traffico API e costi AWS: oltre 20 GB di dati clienti sono stati esportati verso destinazioni sospette in 48 ore. L'analisi preliminare indica che qualcuno ha utilizzato un'API key compromessa per esfiltrazione massiva di dati sensibili. Il CISO sospetta che la chiave sia stata accidentalmente committata in un repository Git e poi sfruttata da un insider. Flag format flag{nome_cognome_apikey_first12chars_total_gb}"

---

## Soluzione

### 1. Ricognizione iniziale

Il database SQLite contiene 8 tabelle:

| Tabella | Righe | Contenuto |
|---------|-------|-----------|
| `employees` | 100 | Dipendenti CloudBank |
| `git_commits` | 377 | Commit con flag `contains_secret` |
| `authorized_api_keys` | 9 | Chiavi API con hash |
| `api_access_logs` | 2113 | Log accessi API |
| `s3_operations` | 1404 | Operazioni S3 |
| `billing_records` | 105 | Costi AWS |
| `slack_messages` | 403 | Messaggi interni |
| `threat_intel` | 4 | IOC noti |

**IOC da `threat_intel`:**
```
45.142.215.89   → known data exfiltration destination (HIGH)
185.220.101.42  → Tor exit node (MEDIUM)
exfil-data-store-2024 → unauthorized S3 bucket (CRITICAL)
customers/export/all  → suspicious bulk export endpoint (HIGH)
```

### 2. Identificazione del commit malevolo

```sql
SELECT gc.timestamp, gc.secret_value, gc.repository,
       e.first_name, e.last_name, e.email, e.department
FROM git_commits gc JOIN employees e ON gc.employee_id = e.id
WHERE gc.contains_secret = 1
ORDER BY gc.timestamp;
```

**4 commit con secrets trovati:**

| Data | Autore | Repo | Chiave (troncata) |
|------|--------|------|-------------------|
| 2024-03-12 | Enrico Romano | backend-api | `sk_live_167fe4...` |
| 2024-03-14 | Stefano Longo | infrastructure | `sk_live_8c467e...` |
| 2024-03-16 | Francesco Costantini | frontend-web | `sk_live_7aa1b8...` |
| **2024-03-18 16:47** | **Marco Santoro** | **backend-api** | **`sk_live_a8f2d9...`** |

Le prime 3 chiavi risultano già revocate (in `authorized_api_keys`). La chiave di Santoro **non è revocata** ed è l'unica la cui revocation_at è NULL con scopes `read:customers,read:orders,write:logs`.

### 3. Correlazione API logs ↔ IOC IP

```sql
SELECT COUNT(*), SUM(bytes_transferred),
       MIN(timestamp), MAX(timestamp)
FROM api_access_logs
WHERE api_key_hash = 'c3f87a7b8b74c38a17fe62c1e3ce92471eea2dc0de73a8b410a242bd7c3c81c8'
  AND source_ip IN ('45.142.215.89','185.220.101.42');
```

**Risultato:**
- Chiamate: **183**
- Totale bytes: **24,238,636,678** (~22.57 GB)
- Endpoint: `/api/v1/customers/export/all` (IOC confermato)
- Finestra: `2024-03-18 19:58` → `2024-03-20 19:49`

### 4. Timeline ricostruita

```
2024-03-18 16:47  Marco Santoro committa sk_live_a8f2... in repo backend-api
                  commit: d8c509b1f2a451b1ae2336436006277fd27998c2
                  msg: "Update API configuration"

2024-03-18 19:58  Prima chiamata da 45.142.215.89 (IOC) con la chiave compromessa
                  → GET /api/v1/customers/export/all → 148 MB

          ↕ 48h di esfiltrazione massiva

2024-03-20 19:49  Ultima chiamata da 45.142.215.89
                  183 totale requests, 22.57 GB trasferiti

Conferma S3: 183 PutObject su bucket "exfil-data-store-2024" = 22.16 GB
Conferma billing: picco API-Gateway $24K (20/03) + $20K (18/03)
```

### 5. Exploit / Estrazione flag

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

## Conclusioni

L'analisi mostra come un singolo errore (committare una API key) possa facilmente degenerare in una perdita massiva di dati e costi ingenti se non intercettato rapidamente. Le misure raccomandate per ridurre il rischio e migliorare la risposta sono:

- **Scansione automatica dei repository** per segreti (pre-commit hooks e controlli in CI) per prevenire commit accidentali.
- **Rotazione immediata e revoca** delle chiavi esposte; usare policy che obblighino la rotazione periodica delle chiavi sensibili.
- **Least privilege**: limitare gli scope delle API alle sole operazioni necessarie.
- **Logging centralizzato e alerting** su pattern anomali (picchi di export, trasferimenti voluminosi, IP sospetti) per rilevare esfiltrazioni in tempo reale.
- **Uso di secret managers** e variabili d'ambiente sicure invece di hardcoding in repository.
- **Formazione** del personale sulle pratiche di gestione segreti e su come evitare commit di credenziali.

Infine, mantenere una timeline dettagliata e le evidenze per supportare l'investigazione forense e le azioni legali, oltre a eseguire un post-mortem per aggiornare processi e policy aziendali.


