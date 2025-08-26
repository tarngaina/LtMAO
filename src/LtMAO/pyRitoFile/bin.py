from .stream import BytesStream
from .helper import FNV1a
from .wad import WADHasher
from enum import Enum

class BINType(Enum):
    # basic
    NONE = 0
    BOOL = 1
    I8 = 2
    U8 = 3
    I16 = 4
    U16 = 5
    I32 = 6
    U32 = 7
    I64 = 8
    U64 = 9
    F32 = 10
    VEC2 = 11
    VEC3 = 12
    VEC4 = 13
    MTX44 = 14
    RGBA = 15
    STRING = 16
    HASH = 17
    FILE = 18
    # complex
    LIST = 128
    LIST2 = 129
    POINTER = 130
    EMBED = 131
    LINK = 132
    OPTION = 133
    MAP = 134
    FLAG = 135

    def __json__(self):
        return self.name
    
    @staticmethod
    def fix(bs, bin_type):
        if bs.legacy_read:
            if bin_type >= 129:
                bin_type += 1
        return BINType(bin_type)


class BINHasher:
    HASHTABLE_NAMES = (
        'hashes.binentries.txt',
        'hashes.binhashes.txt',
        'hashes.bintypes.txt',
        'hashes.binfields.txt',
        'hashes.game.txt',
        'hashes.lcu.txt'
    )

    @staticmethod
    def hex_to_raw(hashtables, hex):
        for table_name in reversed(BINHasher.HASHTABLE_NAMES):
            if table_name in hashtables and hex in hashtables[table_name]:
                return hashtables[table_name][hex]
        return hex
    
    @staticmethod
    def raw_to_hex(raw):
        return f'{FNV1a(raw):08x}'

    @staticmethod
    def hash_to_hex(hash):
        return f'{hash:08x}'
    
    @staticmethod
    def is_hash(raw):
        try: 
            int(raw, 16)
            return True
        except:
            return False

    @staticmethod
    def raw_or_hex_to_hash(raw_or_hex):
        try:
            return int(raw_or_hex, 16)
        except:
            return FNV1a(raw_or_hex)
        
    @staticmethod
    def un_hash_value(hashtables, value, value_type):
        if value_type in (BINType.HASH, BINType.FILE, BINType.LINK):
            return BINHasher.hex_to_raw(hashtables, value)
        elif value_type in (BINType.LIST, BINType.LIST2):
            value.data = [BINHasher.un_hash_value(hashtables, v, value_type) for v in value.data]
        elif value_type in (BINType.EMBED, BINType.POINTER):
            if value.hash_type != '00000000':
                value.hash_type = BINHasher.hex_to_raw(hashtables, value.hash_type)
                for f in value.data:
                    BINHasher.un_hash_field(hashtables, f)
        return value

    @staticmethod
    def un_hash_field(hashtables, field):
        field.hash = BINHasher.hex_to_raw(hashtables, field.hash)
        field.type = BINHasher.hex_to_raw(hashtables, field.type)
        if field.type in (BINType.LIST, BINType.LIST2):
            field.data = [BINHasher.un_hash_value(hashtables, v, field.value_type)
                            for v in field.data]
        elif field.type in (BINType.EMBED, BINType.POINTER):
            if field.hash_type != '00000000':
                field.hash_type = BINHasher.hex_to_raw(hashtables, field.hash_type)
                for f in field.data:
                    BINHasher.un_hash_field(hashtables, f)
        elif field.type == BINType.MAP:
            field.data = {
                BINHasher.un_hash_value(hashtables, key, field.key_type): BINHasher.un_hash_value(hashtables, value, field.value_type) for key, value in field.data.items()
            }
        else:
            field.data = BINHasher.un_hash_value(hashtables, field.data, field.type)

    @staticmethod
    def un_hash_patch(hashtables, patch):
        patch.hash = BINHasher.hex_to_raw(hashtables, patch.hash)
        if patch.type in (BINType.LIST, BINType.LIST2):
            field = patch.data
            field.data = [BINHasher.un_hash_value(hashtables, v, field.value_type)
                            for v in field.data]
        elif patch.type in (BINType.EMBED, BINType.POINTER):
            field = patch.data
            if field.hash_type != '00000000':
                field.hash_type = BINHasher.hex_to_raw(hashtables, field.hash_type)
                for f in field.data:
                    BINHasher.un_hash_field(hashtables, f)
        else:
            patch.data = BINHasher.un_hash_value(hashtables, patch.data, patch.type)


