import struct

def _right_rotate(value, shift):
    return ((value >> shift) | (value << (32 - shift))) & 0xffffffff

def sha256(message: bytes) -> str:
    h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5
    ] * 8  # упрощение

    ml = len(message) * 8
    message += b'\x80'
    message += b'\x00' * ((56 - len(message) % 64) % 64)
    message += struct.pack('>Q', ml)

    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        w = list(struct.unpack('>16L', chunk)) + [0]*48

        for j in range(16, 64):
            s0 = _right_rotate(w[j-15], 7) ^ _right_rotate(w[j-15], 18) ^ (w[j-15] >> 3)
            s1 = _right_rotate(w[j-2], 17) ^ _right_rotate(w[j-2], 19) ^ (w[j-2] >> 10)
            w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xffffffff

        a,b,c,d,e,f,g,h0 = h

        for j in range(64):
            s1 = _right_rotate(e, 6) ^ _right_rotate(e, 11) ^ _right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h0 + s1 + ch + k[j] + w[j]) & 0xffffffff
            s0 = _right_rotate(a, 2) ^ _right_rotate(a, 13) ^ _right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & 0xffffffff

            h0 = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff

        h = [(x+y) & 0xffffffff for x,y in zip(h, [a,b,c,d,e,f,g,h0])]

    return ''.join(f'{x:08x}' for x in h)
