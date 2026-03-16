# No Robots Here

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://no-robots.challs.olicyber.it

---

## Description

> Are you able to find the robots?

---

## Solution

The challenge name itself is the hint: **No Robots Here** points directly to `robots.txt`, a standard file used by websites to tell web crawlers which pages they should or should not index.

### Step 1 — Check robots.txt

Navigate to:

```
http://no-robots.challs.olicyber.it/robots.txt
```

The file contains:

```
User-agent: *
Disallow: /I77p0mhKjr.html
```

The `Disallow` directive reveals a hidden page that the site is trying to keep away from search engines.

### Step 2 — Visit the hidden page

Navigate to the disallowed path:

```
http://no-robots.challs.olicyber.it/I77p0mhKjr.html
```

The page contains the flag.