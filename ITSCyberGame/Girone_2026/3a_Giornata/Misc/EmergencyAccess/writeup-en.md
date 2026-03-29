# Emergency Access

**Competition:** ITSCyberGame<br>
**Category:** Misc<br>
**Service:** `sfide.itscybergame.it:<port_number>`

---

## Description

Legacy emergency terminal with a restrictive shell. The service exposes only a few documented commands, all blocked by a DEBUG mode. The goal is to enable the hidden maintenance mode and retrieve system logs containing the flag.

---

## Solution

### 1. Initial reconnaissance

Connect to the service via netcat:

```bash
ncat sfide.itscybergame.it <port_number>
```

Banner output:

```
--- Welcome to Emergency Terminal v1.0 ---
Type 'help' for available commands.
restricted-sh> help
Available commands: ls, exit, status
```

All documented commands return:

```
ERROR: Access denied. DEBUG mode required.
```

### 2. Enumerating hidden commands

The `help` command lists only `ls`, `exit`, and `status`, but the shell may accept undocumented commands. We fuzz common keywords related to debug/maintenance:

```bash
debug       # no response
debug on    # no response
enable debug # no response
maintenance  # no response
mode debug   # no response
DEBUG        # → ACTIVATION
```

### 3. Bypass: enabling maintenance mode

The `DEBUG` command (case-sensitive, uppercase) is not shown by `help` but is accepted by the shell:

```
restricted-sh> DEBUG
*** MAINTENANCE MODE ACTIVATED ***
Enter unlock code (Hint: 2+2*2):
```

### 4. Solving the challenge math

The system requests a numeric code. The hint `2+2*2` tests operator precedence:

```
2 + 2*2
= 2 + 4      # multiplication first (precedence)
= 6
```

```
restricted-sh> 6
Code accepted. Access to system logs granted.
Log 05/03/2026: Retrieving system flag... flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusions

Two chained weaknesses:

1. **Hidden command disclosure**: the restrictive shell does not display all accepted commands through `help`. Fuzzing common keywords (`DEBUG`, `MAINTENANCE`, `ADMIN`, etc.) is sufficient to discover undocumented hidden commands.

2. **Weak authentication**: the "unlock code" is a trivial arithmetic expression with standard operators. There is no real entropy and no lockout mechanism.

