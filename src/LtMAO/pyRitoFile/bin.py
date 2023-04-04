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


class BINHelper():
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
        elif field_type == BINFieldType.Struct:
            hash_type, = bs.read_u32()
            if hash_type == 0:
                count = 0
            else:
                bs.pad(4)  # size
                count, = bs.read_u16()
            return [
                BINHelper.read_field(bs)
                for i in range(count)
            ]
        elif field_type == BINFieldType.Embed:
            hash_type, = bs.read_u32()
            if hash_type == 0:
                count = 0
            else:
                bs.pad(4)  # size
                count, = bs.read_u16()
            return [
                BINHelper.read_field(bs)
                for i in range(count)
            ]
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
            bs.pad(4)  # size
            count, = bs.read_u32()
            field.values_type = value_type
            field.values = [
                BINHelper.read_value(bs, value_type)
                for i in range(count)
            ]
        elif field.type == BINFieldType.Struct or field.type == BINFieldType.Embed:
            hash_type, = bs.read_u32()
            if hash_type == 0:
                count = 0
            else:
                bs.pad(4)  # size
                count, = bs.read_u16()
            field.values = [
                BINHelper.read_field(bs)
                for i in range(count)
            ]
        elif field.type == BINFieldType.Option:
            value_type = BINHelper.fix_type(bs.read_u8()[0])
            count, = bs.read_u8()
            field.values_type = value_type
            field.values = [
                None if count == 0 else BINHelper.read_value(
                    bs, value_type)
            ]
        elif field.type == BINFieldType.Map:
            key_type, value_type, = bs.read_u8(2)
            key_type, value_type = BINHelper.fix_type(
                key_type), BINHelper.fix_type(value_type)
            bs.pad(4)  # size
            count, = bs.read_u32()
            field.values_type = (key_type, value_type)
            field.values = {
                BINHelper.read_value(bs, key_type): BINHelper.read_value(bs, value_type)
                for i in range(count)
            }
        else:
            field.values = BINHelper.read_value(bs, field.type)

        return field


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
                        f'Failed: Read {path}: Missing PROB after PTCH signature.')

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
                bs.pad(4)  # length
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
                    bs.pad(4)  # size
                    patch.type = BINHelper.fix_type(bs.read_u8()[0])
                    patch.path, = bs.read_a(bs.read_u16()[0])
                    patch.values = BINHelper.read_value(bs, patch.type)

        Log.add(f'Done: Read {path}')
