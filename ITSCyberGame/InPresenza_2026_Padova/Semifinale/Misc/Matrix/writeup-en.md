# Matrix

**Competition:** ITSCyberGame <br>
**Category:** Misc

---

## Description

> "Not everything is where you expect. Welcome to the matrix!"

The challenge presents a webpage with an image (`matrix.png`) and a cryptic hint. The secret isn't in the image itself — it's in the page's heavily obfuscated JavaScript.

---

## Solution

### 1. Initial reconnaissance

Inspect the page source (DevTools → Sources or `view-source:`). There's an inline `<script>` containing obfuscated JavaScript using:
- meaningless variable names (`_0xf4a2`, `_0xd3`, `_0xc7`, ...)
- Base64-encoded strings (passed to `atob()`)
- hex escapes (`\x61\x74\x6f\x62`)
- arrays of codepoints with visual noise

The hint "Not everything is where you expect" suggests looking outside the image — i.e., into the JS source.

### 2. Vulnerability found: secret in client-side JS

The script contains two integer arrays which, when converted with `String.fromCharCode()`, yield the two halves of the flag.

Array 1 — `_0xc7` (also used as an `Icarus-Terminal-04` header value):
```js
var _0xc7 = [102,108,97,103,123,108,95,51,103,48,95,51,95];
// XOR 0x0 on each byte → String.fromCharCode → "flag{..."
```

Array 2 — `_0x44` (assembled in a callback):
```js
var _0x44 = [0x5f,0x64,0x33,0x6c,0x6c,0x34,0x5f,0x73,0x31,0x63,0x75,0x72,0x33,0x7a,0x7a,0x34,0x7d];
// → "...}"
```

The full flag is present client-side; the POST to `/api/v1/auth_check` with header `Icarus-Terminal-04` is incidental.

### 3. Extraction

Python script to extract the flag from the arrays automatically:

```python
part1_bytes = [102,108,97,103,123,108,95,51,103,48,95,51,95]
part2_bytes = [0x5f,0x64,0x33,0x6c,0x6c,0x34,0x5f,0x73,0x31,
               0x63,0x75,0x72,0x33,0x7a,0x7a,0x34,0x7d]

flag = ''.join(chr(b ^ 0x0) for b in part1_bytes + part2_bytes)
print(f"FLAG: {flag}")
```

Or directly in the browser console:

```js
var p1=[102,108,97,103,123,108,95,51,103,48,95,51,95];
var p2=[0x5f,0x64,0x33,0x6c,0x6c,0x34,0x5f,0x73,0x31,0x63,0x75,0x72,0x33,0x7a,0x7a,0x34,0x7d];
console.log([...p1,...p2].map(b=>String.fromCharCode(b)).join(''));
```

---

## Flag

`flag{...}`

---

## Conclusion

This challenge demonstrates a classic mistake: never trust client-side secrecy. Secrets (flags, tokens) stored in JavaScript, even if obfuscated, are recoverable by anyone with access to the page.
