#!/usr/bin/env python3
import hmac
import hashlib
import random
import string
from datetime import datetime, timezone

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def sign(text, key):
    textAsBytes = bytes(text, encoding='ascii')
    keyAsBytes  = bytes(key, encoding='ascii')
    signature = hmac.new(keyAsBytes, textAsBytes, hashlib.sha256)
    return signature.hexdigest()

KNOWN_SIG = "8df8d5bb43380b88a569bc4e601dca18ad18077a22e23f27e3f9e30c0c1ee819"
uptime = 7036909
server_date_str = "Sun, 05 Apr 2026 21:04:21 GMT"

server_ts = datetime.strptime(server_date_str, "%a, %d %b %Y %H:%M:%S %Z")
server_ts = server_ts.replace(tzinfo=timezone.utc)
boot_ts = server_ts.timestamp() - uptime

for delta in range(-120, 121):
    ts = boot_ts + delta
    seed_str = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    random.seed(seed_str)
    key = get_random_string(32)
    sig = sign("not_admin", key)
    if sig == KNOWN_SIG:
        print(f"Seed: {seed_str}")
        print(f"Key: {key}")
        admin_sig = sign("admin", key)
        print(f"Admin signature: {admin_sig}")
        break
