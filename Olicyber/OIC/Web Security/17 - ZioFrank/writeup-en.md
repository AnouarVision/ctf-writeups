# Zio Frank

**Competition:** OliCyber<br>
**Category:** Web / Session Tampering<br>
**URL:** http://zio-frank.challs.olicyber.it

---

## Description

> Uncle Frank has a nice website, but to find the flag you need to be an administrator!

A Ruby on Rails website with a vulnerable session system. The goal is to modify the session cookie to gain administrator access.

---

## Solution

### Step 1 — Session Analysis

After registering an account and logging in, the site assigns a session cookie with the following value:

```
rack.sessions = BAh7CkkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkVjNDM1ZjYwZWI1OTYwMjViMWM3MDJkNzE0ZTc3NmUyNzI5OTJjOGNiNTlkYzc0YmVlOTA5NDFiNzNjMzIzYmEwBjsARkkiCWNzcmYGOwBGSSIxa1d1ZTdLZmxOUlR5ZGJZSlVlcXNCQ2Y5dXpEaU5FM2s4WVBkNzN1dmU5VT0GOwBGSSINdHJhY2tpbmcGOwBGewZJIhRIVFRQX1VTRVJfQUdFTlQGOwBUSSItMjZiYjU2ZmQwZDhmMGI5ZDdhYThhOWEwYzI3ZmU1YmIwMGZiMWNmNQY7AEZJIg11c2VybmFtZQY7AEZJIgpNYXVybwY7AFRJIg1pc19hZG1pbgY7AEZG--07d1859e7c2872d3900df7c647aef484b29fa2e4
```

This is a **serialized and signed** Ruby on Rails session cookie. We decode and analyze its contents.

---

### Step 2 — Decoding the Cookie

The cookie is **Base64-encoded**. Decoding the initial part, we recognize the Rails session structure with the following fields:

| Field | Value |
|---|---|
| `session_id` | `c435f60eb5960253b1c702d714e776e27299...` |
| `csrf` | CSRF token |
| `username` | `Mauro` |
| **`is_admin`** | `false` |

**The critical field is `is_admin`, which is set to `false`.**

---

### Step 3 — Identifying the Vulnerability

Analyzing the source code (`main.rb`), we find the vulnerable endpoint:

```ruby
post '/admin/init' do
  username = "admin-#{SecureRandom.hex}"
  password = SecureRandom.hex
  statement = $client.prepare("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)")
  statement.execute(username, password, 1)
  return "{\"username\":\"#{username}\"}"
end
```

The endpoint creates an admin account and **returns the generated username**. Then, in the registration code:

```ruby
post '/register' do
  begin
    statement = $client.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
    result = statement.execute(params[:username], params[:password])
    # ...
  end
end
```

There is no check preventing registration with a username that already exists as an admin!

---

### Step 4 — Actual Exploit (very simple)

1. Send a POST request to `/admin/init` to obtain the admin username:

```bash
curl -X POST http://zio-frank.challs.olicyber.it/admin/init
```

**Output:**
```json
{"username":"admin-40118bd39c408d357f2186f20c73147b"}
```

2. Copy the received username: `admin-40118bd39c408d357f2186f20c73147b`

3. Visit the registration page and register with:
   - **Username:** `admin-40118bd39c408d357f2186f20c73147b`
   - **Password:** any password of your choice (e.g. `password`)

4. Log in with the same credentials

---

### Step 5 — Result

Once logged in, the system checks whether the user with that username is an admin in the database. Since the `/admin/init` endpoint created an account with `is_admin = 1`, the login detects that you are an admin and displays the flag:

```
Omaggio da zio Frank
La flag è flag{...} 🚀
```

---

## Vulnerabilities Exploited

| Aspect | Detail |
|---|---|
| **Type 1** | Unauthorized Admin Account Creation (`/admin/init` endpoint with no authentication) |
| **Type 2** | Duplicate Username Registration (no uniqueness check on username) |
| **Root Cause** | The system assumes every username is unique, but does not validate this at registration time |
| **Vector** | 1) POST `/admin/init` to obtain the admin username; 2) Register the same username with a different password |
| **Impact** | Administrator access with arbitrary credentials |

---

### The Error Chain

1. The `/admin/init` endpoint creates an admin account without authentication → **username is publicly known**
2. The `/register` endpoint does not validate username uniqueness → **you can register with the same username**
3. The password is not constrained → **you can choose any password**
4. Login checks `is_admin` from the database → **if the username exists as admin, you are admin**

---

## Mitigations

- **Protect the `/admin/init` endpoint** with strict authentication and authorization
- **Validate username uniqueness** during registration (UNIQUE constraint in the database)
- **Prevent account overwrites** by adding a check that blocks registration with already-existing usernames:

```ruby
post '/register' do
  begin
    # Check if username already exists
    existing = $client.prepare("SELECT id FROM users WHERE username = ? LIMIT 1").execute(params[:username])
    if existing.count > 0
      return redirect 'register.html?error=username_exists'
    end

    statement = $client.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
    result = statement.execute(params[:username], params[:password])
    redirect 'login.html'
  rescue Error
    redirect 'register.html?error'
  end
end
```

- Never expose sensitive information such as admin account names through public APIs
- Use UNIQUE database constraints to prevent duplicates
- Log all registration attempts with usernames that already exist

---

## Conclusions

This challenge demonstrates how an improperly protected session can be compromised. Even though Rails provides protection through signing, a flawed implementation or a weak key can expose the application to session tampering.