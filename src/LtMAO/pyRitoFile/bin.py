from io import BytesIO
from .stream import BinStream
from .ermmm import FNV1a
from enum import IntEnum


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

class BINType(IntEnum):
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

class BINHelper:
    size_offsets = []
    legacy_read = False

    @staticmethod
    def fix_type(bin_type):
        if BINHelper.legacy_read:
            if bin_type >= 129:
                bin_type += 1
        return BINType(bin_type)

    @staticmethod
    def find_item(*, items=[], compare_func=None, return_func=None):
        if compare_func != None and len(items) > 0:
            for item in items:
                if compare_func(item):
                    if return_func != None:
                        return return_func(item)
                    else:
                        return item
        return None
    
    @staticmethod
    def find_items(*, items=[], compare_func=None):
        result = []
        if compare_func != None and len(items) > 0:
            for item in items:
                if compare_func(item):
                    result.append(item)
        return result
    
    # read related stuffs
    read_value_dict = {
        BINType.Empty:      lambda bs: bs.read_u16(3),
        BINType.Bool:       lambda bs: bs.read_b()[0],
        BINType.I8:         lambda bs: bs.read_i8()[0],
        BINType.U8:         lambda bs: bs.read_u8()[0],
        BINType.I16:        lambda bs: bs.read_i16()[0],
        BINType.U16:        lambda bs: bs.read_u16()[0],
        BINType.I32:        lambda bs: bs.read_i32()[0],
        BINType.U32:        lambda bs: bs.read_u32()[0],
        BINType.I64:        lambda bs: bs.read_i64()[0],
        BINType.U64:        lambda bs: bs.read_u64()[0],
        BINType.F32:        lambda bs: bs.read_f32()[0],
        BINType.Vec2:       lambda bs: bs.read_vec2()[0],
        BINType.Vec3:       lambda bs: bs.read_vec3()[0],
        BINType.Vec4:       lambda bs: bs.read_vec4()[0],
        BINType.Mtx4:       lambda bs: bs.read_mtx4()[0],
        BINType.RGBA:       lambda bs: bs.read_u8(4),
        BINType.String:     lambda bs: bs.read_s_sized16(encoding='utf-8')[0],
        BINType.Hash:       lambda bs: hash_to_hex(bs.read_u32()[0]),
        BINType.File:       lambda bs: bs.read_u64()[0],
        BINType.Pointer:    lambda bs: BINHelper.read_pointer_or_embed(bs, BINField(type=BINType.Pointer)),
        BINType.Embed:      lambda bs: BINHelper.read_pointer_or_embed(bs, BINField(type=BINType.Embed)),
        BINType.Link:       lambda bs: hash_to_hex(bs.read_u32()[0]),
        BINType.Flag:       lambda bs: bs.read_u8()[0],
    }

    @staticmethod
    def read_value(bs, value_type):
        return BINHelper.read_value_dict[value_type](bs)

    @staticmethod
    def read_basic(bs, field):
        field.data = BINHelper.read_value(bs, field.type)
        return field

    @staticmethod
    def read_list_or_list2(bs, field):
        field.value_type = BINHelper.fix_type(bs.read_u8()[0])
        bs.pad(4)  # size
        count, = bs.read_u32()
        field.data = [
            BINHelper.read_value(bs, field.value_type)
            for i in range(count)
        ]
        return field
        
    @staticmethod
    def read_pointer_or_embed(bs, field):
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
        return field
    
    @staticmethod
    def read_option(bs, field):
        field.value_type = BINHelper.fix_type(bs.read_u8()[0])
        count, = bs.read_u8()
        if count != 0:
            field.data = BINHelper.read_value(bs, field.value_type)
        else:
            field.data = None
        return field

    @staticmethod
    def read_map(bs, field):
        field.key_type = BINHelper.fix_type(bs.read_u8()[0])
        field.value_type = BINHelper.fix_type(bs.read_u8()[0])
        bs.pad(4)  # size
        count, = bs.read_u32()
        field.data = {
            BINHelper.read_value(bs, field.key_type): BINHelper.read_value(bs, field.value_type)
            for i in range(count)
        }
        return field
    
    read_field_dict = {
        field_type:         lambda bs, field: BINHelper.read_basic(bs, field) 
        for field_type in read_value_dict
    }
    read_field_dict.update({
        BINType.List:       lambda bs, field: BINHelper.read_list_or_list2(bs, field),
        BINType.List2:      lambda bs, field: BINHelper.read_list_or_list2(bs, field),
        BINType.Pointer:    lambda bs, field: BINHelper.read_pointer_or_embed(bs, field),
        BINType.Embed:      lambda bs, field: BINHelper.read_pointer_or_embed(bs, field),
        BINType.Option:     lambda bs, field: BINHelper.read_option(bs, field),
        BINType.Map:        lambda bs, field: BINHelper.read_map(bs, field)
    })

    @staticmethod
    def read_field(bs):
        field = BINField(
            hash=hash_to_hex(bs.read_u32()[0]),
            type=BINHelper.fix_type(bs.read_u8()[0])
        )
        return BINHelper.read_field_dict[field.type](bs, field)

    # write related stuffs
    write_value_dict = {
        BINType.Empty:          lambda bs, value: (bs.write_u16(*value), 0),
        BINType.Bool:           lambda bs, value: (bs.write_b(value), 1),
        BINType.I8:             lambda bs, value: (bs.write_i8(value), 1),
        BINType.U8:             lambda bs, value: (bs.write_u8(value), 1),
        BINType.I16:            lambda bs, value: (bs.write_i16(value), 2),
        BINType.U16:            lambda bs, value: (bs.write_u16(value), 2),
        BINType.I32:            lambda bs, value: (bs.write_i32(value), 4),
        BINType.U32:            lambda bs, value: (bs.write_u32(value), 4),
        BINType.I64:            lambda bs, value: (bs.write_i64(value), 8),
        BINType.U64:            lambda bs, value: (bs.write_u64(value), 8),
        BINType.F32:            lambda bs, value: (bs.write_f32(value), 4),
        BINType.Vec2:           lambda bs, value: (bs.write_vec2(value), 8),
        BINType.Vec3:           lambda bs, value: (bs.write_vec3(value), 12),
        BINType.Vec4:           lambda bs, value: (bs.write_vec4(value), 16),
        BINType.Mtx4:           lambda bs, value: (bs.write_mtx4(value), 64),
        BINType.RGBA:           lambda bs, value: (bs.write_u8(*value), 4),
        BINType.String:         lambda bs, value: (bs.write_s_sized16(value, encoding='utf-8'), len(value.encode('utf-8'))+2),
        BINType.Hash:           lambda bs, value: (bs.write_u32(name_or_hex_to_hash(value)), 4),
        BINType.File:           lambda bs, value: (bs.write_u64(value), 8),
        BINType.Pointer:        lambda bs, value: BINHelper.write_pointer_or_embed(bs, value),
        BINType.Embed:          lambda bs, value: BINHelper.write_pointer_or_embed(bs, value),
        BINType.Link:           lambda bs, value: (bs.write_u32(name_or_hex_to_hash(value)), 4),
        BINType.Flag:           lambda bs, value: (bs.write_u8(value), 1),
    }

    @staticmethod
    def write_value(bs, value, value_type, header_size):
        size = BINHelper.write_value_dict[value_type](bs, value)[1]
        return size+5 if header_size else size
    
    @staticmethod
    def write_basic(bs, field):
        return None, BINHelper.write_value(bs, field.data, field.type, header_size=False)

    @staticmethod
    def write_list_or_list2(bs, field):
        size = 0
        bs.write_u8(field.value_type.value)

        return_offset = bs.tell()
        bs.write_u32(0)  # values size
        size += 1 + 4

        content_size = 4
        bs.write_u32(len(field.data))
        for value in field.data:
            content_size += BINHelper.write_value(bs,
                                                    value, field.value_type, header_size=False)
        BINHelper.size_offsets.append((return_offset, content_size))

        size += content_size
        return None, size

    @staticmethod
    def write_pointer_or_embed(bs, field):
        size = 0
        if field.hash_type == '00000000':
            bs.write_u32(0)
            size += 4
        else:
            bs.write_u32(name_or_hex_to_hash(field.hash_type))
            size += 4

            return_offset = bs.tell()
            bs.write_u32(0)  # size
            size += 4

            content_size = 2
            bs.write_u16(len(field.data))
            for value in field.data:
                content_size += BINHelper.write_field(
                    bs, value, header_size=True)
            BINHelper.size_offsets.append((return_offset, content_size))

            size += content_size
        return None, size
    
    @staticmethod
    def write_option(bs, field):
        size = 0
        bs.write_u8(field.value_type.value)
        count = 0 if field.data == None else 1
        bs.write_u8(count)
        size += 1 + 1
        if count != 0:
            size += BINHelper.write_value(bs, field.data, field.value_type, header_size=False)
        return None, size
    
    @staticmethod
    def write_map(bs, field):
        size = 0
        bs.write_u8(
            field.key_type.value,
            field.value_type.value
        )

        return_offset = bs.tell()
        bs.write_u32(0)  # size
        size += 1+1+4

        content_size = 4
        bs.write_u32(len(field.data))
        for key, value in field.data.items():
            content_size += BINHelper.write_value(bs,
                                                    key, field.key_type, header_size=False)
            content_size += BINHelper.write_value(bs,
                                                    value, field.value_type, header_size=False)
        BINHelper.size_offsets.append((return_offset, content_size))

        size += content_size
        return None, size
    
    write_field_dict = {
        field_type:         lambda bs, field: BINHelper.write_basic(bs, field) 
        for field_type in write_value_dict
    }
    write_field_dict.update({
        BINType.List:       lambda bs, field: BINHelper.write_list_or_list2(bs, field),
        BINType.List2:      lambda bs, field: BINHelper.write_list_or_list2(bs, field),
        BINType.Pointer:    lambda bs, field: BINHelper.write_pointer_or_embed(bs, field),
        BINType.Embed:      lambda bs, field: BINHelper.write_pointer_or_embed(bs, field),
        BINType.Option:     lambda bs, field: BINHelper.write_option(bs, field),
        BINType.Map:        lambda bs, field: BINHelper.write_map(bs, field)
    })

    @staticmethod
    def write_field(bs, field, header_size):
        bs.write_u32(name_or_hex_to_hash(field.hash))
        bs.write_u8(field.type.value)
        size = BINHelper.write_field_dict[field.type](bs, field)[1]
        return size+5 if header_size else size


