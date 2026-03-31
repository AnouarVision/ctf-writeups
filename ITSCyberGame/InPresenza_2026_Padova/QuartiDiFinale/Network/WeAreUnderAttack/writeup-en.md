# We Are Under Attack!

**Competition:** ITSCyberGame <br>
**Category:** Network <br>
**File:** network_dump.pcap

---

## Description

Our IT team detected a traffic spike toward the internal inventory management server. The firewall did not log any large outbound file transfers and the web server did not crash, but we suspected an attacker had exfiltrated sensitive data from the backend database. Can you tell us what was taken?

---

## Solution

### Step 1 — Traffic overview

Open the `.pcap` in Wireshark and inspect the protocol hierarchy (`Statistics` → `Protocol Hierarchy`):

```
eth → ip → tcp → http   (28063 frames, 4671 HTTP)
```

All traffic is HTTP over TCP. Apply the `http` display filter and you will immediately notice thousands of GET requests to `/product?id=...`.

### Step 2 — Identify the attack

Apply the filter:

```
http.request.uri contains "SELECT"
```

Decoded URIs reveal SQL injected into the `id` parameter, for example:

```
/product?id=1 AND (SELECT substr((SELECT pin FROM users WHERE username='admin'), 1, 1)) = 'a'
```

The pattern is clear: a Blind Boolean-Based SQL Injection. The attacker tests one character at a time using a fixed position and observes different HTTP responses:

- `200 OK` → condition true (correct character)
- `404 Not Found` → condition false (incorrect character)

There are **2336 automated GET requests** in total.

### Step 3 — Isolate positive responses

To find successful guesses, filter responses with status `200`:

```
http.response.code == 200
```

This yields **53 frames** with a positive response. For each, follow the corresponding request:

1. Click the `200` response packet
2. In the Hypertext Transfer Protocol panel read `Request in frame: N`
3. Jump to frame N (`Ctrl+G`) and read the request URI

Alternatively, export packet dissections to CSV (`File` → `Export Packet Dissections` → `As CSV`) and filter the exported rows for code `200` offline.

### Step 4 — Reconstruct the exfiltrated data

Correlating the 53 `200 OK` responses with their requests and ordering them by the tested position (`substr(..., N, 1)`) reconstructs the extracted database values.

**Table `users` — `pin` (admin):**

| Pos | Char | Frame |
|-----|------|-------|
| 1 | `8` | 728 |
| 2 | `2` | 1388 |
| 3 | `9` | 2132 |
| 4 | `1` | 2780 |

**Table `users` — `password` (admin):**

| Pos | Char | Pos | Char |
|-----|------|-----|------|
| 1 | `a` | 9 | `s` |
| 2 | `d` | 10 | `s` |
| 3 | `m` | 11 | `_` |
| 4 | `i` | 12 | `8` |
| 5 | `n` | 13 | `3` |
| 6 | `_` | 14 | `7` |
| 7 | `p` | 15 | `2` |
| 8 | `4` |     |     |

**Table `backup_codes` — `code` (id=1):**

```
BKP-8922-A1B9-4002
```

(The `-` separators at positions 4, 9 and 14 do not appear in the dump because the attacker skipped them during enumeration.)

**Table `secrets` — `flag` (id=1):**

| Pos | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
|-----|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|-----|
| Char | `f` | `l` | `a` | `g` | `{` | `b` | `l` | `1` | `n` | `d` | `S` | `Q` | `L` | `_` | `H` | `e` | `l` | `l` | `0` |

### Step 5 — Summary of exfiltrated data

| Table | Field | Value |
|-------|-------|-------|
| `users` | `pin` | `8291` |
| `users` | `password` | `admin_p4ss_8372` |
| `backup_codes` | `code` | `BKP-8922-A1B9-4002` |
| `secrets` | `flag` | `flag{bl1ndSQL_Hell0}` |

---

## Flag

```
flag{bl1ndSQL_Hell0}
```

---

## Conclusion

This challenge demonstrates how a Blind Boolean-Based SQL Injection can exfiltrate sensitive data without any large file transfers and without crashing the server, explaining why the firewall logged nothing obvious. The only indication was the high request volume (2336 GETs in quick succession to the same endpoint). Reconstruction was possible by identifying the 53 `200 OK` responses among the 404s, each corresponding to a correctly guessed character, and ordering them by position.
