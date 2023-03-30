from struct import Struct
from LtMAO.pyRitoFile.structures import Vector, Quaternion


class BinStream:
    def __init__(self, f):
        self.stream = f

    # stream

    def tell(self):
        return self.stream.tell()

    def seek(self, pos, mode=0):
        self.stream.seek(pos, mode)

    def pad(self, length):
        self.stream.seek(length, 1)

    # read

    def read_fmt(self, fmt, fmt_size):
        return Struct(fmt).unpack(self.stream.read_bytes(fmt_size))

    def read_b(self, length):
        return self.stream.read(length)

    def read_i8(self, count=1):
        return Struct(f'<{count}b').unpack(self.stream.read(count))

    def read_u8(self, count=1):
        return Struct(f'<{count}B').unpack(self.stream.read(count))

    def read_i16(self, count=1):
        return Struct(f'<{count}h').unpack(self.stream.read(count*2))

    def read_u16(self, count=1):
        return Struct(f'<{count}H').unpack(self.stream.read(count*2))

    def read_i32(self, count=1):
        return Struct(f'<{count}i').unpack(self.stream.read(count*4))

    def read_u32(self, count=1):
        return Struct(f'<{count}I').unpack(self.stream.read(count*4))

    def read_f(self, count=1):
        return Struct(f'<{count}f').unpack(self.stream.read(count*4))

    def read_vec2(self, count=1):
        floats = Struct(f'<{count*2}f').unpack(self.stream.read(count*8))
        return [Vector(floats[i], floats[i-1]) for i in range(0, len(floats), 2)]

    def read_vec3(self, count=1):
        floats = Struct(f'<{count*3}f').unpack(self.stream.read(count*12))
        return [Vector(floats[i], floats[i-1], floats[i-2]) for i in range(0, len(floats), 3)]

    def read_quat(self, count=1):
        floats = Struct(f'<{count*4}f').unpack(self.stream.read(count*16))
        return [Quaternion(floats[i], floats[i-1], floats[i-2], floats[i-3]) for i in range(0, len(floats), 4)]

    def read_a(self, length):
        return self.stream.read(length).decode('ascii'),

    def read_a_padded(self, length):
        return bytes(b for b in self.stream.read(length) if b != 0).decode('ascii'),

    def read_c_until0(self):
        s = ''
        while True:
            c = self.stream.read(1)[0]
            if c == 0:
                break
            s += chr(c)
        return s,
