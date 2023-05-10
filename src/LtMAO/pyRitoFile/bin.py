from io import BytesIO
from LtMAO.pyRitoFile.io import BinStream
from LtMAO.pyRitoFile.hash import FNV1a
from enum import Enum
from json import JSONEncoder


def hash_to_hex(hash):
    return f'{hash:08x}'


def hex_to_hash(hex):
    return int(hex, 16)


def name_to_hash(name):
    return FNV1a(name)


def hex_to_name(hashtables, table_name, hash):
    return hashtables.get(table_name, {}).get(hash, hash)


def name_to_hex(name):
    return hash_to_hex(name_to_hash(name))


def name_or_hex_to_hash(value):
    try:
        return hex_to_hash(value)
    except:
        return name_to_hash(value)


class BINEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        else:
            return JSONEncoder.default(self, obj)


class BINHelper:
    size_offsets = []

    @staticmethod
    def fix_type(bin_type, legacy=False):
        if legacy:
            if bin_type >= 129:
                bin_type += 1
        return BINType(bin_type)

    @staticmethod
    def read_value(bs, value_type):
        value = None
        if value_type == BINType.Empty:
            value = bs.read_u16(3)
        elif value_type == BINType.Bool:
            value = bs.read_b()[0]
        elif value_type == BINType.I8:
            value = bs.read_i8()[0]
        elif value_type == BINType.U8:
            value = bs.read_u8()[0]
        elif value_type == BINType.I16:
            value = bs.read_i16()[0]
        elif value_type == BINType.U16:
            value = bs.read_u16()[0]
        elif value_type == BINType.I32:
            value = bs.read_i32()[0]
        elif value_type == BINType.U32:
            value = bs.read_i32()[0]
        elif value_type == BINType.I64:
            value = bs.read_i64()[0]
        elif value_type == BINType.U64:
            value = bs.read_u64()[0]
        elif value_type == BINType.F32:
            value = bs.read_f32()[0]
        elif value_type == BINType.Vec2:
            value = bs.read_vec2()[0]
        elif value_type == BINType.Vec3:
            value = bs.read_vec3()[0]
        elif value_type == BINType.Vec4:
            value = bs.read_vec4()[0]
        elif value_type == BINType.Mtx4:
            value = bs.read_mtx4()[0]
        elif value_type == BINType.RGBA:
            value = bs.read_u8(4)
        elif value_type == BINType.String:
            size, = bs.read_u16()
            value = bs.read_a(size)[0]
        elif value_type == BINType.Hash:
            value = hash_to_hex(bs.read_u32()[0])
        elif value_type == BINType.File:
            value = bs.read_u64()[0]
        elif value_type == BINType.Pointer or value_type == BINType.Embed:
            field = BINField()
            field.hash_type = hash_to_hex(bs.read_u32()[0])
            if field.hash_type != '00000000':
                field.type = value_type
                bs.pad(4)  # size
                count, = bs.read_u16()
                field.data = [
                    BINHelper.read_field(bs)
                    for i in range(count)
                ]
            value = field
        elif value_type == BINType.Link:
            value = hash_to_hex(bs.read_u32()[0])
        elif value_type == BINType.Flag:
            value = bs.read_u8()[0]
        return value

    @staticmethod
    def read_field(bs):
        field = BINField()
        field.hash = hash_to_hex(bs.read_u32()[0])
        field.type = BINHelper.fix_type(bs.read_u8()[0])
        if field.type == BINType.List or field.type == BINType.List2:
            field.value_type = BINHelper.fix_type(bs.read_u8()[0])
            bs.pad(4)  # size
            count, = bs.read_u32()
            field.data = [
                BINHelper.read_value(bs, field.value_type)
                for i in range(count)
            ]
        elif field.type == BINType.Pointer or field.type == BINType.Embed:
            field.hash_type = hash_to_hex(bs.read_u32()[0])
            if field.hash_type != '00000000':
                bs.pad(4)  # size
                count, = bs.read_u16()
                field.data = [
                    BINHelper.read_field(bs)
                    for i in range(count)
                ]
            else:
                field.data = None
        elif field.type == BINType.Option:
            field.value_type = BINHelper.fix_type(bs.read_u8()[0])
            count, = bs.read_u8()
            if count != 0:
                field.data = BINHelper.read_value(bs, field.value_type)
            else:
                field.data = None
        elif field.type == BINType.Map:
            field.key_type = BINHelper.fix_type(bs.read_u8()[0])
            field.value_type = BINHelper.fix_type(bs.read_u8()[0])
            bs.pad(4)  # size
            count, = bs.read_u32()
            field.data = {
                BINHelper.read_value(bs, field.key_type): BINHelper.read_value(bs, field.value_type)
                for i in range(count)
            }
        else:
            field.data = BINHelper.read_value(bs, field.type)
        return field

    @staticmethod
    def write_value(bs, value, value_type, header_size):
        value_size = 5 if header_size else 0
        if value_type == BINType.Empty:
            bs.write_u16(*value)
        elif value_type == BINType.Bool:
            bs.write_b(value)
            value_size += 1
        elif value_type == BINType.I8:
            bs.write_i8(value)
            value_size += 1
        elif value_type == BINType.U8:
            bs.write_u8(value)
            value_size += 1
        elif value_type == BINType.I16:
            bs.write_i16(value)
            value_size += 2
        elif value_type == BINType.U16:
            bs.write_u16(value)
            value_size += 2
        elif value_type == BINType.I32:
            bs.write_i32(value)
            value_size += 4
        elif value_type == BINType.U32:
            bs.write_u32(value)
            value_size += 4
        elif value_type == BINType.I64:
            bs.write_i64(value)
            value_size += 8
        elif value_type == BINType.U64:
            bs.write_u64(value)
            value_size += 8
        elif value_type == BINType.F32:
            bs.write_f32(value)
            value_size += 4
        elif value_type == BINType.Vec2:
            bs.write_vec2(value)
            value_size += 8
        elif value_type == BINType.Vec3:
            bs.write_vec3(value)
            value_size += 12
        elif value_type == BINType.Vec4:
            bs.write_vec4(value)
            value_size += 16
        elif value_type == BINType.Mtx4:
            bs.write_mtx4(value)
            value_size += 64
        elif value_type == BINType.RGBA:
            bs.write_u8(*value)
            value_size += 4
        elif value_type == BINType.String:
            size = len(value)
            bs.write_u16(size)
            bs.write_a(value)
            value_size += size + 2
        elif value_type == BINType.Hash:
            bs.write_u32(name_or_hex_to_hash(value))
            value_size += 4
        elif value_type == BINType.File:
            bs.write_u64(value)
            value_size += 8
        elif value_type == BINType.Pointer or value_type == BINType.Embed:
            field = value  # treat the value as BINField
            if field.data == None:
                bs.write_u32(0)
                value_size += 4
            else:
                bs.write_u32(name_or_hex_to_hash(field.hash_type))
                value_size += 4

                return_offset = bs.tell()
                bs.write_u32(0)  # size
                value_size += 4

                content_size = 2
                bs.write_u16(len(field.data))
                for value in field.data:
                    content_size += BINHelper.write_field(
                        bs, value, header_size=True)
                BINHelper.size_offsets.append((return_offset, content_size))

                value_size += content_size
        elif value_type == BINType.Link:
            bs.write_u32(name_or_hex_to_hash(value))
            value_size += 4
        elif value_type == BINType.Flag:
            bs.write_u8(value)
            value_size += 1
        return value_size

    @staticmethod
    def write_field(bs, field, header_size):
        field_size = 5 if header_size else 0
        bs.write_u32(name_or_hex_to_hash(field.hash))
        bs.write_u8(field.type.value)
        if field.type == BINType.List or field.type == BINType.List2:
            bs.write_u8(field.value_type.value)

            return_offset = bs.tell()
            bs.write_u32(0)  # values size
            field_size += 1 + 4

            content_size = 4
            bs.write_u32(len(field.data))
            for value in field.data:
                content_size += BINHelper.write_value(bs,
                                                      value, field.value_type, header_size=False)
            BINHelper.size_offsets.append((return_offset, content_size))

            field_size += content_size
        elif field.type == BINType.Pointer or field.type == BINType.Embed:
            if field.data == None:
                bs.write_u32(0)  # hash_type
                field_size += 4
            else:
                bs.write_u32(name_or_hex_to_hash(field.hash_type))
                field_size += 4

                return_offset = bs.tell()
                bs.write_u32(0)  # values size
                field_size += 4

                content_size = 2
                bs.write_u16(len(field.data))
                for value in field.data:
                    content_size += BINHelper.write_field(
                        bs, value, header_size=True)
                BINHelper.size_offsets.append((return_offset, content_size))

                field_size += content_size
        elif field.type == BINType.Option:
            bs.write_u8(field.value_type.value)
            count = 0 if field.data == None else 1
            bs.write_u8(count)
            field_size += 1 + 1
            if count != 0:
                field_size += BINHelper.write_value(bs,
                                                    field.data, field.value_type, header_size=False)
        elif field.type == BINType.Map:
            bs.write_u8(
                field.key_type.value,
                field.value_type.value
            )

            return_offset = bs.tell()
            bs.write_u32(0)  # size
            field_size += 1+1+4

            content_size = 4
            bs.write_u32(len(field.data))
            for key, value in field.data.items():
                content_size += BINHelper.write_value(bs,
                                                      key, field.key_type, header_size=False)
                content_size += BINHelper.write_value(bs,
                                                      value, field.value_type, header_size=False)
            BINHelper.size_offsets.append((return_offset, content_size))

            field_size += content_size
        else:
            field_size += BINHelper.write_value(bs,
                                                field.data, field.type, header_size=False)
        return field_size


