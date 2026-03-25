# Hawkins Lab

**Competition:** ITSCyberGame
**Category:** SSH
**File:** key2
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> Hey Dustin, it's Lucas: I found this private key to access a Hawkins lab server, but something's wrong with its contents... I think the lowercase letters got flipped upside-down...
>
> `pnsʇᴉu ɟɐ ɾoƃƃᴉuƃ ɐ ɥɐʍʞᴉus ɔou bnǝllɐ qopʎɔɐɯ ǝxʇɹɐ dǝɹ sodɹɐʌʌᴉʌǝuzɐ`

The theme is Stranger Things: decode an SSH key where lowercase characters were replaced by upside-down Unicode, connect to the server and find the hidden flag.

---

## Solution

### 1. Decode the hint

The hint text is written in upside-down characters. Decoding produces:

```
dustin fa jogging a hawkins con quella bodycam extra per sopravvivenza
```

### 2. Fix the SSH key

`key2` contains upside-down Unicode characters instead of lowercase ASCII. There are two substitution groups to handle:

- Special upside-down Unicode letters (e.g. `ɐ→a`, `ɔ→c`, `ǝ→e`, etc.)
- Pairs that map to each other (and are tricky because they are valid base64 chars): `n↔u`, `b↔q`, `p↔d` — these must be swapped, not ignored, otherwise the base64/key structure breaks.

Example fixer (concept):

```python
full_flip = {
	'ƃ': 'g', 'ǝ': 'e', 'ɐ': 'a', 'ɔ': 'c', 'ɟ': 'f',
	'ɥ': 'h', 'ᴉ': 'i', 'ɯ': 'm', 'ɹ': 'r', 'ɾ': 'j',
	'ʇ': 't', 'ʌ': 'v', 'ʍ': 'w', 'ʎ': 'y', 'ʞ': 'k',
	'n': 'u', 'u': 'n', 'b': 'q', 'q': 'b', 'p': 'd', 'd': 'p',
}

with open('key2','r',encoding='utf-8') as f:
	data = f.read()

fixed = ''.join(full_flip.get(ch, ch) for ch in data)
with open('key2_fixed','w') as f:
	f.write(fixed)
```

After fixing and saving `key2_fixed`, set permissions and connect:

```bash
chmod 600 key2_fixed
ssh -i key2_fixed -p <port_number> hawkins-lab@sfide.itscybergame.it
```

The server replies with `Welcome to the Upside Down` and all output appears upside-down.

### 3. Explore the host

List the home directory (output is upside-down; commands are typed normally). Files include themed documents and two binaries `gate` and `gate_cctv`.

Running `./gate` prints a friendly message and returns control. The text files are fictional lab documents; none immediately show the flag when visually scanned due to upside-down output.

### 4. Search for the flag

Instead of manually decoding output, search the filesystem for the flag pattern directly:

```bash
grep -r "flag{" ~
```

This finds the hidden file:

```
/home/hawkins-lab/.nuclear_password:flag{...}
```

The `.nuclear_password` hidden file contains the flag.

---

## Flag

```
flag{...}
```

---

## Conclusions

The challenge is about recognizing and reversing upside-down Unicode applied to an SSH private key. Important pitfalls:

- Some ASCII letters flip into each other (`n↔u`, `b↔q`, `p↔d`) and are valid base64 characters, they must be swapped correctly to avoid corrupting key structure.
- After fixing the key, the server's output remains upside-down; use recursive search (`grep -r`) to find the flag instead of relying on manual reading.