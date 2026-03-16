# Click Me

**Competition:** OliCyber<br>
**Category:** Web<br>
**URL:** http://click-me.challs.olicyber.it

---

## Description

> I created a clicker game, can you reach 10 million cookies?

A simple page with a clicker game where you need to reach 10 million cookies. At first glance, it seems to require 10 million manual clicks, but the code contains an obvious vulnerability.

---

## Solution

### Step 1 — HTML Code Analysis

By visiting the site and inspecting the source code (F12 → Sources/Elements), we find the entire game logic:

```javascript
var num = 0;
window.onload = function () {
    var name = prompt("Inserisci il tuo nome");
    var space = document.getElementById("space");
    space.innerHTML = "Pasticceria da: " + name;
}
var cookie = document.getElementById("cookie");
function cookieClick() {
    num += 1;
    var numbers = document.getElementById("numbers");
    document.cookie = "cookies="+num;
    numbers.innerHTML = num;
}
```

---

### Step 2 — Vulnerability Identification

The code has an obvious vulnerability: **the `num` variable is accessible and modifiable directly from the browser console**.

The `cookieClick()` function simply increments `num` by 1, but there's no validation:
- No server-side validation
- The variable is global and modifiable
- The value is saved only in an unprotected cookie

---

### Step 3 — Exploit via Browser Console

Open your browser's console (`F12` → Console) and execute the following command:

```javascript
num = 10000000;
document.getElementById("numbers").innerHTML = num;
document.cookie = "cookies=10000000";
```

---

### Step 4 — Result

After executing the command, the page will display `10000000` and reveal the challenge flag.

## Conclusions

This is a classic example of **client-side insecurity**. The main issues are:

1. **No server-side validation**: cookie counting is handled entirely by the client
2. **Modifiable global variables**: `num` is accessible from the console
3. **No authentication/authorization**: there's no control over who modifies the data
4. **Unprotected cookies**: the cookie value is not signed or encrypted

In a real game, the server should:
- Handle counting server-side
- Validate each click with a token or session ID
- Protect data with cryptographic signatures (HMAC)
- Implement rate limiting to prevent abuse

---