# Empty Website

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://vuoto.challs.olicyber.it

---

## Description

> This website appears to be empty. Where could the flag be?

---

## Solution

The title **"Empty Website"** suggests that the page looks empty at
first glance. However, hidden content in web challenges is often located
inside the website's static files: **HTML, CSS, and JavaScript**. The
correct approach is therefore to inspect all three.

### Step 1 - Analyze the HTML Source

``` bash
curl http://vuoto.challs.olicyber.it/ | grep -i "flag"
```

Inside the HTML source there is a comment containing the **first part**
of the flag:

``` html
<!-- First part of the flag: "flag{..." -->
```

### Step 2 - Analyze the CSS File

``` bash
curl http://vuoto.challs.olicyber.it/css/style.css | grep -i "flag"
```

The CSS file contains a comment with the **second part** of the flag:

``` css
/* Second part of the flag: "..." */
```

### Step 3 - Analyze the JavaScript File

``` bash
curl http://vuoto.challs.olicyber.it/js/script.js | grep -i "flag"
```

The JavaScript file contains a comment with the **third part** of the
flag:

``` js
/* Here is the third part of the flag: "...}" */
```

### Step 4 - Assemble the Flag

By combining the three parts found in the HTML, CSS, and JavaScript
files, we obtain the complete flag:

    flag{...}

### Alternative Command (All-in-One)

``` bash
for url in "" "css/style.css" "js/script.js"; do
  echo "=== $url ==="
  curl -s "http://vuoto.challs.olicyber.it/$url" | grep -i "flag"
done
```
