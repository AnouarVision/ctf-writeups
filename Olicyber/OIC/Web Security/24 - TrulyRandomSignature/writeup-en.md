# TrulyRandomSignature

**Competition:** OliCyber <br>
**Category:** Web <br>
**URL:** http://trulyrandomsignature.challs.olicyber.it

---

## Description
> Having only a cookie with the username is not secure enough, so we decided to sign it! Now it's impossible for someone to modify it without invalidating the signature! Note: if you think you've understood but can't get the flag, check that your Python version matches the server's.

The site signs the cookie `user=not_admin` with HMAC-SHA256 using a key randomly generated at boot. The goal is to forge a `user=admin` cookie with a valid signature to access `/admin` and retrieve the flag.

---

## Solution

### 1. Initial reconnaissance

```bash
curl -si "http://trulyrandomsignature.challs.olicyber.it/"
```

Response:
```
X-Uptime: 7036909
Date: Sun, 05 Apr 2026 21:04:21 GMT
Set-Cookie: user=not_admin
Set-Cookie: signature=8df8d5bb43380b88a569bc4e601dca18ad18077a22e23f27e3f9e30c0c1ee819
```

### 2. Vulnerability — Predictable `random` seed

From `app.py`:

```python
seed = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
random.seed(seed)
SUPER_SECRET_KEY = get_random_string(32)
```

The seed is the **UTC timestamp (seconds)** of the server boot time. From the `X-Uptime` header we know how long the server has been running → we can reconstruct the exact boot time and brute-force nearby seconds until the generated signature matches the known one.

### 3. Exploit

Exploit script: [trulyrandomsign.py](trulyrandomsign.py)

Output:
```
Seed: 2026-01-14 10:22:31
Key: ukgsiftrxuqiachnbtsawzuglhtjykgm
Admin signature: 95848dbc4277a386606ee9ec39db126e66da72f64afd1ef6ac32c508109c4340
```

Access `/admin` with the forged cookie:

```bash
curl -si "http://trulyrandomsignature.challs.olicyber.it/admin" \
  --cookie "user=admin; signature=95848dbc4277a386606ee9ec39db126e66da72f64afd1ef6ac32c508109c4340"
```

---

## Flag

```
flag{...}
```

---

## Conclusions

Python's `random` is **not cryptographically secure** and its state is fully determined by the seed. Using a timestamp in seconds as the seed reduces the search space to a few hundred values to brute-force.

**Correct fix:** use `secrets` or `os.urandom()` to generate the key, which do not depend on predictable seeds.