class BINReader:
    read_value_dict = {
        BINType.NONE:       lambda: None,
        BINType.BOOL:       lambda bs: bs.read_b()[0],
        BINType.I8:         lambda bs: bs.read_i8()[0],
        BINType.U8:         lambda bs: bs.read_u8()[0],
        BINType.I16:        lambda bs: bs.read_i16()[0],
        BINType.U16:        lambda bs: bs.read_u16()[0],
        BINType.I32:        lambda bs: bs.read_i32()[0],
        BINType.U32:        lambda bs: bs.read_u32()[0],
        BINType.I64:        lambda bs: bs.read_i64()[0],
        BINType.U64:        lambda bs: bs.read_u64()[0],
        BINType.F32:        lambda bs: bs.read_f32()[0],
        BINType.VEC2:       lambda bs: bs.read_vec2()[0],
        BINType.VEC3:       lambda bs: bs.read_vec3()[0],
        BINType.VEC4:       lambda bs: bs.read_vec4()[0],
        BINType.MTX44:      lambda bs: bs.read_mtx4()[0],
        BINType.RGBA:       lambda bs: bs.read_u8(4),
        BINType.STRING:     lambda bs: bs.read_s_sized16(encoding='utf-8')[0],
        BINType.HASH:       lambda bs: BINHasher.hash_to_hex(bs.read_u32()[0]),
        BINType.FILE:       lambda bs: WADHasher.hash_to_hex(bs.read_u64()[0]),
        BINType.LIST:       lambda bs: BINReader.read_list_or_list2(bs, BINField(type=BINType.LIST)),
        BINType.LIST2:      lambda bs: BINReader.read_list_or_list2(bs, BINField(type=BINType.LIST2)),
        BINType.POINTER:    lambda bs: BINReader.read_pointer_or_embed(bs, BINField(type=BINType.POINTER)),
        BINType.EMBED:      lambda bs: BINReader.read_pointer_or_embed(bs, BINField(type=BINType.EMBED)),
        BINType.LINK:       lambda bs: BINHasher.hash_to_hex(bs.read_u32()[0]),
        BINType.FLAG:       lambda bs: bs.read_u8()[0],
    }

    @staticmethod
    def read_value(bs, value_type):
        return BINReader.read_value_dict[value_type](bs)

    @staticmethod
    def read_basic(bs, field):
        field.data = BINReader.read_value(bs, field.type)
        return field

    @staticmethod
    def read_list_or_list2(bs, field):
        field.value_type = BINType.fix(bs, bs.read_u8()[0])
        bs.pad(4)  # size
        count, = bs.read_u32()
        field.data = [
            BINReader.read_value(bs, field.value_type)
            for i in range(count)
        ]
        return field
        
    @staticmethod
    def read_pointer_or_embed(bs, field):
        field.hash_type = BINHasher.hash_to_hex(bs.read_u32()[0])
        if field.hash_type != '00000000':
            bs.pad(4)  # size
            count, = bs.read_u16()
            field.data = [
                BINReader.read_field(bs)
                for i in range(count)
            ]
        else:
            field.data = None
        return field
    
    @staticmethod
    def read_option(bs, field):
        field.value_type = BINType.fix(bs, bs.read_u8()[0])
        count, = bs.read_u8()
        field.data = BINReader.read_value(bs, field.value_type) if count != 0 else None
        return field

    @staticmethod
    def read_map(bs, field):
        field.key_type = BINType.fix(bs, bs.read_u8()[0])
        field.value_type = BINType.fix(bs, bs.read_u8()[0])
        bs.pad(4)  # size
        count, = bs.read_u32()
        field.data = {
            BINReader.read_value(bs, field.key_type): BINReader.read_value(bs, field.value_type)
            for i in range(count)
        }
        return field
    
    read_field_dict = {
        field_type:         lambda bs, field: BINReader.read_basic(bs, field) 
        for field_type in read_value_dict
    }
    read_field_dict.update({
        BINType.LIST:       lambda bs, field: BINReader.read_list_or_list2(bs, field),
        BINType.LIST2:      lambda bs, field: BINReader.read_list_or_list2(bs, field),
        BINType.POINTER:    lambda bs, field: BINReader.read_pointer_or_embed(bs, field),
        BINType.EMBED:      lambda bs, field: BINReader.read_pointer_or_embed(bs, field),
        BINType.OPTION:     lambda bs, field: BINReader.read_option(bs, field),
        BINType.MAP:        lambda bs, field: BINReader.read_map(bs, field)
    })

    @staticmethod
    def read_field(bs):
        field = BINField(
            hash=BINHasher.hash_to_hex(bs.read_u32()[0]),
            type=BINType.fix(bs, bs.read_u8()[0])
        )
        return BINReader.read_field_dict[field.type](bs, field)


