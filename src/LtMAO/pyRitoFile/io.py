from struct import Struct
from ..pyRitoFile.structs import Vector, Quaternion, Matrix4


class BinStream:
    def __init__(self, f):
        self.stream = f

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # stream
    def tell(self):
        return self.stream.tell()

    def seek(self, pos, mode=0):
        self.stream.seek(pos, mode)

    def pad(self, length):
        self.stream.seek(length, 1)

    def end(self):
        return_offset = self.stream.tell()
        self.stream.seek(0, 2)
        e = self.stream.tell()
        self.stream.seek(return_offset)
        return e

    def close(self):
        self.stream.close()

    def raw(self):
        self.seek(0)
        return self.stream.read()

    # read

    def read_fmt(self, fmt, fmt_size):
        return Struct(fmt).unpack(self.stream.read(fmt_size))

    def read(self, length):
        return self.stream.read(length)

    def read_b(self, count=1):
        return Struct(f'<{count}?').unpack(self.stream.read(count))

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

    def read_i64(self, count=1):
        return Struct(f'<{count}q').unpack(self.stream.read(count*8))

    def read_u64(self, count=1):
        return Struct(f'<{count}Q').unpack(self.stream.read(count*8))

    def read_f32(self, count=1):
        return Struct(f'<{count}f').unpack(self.stream.read(count*4))

    def read_vec2(self, count=1):
        floats = Struct(f'<{count*2}f').unpack(self.stream.read(count*8))
        return [Vector(floats[i], floats[i+1]) for i in range(0, len(floats), 2)]

    def read_vec3(self, count=1):
        floats = Struct(f'<{count*3}f').unpack(self.stream.read(count*12))
        return [Vector(floats[i], floats[i+1], floats[i+2]) for i in range(0, len(floats), 3)]

    def read_vec4(self, count=1):
        floats = Struct(f'<{count*4}f').unpack(self.stream.read(count*16))
        return [Vector(floats[i], floats[i+1], floats[i+2], floats[i+3]) for i in range(0, len(floats), 4)]

    def read_quat(self, count=1):
        floats = Struct(f'<{count*4}f').unpack(self.stream.read(count*16))
        return [Quaternion(floats[i], floats[i+1], floats[i+2], floats[i+3]) for i in range(0, len(floats), 4)]

    def read_mtx4(self):
        return Matrix4(*Struct(f'16f').unpack(self.stream.read(64))),

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

    # write

    def write_fmt(self, fmt, *values):
        self.stream.write(Struct(fmt).pack(*values))

    def write(self, values):
        self.stream.write(values)

    def write_b(self, *values):
        self.stream.write(Struct(f'<{len(values)}?').pack(*values))

    def write_i8(self, *values):
        self.stream.write(Struct(f'<{len(values)}b').pack(*values))

    def write_u8(self, *values):
        self.stream.write(Struct(f'<{len(values)}B').pack(*values))

    def write_i16(self, *values):
        self.stream.write(Struct(f'<{len(values)}h').pack(*values))

    def write_u16(self, *values):
        self.stream.write(Struct(f'<{len(values)}H').pack(*values))

    def write_i32(self, *values):
        self.stream.write(Struct(f'<{len(values)}i').pack(*values))

    def write_u32(self, *values):
        self.stream.write(Struct(f'<{len(values)}I').pack(*values))

    def write_i64(self, *values):
        self.stream.write(Struct(f'<{len(values)}q').pack(*values))

    def write_u64(self, *values):
        self.stream.write(Struct(f'<{len(values)}Q').pack(*values))

    def write_f32(self, *values):
        self.stream.write(Struct(f'<{len(values)}f').pack(*values))

    def write_vec2(self, *values):
        floats = [f for vec in values for f in vec]
        self.stream.write(Struct(f'<{len(floats)}f').pack(*floats))

    def write_vec3(self, *values):
        floats = [f for vec in values for f in vec]
        self.stream.write(Struct(f'<{len(floats)}f').pack(*floats))

    def write_vec4(self, *values):
        floats = [f for vec in values for f in vec]
        self.stream.write(Struct(f'<{len(floats)}f').pack(*floats))

    def write_quat(self, *values):
        floats = [f for quat in values for f in quat]
        self.stream.write(Struct(f'<{len(floats)}f').pack(*floats))

    def write_mtx4(self, mtx4):
        floats = [f for f in mtx4]
        self.stream.write(Struct('16f').pack(*floats))

    def write_a(self, value):
        self.stream.write(value.encode('ascii'))

    def write_a_padded(self, value, length):
        if len(value) > length:
            value = value[:length]
        self.stream.write(value.encode('ascii') + b'\x00'*(length-len(value)))
