from io import BytesIO
from ..pyRitoFile.io import BinStream
from enum import Enum
import gzip
import pyzstd
from xxhash import xxh64, xxh3_64

signature_to_extension = {
    b'OggS': 'ogg',
    bytes.fromhex('00010000'): 'ttf',
    bytes.fromhex('1a45dfa3'): 'webm',
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
    bytes.fromhex('33221100'): 'skn',
    b'PreLoadBuildingBlocks = {': 'preload',
    b'\x1bLuaQ\x00\x01\x04\x04': 'luabin',
    b'\x1bLuaQ\x00\x01\x04\x08': 'luabin64',
    bytes.fromhex('023d0028'): 'troybin',
    b'[ObjectBegin]': 'sco',
    b'OEGM': 'mapgeo',
    b'TEX\0': 'tex',
    b'RW': 'wad'
}


def guess_extension(data):
    if data[4:8] == bytes.fromhex('c34ffd22'):
        return 'skl'
    else:
        for signature, extension in signature_to_extension.items():
            if data.startswith(signature):
                return extension


def parse_extension(path):
    if path.endswith('.wad.client'):
        return 'wad'
    for _, extension in signature_to_extension.items():
        if path.endswith(extension):
            return extension


def hash_to_hex(hash):
    return f'{hash:016x}'


def hex_to_hash(hex):
    return int(hex, 16)


def name_to_hash(name):
    return xxh64(name.lower()).intdigest()


def hex_to_name(hashtables, table_name, hash):
    return hashtables.get(table_name, {}).get(hash, hash)


def name_to_hex(name):
    return xxh64(name.lower()).hexdigest()


def name_or_hex_to_hash(value):
    try:
        return hex_to_hash(value)
    except:
        return name_to_hash(value)


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
            self.extension = guess_extension(self.data)

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
        bs.write_u64(name_or_hex_to_hash(chunk_hash))
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

    def __init__(self, signature=None, version=None, chunks=[]):
        self.signature = signature
        self.version = version
        self.chunks = chunks

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__ if key != 'IO'}

    def stream(self, path, mode, raw=None):
        if raw != None:
            if raw == True:  # the bool True value
                return BinStream(BytesIO())
            else:
                return BinStream(BytesIO(raw))
        return BinStream(open(path, mode))

    def read(self, path, raw=None):
        with self.stream(path, 'rb', raw) as bs:
            # read header
            self.signature, = bs.read_a(2)
            if self.signature != 'RW':
                raise Exception(
                    f'pyRitoFile: Failed: Read WAD {path}: Wrong file signature: {self.signature}')
            major, minor = bs.read_u8(2)
            self.version = float(f'{major}.{minor}')
            if major > 3:
                raise Exception(
                    f'pyRitoFile: Failed: Read WAD {path}: Unsupported file version: {self.version}')
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
                chunk.hash = hash_to_hex(bs.read_u64()[0])
                chunk.offset, chunk.compressed_size, chunk.decompressed_size, = bs.read_u32(
                    3)
                chunk.compression_type = WADCompressionType(
                    bs.read_u8()[0] & 15)
                chunk.duplicated, = bs.read_b()
                chunk.subchunk_start, = bs.read_u16()
                chunk.subchunk_count = chunk.compression_type.value >> 4
                chunk.checksum = bs.read_u64()[0] if major >= 2 else 0

    def write(self, path, raw=None):
        with self.stream(path, 'wb', raw) as bs:
            # write header
            bs.write_a('RW')  # signature
            bs.write_u8(3, 3)  # version
            bs.write(b'\x00' * 256)  # pad 256 bytes
            bs.write_u64(0)  # wad checksum
            bs.write_u32(len(self.chunks))
            # write chunks
            for chunk in self.chunks:
                bs.write_u64(name_or_hex_to_hash(chunk.hash))
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
            chunk.hash = hex_to_name(hashtables, 'hashes.game.txt', chunk.hash)
            if '.' in chunk.hash and chunk.extension == None:
                chunk.extension = parse_extension(chunk.hash)
        self.chunks = sorted(self.chunks, key=lambda chunk: chunk.hash)