class BINWriter:
    write_value_dict = {
        BINType.NONE:           lambda: (None, 0),
        BINType.BOOL:           lambda bs, value: (bs.write_b(value), 1),
        BINType.I8:             lambda bs, value: (bs.write_i8(value), 1),
        BINType.U8:             lambda bs, value: (bs.write_u8(value), 1),
        BINType.I16:            lambda bs, value: (bs.write_i16(value), 2),
        BINType.U16:            lambda bs, value: (bs.write_u16(value), 2),
        BINType.I32:            lambda bs, value: (bs.write_i32(value), 4),
        BINType.U32:            lambda bs, value: (bs.write_u32(value), 4),
        BINType.I64:            lambda bs, value: (bs.write_i64(value), 8),
        BINType.U64:            lambda bs, value: (bs.write_u64(value), 8),
        BINType.F32:            lambda bs, value: (bs.write_f32(value), 4),
        BINType.VEC2:           lambda bs, value: (bs.write_vec2(value), 8),
        BINType.VEC3:           lambda bs, value: (bs.write_vec3(value), 12),
        BINType.VEC4:           lambda bs, value: (bs.write_vec4(value), 16),
        BINType.MTX44:          lambda bs, value: (bs.write_mtx4(value), 64),
        BINType.RGBA:           lambda bs, value: (bs.write_u8(*value), 4),
        BINType.STRING:         lambda bs, value: (bs.write_s_sized16(value, encoding='utf-8'), len(value.encode('utf-8'))+2),
        BINType.HASH:           lambda bs, value: (bs.write_u32(BINHasher.raw_or_hex_to_hash(value)), 4),
        BINType.FILE:           lambda bs, value: (bs.write_u64(WADHasher.raw_or_hex_to_hash(value)), 8),
        BINType.LIST:           lambda bs, value: BINWriter.write_list_or_list2(bs, value),
        BINType.LIST2:          lambda bs, value: BINWriter.write_list_or_list2(bs, value),
        BINType.POINTER:        lambda bs, value: BINWriter.write_pointer_or_embed(bs, value),
        BINType.EMBED:          lambda bs, value: BINWriter.write_pointer_or_embed(bs, value),
        BINType.LINK:           lambda bs, value: (bs.write_u32(BINHasher.raw_or_hex_to_hash(value)), 4),
        BINType.FLAG:           lambda bs, value: (bs.write_u8(value), 1),
    }

    @staticmethod
    def write_value(bs, value, value_type, header_size):
        size = BINWriter.write_value_dict[value_type](bs, value)[1]
        return size+5 if header_size else size
    
    @staticmethod
    def write_basic(bs, field):
        return None, BINWriter.write_value(bs, field.data, field.type, header_size=False)

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
            content_size += BINWriter.write_value(bs,
                                                    value, field.value_type, header_size=False)
        bs.size_offsets.append((return_offset, content_size))

        size += content_size
        return None, size

    @staticmethod
    def write_pointer_or_embed(bs, field):
        size = 0
        if field.hash_type == '00000000':
            bs.write_u32(0)
            size += 4
        else:
            bs.write_u32(BINHasher.raw_or_hex_to_hash(field.hash_type))
            size += 4

            return_offset = bs.tell()
            bs.write_u32(0)  # size
            size += 4

            content_size = 2
            bs.write_u16(len(field.data))
            for value in field.data:
                content_size += BINWriter.write_field(
                    bs, value, header_size=True)
            bs.size_offsets.append((return_offset, content_size))

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
            size += BINWriter.write_value(bs, field.data, field.value_type, header_size=False)
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
            content_size += BINWriter.write_value(bs,
                                                    key, field.key_type, header_size=False)
            content_size += BINWriter.write_value(bs,
                                                    value, field.value_type, header_size=False)
        bs.size_offsets.append((return_offset, content_size))

        size += content_size
        return None, size
    
    write_field_dict = {
        field_type:         lambda bs, field: BINWriter.write_basic(bs, field) 
        for field_type in write_value_dict
    }
    write_field_dict.update({
        BINType.LIST:       lambda bs, field: BINWriter.write_list_or_list2(bs, field),
        BINType.LIST2:      lambda bs, field: BINWriter.write_list_or_list2(bs, field),
        BINType.POINTER:    lambda bs, field: BINWriter.write_pointer_or_embed(bs, field),
        BINType.EMBED:      lambda bs, field: BINWriter.write_pointer_or_embed(bs, field),
        BINType.OPTION:     lambda bs, field: BINWriter.write_option(bs, field),
        BINType.MAP:        lambda bs, field: BINWriter.write_map(bs, field)
    })

    @staticmethod
    def write_field(bs, field, header_size):
        bs.write_u32(BINHasher.raw_or_hex_to_hash(field.hash))
        bs.write_u8(field.type.value)
        size = BINWriter.write_field_dict[field.type](bs, field)[1]
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
        if self.type == BINType.LIST or self.type == BINType.LIST2:
            dic.pop('key_type')
            dic.pop('hash_type')
        elif self.type == BINType.POINTER or self.type == BINType.EMBED:
            dic.pop('key_type')
            dic.pop('value_type')
        elif self.type == BINType.MAP:
            dic.pop('hash_type')
        else:
            dic.pop('key_type')
            dic.pop('hash_type')
            dic.pop('value_type')
        return dic
    
    def get_items(self, compare_func):
        res = []
        for item in self.data:
            if compare_func(item):
                res.append(item)
        return res
    

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

    def get_items(self, compare_func):
        res = []
        for item in self.data:
            if compare_func(item):
                res.append(item)
        return res

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

    def read(self, path, raw=False):
        with BytesStream.reader(path, raw) as bs:
            # header
            self.signature, = bs.read_s(4, encoding='utf-8')
            if self.signature not in ('PROP', 'PTCH'):
                raise Exception(
                    f'pyRitoFile: Error: Read BIN {path}: Wrong file signature: {self.signature}')
            if self.signature == 'PTCH':
                self.is_patch = True
                bs.pad(8)  # patch header
                magic, = bs.read_s(4, encoding='utf-8')
                if magic != 'PROP':
                    raise Exception(
                        f'pyRitoFile: Error: Read BIN {path}: Missing PROP after PTCH signature.')
            self.version, = bs.read_u32()
            if self.version not in (1, 2, 3):
                raise Exception(
                    f'pyRitoFile: Error: Read BIN {path}: Unsupported file version: {self.version}')
            # links
            if self.version >= 2:
                link_count, = bs.read_u32()
                self.links = [bs.read_s_sized16(encoding='utf-8')[0] for _ in range(link_count)]
            # entry_types + entries
            entry_count, = bs.read_u32()
            entry_types = bs.read_u32(entry_count)
            entry_offset = bs.tell()
            try:
                bs.legacy_read = False
                # read as new bin
                self.entries = [BINEntry() for i in range(entry_count)]
                for entry_id, entry in enumerate(self.entries):
                    entry.type = BINHasher.hash_to_hex(entry_types[entry_id])
                    bs.pad(4)  # size
                    entry.hash = BINHasher.hash_to_hex(bs.read_u32()[0])
                    field_count, = bs.read_u16()
                    entry.data = [BINReader.read_field(
                        bs) for i in range(field_count)]
            except ValueError:
                # legacy bin, fall back
                bs.seek(entry_offset)
                bs.legacy_read = True
                self.entries = [BINEntry() for i in range(entry_count)]
                for entry_id, entry in enumerate(self.entries):
                    entry.type = BINHasher.hash_to_hex(entry_types[entry_id])
                    bs.pad(4)  # size
                    entry.hash = BINHasher.hash_to_hex(bs.read_u32()[0])
                    field_count, = bs.read_u16()
                    entry.data = [BINReader.read_field(
                        bs) for i in range(field_count)]
            except Exception as e:
                # raise any other errors
                raise e
            # patches
            if self.is_patch and self.version >= 3:
                patch_count, = bs.read_u32()
                self.patches = [BINPatch() for i in range(patch_count)]
                for patch in self.patches:
                    patch.hash = BINHasher.hash_to_hex(bs.read_u32()[0])
                    bs.pad(4)  # size
                    patch.type = BINType.fix(bs, bs.read_u8()[0])
                    patch.path, = bs.read_s_sized16(encoding='utf-8')
                    patch.data = BINReader.read_value(bs, patch.type)

            return self
        
    def write(self, path, raw=False):
        with BytesStream.writer(path, raw) as bs:
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
                bs.write_u32(BINHasher.raw_or_hex_to_hash(entry.type))
            bs.size_offsets = []  # this help to write sizes
            for entry in self.entries:
                return_offset = bs.tell()

                bs.write_u32(0)  # size
                entry_size = 4+2

                bs.write_u32(BINHasher.raw_or_hex_to_hash(entry.hash))
                bs.write_u16(len(entry.data))
                for field in entry.data:
                    entry_size += BINWriter.write_field(
                        bs, field, header_size=True)
                bs.size_offsets.append((return_offset, entry_size))
            # patches
            if self.is_patch:
                bs.write_u32(len(self.patches))
                for patch in self.patches:
                    bs.write_u32(BINHasher.raw_or_hex_to_hash(patch.hash))

                    return_offset = bs.tell()
                    bs.write_u32(0)  # size
                    patch_size = 1 + 2 + len(patch.path)

                    bs.write_u8(patch.type.value)
                    bs.write_s_sized16(patch.path, encoding='utf-8')
                    patch_size += BINWriter.write_value(
                        bs, patch.data, patch.type, header_size=False)
                    bs.size_offsets.append(
                        (return_offset, patch_size))
            # jump around and write size
            for offset, size in bs.size_offsets:
                bs.seek(offset)
                bs.write_u32(size)
            return bs.raw() if raw else None

    def un_hash(self, hashtables=None):
        if hashtables == None:
            return
        for entry in self.entries:
            entry.hash = BINHasher.hex_to_raw(hashtables, entry.hash)
            entry.type = BINHasher.hex_to_raw(hashtables, entry.type)
            for field in entry.data:
                BINHasher.un_hash_field(hashtables, field)
        if self.is_patch:
            for patch in self.patches:
                BINHasher.un_hash_patch(hashtables, patch)

    def get_items(self, compare_func):
        res = []
        for item in self.entries:
            if compare_func(item):
                res.append(item)
        return res
    