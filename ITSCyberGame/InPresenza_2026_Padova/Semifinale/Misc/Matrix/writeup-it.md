# Matrix

**Competizione:** ITSCyberGame <br>
**Categoria:** Misc

---

## Descrizione

> "Non sempre tutto è dove ti aspetti. Benvenuto nel matrix!"

La challenge presenta una pagina con un'immagine (`matrix.png`) e un hint criptico. Il segreto non è nell'immagine, è nel codice JavaScript della pagina, fortemente offuscato.

---

## Soluzione

### 1. Ricognizione iniziale

Ispezionando il sorgente della pagina (DevTools → Sources, oppure `view-source:`), si trova un tag `<script>` con codice JavaScript offuscato tramite:
- Nomi di variabili senza senso (`_0xf4a2`, `_0xd3`, `_0xc7`...)
- Stringhe codificate in Base64 (passate a `atob()`)
- Escape esadecimali per ulteriore offuscamento (`\x61\x74\x6f\x62`)
- Array di codepoint XOR-ati con `0x0` (XOR con zero = identità, è solo noise visivo)

L'hint "Non sempre tutto è dove ti aspetti" suggerisce di guardare **fuori dall'immagine** ovvero nel sorgente JS.

### 2. Vulnerabilità individuata: Secret in Client-Side JS

Il codice contiene due array di interi che, convertiti con `String.fromCharCode()`, producono le due metà della flag.

**Array 1 — `_0xc7`** (usato anche come valore dell'header di autenticazione):
```js
var _0xc7 = [102,108,97,103,123,108,95,51,103,48,95,51,95];
// XOR 0x0 su ogni byte → String.fromCharCode → "flag{..."
```

**Array 2 — `_0x44`** (costruito nella callback della risposta HTTP):
```js
var _0x44 = [0x5f,0x64,0x33,0x6c,0x6c,0x34,0x5f,0x73,0x31,0x63,0x75,0x72,0x33,0x7a,0x7a,0x34,0x7d];
// → "...}"
```

Il codice fa anche una chiamata POST a `/api/v1/auth_check` con l'header `Icarus-Terminal-04` valorizzato con la prima metà della flag ma la flag completa si ottiene interamente dal client.

### 3. Exploit

Script Python per estrarre automaticamente la flag dal sorgente:

```python
#!/usr/bin/env python3

part1_bytes = [102,108,97,103,123,108,95,51,103,48,95,51,95]
part2_bytes = [0x5f,0x64,0x33,0x6c,0x6c,0x34,0x5f,0x73,0x31,
               0x63,0x75,0x72,0x33,0x7a,0x7a,0x34,0x7d]

flag = ''.join(chr(b ^ 0x0) for b in part1_bytes + part2_bytes)
print(f"FLAG: {flag}")
```

Output:
```
FLAG: flag{...}
```

Oppure, direttamente in console del browser (DevTools → Console):

```js
var p1=[102,108,97,103,123,108,95,51,103,48,95,51,95];
var p2=[0x5f,0x64,0x33,0x6c,0x6c,0x34,0x5f,0x73,0x31,0x63,0x75,0x72,0x33,0x7a,0x7a,0x34,0x7d];
console.log([...p1,...p2].map(b=>String.fromCharCode(b)).join(''));
```

---

## Flag

`flag{...}`

---

## Conclusioni

La challenge insegna una vulnerabilità classica: **non fidarsi della sicurezza lato client**. Qualsiasi segreto (flag, token, chiave) hardcodato in JavaScript, anche se offuscato, è recuperabile da chiunque abbia accesso al browser. L'offuscamento non è cifratura.