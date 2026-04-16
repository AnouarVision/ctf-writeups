# Corrupted Key Exchange

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc corrupted.challs.olicyber.it 10604`

---

## Descrizione

> Bob e Alice non sanno che ho installato un virus dentro ai server che usano per comunicare. Hai totale controllo sui parametri usati per scambiare le chiavi.

Viene fornito il codice sorgente del server. Il server legge i parametri DH $(g, p)$ da un file che l'attaccante può sovrascrivere liberamente, esegue uno scambio di chiavi tra Alice e Bob, e cifra la flag con AES-ECB usando il segreto condiviso derivato.

---

## Analisi del codice

Il server esegue uno scambio Diffie-Hellman tra Alice e Bob usando i parametri letti dal file:

```python
Alice_public = pow(g, Alice_private, p)
Bob_public   = pow(g, Bob_private,   p)

Shared_secret = pow(g, Alice_private * Bob_private, p)
key = (Shared_secret % (2**(8*16) - 1)).to_bytes(16, 'big')

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(FLAG, 16))
```

La vulnerabilità è che i parametri $(g, p)$ provengono interamente dall'input dell'attaccante, senza alcuna validazione.

---

## Soluzione

### Step 1 — Attacco: Parameter Injection con $g = 1$

Si sfrutta la proprietà algebrica fondamentale dell'esponenziazione:

$$1^x = 1, \quad \forall x \in \mathbb{Z}$$

Se l'attaccante impone $g = 1$, allora indipendentemente dalle chiavi private scelte da Alice e Bob:

$$A = g^{a} \bmod p = 1^{a} \bmod p = 1$$
$$B = g^{b} \bmod p = 1^{b} \bmod p = 1$$

Il segreto condiviso diventa:

$$S = g^{ab} \bmod p = 1^{ab} \bmod p = 1$$

La chiave AES è quindi completamente deterministica:

$$K = \left(1 \bmod (2^{128} - 1)\right)\text{.to\_bytes}(16) = \underbrace{00\cdots01}_{16 \text{ byte}}$$

ovvero `0x00000000000000000000000000000001`.

---

### Step 2 — Scelta di $p$

Il file deve contenere due valori in esadecimale: `g` e `p`. Si sceglie come $p$ il primo MODP di RFC 3526 a 1536 bit, un valore noto e valido che il server accetta senza errori:

$$p = \texttt{ffffffff\ldots ffffffff} \quad \text{(prime di Oakley Group 5)}$$

---

### Step 3 — Decifratura

Con la chiave $K$ nota, la decifratura AES-ECB è immediata:

$$\text{FLAG} = D_K(C) = \text{AES-ECB-Decrypt}(K, C)$$

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

key = (1 % (2**(8*16) - 1)).to_bytes(16, 'big')
ct  = b64decode("HZJNGZczSDtWjBLe4zYaVi5U5CmD2lhwBpPRu4e3PLw=")

cipher = AES.new(key, AES.MODE_ECB)
print(unpad(cipher.decrypt(ct), 16).decode())
```

**Output:**
```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> La sicurezza di Diffie-Hellman non risiede solo nell'algoritmo, ma nella correttezza dei parametri. Parametri non validati annullano completamente ogni garanzia crittografica.

Tre osservazioni fondamentali:

1. **$g = 1$ collassa il gruppo a un singolo elemento:** il gruppo ciclico $\langle g \rangle \subseteq (\mathbb{Z}/p\mathbb{Z})^*$ generato da $g = 1$ ha ordine 1, contiene solo l'elemento identità. Lo spazio dei segreti condivisibili si riduce da $|\langle g \rangle| = p-1$ possibili valori a esattamente **1 valore**, rendendo il segreto completamente predicibile senza conoscere le chiavi private.

2. **Validazione dei parametri è obbligatoria:** i parametri DH sicuri devono soddisfare condizioni precise, $p$ deve essere un primo sicuro, $g$ deve essere un generatore di un sottogruppo di ordine grande, e $g \notin \{0, 1, p-1\}$. Lo standard RFC 7919 definisce gruppi DH pre-approvati (*finite field cryptography named groups*) proprio per evitare che implementazioni naive accettino parametri degenerati. In questo codice l'assenza di qualsiasi controllo su $g$ rende l'attacco banale.

3. **AES-ECB non nasconde i pattern:** anche se la chiave fosse stata sicura, l'uso di AES-ECB è problematico, blocchi di plaintext identici producono blocchi di ciphertext identici. Per messaggi brevi come una flag il problema è meno evidente, ma per messaggi strutturati ECB rivela la struttura del plaintext. Le modalità sicure (CBC, CTR, GCM) usano un IV o nonce per garantire che lo stesso plaintext produca ciphertext diversi ad ogni cifratura.