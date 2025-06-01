from .stream import BytesStream
from enum import Enum


class TEXFormat(Enum):
    ETC1 = 1
    ETC2_EAC = 2
    ETC2 = 3
    DXT1 = 10
    DXT5 = 12
    BGRA8 = 20

    def __json__(self):
        return self.name


class TEX:
    __slots__ = (
        'signature', 'width', 'height',
        'format', 'unknown1', 'unknown2', 'mipmaps',
        'data'
    )

    def __init__(self, signature=None, width=None, height=None, format=None, unknown1=None, unknown2=None, mipmaps=False, data=None):
        self.signature = signature
        self.width = width
        self.height = height
        self.format = format
        self.unknown1 = unknown1
        self.unknown2 = unknown2
        self.mipmaps = mipmaps
        self.data = data

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def read(self, path, raw=False):
        with BytesStream.reader(path, raw) as bs:
            # read headers
            self.signature, = bs.read_u32()
            if self.signature != 0x00584554:
                raise Exception(
                    f'pyRitoFile: Error: Read TEX {path}: Wrong file signature: {hex(self.signature)}')
            self.width, self.height = bs.read_u16(2)
            self.unknown1, self.format, self.unknown2 = bs.read_u8(3)
            self.format = TEXFormat(self.format)
            self.mipmaps, = bs.read_b()
            # read data
            if self.mipmaps and self.format in (TEXFormat.DXT1, TEXFormat.DXT5, TEXFormat.BGRA8):
                # if mipmaps and supported format
                if self.format == TEXFormat.DXT1:
                    block_size = 4
                    bytes_per_block = 8
                elif self.format == TEXFormat.DXT5:
                    block_size = 4
                    bytes_per_block = 16
                else:
                    block_size = 1
                    bytes_per_block = 4
                mipmap_count = 32 - \
                    len(f'{max(self.width, self.height):032b}'.split(
                        '1', 1)[0])
                self.data = []
                for i in reversed(range(mipmap_count)):
                    current_width = max(self.width // (1 << i), 1)
                    current_height = max(self.height // (1 << i), 1)
                    block_width = (current_width +
                                   block_size - 1) // block_size
                    block_height = (current_height +
                                    block_size - 1) // block_size
                    current_size = bytes_per_block * block_width * block_height
                    self.data.append(bs.read(current_size))
            else:
                self.data = [bs.read(-1)]

            return self
        
    def write(self, path, raw=False):
        with BytesStream.writer(path, raw) as bs:
            # write headers
            bs.write_u32(0x00584554)
            bs.write_u16(self.width, self.height)
            bs.write_u8(1, self.format.value, 0)  # unknown1, format, unknown2
            bs.write_b(self.mipmaps)
            if self.mipmaps and self.format in (TEXFormat.DXT1, TEXFormat.DXT5, TEXFormat.BGRA8):
                for block_data in self.data:
                    bs.write(block_data)
            else:
                bs.write(self.data[0])
