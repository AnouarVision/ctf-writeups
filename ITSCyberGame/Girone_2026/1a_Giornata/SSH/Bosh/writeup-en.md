# Bosh

**Competition:** ITSCyberGame
**Category:** SSH
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> To access the machine via SSH use the user `ITSCyberGame` and password `ITSCyberGame` :)

---

## Solution

### Step 1 — SSH connection

```bash
ssh -p 17520 ITSCyberGame@sfide.itscybergame.it
# password: ITSCyberGame
```

### Step 2 — Initial reconnaissance

Some common commands behave oddly:

```bash
ITSCyberGame@aa2c28ad8dce:~$ ls        # shows a train animation
ITSCyberGame@aa2c28ad8dce:~$ ls -la    # shows a train animation
ITSCyberGame@aa2c28ad8dce:~$ cat /etc/passwd
rm: remove write-protected regular file '/etc/passwd'?
```

`cat` asks to *remove* the file instead of printing it. Something is wrong.

### Step 3 — Check aliases

List defined aliases:

```bash
ITSCyberGame@aa2c28ad8dce:~$ alias
alias cat='rm'
alias cd='hollywood'
alias find='sudo apt update && upgrade'
alias grep='cowsay'
alias ls='sl'
...
```

Several common commands are remapped to useless or destructive aliases:

| Command | Alias | Effect |
|---|---|---|
| `ls` | `sl` | Shows an animated train |
| `cat` | `rm` | Removes the file instead of reading it |
| `cd` | `hollywood` | Opens a fake terminal animation |
| `find` | `sudo apt update && upgrade` | Runs package updates |
| `grep` | `cowsay` | Prints text as a cow |

### Step 4 — Bypass using absolute paths

Aliases only apply to the short command names. Calling the absolute binary path executes the real program and ignores aliases:

```bash
ITSCyberGame@1697bd62f0e7:~$ /bin/ls -la
total 32
drwxr-x--- 1 ITSCyberGame ITSCyberGame 4096 Mar 23 22:16 .
drwxr-xr-x 1 root         root         4096 Feb  2 18:45 ..
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  220 Mar 31  2024 .bash_logout
-rw-r--r-- 1 ITSCyberGame ITSCyberGame 3913 Feb  2 18:45 .bashrc
drwx------ 2 ITSCyberGame ITSCyberGame 4096 Mar 23 22:16 .cache
-rw------- 1 ITSCyberGame ITSCyberGame   31 Mar 23 22:16 .flag.txt
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  807 Mar 31  2024 .profile
```

The flag file is a hidden dotfile (`.flag.txt`) which does not appear with plain `ls`.

```bash
ITSCyberGame@1697bd62f0e7:~$ /bin/cat .flag.txt
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusions

Two lessons:
- Bash aliases apply only to short command names; using absolute paths like `/bin/ls` or `/bin/cat` bypasses aliases. Alternatively, `unalias cat ls find` restores commands in the current session.
- Hidden files (dotfiles) are not listed by `ls` without the `-a`/`-la` flag; check for them when hunting for flags.