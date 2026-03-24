from pwn import *
import re

HOST = "sfide.itscybergame.it"
PORT = <port_number>

PATTERN = r'(add|sub|mul)(?![a-zA-Z_])\((-?\d+),(-?\d+)\)'
FLAG_RE  = re.compile(r'flag\{[^}]+\}')

def compute(line):
    total = 0
    for op, x, y in re.findall(PATTERN, line):
        x, y = int(x), int(y)
        if op == 'add':
            total += x + y
        elif op == 'sub':
            total += x - y
        elif op == 'mul':
            total += x * y
    return total

conn = remote(HOST, PORT)

conn.recvuntil(b"Press Enter to start.")
conn.sendline(b"")

i = 0

while True:
    try:
        line = conn.recvline(timeout=5).decode(errors='replace').strip()
    except EOFError:
        log.warning("Connection closed by remote host.")
        break

    if not line:
        continue

    m = FLAG_RE.search(line)
    if m:
        print(f"\n FLAG: {m.group()}")
        break

    if any(kw in line.lower() for kw in ['wrong', 'invalid', 'binary ended']):
        print(f"\n>>> {line}")
        break

    i += 1
    result = compute(line)
    log.info(f"[{i:03d}] line={result:>8}")
    conn.sendline(str(result).encode())

try:
    rest = conn.recvall(timeout=3).decode(errors='replace').strip()
    if rest:
        m = FLAG_RE.search(rest)
        if m:
            print(f"\n FLAG: {m.group()}")
        else:
            print(f"\n>>> FINAL: {rest}")
except:
    pass

conn.close()