class BINField:
    __slots__ = ('hash', 'type', 'hash_type', 'key_type', 'value_type', 'data')

    def __init__(self, hash=None, type=None, hash_type=None, key_type=None, value_type=None, data=None):
        self.hash = hash
        self.type = type
        self.hash_type = hash_type
        self.key_type = key_type
        self.value_type = value_type
        self.data = data

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

    def __init__(self, hash=None, path=None, type=None, data=None):
        self.hash = hash
        self.path = path
        self.type = type
        self.data = data

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class BINEntry:
    __slots__ = ('hash', 'type', 'data')

    def __init__(self, hash=None, type=None, data=None):
        self.hash = hash
        self.type = type
        self.data = data

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class BIN:
    __slots__ = (
        'signature', 'version', 'is_patch',
        'links', 'entries', 'patches'
    )

    def __init__(self, signature=None, version=None, is_patch=False, links=None, entries=None, patches=None):
        self.signature = signature
        self.version = version
        self.is_patch = is_patch
        self.links = links
        self.entries = entries
        self.patches = patches

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
            self.signature, = bs.read_s(4, encoding='utf-8')
            if self.signature not in ('PROP', 'PTCH'):
                raise Exception(
                    f'pyRitoFile: Failed: Read BIN {path}: Wrong file signature: {self.signature}')
            if self.signature == 'PTCH':
                self.is_patch = True
                bs.pad(8)  # patch header
                magic, = bs.read_s(4, encoding='utf-8')
                if magic != 'PROP':
                    raise Exception(
                        f'pyRitoFile: Failed: Read BIN {path}: Missing PROP after PTCH signature.')
            self.version, = bs.read_u32()
            if self.version not in (1, 2, 3):
                raise Exception(
                    f'pyRitoFile: Failed: Read BIN {path}: Unsupported file version: {self.version}')
            # links
            if self.version >= 2:
                link_count, = bs.read_u32()
                self.links = [bs.read_s_sized16(encoding='utf-8')[0] for _ in range(link_count)]
            # entry_types + entries
            entry_count, = bs.read_u32()
            entry_types = bs.read_u32(entry_count)
            entry_offset = bs.tell()
            try:
                # read as new bin
                self.entries = [BINEntry() for i in range(entry_count)]
                for entry_id, entry in enumerate(self.entries):
                    entry.type = hash_to_hex(entry_types[entry_id])
                    bs.pad(4)  # size
                    entry.hash = hash_to_hex(bs.read_u32()[0])
                    field_count, = bs.read_u16()
                    entry.data = [BINHelper.read_field(
                        bs) for i in range(field_count)]
            except ValueError:
                # legacy bin, fall back
                bs.seek(entry_offset)
                BINHelper.legacy_read = True
                self.entries = [BINEntry() for i in range(entry_count)]
                for entry_id, entry in enumerate(self.entries):
                    entry.type = hash_to_hex(entry_types[entry_id])
                    bs.pad(4)  # size
                    entry.hash = hash_to_hex(bs.read_u32()[0])
                    field_count, = bs.read_u16()
                    entry.data = [BINHelper.read_field(
                        bs) for i in range(field_count)]
                BINHelper.legacy_read = False
            except Exception as e:
                # raise any other errors
                raise e
            # patches
            if self.is_patch and self.version >= 3:
                patch_count, = bs.read_u32()
                self.patches = [BINPatch() for i in range(patch_count)]
                for patch in self.patches:
                    patch.hash = hash_to_hex(bs.read_u32()[0])
                    bs.pad(4)  # size
                    patch.type = BINHelper.fix_type(bs.read_u8()[0])
                    patch.path, = bs.read_s_sized16(encoding='utf-8')
                    patch.data = BINHelper.read_value(bs, patch.type)

    def write(self, path, raw=None):
        with self.stream(path, 'wb', raw) as bs:
            # header
            if self.is_patch:
                bs.write_s('PTCH', encoding='utf-8')
                bs.write_u32(1, 0)  # patch header
            bs.write_s('PROP', encoding='utf-8')
            bs.write_u32(3)  # version
            # links
            bs.write_u32(len(self.links))
            for link in self.links:
                bs.write_s_sized16(link, encoding='utf-8')
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
                    bs.write_s_sized16(patch.path, encoding='utf-8')
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
                if value.hash_type != '00000000':
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
                if field.hash_type != '00000000':
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
