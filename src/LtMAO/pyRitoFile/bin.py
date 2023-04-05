from LtMAO.prettyUI.helper import Log
from LtMAO.pyRitoFile.io import BinStream


from enum import Enum
from json import dump, dumps, JSONEncoder


class BINEconder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        else:
            return JSONEncoder.default(self, obj)


class BINFieldType(Enum):
    # basic#
    Empty = 0
    Bool = 1
    I8 = 2
    U8 = 3
    I16 = 4
    U16 = 5
    I32 = 6
    U32 = 7
    I64 = 8
    U64 = 9
    Float = 10
    Vec2 = 11
    Vec3 = 12
    Vec4 = 13
    Matrix4 = 14
    Color = 15
    String = 16
    Hash = 17
    Path = 18
    # complex
    Container1 = 128
    Container2 = 129
    Struct = 130
    Embed = 131
    Link = 132
    Option = 133
    Map = 134
    Flag = 135

    def __json__(self):
        return self.name


class BINHelper:
    return_offsets = []

    @staticmethod
    def fix_type(field_type, legacy=False):
        if legacy:
            if field_type >= 129:
                field_type += 1
        return BINFieldType(field_type)

    @staticmethod
    def read_value(bs, field_type):
        if field_type == BINFieldType.Empty:
            return bs.read_u16(3)
        elif field_type == BINFieldType.Bool:
            return bs.read_b()[0]
        elif field_type == BINFieldType.I8:
            return bs.read_i8()[0]
        elif field_type == BINFieldType.U8:
            return bs.read_u8()[0]
        elif field_type == BINFieldType.I16:
            return bs.read_i16()[0]
        elif field_type == BINFieldType.U16:
            return bs.read_u16()[0]
        elif field_type == BINFieldType.I32:
            return bs.read_i32()[0]
        elif field_type == BINFieldType.U32:
            return bs.read_i32()[0]
        elif field_type == BINFieldType.I64:
            return bs.read_i64()[0]
        elif field_type == BINFieldType.U64:
            return bs.read_u64()[0]
        elif field_type == BINFieldType.Float:
            return bs.read_f()[0]
        elif field_type == BINFieldType.Vec2:
            return bs.read_vec2()[0]
        elif field_type == BINFieldType.Vec3:
            return bs.read_vec3()[0]
        elif field_type == BINFieldType.Vec4:
            return bs.read_vec4()[0]
        elif field_type == BINFieldType.Matrix4:
            return bs.read_f(16)
        elif field_type == BINFieldType.Color:
            return bs.read_u8(4)
        elif field_type == BINFieldType.String:
            size, = bs.read_u16()
            return bs.read_a(size)[0]
        elif field_type == BINFieldType.Hash:
            return hex(bs.read_u32()[0])
        elif field_type == BINFieldType.Path:
            return bs.read_u64()[0]
        elif field_type == BINFieldType.Struct or field_type == BINFieldType.Embed:
            field = BINField()
            hash_type, = bs.read_u32()
            if hash_type != 0:
                # bs.pad(4)  # size
                field.type = field_type
                field.size, = bs.read_u32()
                count, = bs.read_u16()
                field.values_type = hex(hash_type)
                field.values = [
                    BINHelper.read_field(bs)
                    for i in range(count)
                ]
            return field
        elif field_type == BINFieldType.Link:
            return bs.read_u32()[0]
        elif field_type == BINFieldType.Flag:
            return bs.read_u8()[0]

    @staticmethod
    def read_field(bs):
        field = BINField()
        field.hash = hex(bs.read_u32()[0])
        field.type, = bs.read_u8()
        field.type = BINHelper.fix_type(field.type)
        if field.type == BINFieldType.Container1 or field.type == BINFieldType.Container2:
            value_type = BINHelper.fix_type(bs.read_u8()[0])
            # bs.pad(4)  # size
            field.size, = bs.read_u32()
            count, = bs.read_u32()
            field.values_type = value_type
            field.values = [
                BINHelper.read_value(bs, value_type)
                for i in range(count)
            ]
        elif field.type == BINFieldType.Struct or field.type == BINFieldType.Embed:
            hash_type, = bs.read_u32()
            if hash_type != 0:
                # bs.pad(4)  # size
                field.size, = bs.read_u32()
                count, = bs.read_u16()
                field.values_type = hex(hash_type)
                field.values = [
                    BINHelper.read_field(bs)
                    for i in range(count)
                ]
        elif field.type == BINFieldType.Option:
            value_type = BINHelper.fix_type(bs.read_u8()[0])
            field.values_type = value_type
            count, = bs.read_u8()
            if count != 0:
                field.values = BINHelper.read_value(bs, value_type)
        elif field.type == BINFieldType.Map:
            key_type, value_type, = bs.read_u8(2)
            key_type, value_type = BINHelper.fix_type(
                key_type), BINHelper.fix_type(value_type)
            # bs.pad(4)  # size
            field.size, = bs.read_u32()
            count, = bs.read_u32()
            field.values_type = (key_type, value_type)
            field.values = {
                BINHelper.read_value(bs, key_type): BINHelper.read_value(bs, value_type)
                for i in range(count)
            }
        else:
            field.values = BINHelper.read_value(bs, field.type)
        return field

    @staticmethod
    def write_value(bs, field_type, values, header_size):
        size = 5 if header_size else 0
        if field_type == BINFieldType.Empty:
            bs.write_u16(*values)
            return size
        elif field_type == BINFieldType.Bool:
            bs.write_b(values)
            return size+1
        elif field_type == BINFieldType.I8:
            bs.write_i8(values)
            return size+1
        elif field_type == BINFieldType.U8:
            bs.write_u8(values)
            return size+1
        elif field_type == BINFieldType.I16:
            bs.write_i16(values)
            return size+2
        elif field_type == BINFieldType.U16:
            bs.write_u16(values)
            return size+2
        elif field_type == BINFieldType.I32:
            bs.write_i32(values)
            return size+4
        elif field_type == BINFieldType.U32:
            bs.write_u32(values)
            return size+4
        elif field_type == BINFieldType.I64:
            bs.write_i64(values)
            return size+8
        elif field_type == BINFieldType.U64:
            bs.write_u64(values)
            return size+8
        elif field_type == BINFieldType.Float:
            bs.write_f(values)
            return size+4
        elif field_type == BINFieldType.Vec2:
            bs.write_vec2(values)
            return size+8
        elif field_type == BINFieldType.Vec3:
            bs.write_vec3(values)
            return size+12
        elif field_type == BINFieldType.Vec4:
            bs.write_vec4(values)
            return size+16
        elif field_type == BINFieldType.Matrix4:
            bs.write_f(*values)
            return size+64
        elif field_type == BINFieldType.Color:
            bs.write_u8(*values)
            return size+4
        elif field_type == BINFieldType.String:
            bs.write_u16(len(values))
            bs.write_a(values)
            return size+len(values) + 2
        elif field_type == BINFieldType.Hash:
            bs.write_u32(int(values, 16))
            return size+4
        elif field_type == BINFieldType.Path:
            bs.write_u64(values)
            return size+8
        elif field_type == BINFieldType.Struct or field_type == BINFieldType.Embed:
            field = values
            if field.values == None:
                bs.write_u32(0)
                size += 4
            else:
                bs.write_u32(int(field.values_type, 16))
                size += 4

                # smart
                return_offset = bs.tell()
                bs.write_u32(0)
                size += 4
                content_size = 2
                bs.write_u16(len(field.values))
                for value in field.values:
                    content_size += BINHelper.write_field(
                        bs, value, header_size=True)

                BINHelper.return_offsets.append((return_offset, content_size))
                size += content_size
            return size

        elif field_type == BINFieldType.Link:
            bs.write_u32(value)
            return size+4
        elif field_type == BINFieldType.Flag:
            bs.write_u8(value)
            return size+1

    @staticmethod
    def write_field(bs, field, header_size):
        bs.write_u32(int(field.hash, 16))
        bs.write_u8(field.type.value)
        field.size = 5 if header_size else 0
        if field.type == BINFieldType.Container1 or field.type == BINFieldType.Container2:
            bs.write_u8(field.values_type.value)
            # smart
            return_offset = bs.tell()
            bs.write_u32(0)
            field.size += 1 + 4
            content_size = 4
            bs.write_u32(len(field.values))
            for value in field.values:
                content_size += BINHelper.write_value(bs,
                                                      field.values_type, value, header_size=False)

            BINHelper.return_offsets.append((return_offset, content_size))
            field.size += content_size
        elif field.type == BINFieldType.Struct or field.type == BINFieldType.Embed:
            if field.values == None:
                bs.write_u32(0)
                field.size += 4
            else:
                bs.write_u32(int(field.values_type, 16))
                field.size += 4
                # smart
                return_offset = bs.tell()
                bs.write_u32(0)
                field.size += 4
                content_size = 2
                bs.write_u16(len(field.values))
                for value in field.values:
                    content_size += BINHelper.write_field(
                        bs, value, header_size=True)

                BINHelper.return_offsets.append((return_offset, content_size))
                field.size += content_size
        elif field.type == BINFieldType.Option:

            bs.write_u8(field.values_type.value)
            count = 0 if field.values == None else 1
            bs.write_u8(count)
            field.size += 1 + 1
            if count != 0:
                field.size += BINHelper.write_value(bs,
                                                    field.values_type, field.values, header_size=False)
        elif field.type == BINFieldType.Map:
            bs.write_u8(
                field.values_type[0].value,
                field.values_type[1].value
            )
            # smart

            return_offset = bs.tell()
            bs.write_u32(0)
            field.size += 1+1+4
            content_size = 4
            bs.write_u32(len(field.values))
            for key, value in field.values.items():
                content_size += BINHelper.write_value(bs,
                                                      field.values_type[0], key, header_size=False)
                content_size += BINHelper.write_value(bs,
                                                      field.values_type[1], value, header_size=False)
            BINHelper.return_offsets.append((return_offset, content_size))
            field.size += content_size
        else:
            field.size += BINHelper.write_value(bs,
                                                field.type, field.values, header_size=False)
        return field.size


