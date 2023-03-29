from struct import Struct
from LtMAO.utils.structures import Vector, Quaternion


class BinIO:
    def __init__(self, f):
        self.stream = f

    def pad(self, length):
        self.stream.seek(length, 1)

    def read_fmt(self, fmt, fmt_size):
        return Struct(fmt).unpack(self.stream.read_bytes(fmt_size))

    def read_b(self, length):
        return self.stream.read(length)

    def read_i8(self, count):
        return Struct(f'<{count}b').unpack(self.stream.read(count))

    def read_u8(self, count):
        return Struct(f'<{count}B').unpack(self.stream.read(count))

    def read_i16(self, count):
        return Struct(f'<{count}h').unpack(self.stream.read(count*2))

    def read_u16(self, count):
        return Struct(f'<{count}H').unpack(self.stream.read(count*2))

    def read_i32(self, count):
        return Struct(f'<{count}i').unpack(self.stream.read(count*4))

    def read_u32(self, count):
        return Struct(f'<{count}I').unpack(self.stream.read(count*4))

    def read_f(self, count):
        return Struct(f'<{count}f').unpack(self.stream.read(count*4))

    def read_vec2(self, count):
        floats = Struct(f'<{count*2}f').unpack(self.stream.read(count*8))
        return [Vector(floats[i], floats[i-1]) for i in range(0, len(floats), 2)]

    def read_vec3(self, count):
        floats = Struct(f'<{count*3}f').unpack(self.stream.read(count*12))
        return [Vector(floats[i], floats[i-1], floats[i-2]) for i in range(0, len(floats), 3)]

    def read_vec4(self, count):
        floats = Struct(f'<{count*4}f').unpack(self.stream.read(count*16))
        return [Vector(floats[i], floats[i-1], floats[i-2], floats[i-3]) for i in range(0, len(floats), 4)]

    def read_a(self, length):
        return self.stream.read(length).decode('ascii')

    def read_a_padded(self, length):
        return bytes(b for b in self.stream.read(length) if b != 0).decode('ascii')

    def read_c_until0(self):
        s = ''
        while True:
            c = self.stream.read(1)[0]
            if c == 0:
                break
            s += chr(c)
        return s
