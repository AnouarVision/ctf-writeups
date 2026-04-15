# Classic Cipher

**Competizione:** OliCyber<br>
**Categoria:** Crypto

---

## Descrizione
> Ciphertext: `xcqv{gvyavn_zvztv_etvtddlnxcgy}`
---

## Analisi del codice

```python
def generateKey():
    start = random.randint(1, 25)
    key = "".join([alphabet[start:], alphabet[0:start]])
    return key
```

La chiave iniziale è una rotazione ciclica dell'alfabeto di `start` posizioni a sinistra:

$$K^{(0)} = \sigma^{\text{start}}(\mathcal{A})$$

dove $\mathcal{A} = (\texttt{a}, \texttt{b}, \ldots, \texttt{z})$ e $\sigma$ è l'operatore di rotazione sinistra di un passo su $\mathbb{Z}_{26}$.

```python
def encrypt(plain, key):
    for k in range(len(plain)):
        i = alphabet.index(character)
        characterEncrypted = key[i]
        key = "".join([key[len(key)-1:], key[0:len(key)-1]])
```

Ad ogni passo $t$, la lettera in posizione $i$ viene cifrata come $K^{(t)}[i]$, dopodiché la chiave viene ruotata a **destra** di un passo:

$$K^{(t+1)} = \sigma^{-1}(K^{(t)})$$

---

## Modello matematico

Sia $\mathcal{A} = \{0, 1, \ldots, 25\}$ l'alfabeto identificato con $\mathbb{Z}_{26}$. La chiave al passo $t$ è:

$$K^{(t)}[j] = (j + \text{start} - t) \bmod 26 \qquad \forall j \in \mathbb{Z}_{26}$$

La cifratura del carattere in posizione $i$ al passo $t$ è quindi:

$$C_t = K^{(t)}[P_t] = (P_t + \text{start} - t) \bmod 26$$

dove $P_t \in \mathbb{Z}_{26}$ è il valore numerico della lettera in chiaro.

La decifratura si ottiene invertendo la mappa:

$$P_t = (C_t - \text{start} + t) \bmod 26$$

Questa struttura è analoga a quella di una **macchina a rotore** elementare: la chiave non è statica ma evolve deterministicamente ad ogni carattere cifrato, introducendo una dipendenza dalla posizione $t$ nel messaggio.

---

## Soluzione

### Step 1 — Spazio delle chiavi

Il parametro `start` è campionato uniformemente da $\{1, \ldots, 25\}$, producendo uno spazio delle chiavi di cardinalità:

$$|\mathcal{K}| = 25$$

Questo rende il bruteforce computazionalmente banale: $O(25 \cdot n)$ operazioni, dove $n$ è la lunghezza del ciphertext.

### Step 2 — Known Plaintext Attack

Il formato della flag è noto: i primi quattro caratteri del plaintext sono $\texttt{flag}$, corrispondenti a $P = (5, 11, 0, 6)$ in $\mathbb{Z}_{26}$.

Per $t = 0$ (primo carattere):

$$C_0 = (P_0 + \text{start}) \bmod 26$$
$$\texttt{x} = (5 + \text{start}) \bmod 26$$
$$\text{start} = (23 - 5) \bmod 26 = 18$$

Verifica sulle posizioni successive:

$$t=1: \quad C_1 = (11 + 18 - 1) \bmod 26 = 28 \bmod 26 = 2 \quad \longrightarrow \quad \texttt{c} \checkmark$$
$$t=2: \quad C_2 = (0 + 18 - 2) \bmod 26 = 16 \quad \longrightarrow \quad \texttt{q} \checkmark$$
$$t=3: \quad C_3 = (6 + 18 - 3) \bmod 26 = 21 \quad \longrightarrow \quad \texttt{v} \checkmark$$

La chiave è univocamente determinata: $\text{start} = 18$.

### Step 3 — Decifratura completa

Applicando $P_t = (C_t - 18 + t) \bmod 26$ a ogni carattere alfabetico:

```python
alphabet = "abcdefghijklmnopqrstuvwxyz"

def decrypt(ciphertext, start):
    key = alphabet[start:] + alphabet[:start]
    plaintext = ""
    for c in ciphertext:
        if c.islower():
            i = key.index(c)
            plaintext += alphabet[i]
            key = key[-1:] + key[:-1]
        elif c.isupper():
            i = key.index(c.lower())
            plaintext += alphabet[i].upper()
            key = key[-1:] + key[:-1]
        else:
            plaintext += c
    return plaintext

ciphertext = "xcqv{gvyavn_zvztv_etvtddlnxcgy}"
print(decrypt(ciphertext, 18))
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge illustra tre proprietà fondamentali dei cifrari a rotore elementari:

1. **Spazio delle chiavi insufficiente**: $|\mathcal{K}| = 25$ è un insieme finito di taglia trascurabile. Per un cifrario sicuro lo spazio delle chiavi deve soddisfare $|\mathcal{K}| \geq 2^{128}$, rendendo l'enumerazione computazionalmente intrattabile per il teorema della complessità del bruteforce.

2. **La rotazione della chiave non aggiunge entropia**: la funzione $K^{(t)}[j] = (j + \text{start} - t) \bmod 26$ è completamente determinata da un unico parametro scalare $\text{start} \in \mathbb{Z}_{25}$. La dipendenza da $t$ è lineare e quindi invertibile analiticamente, non proteggendo dalla crittoanalisi.

3. **Il Known Plaintext Attack è immediato**: la linearità della mappa di cifratura in $\mathbb{Z}_{26}$ consente di ricavare $\text{start}$ dalla sola conoscenza di $(P_0, C_0)$, riducendo l'attacco a una singola sottrazione modulare. Cifrari moderni come AES sono progettati per resistere al KPA anche con migliaia di coppie note.