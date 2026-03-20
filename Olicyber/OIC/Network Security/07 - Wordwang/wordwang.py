import socket
import time

HOST = 'wordwang.challs.olicyber.it'
PORT = 10601

def recv_all(s, timeout=2):
    s.settimeout(timeout)
    data = b''
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    return data

s = socket.socket()
s.connect((HOST, PORT))

time.sleep(0.5)
banner = recv_all(s, timeout=1.5)

lines = banner.decode(errors='replace').strip().split('\n')
words = [l.strip() for l in lines if l.strip() and 'Welcome' not in l and 'The show' not in l]

candidates = []
for w in words:
    candidates += [
        f'?{w}!',
        f'?{w.upper()}!',
        f'?{w.lower()}!',
        f'?{w.capitalize()}!',
    ]

for attempt in candidates:
    msg = attempt + '\n'
    s.sendall(msg.encode())
    time.sleep(0.3)
    resp = recv_all(s, timeout=1.5)
    resp_str = resp.decode(errors='replace').strip()
    if 'flag' in resp_str.lower() or ('wordwang' in resp_str.lower() and 'NOT' not in resp_str):
        print(f"FLAG: {resp_str}")
        break

s.close()
