#!/usr/bin/env python3
import ctypes
import struct
import numpy as np


def find_x_for_chunk(key32, magic64):
    k = ctypes.c_int64(ctypes.c_int32(key32).value).value
    magic = ctypes.c_int64(magic64 & 0xFFFFFFFFFFFFFFFF).value
    C1 = np.int64(ctypes.c_int64(0xffffffff21524111).value)
    C2 = np.int64(ctypes.c_int64(0xfffffffe42a48220).value)

    for base in range(0, 1 << 32, 1 << 16):
        raw = np.arange(base, min(base + (1 << 16), 1 << 32), dtype=np.uint32)
        xs = raw.view(np.int32).astype(np.int64)
        prods = xs * np.int64(k)
        r = (prods + C1) - ((prods * np.int64(2)) | C2) - np.int64(2)
        e = (r * np.int64(2) | np.int64(0x266f81bc)) - (r ^ np.int64(0x1337c0de))
        matches = np.where(e == np.int64(magic))[0]
        for idx in matches:
            yield int(raw[idx])


CHUNKS = [
    (0x11223344, 0x06eb47d7e7e064d5),
    (0x44332211, 0x1d2a0feb82421ea2),
    (0x22443311, 0x0cc765c69dd9f135),
    (0x33221144, 0x17a7500135cf0041),
    (0x11332244, 0x0669bb5b1f8b6641),
    (0x44223311, 0x1956622866f71079),
    (0x33112244, 0x12fd9cf80ace591d),
    (0x22331144, 0x07601425c0f457c5),
    (0x11442233, 0x00000008c420cce6),
]


def main():
    flag = b""
    for key, magic in CHUNKS:
        gen = find_x_for_chunk(key, magic)
        try:
            val = next(gen)
        except StopIteration:
            raise SystemExit(f"No solution found for chunk key=0x{key:08x}")
        flag += struct.pack('<I', val)

    print(flag.rstrip(b'\x00').decode())


if __name__ == '__main__':
    main()
