from io import BytesIO
from LtMAO.pyRitoFile.io import BinStream
from json import JSONEncoder
from enum import Enum
import os
import os.path
import gzip
import pyzstd
from xxhash import xxh64


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
    b'TEX\0': 'tex'
}


def hex_to_name(hashtables, table_name, hash):
    return hashtables.get(table_name, {}).get(hash, hash)


def hash_to_hex(hash):
    return f'{hash:016x}'


def name_to_hex(name):
    return xxh64(name.lower()).hexdigest()


class WADHelper:
    def unpack(wad, raw, LOG=print):
        os.makedirs(raw, exist_ok=True)
        for chunk in wad.chunks:
            chunk.read_data(wad)
            fo_path = os.path.join(raw, chunk.hash)
            if chunk.extension != None:
                ext = f'.{chunk.extension}'
                if not fo_path.endswith(ext):
                    fo_path += ext
            fo_path = fo_path.replace('\\', '/')
            os.makedirs(os.path.dirname(fo_path), exist_ok=True)
            with open(fo_path, 'wb') as fo:
                fo.write(chunk.data)
            chunk.free_data()
            LOG(f'Done: Extracted: {chunk.hash}')

    def pack(raw, wad):
        pass


class WADEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        else:
            return JSONEncoder.default(self, obj)


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
        'hash', 'offset',
        'compressed_size', 'decompressed_size', 'compression_type',
        'duplicated', 'subchunk_start', 'subchunk_count',
        'checksum', 'data', 'extension'
    )

    def __init__(self):
        self.hash = None
        self.offset = None
        self.compressed_size = None
        self.decompressed_size = None
        self.compression_type = None
        self.duplicated = None
        self.subchunk_start = None
        self.subchunk_count = None
        self.checksum = None
        self.data = None
        self.extension = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__ if key != 'data'}

    def free_data(self):
        self.data = None

    def read_data(self, wad):
        with wad.IO() as f:
            bs = BinStream(f)
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
            elif self.compression_type in (WADCompressionType.Zstd, WADCompressionType.ZstdChunked):
                self.data = pyzstd.decompress(raw)
            # guess extension
            if self.data[4:8] == bytes.fromhex('c34ffd22'):
                self.extension = 'skl'
            else:
                for signature, extension in signature_to_extension.items():
                    if self.data.startswith(signature):
                        self.extension = extension
                        break


class WAD:
    __slots__ = ('IO', 'signature', 'version', 'chunks')

    def __init__(self):
        self.IO = None
        self.signature = None
        self.version = None
        self.chunks = []

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__ if key != 'IO'}

    def read(self, path, raw=None):
        def IO(): return open(path, 'rb') if raw == None else lambda: BytesIO(raw)
        self.IO = IO
        with IO() as f:
            bs = BinStream(f)
            # read header
            self.signature, = bs.read_a(2)
            if self.signature != 'RW':
                raise Exception(
                    f'Failed: Read WAD {path}: Wrong file signature: {self.signature}')
            major, minor = bs.read_u8(2)
            self.version = float(f'{major}.{minor}')
            if major > 3:
                raise Exception(
                    f'Failed: Read WAD {path}: Unsupported file version: {self.version}')
            data_checksum = 0
            if major == 2:
                ecdsa_len = bs.read_u8()
                bs.pad(83)
                data_checksum, = bs.read_u64()
            elif major == 3:
                bs.pad(256)
                data_checksum, = bs.read_u64()
            if major == 1 or major == 2:
                toc_start_offset, toc_file_entry_size = bs.read_u16(
                    2)
            # read chunks
            chunk_count, = bs.read_u32()
            self.chunks = [WADChunk() for i in range(chunk_count)]
            for i in range(chunk_count):
                chunk = self.chunks[i]
                chunk.hash = hash_to_hex(bs.read_u64()[0])
                chunk.offset, chunk.compressed_size, chunk.decompressed_size, = bs.read_u32(
                    3)
                chunk.compression_type = WADCompressionType(
                    bs.read_u8()[0] & 15)
                chunk.duplicated, = bs.read_b()
                chunk.subchunk_start, = bs.read_u16()
                chunk.subchunk_count = chunk.compression_type.value >> 4
                chunk.checksum = bs.read_u64()[0] if major >= 2 else 0

    def un_hash(self, hashtables=None):
        if hashtables == None:
            return
        for chunk in self.chunks:
            chunk.hash = hex_to_name(hashtables, 'hashes.game.txt', chunk.hash)
            chunk.extension = '.'.join(chunk.hash.split('.')[1:])
        self.chunks = sorted(self.chunks, key=lambda chunk: chunk.hash)
