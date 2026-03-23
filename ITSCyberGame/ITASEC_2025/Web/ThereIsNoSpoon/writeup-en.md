# There Is No Spoon

**Competition:** ITSCyberGame<br>
**Category:** Web<br>

---

## Description

> Neo received a secret message from the real world, but the Agents hid it in the code of the simulation. Only those who know where to look will find it.

---

## Solution

The title is already a hint: *"There Is No Spoon"*—don't look for the obvious. The page only shows an animated canvas with falling green characters and a generic message. The flag is not visible on screen.

### Step 1 — Inspect the Source

The first move in any web/misc challenge is to inspect the page source (`Ctrl+U` or DevTools). Scrolling down, you find a long hidden HTML comment:

```html
<!--
Neo, the answer you seek is hidden within the code.
The Matrix has many secrets, but only the true chosen one will find it.

filo di codice scorre nel buio,
luci verdi danzano in un flusso continuo.
aspetti risposte, cerchi un motivo,
guarda più a fondo, segui l'istinto.
{Il mondo si piega, il codice è chiave,
...
}Ora decidi: pillola o cammino?"
-->
```

The comment contains a 30-line poem. Some lines start with unusual characters: uppercase letters in the middle of a sentence, digits, underscores, and curly braces `{` `}`. This is suspicious.

### Step 2 — Read the Acrostic

Extracting the **first character of each line** of the poem reveals the flag:

```python
poem = """filo di codice scorre nel buio,
luci verdi danzano in un flusso continuo.
aspetti risposte, cerchi un motivo,
guarda più a fondo, segui l'istinto.
{Il mondo si piega, il codice è chiave,
...
}Ora decidi: pillola o cammino?"""

first_chars = [line[0] for line in poem.strip().split('\n')]
print(''.join(first_chars))
```

```
flag{...}
```

It's an **acrostic**: the flag is encoded vertically, hidden in the initials of each verse—a simple but effective steganographic technique, made invisible by the length of the text and the context.