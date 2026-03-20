import struct

with open('net2.pcap', 'rb') as f:
    f.read(24)
    pkts = []
    while True:
        rec = f.read(16)
        if len(rec) < 16:
            break
        _, _, incl_len, _ = struct.unpack('<IIII', rec)
        data = f.read(incl_len)
        pkts.append(data)

chars = []
for p in pkts:
    if len(p) >= 14:
        eth_type = struct.unpack('>H', p[12:14])[0]
        if eth_type == 0xFFFF:
            chars.append(chr(p[0]))

print(''.join(chars))
