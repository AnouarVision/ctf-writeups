# corrupted_code

**Competition:** ITSCyberGame
**Category:** Pwn
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> This annoying machine corrupted the RAM dump again. Can you help me recover my data from the recovery tool outputs? You will receive 100 corrupted strings containing several instances of `add(x,y)`, `sub(x,y)` and `mul(x,y)`; compute the result of each valid instruction while ignoring corrupted text and reply each round with the cumulative sum.

The server sends 100 noisy text lines. For each line, identify the valid instructions, compute their results and reply with the correct value for that round.

---

## Protocol analysis

On connection the server sends an example dump:

```
add(X,Y)*foradd( 34,56)=sub(12 ,34)defadd(X,Y)addd(90,12)add(52,45)mul(13,90)...
```

The server replies with `Invalid input! The correct answer was: 1524` if you send a wrong value.

Inspecting the example reveals validity rules:

| Instruction | Valid? | Reason |
|---|---:|---|
| `add(52,45)` | YES | Correct form |
| `addd(90,12)` | NO | Extra suffix (`addd`) |
| `add(X,Y)` | NO | Non-integer args |
| `add(12,34,56)` | NO | Three args |
| `add( 34,56)` | NO | Space inside arg |
| `add(56,78]` | NO | Wrong bracket |
| `fromsub(53,62)` | YES | Prefix allowed, name present |
| `sub(78_90)` | NO | Underscore in arg |

Key rule: the function name must not have literal suffixes (`addd`, `subb`) but arbitrary prefixes are allowed. Arguments must be pure integers with no spaces.

---

## Solution

### Correct regex

```python
PATTERN = r'(add|sub|mul)(?![a-zA-Z_])\((-?\d+),(-?\d+)\)'
```

- `(?![a-zA-Z_])`: negative lookahead to block suffixes like `addd`, `subb`
- `(-?\d+)`: pure integer, no spaces
- No lookbehind: `fromsub(...)` is valid

Verify on the example:

```python
# Matches: add(52,45), mul(13,90), sub(53,62), add(25,2),
#          sub(93,57), add(6,48), sub(60,64), mul(1,4),
#          add(70,54), sub(72,47)
# Total: 1524
```

### Script

The automation script is provided separately as `corrupted_code.py` in the challenge folder. Run it with:

```
python3 corrupted_code.py
```

The script connects to the server, applies the regex above and sends answers automatically; the full source is available in `corrupted_code.py` for inspection or modification.

---

## Flag

```
flag{...}
```

---

## Conclusions

The challenge tests robust parsing of noisy text. The critical point was identifying exactly which instructions are valid: the negative lookahead `(?![a-zA-Z_])` blocks literal suffixes (`addd`, `subb`) while prefixes such as `fromsub` or `computeadd` remain allowed since the base name appears. Arguments must be pure integers with no spaces or special characters.
