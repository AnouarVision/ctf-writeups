# You Complete Me — CTF Write-up

## Description

> A new company has just unveiled its new product: an IoT keyboard!
> The main feature is a cloud autocompletion service: for every character you type on the keyboard, the server sends you a list of words that could complete what you are writing.
> A user typed all the characters of a word we are interested in, but of course they decided to encrypt all communication, so we expect that the messages cannot be decrypted.
> Can you recover the word that was typed?

---

## Protocol Analysis

Reading the `challenge.py` file, you can understand how the system works:

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

The flow is as follows:

1. The **client** sends a character encrypted with AES-ECB.
2. The **server** decrypts the character, updates the prefix, and returns all dictionary words that start with that prefix, also encrypted with AES-ECB.
3. This repeats until the user has typed the entire word.

---

## Vulnerability: side-channel on response size

At first glance, it seems impossible to recover the word: everything is encrypted with AES and we don't have the key.

However, there is a critical **information leakage**: the server encrypts the words but does not hide **how many** words it returns. Since the list shrinks with each character typed, the **number of words per round** depends deterministically on the prefix and thus on the plaintext characters.

This is a classic **side-channel attack**: we don't need to decrypt anything, because the information leaks through the *length of the response*.

---

## Extracting the pcap traffic

Analyzing the pcap with `dpkt`, you identify two TCP flows on loopback:

- **Client → Server** (port 54832 → 6000): 13 packets containing the encrypted characters.
- **Server → Client** (port 6000 → 54832): the lists of encrypted words, ending with `\nend\n`.

```
Client sends 13 encrypted characters (each is 32 hex chars = 16 byte AES block):
  [0]  ba230ba2c7a0190bd3fc1a6397462e19
  [1]  a2aa0d4635371ae029bff4f4ad772315
  [2]  453caa8dc602b776b94263ce187f3ee4
  [3]  62162a57eb11e2cab103c250895759c3
  [4]  f33cefec189ad8968d2b5d18bb4462d7
  [5]  f33cefec189ad8968d2b5d18bb4462d7  ← same ciphertext as [4]
  [6]  0c4f27de24f65e22b87bee65ca130c8f
  [7]  62162a57eb11e2cab103c250895759c3  ← same ciphertext as [3]
  [8]  991f4d3f3ed332d13a0ca417f592f62c
  [9]  9ed71db6defad585eaa5dc0cc173e45d
  [10] d7c41006035ffc41e66bc6113ade9c44
  [11] 62162a57eb11e2cab103c250895759c3  ← same ciphertext as [3]
  [12] 35d319445ae1001c9a4bde9136d9fad1
```

The server replies with a decreasing number of words for each round:

| Round | Words returned |
|-------|---------------|
| 0     | 3952          |
| 1     | 825           |
| 2     | 23            |
| 3     | 3             |
| 4     | 2             |
| 5     | 2             |
| 6     | 1             |
| 7–12  | 1             |

> **Note:** the same ciphertext in rounds 3, 7, 11 confirms that the character typed in those positions is identical, further plaintext information extracted for free from AES-ECB.

---

## Reconstructing the word

Knowing the number of words returned for each round, you can simulate `get_words_by_prefix` on `words.txt` and find for each position the ASCII character that leads to that exact count:

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

At each step there is only one candidate and the algorithm converges uniquely.

---

## Flag

```
flag{...}
```

---

## Conclusions

The real problem is not AES; AES-ECB is already vulnerable to deterministic encryption of identical blocks (you see repeated ciphertexts in rounds 3/7/11), but here the main point is even subtler: **encrypting data is not enough if the system reveals structural information about the responses**.
