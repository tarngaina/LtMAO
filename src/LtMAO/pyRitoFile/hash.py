
def Elf(s):
    h = 0
    for c in s.lower():
        h = (h << 4) + ord(c)
        t = (h & 0xF0000000)
        if t != 0:
            h ^= (t >> 24)
        h &= ~t
    return h


def FNV1a(s):
    h = 0x811c9dc5
    for b in s.encode('ascii').lower():
        h = ((h ^ b) * 0x01000193) % 0x100000000
    return h