class BINField:
    def __init__(self):
        self.hash = None
        self.type = None
        self.values_type = None
        self.values = []

    def __json__(self):
        dic = vars(self)
        if self.values_type == None:
            dic.pop('values_type')
        return dic


class BINPatch:
    def __init__(self):
        self.hash = None
        self.path = None
        self.type = None
        self.values = None

    def __json__(self):
        return vars(self)


class BINEntry:
    def __init__(self):
        self.hash = None
        self.type = None
        self.fields = []

    def __json__(self):
        return vars(self)


class BIN:
    def __init__(self):
        self.signature = None
        self.version = None
        self.is_patch = False
        self.links = []
        self.entries = []
        self.patches = []

    def __json__(self):
        return vars(self)

    def read(self, path):
        Log.add(f'Running: Read {path}')
        with open(path, 'rb') as f:
            bs = BinStream(f)

            self.signature, = bs.read_a(4)
            if self.signature not in ('PROP', 'PTCH'):
                raise Exception(
                    f'Failed: Read {path}: Wrong file signature: {self.signature}')

            if self.signature == 'PTCH':
                self.is_patch = True
                bs.pad(8)  # patch header
                magic, = bs.read_a(4)
                if magic != 'PROP':
                    raise Exception(
                        f'Failed: Read {path}: Missing PROP after PTCH signature.')

            self.version, = bs.read_u32()
            if self.version not in (1, 2, 3):
                raise Exception(
                    f'Failed: Read {path}: Unsupported file version: {self.version}')

            if self.version >= 2:
                link_count, = bs.read_u32()
                self.links = [
                    bs.read_a(bs.read_i16()[0]) for i in range(link_count)]

            entry_count, = bs.read_u32()
            entry_types = bs.read_u32(entry_count)
            self.entries = [BINEntry() for i in range(entry_count)]
            for i in range(entry_count):
                entry = self.entries[i]

                entry.type = hex(entry_types[i])
                # bs.pad(4)  # length
                entry.size, = bs.read_u32()
                entry.hash = hex(bs.read_u32()[0])

                field_count, = bs.read_u16()
                entry.fields = [BINHelper.read_field(
                    bs) for j in range(field_count)]

            if self.is_patch and self.version >= 3:
                patch_count, = bs.read_u32()
                self.patches = [BINPatch() for i in range(patch_count)]
                for i in range(patch_count):
                    patch = self.patches[i]
                    patch.hash = hex(bs.read_u32()[0])
                    # bs.pad(4)  # size
                    patch.type = BINHelper.fix_type(bs.read_u8()[0])
                    patch.path, = bs.read_a(bs.read_u16()[0])
                    patch.values = BINHelper.read_value(bs, patch.type)

        Log.add(f'Done: Read {path}')

    def write(self, path):
        Log.add(f'Running: Write {path}')

        with open(path, 'wb+') as f:
            bs = BinStream(f)
            if self.is_patch:
                bs.write_a('PTCH')
                bs.write_u32(1, 0)  # patch header

            bs.write_a('PROP')
            bs.write_u32(3)  # version

            bs.write_u32(len(self.links))
            for link in self.links:
                bs.write_u16(len(link))
                bs.write_a(link)
            BINHelper.return_offsets = []
            bs.write_u32(len(self.entries))
            for entry in self.entries:
                bs.write_u32(int(entry.type, 16))
            for entry in self.entries:

                return_offset = bs.tell()
                bs.write_u32(0)  # size

                bs.write_u32(int(entry.hash, 16))
                bs.write_u16(len(entry.fields))

                entry.size = 4+2
                for field in entry.fields:
                    entry.size += BINHelper.write_field(
                        bs, field, header_size=True)

                BINHelper.return_offsets.append((return_offset, entry.size))

            for return_offset, size in BINHelper.return_offsets:
                bs.seek(return_offset)
                bs.write_u32(size)

        Log.add(f'Done: Write {path}')
