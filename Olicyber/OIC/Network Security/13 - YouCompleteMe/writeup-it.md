# You Complete Me — CTF Write-up

## Descrizione

> Una nuova azienda ha appena rivelato il suo nuovo prodotto: una tastiera IoT!
> La feature di punta è un servizio cloud di autocompletion: ad ogni carattere che premi sulla tastiera, ti viene inviato dal server una lista di parole che possono essere il completamento di ciò che stai scrivendo.
> Un utente ha digitato tutti i caratteri di una parola di nostro interesse, ma ovviamente hanno deciso di cifrare tutta la comunicazione, quindi ci aspettiamo che non si possano decrittare i messaggi.
> Sei in grado di recuperare la parola digitata?

---

## Analisi del protocollo

Leggendo il file `challenge.py` si capisce come funziona il sistema:

```python
aes = AES.new(key, AES.MODE_ECB)
BLOCK_LENGTH = 16

def encrypt_word(word):
    return aes.encrypt(pad(word, BLOCK_LENGTH)).hex()

def decrypt_char(char):
    ch = unpad(aes.decrypt(bytes.fromhex(char)), BLOCK_LENGTH)
    assert(len(ch) == 1)
    return ch

def get_words_by_prefix(prefix):
    prefix, last_char = prefix[:-1], prefix[-1].to_bytes(1, 'big')
    lower_bound = prefix + last_char
    upper_bound = prefix + next_char(last_char)
    return [w for w in words if lower_bound <= w < upper_bound]

def handle():
    curr_prefix = b''
    while True:
        char = input()
        curr_prefix += decrypt_char(char)
        words = [encrypt_word(w) for w in get_words_by_prefix(curr_prefix)]
        print('\n'.join(words))
        print('end')
```

Il flusso è il seguente:

1. Il **client** invia un carattere cifrato con AES-ECB.
2. Il **server** decifra il carattere, aggiorna il prefisso e restituisce tutte le parole del dizionario che iniziano con quel prefisso, anch'esse cifrate con AES-ECB.
3. Si ripete fino a quando l'utente ha digitato l'intera parola.

---

## Vulnerabilità: side-channel sulla dimensione della risposta

A prima vista sembra impossibile recuperare la parola: tutto è cifrato con AES e non abbiamo la chiave.

Tuttavia c'è un **information leakage** critico: il server cifra le parole ma non nasconde **quante** parole restituisce. Dato che la lista si restringe ad ogni carattere digitato, il **numero di parole per ogni round** dipende deterministicamente dal prefisso e quindi dai caratteri in chiaro.

Questo è un classico **side-channel attack**: non ci serve decrittare nulla, perché l'informazione trapela attraverso la *lunghezza della risposta*.

---

## Estrazione del traffico pcap

Analizzando il pcap con `dpkt` si identificano due flussi TCP sulla loopback:

- **Client → Server** (porta 54832 → 6000): 13 pacchetti contenenti i caratteri cifrati.
- **Server → Client** (porta 6000 → 54832): le liste di parole cifrate, terminate da `\nend\n`.

```
Client invia 13 caratteri cifrati (ognuno è 32 hex chars = 16 byte AES block):
  [0]  ba230ba2c7a0190bd3fc1a6397462e19
  [1]  a2aa0d4635371ae029bff4f4ad772315
  [2]  453caa8dc602b776b94263ce187f3ee4
  [3]  62162a57eb11e2cab103c250895759c3
  [4]  f33cefec189ad8968d2b5d18bb4462d7
  [5]  f33cefec189ad8968d2b5d18bb4462d7  ← stesso ciphertext del [4]
  [6]  0c4f27de24f65e22b87bee65ca130c8f
  [7]  62162a57eb11e2cab103c250895759c3  ← stesso ciphertext del [3]
  [8]  991f4d3f3ed332d13a0ca417f592f62c
  [9]  9ed71db6defad585eaa5dc0cc173e45d
  [10] d7c41006035ffc41e66bc6113ade9c44
  [11] 62162a57eb11e2cab103c250895759c3  ← stesso ciphertext del [3]
  [12] 35d319445ae1001c9a4bde9136d9fad1
```

Il server risponde con un numero decrescente di parole per ogni round:

| Round | Parole restituite |
|-------|-------------------|
| 0     | 3952              |
| 1     | 825               |
| 2     | 23                |
| 3     | 3                 |
| 4     | 2                 |
| 5     | 2                 |
| 6     | 1                 |
| 7–12  | 1                 |

> **Nota:** lo stesso ciphertext nei round 3, 7, 11 conferma che il carattere digitato in quelle posizioni è identico, ulteriore informazione in chiaro estratta gratuitamente da AES-ECB.

---

## Ricostruzione della parola

Sapendo il numero di parole restituite per ogni round, si può simulare `get_words_by_prefix` su `words.txt` e trovare per ogni posizione il carattere ASCII che porta esattamente a quel conteggio:

```python
def next_char(char):
    return (ord(char) + 1).to_bytes(1, 'big')

def get_words_by_prefix(prefix, words):
    if not prefix:
        return words
    prefix_body, last_char = prefix[:-1], prefix[-1].to_bytes(1, 'big')
    lower_bound = prefix_body + last_char
    upper_bound = prefix_body + next_char(last_char)
    return [w for w in words if lower_bound <= w < upper_bound]

word_counts = [3952, 825, 23, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1]

candidates = [b'']
for step, target_count in enumerate(word_counts):
    new_candidates = []
    for prefix in candidates:
        for c in range(32, 127):
            new_prefix = prefix + bytes([c])
            result = get_words_by_prefix(new_prefix, words)
            if len(result) == target_count:
                new_candidates.append(new_prefix)
    candidates = new_candidates

print(candidates)
```

Ad ogni passo c'è un solo candidato e l'algoritmo converge univocamente.

---

## Flag

```
flag{...}
```

---

## Conclusioni

Il vero problema non è AES, AES-ECB è già di per sé vulnerabile alla cifratura deterministica di blocchi identici (si vedono i ciphertext ripetuti nei round 3/7/11), ma qui il punto centrale è ancora più sottile: **cifrare i dati non basta se il sistema rivela informazioni strutturali sulle risposte**.