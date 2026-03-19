#!/usr/bin/env python3
import socket
import time

HOST = "melody.challs.olicyber.it"
PORT = 10020

VALID = {
    2:  "0cce6bab87baa7031b69539ac1a211f202fc35cc8f3ac27fdb7e527527310f0e",
    23: "2a3a1630446304ab588ef90f32b8d3db88933f9737016e60df5cb3a2dca19b74",
    68: "23c90a60a0d2d24b53eca03ac2c4f4194c617f001fa1bf99b20cede152cc240f",
}

def try_connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((HOST, PORT))
        data = b""

        while b"NONCE" not in data:
            data += s.recv(1024)

        lines = data.decode(errors="replace").strip().splitlines()
        nonce = None
        for line in lines:
            if line.startswith("NONCE"):
                nonce = int(line.split()[1])
                break

        if nonce is None:
            return None, None

        if nonce not in VALID:
            return nonce, None

        response = VALID[nonce] + "\n"
        s.sendall(response.encode())

        result = b""
        try:
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                result += chunk
        except socket.timeout:
            pass

        return nonce, result.decode(errors="replace")


print("Replay attack started. Looking for nonce 2, 23 or 68...\n")

for attempt in range(1, 200):
    try:
        nonce, result = try_connect()

        if nonce is None:
            print(f"[{attempt:3d}] Nonce not received, retrying...")
            continue

        if result is None:
            print(f"[{attempt:3d}] NONCE={nonce:3d} -> unknown, retrying")
            time.sleep(0.3)
            continue

        print(f"[{attempt:3d}] NONCE={nonce:3d} -> MATCH! Response sent")
        print(f"       Server: {result.strip()}")

        if "FLAG" in result:
            print("\n[!] FLAG FOUND!")
            break

    except Exception as e:
        print(f"[{attempt:3d}] Error: {e}, retrying...")
        time.sleep(0.5)
