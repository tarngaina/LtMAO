from io import BytesIO
from LtMAO.pyRitoFile.io import BinStream
from json import JSONEncoder
from enum import Enum
import gzip
import pyzstd

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


# def name_to_hex(name):
#   return hash_to_hex(FNV1a(name))


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
    def __init__(self):
        pass

    def __json__(self):
        # return {key: getattr(self, key) for key in self.__slots__}
        dic = vars(self)
        dic.pop('data')
        return dic


class WAD:

    def __init__(self):
        pass

    def __json__(self):
        # return {key: getattr(self, key) for key in self.__slots__}
        return vars(self)

    def read(self, path, raw=None):
        IO = open(path, 'rb') if raw == None else BytesIO(raw)
        with IO as f:
            bs = BinStream(f)

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

            for chunk in self.chunks:
                bs.seek(chunk.offset)
                data = f.read(chunk.compressed_size)
                if chunk.compression_type == WADCompressionType.Raw:
                    chunk.data = data
                elif chunk.compression_type == WADCompressionType.Gzip:
                    chunk.data = gzip.decompress(data)
                elif chunk.compression_type == WADCompressionType.Satellite:
                    print(data)  # ???
                    chunk.data = None
                elif chunk.compression_type == WADCompressionType.Zstd:
                    chunk.data = pyzstd.decompress(data)
                elif chunk.compression_type == WADCompressionType.ZstdChunked:
                    if data[:4] == b'\x28\xb5\x2f\xfd':  # zstd header
                        chunk.data = pyzstd.decompress(data)
                    chunk.data = data

                chunk.extension = None
                for signature, extension in signature_to_extension.items():
                    if chunk.data.startswith(signature):
                        chunk.extension = extension
                        break

    def un_hash(self, hashtables=None):
        if hashtables == None:
            return

        for chunk in self.chunks:
            chunk.hash = hex_to_name(hashtables, 'hashes.game.txt', chunk.hash)