class BINType(Enum):
    # basic
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
    F32 = 10
    Vec2 = 11
    Vec3 = 12
    Vec4 = 13
    Mtx4 = 14
    RGBA = 15
    String = 16
    Hash = 17
    File = 18
    # complex
    List = 128
    List2 = 129
    Pointer = 130
    Embed = 131
    Link = 132
    Option = 133
    Map = 134
    Flag = 135

    def __json__(self):
        return self.name


class BINField:
    __slots__ = ('hash', 'type', 'hash_type', 'key_type', 'value_type', 'data')

    def __init__(self):
        self.hash = None
        self.type = None
        self.hash_type = None
        self.key_type = None
        self.value_type = None
        self.data = []

    def __json__(self):
        dic = {key: getattr(self, key) for key in self.__slots__}
        if self.type == BINType.List or self.type == BINType.List2:
            dic.pop('key_type')
            dic.pop('hash_type')
        elif self.type == BINType.Pointer or self.type == BINType.Embed:
            dic.pop('key_type')
            dic.pop('value_type')
        elif self.type == BINType.Map:
            dic.pop('hash_type')
        else:
            dic.pop('key_type')
            dic.pop('hash_type')
            dic.pop('value_type')
        return dic


class BINPatch:
    __slots__ = ('hash', 'path', 'type', 'data')

    def __init__(self):
        self.hash = None
        self.path = None
        self.type = None
        self.data = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class BINEntry:
    __slots__ = ('hash', 'type', 'data')

    def __init__(self):
        self.hash = None
        self.type = None
        self.data = []

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class BIN:
    __slots__ = (
        'signature', 'version', 'is_patch',
        'links', 'entries', 'patches'
    )

    def __init__(self):
        self.signature = None
        self.version = None
        self.is_patch = False
        self.links = []
        self.entries = []
        self.patches = []

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def stream(self, path, mode, raw=None):
        if raw != None:
            if raw == True:  # the bool True value
                return BinStream(BytesIO())
            else:
                return BinStream(BytesIO(raw))
        return BinStream(open(path, mode))

    def read(self, path, raw=None):
        with self.stream(path, 'rb', raw) as bs:
            # header
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
            # links
            if self.version >= 2:
                link_count, = bs.read_u32()
                self.links = [
                    bs.read_a(bs.read_i16()[0])[0] for i in range(link_count)]
            # entry_types + entries
            entry_count, = bs.read_u32()
            entry_types = bs.read_u32(entry_count)
            self.entries = [BINEntry() for i in range(entry_count)]
            for i in range(entry_count):
                entry = self.entries[i]

                entry.type = hash_to_hex(entry_types[i])
                bs.pad(4)  # size
                entry.hash = hash_to_hex(bs.read_u32()[0])

                field_count, = bs.read_u16()
                entry.data = [BINHelper.read_field(
                    bs) for j in range(field_count)]
            # patches
            if self.is_patch and self.version >= 3:
                patch_count, = bs.read_u32()
                self.patches = [BINPatch() for i in range(patch_count)]
                for i in range(patch_count):
                    patch = self.patches[i]
                    patch.hash = hash_to_hex(bs.read_u32()[0])
                    bs.pad(4)  # size
                    patch.type = BINHelper.fix_type(bs.read_u8()[0])
                    patch.path, = bs.read_a(bs.read_u16()[0])
                    patch.data = BINHelper.read_value(bs, patch.type)

    def write(self, path, raw=None):
        with self.stream(path, 'wb', raw) as bs:
            # header
            if self.is_patch:
                bs.write_a('PTCH')
                bs.write_u32(1, 0)  # patch header
            bs.write_a('PROP')
            bs.write_u32(3)  # version
            # links
            bs.write_u32(len(self.links))
            for link in self.links:
                bs.write_u16(len(link))
                bs.write_a(link)
            # entry_types + entries
            bs.write_u32(len(self.entries))
            for entry in self.entries:
                bs.write_u32(name_or_hex_to_hash(entry.type))
            BINHelper.size_offsets = []  # this help to write sizes
            for entry in self.entries:
                return_offset = bs.tell()

                bs.write_u32(0)  # size
                entry_size = 4+2

                bs.write_u32(name_or_hex_to_hash(entry.hash))
                bs.write_u16(len(entry.data))
                for field in entry.data:
                    entry_size += BINHelper.write_field(
                        bs, field, header_size=True)
                BINHelper.size_offsets.append((return_offset, entry_size))
            # patches
            if self.is_patch:
                bs.write_u32(len(self.patches))
                for patch in self.patches:
                    bs.write_u32(name_or_hex_to_hash(path.hash))

                    return_offset = bs.tell()
                    bs.write_u32(0)  # size
                    patch_size = 1 + 2 + len(patch.path)

                    bs.write_u8(patch.type.value)
                    bs.write_u16(len(patch.path))
                    bs.write_a(patch.path)
                    patch_size += BINHelper.write_value(
                        bs, patch.type, header_size=False)
                    BINHelper.size_offsets.append(
                        (return_offset, patch_size))
            # jump around and write size
            for offset, size in BINHelper.size_offsets:
                bs.seek(offset)
                bs.write_u32(size)
            return bs.raw() if raw else None

    def un_hash(self, hashtables=None):
        if hashtables == None:
            return

        def un_hash_value(value, value_type):
            if value_type == BINType.Hash:
                return hex_to_name(hashtables, 'hashes.binhashes.txt', value)
            elif value_type == BINType.Link:
                return hex_to_name(hashtables, 'hashes.binentries.txt', value)
            elif value_type in (BINType.List, BINType.List2):
                value.data = [un_hash_value(v, value_type) for v in value.data]
            elif value_type in (BINType.Embed, BINType.Pointer):
                value.hash_type = hex_to_name(
                    hashtables, 'hashes.bintypes.txt',  value.hash_type)
                for f in value.data:
                    un_hash_field(f)
            return value

        def un_hash_field(field):
            field.hash = hex_to_name(
                hashtables, 'hashes.binfields.txt', field.hash)
            field.type = hex_to_name(
                hashtables, 'hashes.bintypes.txt', field.type)
            if field.type in (BINType.List, BINType.List2):
                field.value_type = hex_to_name(
                    hashtables, 'hashes.bintypes.txt', field.value_type)
                field.data = [un_hash_value(v, field.value_type)
                              for v in field.data]
            elif field.type in (BINType.Embed, BINType.Pointer):
                field.hash_type = hex_to_name(
                    hashtables, 'hashes.bintypes.txt', field.hash_type)
                for f in field.data:
                    un_hash_field(f)
            elif field.type == BINType.Map:
                field.key_type = hex_to_name(
                    hashtables, 'hashes.bintypes.txt', field.key_type)
                field.value_type = hex_to_name(
                    hashtables, 'hashes.bintypes.txt', field.value_type)
                field.data = {
                    un_hash_value(key, field.key_type): un_hash_value(value, field.value_type) for key, value in field.data.items()
                }
            else:
                field.data = un_hash_value(field.data, field.type)

        for entry in self.entries:
            entry.hash = hex_to_name(
                hashtables, 'hashes.binentries.txt', entry.hash)
            entry.type = hex_to_name(
                hashtables, 'hashes.bintypes.txt', entry.type)
            for field in entry.data:
                un_hash_field(field)
