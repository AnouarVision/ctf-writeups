# A Diffiecult Communication

**Competizione:** OliCyber<br>
**Categoria:** Crypto<br>
**Servizio:** `nc crypto-13.challs.olicyber.it 30006`

---

## Descrizione

> Questa challenge è molto simile alla precedente: sarai però tu a dover scegliere i parametri per instanziare il protocollo di Diffie-Hellman, questa volta.

Il server chiede di scegliere un safe prime $p$ da almeno 1024 bit e un generatore $g$, eseguire uno scambio DH con Alice e usare il segreto condiviso per decifrare un messaggio AES-CBC.

---

## Background matematico

**Safe prime.** Un primo $p$ si dice *safe prime* se anche $q = (p-1)/2$ è primo. In questo caso il gruppo $(\mathbb{Z}/p\mathbb{Z})^*$ ha ordine $p-1 = 2q$, con sottogruppi di ordine $1, 2, q, 2q$. Questo rende il DLP resistente ad attacchi come Pohlig-Hellman, che sfruttano la fattorizzazione dell'ordine del gruppo.

**Generatore primitivo.** Un elemento $g$ è un generatore primitivo di $(\mathbb{Z}/p\mathbb{Z})^*$ se il suo ordine è esattamente $p-1$. Per un safe prime $p = 2q+1$, i possibili ordini di $g$ sono $1, 2, q, 2q$. Quindi $g$ è primitivo se e solo se:

$$g^2 \not\equiv 1 \pmod{p} \qquad \text{e} \qquad g^q \not\equiv 1 \pmod{p}$$

Questo spiega perché $g = 2$ non era accettato: $2^q \equiv 1 \pmod{p}$, ovvero 2 ha ordine $q$ invece di $p-1$, generando solo un sottogruppo di indice 2.

---

## Soluzione

### Step 1 — Scelta dei parametri

Si usa il safe prime MODP di RFC 3526 a 1536 bit, già noto e verificato:

$$p = 32317006071311007\ldots90559 \quad \text{(1536 bit)}$$

Per trovare un generatore primitivo si cerca il primo $g \geq 2$ che soddisfi entrambe le condizioni:

```python
q = (p - 1) // 2
for g in range(2, 100):
    if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
        print(g)  # g = 11
        break
```

$g = 2$ fallisce perché $2^q \equiv 1 \pmod{p}$. Il primo generatore valido è $g = \mathbf{11}$.

---

### Step 2 — Scambio di chiavi DH

Si sceglie una chiave privata casuale $b \in [2, p-2]$ e si calcola la chiave pubblica:

$$A = g^b \bmod p$$

che viene inviata ad Alice. Alice risponde con la propria chiave pubblica $B$ (in esadecimale).

Il segreto condiviso si calcola come:

$$S = B^b \bmod p = g^{ab} \bmod p$$

---

### Step 3 — Decifratura AES-CBC

Alice cifra il messaggio con AES-CBC usando i **primi 16 byte** del segreto condiviso $S$ come chiave:

$$\text{key} = S_{\text{bytes}}[0:16]$$

La decifratura è:

$$P_i = D_K(C_i) \oplus C_{i-1}, \qquad C_0 = \text{IV}$$

---

### Exploit

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

p = 32317006071311007300338913926423828248817941241140239112842009751400741706634354222619689417363569347117901737909704191754605873209195028853758986185622153212175412514901774520270235796078236248884246189477587641105928646099411723245426622522193230540919037680524235519125679715870117001058055877651038861847280257976054903569732561526167081339361799541336476559160368317896729073178384589680639671900977202194168647225871031411336429319536193471636533209717077448227988588565369208645296636077250268955505928362751121174096972998068410554359584866583291642136218231078990999448652468262416972035911852507045361090559
g = 11

b = 2057939323469767579258041254911331312406921907737196803070551296365158479188311823295034201349665400738949645153954296141944445345691211271053605784570580492308271406168808986255519252927126325446163648664692269297613274235101077169788925775651956866975328351255724713250718624090763626666826245871079085084419213555811587175294646662587845459052516736903985553414492584446247418871507388028097097298189224204931891506453462041423465954548010828355362058571908502187963055121965695828102359807101621860378459488302416177917148971576455546003652450556842593139524593133569853174340230437482085895484367896690235284115

Alice_pub = int("194f9f71ee2d44f46728746b878c9df268a9e4cadd4aba53c67ea05639d3b51cb94c2fc383a2305573b2b7b1ec9eb1d78fa22929f5063bf8d3aabc0a9620c194690b47a2d858ba5d6003b98a5cda9e02dcb3c4449a8177a616c39990e19fcaffb0715a3cd1d6fbcd56a0e8899ffac14b0078756e90cfa895753183d54637225a768f66ba5791636d50b6f2105eef683bc1f1918a1e06e2690ae212d0244fc8a84dd84f4afffec6a5d894b3ca0ec97cb4672ba110a131ba86fcd56baa929677a5d2bde3a2ceb03b5d09c139eafbcf58c66789026e3ecbb1b071f826cbc49a6a2ec4eba26a56273cea0ee996ea250f8cc7363b362e6e07a5bbaebcb1ebe2953e1b", 16)

shared = pow(Alice_pub, b, p)
shared_bytes = shared.to_bytes((shared.bit_length() + 7) // 8, 'big')
key = shared_bytes[:16]

IV  = bytes.fromhex("f4bb33d5c6c493d005adeaf676841324")
msg = bytes.fromhex("c49819031df33ccec1f0aca164d75249679c2ef6bf1ae10ac84f72fd324d332ec119500f36c9b465c7ff15b47a30765f77f2c859db8ff9986da57c069f9caa6b")

cipher = AES.new(key, AES.MODE_CBC, IV)
print(unpad(cipher.decrypt(msg), 16).decode())
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

> DH su safe prime garantisce che il DLP sia difficile anche per attaccanti che conoscono la struttura del gruppo — ma scegliere un generatore sbagliato può ridurre drasticamente lo spazio di lavoro.

Tre osservazioni fondamentali:

1. **Perché i safe prime:** su un primo $p = 2q+1$ con $q$ primo, l'ordine del gruppo è $p-1 = 2q$, che ha solo i fattori $2$ e $q$. L'attacco di Pohlig-Hellman riduce il DLP ai sottogruppi di ordine pari ai fattori primi dell'ordine del gruppo, con $q$ grande (centinaia di bit), entrambi i sottogruppi sono resistenti.

2. **Perché $g=2$ era rifiutato:** 2 ha ordine $q$ in questo gruppo, non $p-1$. Usarlo come generatore significa lavorare in un sottogruppo di indice 2, dimezzando effettivamente lo spazio delle chiavi e riducendo la sicurezza.

3. **KDF implicita:** usare direttamente i primi byte del segreto DH come chiave AES è una pratica sconsigliata in produzione. Il segreto condiviso $S = g^{ab} \bmod p$ non è uniformemente distribuito sui bit, in pratica si usa una *Key Derivation Function* (KDF) come HKDF per derivare una chiave crittograficamente sicura da $S$.