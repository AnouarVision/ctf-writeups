# Modes of Operation Starter

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Prendi familiarità con l'interfaccia API e usala per recuperare la flag.

Sono disponibili due endpoint API:

- `GET /block_cipher_starter/encrypt_flag/`: cifra la flag con AES-ECB e restituisce il testo cifrato in hex.
- `GET /block_cipher_starter/decrypt/<ciphertext>/`: decifra qualsiasi testo cifrato hex con la stessa chiave AES-ECB e restituisce il testo in chiaro in hex.

---

## Fondamenti teorici

### Modalità ECB (Electronic Codebook)

**ECB** è la modalità di operazione più semplice di AES. Ogni blocco da 16 byte del testo in chiaro viene cifrato indipendentemente con la stessa chiave:

$$C_i = E_k(P_i)$$

Poiché cifratura e decifratura sono operazioni inverse:

$$P_i = D_k(C_i)$$

non esiste alcun concatenamento, nessun IV e nessuna casualità tra i blocchi. Questo ha due conseguenze critiche:

1. **Determinismo**: lo stesso blocco di testo in chiaro produce sempre lo stesso blocco di testo cifrato con la stessa chiave. Questo rivela informazioni strutturali sul testo in chiaro (il famoso problema del "pinguino ECB").
2. **Decifratura arbitraria**: chiunque abbia accesso all'endpoint di decifratura può decifrare qualsiasi testo cifrato, inclusa la flag cifrata, senza mai conoscere la chiave.

Questa seconda proprietà è esattamente ciò che la challenge sfrutta.

---

## Soluzione

L'attacco è una singola interazione a due passi con l'API:

**Passo 1.** Chiamare `encrypt_flag` per ottenere il testo cifrato della flag:

```
GET /block_cipher_starter/encrypt_flag/
→ {"ciphertext": "<hex>"}
```

**Passo 2.** Passare quel testo cifrato direttamente a `decrypt`:

```
GET /block_cipher_starter/decrypt/<hex>/
→ {"plaintext": "<hex>"}
```

**Passo 3.** Decodificare il plaintext hex in ASCII.

### Script

```python
#!/usr/bin/env python3

import requests

BASE = "https://aes.cryptohack.org/block_cipher_starter"

ct = requests.get(f"{BASE}/encrypt_flag/").json()["ciphertext"]
print("Ciphertext:", ct)

pt_hex = requests.get(f"{BASE}/decrypt/{ct}/").json()["plaintext"]
print("Plaintext hex:", pt_hex)

flag = bytes.fromhex(pt_hex).decode()
print("Flag:", flag)
```

---

### Flag

```
crypto{...}
```

---

## Conclusioni

Questa challenge illustra la debolezza più fondamentale della modalità ECB: l'**oracolo di decifratura**. Se un attaccante ha accesso a un endpoint di decifratura che usa la stessa chiave della cifratura, e l'endpoint accetta testi cifrati arbitrari, allora nessun testo cifrato è segreto, incluso quello prodotto dal server stesso.