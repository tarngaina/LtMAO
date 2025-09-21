from .stream import BytesStream
from enum import Enum
import gzip

# not safe because external modules
try: 
    import pyzstd
    from xxhash import xxh64, xxh3_64
except:
    print('Warning: pyRitoFile.wad failed to import pyzstd, xxhash.')

class WADExtensioner:
    signature_to_extension = {
        b'OggS': 'ogg',
        bytes.fromhex('00 01 00 00'): 'ttf',
        bytes.fromhex('1A 45 DF A3'): 'webm',
        b'true': 'ttf',
        b'OTTO\0': 'otf',
        b'"use strict";': 'min.js',
        b'<template ': 'template.html',
        b'<!-- Elements -->': 'template.html',
        b'DDS ': 'dds',
        b'<svg': 'svg',
        b'PROP': 'bin',
        b'PTCH': 'bin',
        b'BKHD': 'bnk',
        b'r3d2Mesh': 'scb',
        b'r3d2anmd': 'anm',
        b'r3d2canm': 'anm',
        b'r3d2sklt': 'skl',
        b'r3d2': 'wpk',
        bytes.fromhex('33 22 11 00'): 'skn',
        b'PreLoadBuildingBlocks = {': 'preload',
        b'\x1bLuaQ\x00\x01\x04\x04': 'luabin',
        b'\x1bLuaQ\x00\x01\x04\x08': 'luabin64',
        bytes.fromhex('02 3D 00 28'): 'troybin',
        b'[ObjectBegin]': 'sco',
        b'OEGM': 'mapgeo',
        b'TEX\0': 'tex',
        b'RW': 'wad',
        bytes.fromhex('89 50 4E 47 0D 0A 1A 0A'): 'png',
        bytes.fromhex('FF D8 FF'): 'jpg',
        b'gimp xcf': 'xcf',
        b'8BPS': 'psd',
        b'BLENDER': 'blend',
        b'Kaydara FBX Binary': 'fbx', 
        b'FOR4': 'mb',
        b'FOR8': 'mb',
        b'#MayaIcons': 'swatches',
        b'#PROP_text': 'py',
        bytes.fromhex('5B 0A 20 20'): 'json',
        bytes.fromhex('7B 0A 20 20'): 'json',
    }

    @staticmethod
    def guess_extension(data):
        if data[4:8] == bytes.fromhex('C3 4F FD 22'):
            return 'skl'
        else:
            for signature, extension in WADExtensioner.signature_to_extension.items():
                if data.startswith(signature):
                    return extension

    @staticmethod
    def get_extension(path):
        if path.endswith('.wad.client'):
            return 'wad'
        for _, extension in WADExtensioner.signature_to_extension.items():
            if path.endswith(extension):
                return extension
            

class WADHasher:
    HASHTABLE_NAMES = (
        'hashes.game.txt',
        'hashes.lcu.txt',
    )
    @staticmethod
    def hex_to_raw(hashtables, hex):
        for table_name in reversed(WADHasher.HASHTABLE_NAMES):
            if table_name in hashtables and hex in hashtables[table_name]:
                return hashtables[table_name][hex]
        return hex
    
    @staticmethod
    def raw_to_hex(raw):
        return f'{xxh64(raw.lower()).intdigest():016x}'

    @staticmethod
    def hash_to_hex(hash):
        return f'{hash:016x}'
    
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
            return xxh64(raw_or_hex.lower()).intdigest()
        

class WADCompressionType(Enum):
    Raw = 0
    Gzip = 1
    Satellite = 2
    Zstd = 3
    ZstdChunked = 4

    def __json__(self):
        return self.name


