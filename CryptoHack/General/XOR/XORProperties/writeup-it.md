# XOR Properties

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Tre chiavi casuali sono state messe in XOR tra loro e con la flag. Usare le proprietà dello XOR per annullare la cifratura e recuperare la flag.

Vengono forniti i seguenti valori codificati in hex:

```
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
```

---

## Fondamenti teorici

### Le quattro proprietà dello XOR

| Proprietà | Enunciato |
|:---|:---|
| Commutativa | $A \oplus B = B \oplus A$ |
| Associativa | $A \oplus (B \oplus C) = (A \oplus B) \oplus C$ |
| Elemento neutro | $A \oplus 0 = A$ |
| Auto-inverso | $A \oplus A = 0$ |

Insieme, queste quattro proprietà rendono $(\{0,1\}^n, \oplus)$ un **gruppo abeliano**. La conseguenza operativamente più utile è la **legge di cancellazione**: per qualsiasi $A, K$, se $C = A \oplus K$ allora $C \oplus K = A \oplus K \oplus K = A \oplus 0 = A$. Applicare lo XOR con la chiave una seconda volta annulla la cifratura.

---

## Soluzione

### Derivazione algebrica

I tre passi applicano ciascuno la legge di cancellazione per isolare un'incognita da una relazione XOR nota.

**Passo 1 — Recupero di KEY2**

$$\text{KEY2} \oplus \text{KEY1} = R_1 \implies \text{KEY2} = R_1 \oplus \text{KEY1}$$

**Passo 2 — Recupero di KEY3**

$$\text{KEY2} \oplus \text{KEY3} = R_2 \implies \text{KEY3} = R_2 \oplus \text{KEY2}$$

**Passo 3 — Recupero della FLAG**

Per commutatività e associatività, l'ordine delle chiavi nel testo cifrato è irrilevante:

$$C = \text{FLAG} \oplus \text{KEY1} \oplus \text{KEY2} \oplus \text{KEY3}$$

$$\text{FLAG} = C \oplus \text{KEY1} \oplus \text{KEY2} \oplus \text{KEY3}$$

Ogni chiave si annulla con se stessa: $\text{KEY}_i \oplus \text{KEY}_i = 0$, lasciando soltanto FLAG.

### Script

```python
#!/usr/bin/env python3

hex_key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
hex_key2_xor_key1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
hex_key2_xor_key3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
hex_flag_xor_key1_xor_key3_xor_key2 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

key1 = bytes.fromhex(hex_key1)
key2_xor_key1 = bytes.fromhex(hex_key2_xor_key1)
key2 = bytes([a ^ b for a, b in zip(key2_xor_key1, key1)])

key2_xor_key3 = bytes.fromhex(hex_key2_xor_key3)
key3 = bytes([a ^ b for a, b in zip(key2_xor_key3, key2)])

ciphertext = bytes.fromhex(hex_flag_xor_key1_xor_key3_xor_key2)
flag = bytes([a ^ b ^ c ^ d for a, b, c, d in zip(ciphertext, key1, key2, key3)])

print(flag)
```

### Tabella dei passi

| Passo | Noti | Incognita | Operazione |
|:---:|:---|:---|:---|
| 1 | KEY1, KEY2 $\oplus$ KEY1 | KEY2 | $\text{KEY2} = (K2 \oplus K1) \oplus K1$ |
| 2 | KEY2, KEY2 $\oplus$ KEY3 | KEY3 | $\text{KEY3} = (K2 \oplus K3) \oplus K2$ |
| 3 | KEY1, KEY2, KEY3, ciphertext | FLAG | $\text{FLAG} = C \oplus K1 \oplus K2 \oplus K3$ |

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge dimostra che la cifratura XOR è robusta soltanto quanto la segretezza delle sue chiavi. Quando sono disponibili informazioni parziali sulle chiavi, qui vengono fornite direttamente combinazioni XOR delle chiavi, la struttura algebrica dello XOR consente di ricostruire le incognite una per una, fino a esporre completamente il testo in chiaro.