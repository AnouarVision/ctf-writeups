# labyrinth_protocol

**Competition:** ITSCyberGame <br>
**Category:** Software <br>
**Service:** `./labyrinth_protocol <sync_key>`

---

## Description

> An old research-station terminal requests a synchronization key to access the system, but the disk containing the verification program is corrupted and it's practically impossible to recover the correct input by reading the source. It'll be hard to access the data our team needs...

The program expects a `sync key` argument. The disk is corrupted: you can't recover the key by reading the source. Goal: reconstruct the key by analyzing the verification logic in the binary.

---

## Solution

### 1. Initial reconnaissance

```
file labyrinth_protocol
# ELF 64-bit LSB pie executable, x86-64, stripped

checksec --file=labyrinth_protocol
# Partial RELRO | No Canary | NX enabled | PIE enabled | No Symbols
```

Relevant strings:

```
[!] Initializing Labyrinth Protocol...
[-] Usage: %s <sync_key>
[!] Validating sync key...
CHUNK %d: 0x%x
[+] ACCESS GRANTED!
[-] ACCESS DENIED
```

The program prints the key chunks and then calls a verification function.

### 2. Analysis of the verification function (0x14cc)

The function receives `(uint32_t x, uint32_t key, uint64_t magic)`.

It computes:

```c
int64_t f = (int64_t)(int32_t)x * (int64_t)(int32_t)key;
```

Algebraic proof: denoting `A = x&k`, `B = x&~k`, `C = ~x&k`:

```
f = A(A+B+C) + BC = A² + AB + AC + BC = (A+B)(A+C) = x·k
```

After the multiplication a chain of deterministic transforms is applied:

```python
C1 = 0xffffffff21524111  # signed: -3715923183
C2 = 0xfffffffe42a48220  # signed: -7831831008
val1 = f + C1
val2 = (f * 2) | C2
r = val1 - val2 - 2
e = (r * 2 | 0x266f81bc) - (r ^ 0x1337c0de)
# check: e == magic
```

### 3. Exploit

Each 32-bit chunk is independent: enumerate the full `[0, 2^32)` space using NumPy vectorized operations. A helper script [labyrinth_protocol.py](./labyrinth_protocol.py) in the same folder performs the enumeration and reconstructs the key.

Run:

```bash
python3 labyrinth_protocol.py
```

---

## Flag

```
flag{...}
```

---

## Conclusions

**Vulnerability / technique:** White-box reversing of a custom verification function.

**Lesson:** The boolean-looking expression `(x&k)*(x|k) + (x&~k)*(~x&k)` reduces algebraically to `x*k`. Recognizing this simplification turns an apparently hard problem (inverting a non-linear 64-bit function) into a simple 32-bit enumeration, feasible in seconds with NumPy.

Memory protections like NX and PIE were irrelevant: the challenge was purely logical/algorithmic, not a memory exploit.
