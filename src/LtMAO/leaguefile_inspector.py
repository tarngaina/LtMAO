from LtMAO import pyRitoFile
from LtMAO import hash_manager
from LtMAO import ext_tools
import os

LOG = print


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


def guess_extension(path):
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

    with open(path, 'rb') as f:
        data = f.read(100)
    for signature, extension in signature_to_extension.items():
        if data.startswith(signature):
            return extension
    if len(data) > 8:
        if data[4:8] == bytes.fromhex('c34ffd22'):
            return 'skl'


def read_lfi(path, hashtables=None):
    json = None
    with open(path, 'rb') as f:
        data = f.read(100)
    ftype = pyRitoFile.guess_extension(data)
    try:
        if ftype == 'skl':
            obj = pyRitoFile.read_skl(path)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            json = pyRitoFile.to_json(obj)
        elif ftype == 'skn':
            obj = pyRitoFile.read_skn(path)
            LOG(f'Done: File Inspector: Read SKN: {path}')
            json = pyRitoFile.to_json(obj)
        elif ftype == 'sco':
            obj = pyRitoFile.read_sco(path)
            LOG(f'Done: File Inspector: Read SCO: {path}')
            json = pyRitoFile.to_json(obj)
        elif ftype == 'scb':
            obj = pyRitoFile.read_scb(path)
            LOG(f'Done: File Inspector: Read SCB: {path}')
            json = pyRitoFile.to_json(obj)
        elif ftype == 'bin':
            obj = pyRitoFile.read_bin(path)
            obj.un_hash(hashtables)
            LOG(f'Done: File Inspector: Read BIN: {path}')
            json = pyRitoFile.to_json(obj)
        elif ftype == 'wad':
            obj = pyRitoFile.read_wad(path)
            obj.un_hash(hashtables)
            # read chunk data to guess extension (incase poor unhash)
            with obj.stream(path, 'rb') as bs:
                for chunk in obj.chunks:
                    chunk.read_data(bs)
                    chunk.free_data()
            LOG(f'Done: File Inspector: Read WAD: {path}')
            json = pyRitoFile.to_json(obj)
        else:
            LOG(f'Failed: File Inspector: Read: {path}: Unknown file type')
    except Exception as e:
        LOG(f'Failed: File Inspector: Read: {path}: {e}')
    return path, to_human(os.stat(path).st_size), ftype, json


def read_ritobin(path):
    json = None
    try:
        p = ext_tools.RITOBIN.run(
            src=path,
            dir_hashes=hash_manager.CustomHashes.local_dir
        )
        if p.returncode != 0:
            raise Exception('Failed to read with ritobin.')
        py_file = '.'.join(path.split('.bin')[:-1]) + '.py'
        with open(py_file, 'r') as f:
            json = f.read()
        os.remove(py_file)
        LOG(f'Done: File Inspector: Read BIN: {path}')
    except Exception as e:
        LOG(f'Failed: File Inspector: Read Ritobin: {path}: {e}')
    return path, to_human(os.stat(path).st_size), 'bin', json


def prepare(_LOG):
    global LOG
    LOG = _LOG
