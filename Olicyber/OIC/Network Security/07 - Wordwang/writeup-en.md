# WordWang
**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** `capture.pcap`

---

## Description

> After the spectacular success of NumberWang, we're back with a new edition of the game loved by people aged 25 to 25 and a half: WordWang! Can you get the WordWang?
>
> `nc wordwang.challs.olicyber.it 10601`

---

## Solution

### Step 1 — Analyze the PCAP

The file `capture.pcap` contains a TCP session to the WordWang service. Extracting the payloads reconstructs the full conversation between client and server:

```
[SERVER] Welcome to Wordwang! The show where the words are wanged!
[SERVER] speech
[SERVER] provide

[CLIENT] speech       -> That's NOT wordwang!
[CLIENT] SPEECH       -> That's NOT wordwang!
[CLIENT] PROVIDE      -> That's NOT wordwang!
[CLIENT] provide?     -> That's NOT wordwang!
[CLIENT] SPEECH?      -> That's NOT wordwang!
[CLIENT] PROVIDE!     -> That's NOT wordwang!
[CLIENT] !PROVIDE?    -> That's NOT wordwang!
[CLIENT] ?SPEECH!     -> That's wordwang! Here's the flag: [REDACTED]
```

### Step 2 — Identify the winning pattern

Analyzing the sequence of failed attempts and the winning attempt, the rule emerges:

| Attempt      | Result |
|--------------|--------|
| `speech`     | X      |
| `SPEECH`     | X      |
| `SPEECH?`    | X      |
| `PROVIDE!`   | X      |
| `!PROVIDE?`  | X      |
| `?SPEECH!`   | ✔      |

**The winning formula is: `?<UPPERCASE_WORD>!`**

- `?` as prefix
- Word in **UPPERCASE**
- `!` as suffix

### Step 3 — Exploit script

For a ready-to-use script that automates the solution, see the [`wordwang.py`](wordwang.py) file in the challenge folder.

### Step 4 — Run and get the flag

```
$ python3 wordwang.py
Found words: ['brother']
Sending: '?brother!\n'  -> "That's NOT wordwang!"
Sending: '?BROTHER!\n'  -> "That's wordwang! Here's the flag: flag{...}"
```

---

## Conclusions

1. **Network traffic analysis**: The PCAP file contained a full game session, allowing the correct pattern to be reconstructed by trial and error, without blind brute-forcing the live service.

2. **Hidden pattern**: The `?<WORD>!` rule is not documented by the service — the only way to discover it is to observe the captured session and systematically compare failed attempts with the winning one.

3. **Automation required**: Since the word changes with every connection, a manual solution is not practical. The script must dynamically read the word and apply the correct pattern automatically.
