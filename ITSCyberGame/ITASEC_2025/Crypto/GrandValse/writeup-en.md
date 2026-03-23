# Grand Valse

**Competition:** ITSCyberGame<br>
**Category:** Crypto<br>

---

## Description

> An old phone was found at the headquarters of a well-known hacker group. Among its messages, one seems particularly interesting: `843 3524 47 3524 9484 4 4678323 63 2`

---

## Solution

The title **"Grand Valse"** and the reference to an **old phone** are the key hints: this is about the **T9 text input method** (Predictive Text), used on mobile phones in the 1990s-2000s.

### Step 1 — Recognizing the cipher

On a T9 keypad, each number key corresponds to multiple letters:

```
2=ABC  3=DEF  4=GHI  5=JKL
6=MNO  7=PQRS 8=TUV  9=WXYZ
```

In **predictive** T9 mode, each digit sequence (separated by spaces) corresponds to a whole word, without needing to press the same key multiple times. The system guesses the word based on possible combinations.

### Step 2 — Decoding

Analyze each group separated by spaces:

| Sequence  | Possible Letters         | Word    |
|-----------|--------------------------|---------|
| `843`     | t/u/v + g/h/i + d/e/f    | **THE** |
| `3524`    | d/e/f + j/k/l + a/b/c + g/h/i | **FLAG** |
| `47`      | g/h/i + p/q/r/s          | **IS**  |
| `3524`    | d/e/f + j/k/l + a/b/c + g/h/i | **FLAG** |
| `9484`    | w/x/y/z + g/h/i + t/u/v + g/h/i | **WITH** |
| `4`       | g/h/i                    | **4** *(single digit)* |
| `4678323` | i + n + s + t + e + a + d | **INSTEAD** |
| `63`      | m/n/o + d/e/f            | **OF**  |
| `2`       | a/b/c                    | **A**   |

The cleartext message is:

```
THE FLAG IS FLAG WITH 4 INSTEAD OF A
```

### Step 3 — Build the flag

The sentence is a literal instruction: take the word **FLAG** and replace the letter **A** with the number **4**:

```
FLAG → FL4G
```

---

## Flag

```
flag{...}
```
