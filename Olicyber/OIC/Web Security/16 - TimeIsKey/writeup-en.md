# Time is Key

**Competition:** OliCyber<br>
**Category:** Web / Timing Attack<br>
**URL:** http://time-is-key.challs.olicyber.it

---

## Description

> No time! Quick! Get the flag now!

A challenge based on **timing attack**: the server's response reveals how many flag characters are correct based on the time taken.

**Notes:**
- The flag contains only lowercase letters and numbers
- The flag is NOT in standard format → must be wrapped manually in `flag{...}`

---

## Solution

### Step 1 — Source Code Analysis

The first step is to retrieve the source code of the vulnerable page:

```bash
curl -s 'http://time-is-key.challs.olicyber.it/index.php?show_source'
```

```php
<?php
    $flag = getenv("flag");
    if (isset($_POST["flag"]) && !is_array($_POST["flag"])){
        $your_flag = $_POST["flag"];
        $flag_len = 6;
        if (strlen($your_flag) !== $flag_len){
            die("Sbagliato! :(");
        }
        for ($i = 0; $i < $flag_len; $i++){
            if ($your_flag[$i] !== $flag[$i]){
                die("Sbagliato! :(");    // stops immediately
            }
            usleep(1000000);             // +1 second for each correct character
        }
        die("Che stai aspettando? Invia la flag!");
    }
?>
```

---

### Step 2 — Understanding the Vulnerability

The server compares the submitted flag **character by character**, and for each **correct** character waits `1,000,000 µs` = **1 second** before moving to the next. At the first wrong character it terminates immediately.

This creates a measurable **temporal oracle**:

| Correct Characters | Expected Response Time |
|---|---|
| 0 | ~0.2s |
| 1 | ~1.2s |
| 2 | ~2.2s |
| 3 | ~3.2s |
| 4 | ~4.2s |
| 5 | ~5.2s |
| 6 | ~6.2s |

---

### Step 3 — Timing Attack

Instead of having to try all possible combinations (`36^6 ≈ 2 billion`), the timing attack reduces the problem to `36 × 6 = 216 attempts` — one per character per position.

For each position, we test all possible characters and measure the response time. The character that produces the longest time is the correct one.

---

### Step 4 — Automating the Timing Attack

To automate the timing attack, a Python script tests all possible characters for each position and identifies which produces the longest response time.

The strategy is:
1. For each position in the flag (0-5)
2. Test all possible characters (a-z, 0-9)
3. Measure the response time
4. The character with the longest time is the correct one
5. Repeat until the flag is complete

**The Python exploit script is available in this folder → [`timeiskey.py`](timeiskey.py)**

---

### Step 5 — Expected Output

The script tests all 36 characters for each position. For the first position, for example:

```
  [1/6] aaaaaa → 0.19s
  [1/6] baaaaa → 0.18s
  [1/6] caaaaa → 0.20s
  ...
  [1/6] 7aaaaa → 1.21s       ← time spike! Correct character is '7'
  ...
  [1/6] 9aaaaa → 0.19s

[+] Flag finora: 7 (tempo: 1.21s)

  [2/6] 7aaaaa → 1.20s
  [2/6] 7baaaa → 1.19s
  ...
  [2/6] 71aaaa → 2.22s       ← time spike! Correct character is '1'
  ...

[+] Flag finora: 71 (tempo: 2.22s)

  ...

[+] Flag finora: 71m1n6 (tempo: 6.21s)

flag{71m1n6}
```

The pattern is clear: a wrong attempt takes ~0.2s, while each correct character adds exactly **~1 second** to the response time, making the spike easy to spot.

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | Timing Attack (Time-Based Oracle) |
| **Root Cause** | `usleep()` executed only after a correct character |
| **Effect** | Response time reveals how many characters are correct |
| **Impact** | Flag enumeration character by character |

---

## Conclusions

- Timing attacks are real and difficult to mitigate completely
- Don't use `usleep()` or delays in business logic for security measures
- Implement **constant-time comparison** (e.g., `hash_equals()` in PHP)
- Add **random jitter** to response times to hide patterns
- Implement **rate limiting** to prevent automated testing
- Log failed attempts and block clients with too many errors