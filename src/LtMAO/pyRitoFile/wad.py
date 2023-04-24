from io import BytesIO
from LtMAO.pyRitoFile.io import BinStream
from json import JSONEncoder
from enum import Enum
import os
import os.path
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
    b'TEX\0': 'tex'
}


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


class WADHelper:
    def unpack(wad, raw, LOG=print):
        # ensure folder
        os.makedirs(raw, exist_ok=True)
        bs = BinStream(open(wad, 'rb'))
        for chunk in wad.chunks:
            chunk.read_data(bs)
            # output file path of this chunk
            file_path = os.path.join(raw, chunk.hash)
            # add extension to file path if know
            if chunk.extension != None:
                ext = f'.{chunk.extension}'
                if not file_path.endswith(ext):
                    file_path += ext
            file_path = file_path.replace('\\', '/')
            # ensure folder of this file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # write out chunk data to file
            with open(file_path, 'wb') as fo:
                fo.write(chunk.data)
            chunk.free_data()
            LOG(f'Done: Unpacked: {chunk.hash}')
        bs.close()

    def pack(raw, wad, LOG=print):
        def check_hashed_name(basename):
            try:
                int(basename, 16)
                return True
            except:
                return False
        # create wad first with only infos
        meta_wad = WAD()
        file_paths = []
        for root, dirs, files in os.walk(raw):
            for id, file in enumerate(files):
                # prepare paths of raw files
                file_paths.append(os.path.join(root, file).replace('\\', '/'))
                # prepare chunk hash: remove extension of hashed file
                # example: 6bff35087d62f95d.bin -> 6bff35087d62f95d
                basename = file.split('.')[0]
                if check_hashed_name(basename):
                    file = basename
                # create chunk infos
                chunk = WADChunk()
                chunk.id = id
                chunk.hash = os.path.relpath(os.path.join(
                    root, file), raw).replace('\\', '/')
                chunk.offset = 0
                chunk.compressed_size = 0
                chunk.decompressed_size = 0
                chunk.compression_type = WADCompressionType.Zstd
                chunk.duplicated = False
                chunk.subchunk_start = 0
                chunk.subchunk_count = 0
                chunk.checksum = 0
                meta_wad.chunks.append(chunk)
        # write wad
        meta_wad.write(wad)
        # open back the wad, append data from raw files and rewrite info
        bs = BinStream(open(wad, 'rb+'))
        for id, chunk in enumerate(meta_wad.chunks):
            with open(file_paths[id], 'rb') as f:
                data = f.read()
            chunk.write_data(bs, data)
            chunk.free_data()
            LOG(f'Done: Packed: {chunk.hash}')
        bs.close()


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
        'id', 'hash', 'offset',
        'compressed_size', 'decompressed_size', 'compression_type',
        'duplicated', 'subchunk_start', 'subchunk_count',
        'checksum', 'data', 'extension'
    )

    def __init__(self):
        self.id = None
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

    def build(self, id, hash, data):
        self.data = pyzstd.compress(data)
        self.id = id
        self.hash = hash
        self.offset = 0
        self.compressed_size = len(self.data)
        self.decompressed_size = len(data)
        self.compression_type = WADCompressionType.Zstd
        self.duplicated = False
        self.subchunk_start = 0
        self.subchunk_count = 0
        self.checksum = xxh3_64(self.data).intdigest()

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

    def write_data(self, bs, data):
        self.data = pyzstd.compress(data)
        self.compressed_size = len(self.data)
        self.decompressed_size = len(data)
        self.checksum = xxh3_64(self.data).intdigest()
        # go to end file, save data offset and write chunk data
        bs.seek(0, 2)
        self.offset = bs.tell()
        bs.write(self.data)
        # go to this chunk offset and write stuffs
        # hack: the first chunk start at 272 (because we write version 3.3)
        chunk_offset = 272 + self.id * 32
        bs.seek(chunk_offset)
        bs.pad(8)  # pad hash
        bs.write_u32(
            self.offset,
            self.compressed_size,
            self.decompressed_size
        )
        bs.pad(4)  # pad compression type, duplicated and subchunk_start
        bs.write_u64(self.checksum)


class WAD:
    __slots__ = ('signature', 'version', 'chunks')

    def __init__(self):
        self.signature = None
        self.version = None
        self.chunks = []

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__ if key != 'IO'}

    def read(self, path, raw=None):
        def IO(): return open(path, 'rb') if raw == None else BytesIO(raw)
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
            for i in range(chunk_count):
                chunk = self.chunks[i]
                chunk.id = i
                chunk.hash = hash_to_hex(bs.read_u64()[0])
                chunk.offset, chunk.compressed_size, chunk.decompressed_size, = bs.read_u32(
                    3)
                chunk.compression_type = WADCompressionType(
                    bs.read_u8()[0] & 15)
                chunk.duplicated, = bs.read_b()
                chunk.subchunk_start, = bs.read_u16()
                chunk.subchunk_count = chunk.compression_type.value >> 4
                chunk.checksum = bs.read_u64()[0] if major >= 2 else 0

    def write(self, path):
        with open(path, 'wb') as f:
            bs = BinStream(f)
            # write header
            bs.write_a('RW')  # signature
            bs.write_u8(3, 3)  # version
            bs.write(b'\x00' * 256)  # pad 256 bytes
            bs.write_u64(0)  # wad checksum
            bs.write_u32(len(self.chunks))
            # write chunks
            for chunk in self.chunks:
                test = name_or_hex_to_hash(chunk.hash)
                bs.write_u64(test)
                bs.write_u32(
                    chunk.offset,
                    chunk.compressed_size,
                    chunk.decompressed_size
                )
                bs.write_u8(chunk.compression_type.value)
                bs.write_b(chunk.duplicated)
                bs.write_u16(chunk.subchunk_start)
                bs.write_u64(chunk.checksum)

    def un_hash(self, hashtables=None):
        if hashtables == None:
            return
        for chunk in self.chunks:
            chunk.hash = hex_to_name(hashtables, 'hashes.game.txt', chunk.hash)
            chunk.extension = '.'.join(chunk.hash.split('.')[1:])
        self.chunks = sorted(self.chunks, key=lambda chunk: chunk.hash)
