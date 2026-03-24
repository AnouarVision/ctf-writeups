# Follow the rainbow

**Competition:** ITSCyberGame
**Category:** SSH
**Connection:** `sfide.itscybergame.it:<port_number>`

---

## Description

> Follow the rainbow and it will lead you to the flag. Connect via SSH with ITSCyberGame:rainbow.

Log in to an SSH server using the provided credentials. The goal is to find the flag by following the "rainbow".

---

## Solution

### 1. SSH connection

```bash
ssh -p <port_number> ITSCyberGame@sfide.itscybergame.it
# password: rainbow
```

The home directory is essentially empty:

```bash
ITSCyberGame@5729c66040d4:~$ ls -la
total 28
drwxr-x--- 1 ITSCyberGame ITSCyberGame 4096 .
drwxr-xr-x 1 root         root         4096 ..
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  220 .bash_logout
-rw-r--r-- 1 ITSCyberGame ITSCyberGame 3989 .bashrc
drwx------ 2 ITSCyberGame ITSCyberGame 4096 .cache
-rw-r--r-- 1 ITSCyberGame ITSCyberGame  807 .profile
```

### 2. Inspect `.bashrc`

At the end of `.bashrc` there is a custom function:

```bash
prompt_color() {
  color_code=$(/usr/local/bin/color-changer color 2>/dev/null || echo "\[\033[38;5;196m\]")
  PS1="${color_code}\u@\h:\w\$ \[\033[0m\]"
}
PROMPT_COMMAND="prompt_color"
export PROMPT_COMMAND
```

The prompt changes color on every command by calling `/usr/local/bin/color-changer color` — this is the "rainbow".

### 3. Inspect the binary

```bash
ls -la /usr/local/bin/color-changer
# -rwxr-xr-x 1 root root 706768 Feb  4 12:06 /usr/local/bin/color-changer
```

`color-changer` is a custom root-owned binary. Running it with `--help` shows:

```bash
/usr/local/bin/color-changer
/usr/local/bin/color-changer list
/usr/local/bin/color-changer next
flag{...}
```

The flag is printed directly in the binary's help output.

---

## Flag

```
flag{...}
```

---

## Conclusion

The "rainbow" was the `/usr/local/bin/color-changer` binary invoked by `PROMPT_COMMAND` in `.bashrc`. Inspecting the binary with `--help` printed the flag. The challenge highlights the importance of checking shell configuration and investigating non-standard binaries present on a system.