class WADChunk:
    __slots__ = (
        'id', 'hash', 'offset',
        'compressed_size', 'decompressed_size', 'compression_type',
        'duplicated', 'subchunk_start', 'subchunk_count',
        'checksum', 'data', 'extension'
    )

    def __init__(self, id=None, hash=None, offset=None, compressed_size=None, decompressed_size=None, compression_type=None, duplicated=None, subchunk_start=None, subchunk_count=None, checksum=None, data=None, extension=None):
        self.id = id
        self.hash = hash
        self.offset = offset
        self.compressed_size = compressed_size
        self.decompressed_size = decompressed_size
        self.compression_type = compression_type
        self.duplicated = duplicated
        self.subchunk_start = subchunk_start
        self.subchunk_count = subchunk_count
        self.checksum = checksum
        self.data = data
        self.extension = extension

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__ if key != 'data'}

    @staticmethod
    def default(*, id=0, hash='', offset=0, compressed_size=0, decompressed_size=0, compression_type=WADCompressionType.Raw, duplicated=False, subchunk_start=0, subchunk_count=0, checksum=0):
        chunk = WADChunk()
        chunk.id = id
        chunk.hash = hash
        chunk.offset = offset
        chunk.compressed_size = compressed_size
        chunk.decompressed_size = decompressed_size
        chunk.compression_type = compression_type
        chunk.duplicated = duplicated
        chunk.subchunk_start = subchunk_start
        chunk.subchunk_count = subchunk_count
        chunk.checksum = checksum
        return chunk

    def free_data(self):
        self.data = None

    def read_data(self, bs):
        # read data and decompress
        bs.seek(self.offset)
        raw = bs.read(self.compressed_size)
        if self.compression_type == WADCompressionType.Raw:
            self.data = raw
        elif self.compression_type == WADCompressionType.Gzip:
            self.data = gzip.decompress(raw)
        elif self.compression_type == WADCompressionType.Satellite:
            # Satellite is not supported
            self.data = None
        elif self.compression_type == WADCompressionType.Zstd:
            self.data = pyzstd.decompress(raw)
        elif self.compression_type == WADCompressionType.ZstdChunked:
            if raw[:4] == b'\x28\xb5\x2f\xfd':
                self.data = pyzstd.decompress(raw)
            else:
                self.data = raw
        # guess extension
        if self.extension == None:
            self.extension = WADExtensioner.guess_extension(self.data)

    def write_data(self, bs, chunk_id, chunk_hash, chunk_data, *, previous_chunks=None):
        self.hash = chunk_hash
        if self.extension in ('bnk', 'wpk'):
            self.data = chunk_data
            self.compression_type = WADCompressionType.Raw
        else:
            self.data = pyzstd.compress(chunk_data)
            self.compression_type = WADCompressionType.Zstd
        self.compressed_size = len(self.data)
        self.decompressed_size = len(chunk_data)
        self.checksum = xxh3_64(self.data).intdigest()
        # check duplicated data
        if previous_chunks:
            duped_id, duped_chunk = None, None
            for id, chunk in enumerate(previous_chunks):
                if chunk.checksum == self.checksum and chunk.compressed_size == self.compressed_size and chunk.decompressed_size == self.decompressed_size:
                    duped_id = id
                    duped_chunk = chunk
                    break
            if duped_chunk != None:
                # if there is a duped chunk in previous
                if not duped_chunk.duplicated:
                    # if the chunk was not a duped chunk
                    # rewrite the duplicated value for the previous chunk
                    duped_chunk.duplicated = True
                    bs.seek(272 + duped_id * 32 + 21)
                    bs.write_b(duped_chunk.duplicated)
                # set this chunk as duplicated and copy the offset from duped chunk
                self.duplicated = True
                self.offset = duped_chunk.offset
        if not self.duplicated:
            # if its duplicated dont need to write data
            # go to end file, save data offset and write chunk data
            bs.seek(0, 2)
            self.offset = bs.tell()
            bs.write(self.data)
        # go to this chunk offset and write stuffs
        # hack: the first chunk start at 272 (because we write version 3.3)
        self.id = chunk_id
        chunk_offset = 272 + chunk_id * 32
        bs.seek(chunk_offset)
        bs.write_u64(WADHasher.raw_or_hex_to_hash(chunk_hash))
        bs.write_u32(
            self.offset,
            self.compressed_size,
            self.decompressed_size
        )
        bs.write_u8(self.compression_type.value)
        bs.write_b(self.duplicated)
        bs.write_u16(0)
        bs.write_u64(self.checksum)


class WAD:
    __slots__ = ('signature', 'version', 'chunks')

    def __init__(self, signature=None, version=None, chunks=None):
        self.signature = signature
        self.version = version
        self.chunks = chunks

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__ if key != 'IO'}

    def read(self, path, raw=False):
        with BytesStream.reader(path, raw) as bs:
            # read header
            self.signature, = bs.read_s(2)
            if self.signature != 'RW':
                raise Exception(
                    f'pyRitoFile: Error: Read WAD {path}: Wrong file signature: {self.signature}')
            major, minor = bs.read_u8(2)
            self.version = float(f'{major}.{minor}')
            if major > 3:
                raise Exception(
                    f'pyRitoFile: Error: Read WAD {path}: Unsupported file version: {self.version}')
            wad_checksum = 0
            if major == 2:
                ecdsa_len = bs.read_u8()
                bs.pad(83)
                wad_checksum, = bs.read_u64()
            elif major == 3:
                bs.pad(256)
                wad_checksum, = bs.read_u64()
            if major == 1 or major == 2:
                toc_start_offset, toc_file_entry_size = bs.read_u16(
                    2)
            # read chunks
            chunk_count, = bs.read_u32()
            self.chunks = [WADChunk() for i in range(chunk_count)]
            for chunk_id, chunk in enumerate(self.chunks):
                chunk.id = chunk_id
                chunk.hash = WADHasher.hash_to_hex(bs.read_u64()[0])
                chunk.offset, chunk.compressed_size, chunk.decompressed_size, = bs.read_u32(
                    3)
                chunk.compression_type = WADCompressionType(
                    bs.read_u8()[0] & 15)
                chunk.duplicated, = bs.read_b()
                chunk.subchunk_start, = bs.read_u16()
                chunk.subchunk_count = chunk.compression_type.value >> 4
                chunk.checksum = bs.read_u64()[0] if major >= 2 else 0
            
            return self

    def write(self, path, raw=False):
        with BytesStream.writer(path, raw) as bs:
            # write header
            bs.write_s('RW')  # signature
            bs.write_u8(3, 3)  # version
            bs.write(b'\x00' * 256)  # pad 256 bytes
            bs.write_u64(0)  # wad checksum
            bs.write_u32(len(self.chunks))
            # write chunks
            for chunk in self.chunks:
                bs.write_u64(WADHasher.raw_or_hex_to_hash(chunk.hash))
                bs.write_u32(
                    chunk.offset,
                    chunk.compressed_size,
                    chunk.decompressed_size
                )
                bs.write_u8(chunk.compression_type.value)
                bs.write_b(chunk.duplicated)
                bs.write_u16(chunk.subchunk_start)
                bs.write_u64(chunk.checksum)
            return bs.raw() if raw else None

    def un_hash(self, hashtables=None):
        if hashtables == None:
            return
        for chunk in self.chunks:
            chunk.hash = WADHasher.hex_to_raw(hashtables, chunk.hash)
            if '.' in chunk.hash and chunk.extension == None:
                chunk.extension = WADExtensioner.get_extension(chunk.hash)
        self.chunks = sorted(self.chunks, key=lambda chunk: chunk.hash)

    def get_items(self, compare_func):
        res = []
        for item in self.chunks:
            if compare_func(item):
                res.append(item)
        return res
