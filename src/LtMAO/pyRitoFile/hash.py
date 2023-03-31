
def Elf(s):
    s = s.lower()
    h = 0
    for c in s:
        h = (h << 4) + ord(c)
        t = (h & 0xF0000000)
        if t != 0:
            h ^= (t >> 24)
        h &= ~t
    return h
