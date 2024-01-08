import os
from zipfile import ZipFile
import json
from . import pyRitoFile, hash_manager


LOG = print
local_dir = './resources/vo_helper'
langs_file = f'{local_dir}/langs.json'
LANGS = {}


def load_langs():
    global LANGS
    with open(langs_file, 'r') as f:
        LANGS = json.load(f)


def scan_fantome(path):
    info, image, wads = None, False, []
    with ZipFile(path, 'r') as zip:
        names = zip.namelist()
        for name in names:
            if name == 'META/info.json':
                info = json.loads(zip.read(name))
            elif name == 'META/image.png':
                image = True
            elif name.startswith('WAD/'):
                wads.append(name)
    if info == None:
        raise Exception(
            f'vo_helper: Failed: Scan FANTOME: {path}: This file does not contains META/info.json.'
        )
    return info, image, wads


def read_fantome(path):
    info, image, wads = None, None, []
    with ZipFile(path, 'r') as zip:
        names = zip.namelist()
        for name in names:
            if name == 'META/info.json':
                info = json.loads(zip.read(name))
            elif name == 'META/image.png':
                image = zip.read(name)
            elif name.startswith('WAD/'):
                wads.append([name, zip.read(name)])
    return info, image, wads


def make_fantome(fantome_name, output_dir, info, image, wads, langs):
    hash_manager.CustomHashes.read_wad_hashes()
    # read vo wads first
    parsed = []
    for wad_name, wad_data in wads:
        wad = None
        is_vo = '_' in wad_name
        if is_vo:
            wad = pyRitoFile.read_wad('', raw=wad_data)
            wad.un_hash(hash_manager.HASHTABLES)
            with wad.stream('', 'rb', raw=wad_data) as bs:
                for chunk in wad.chunks:
                    chunk.read_data(bs)
            LOG(f'vo_helper: Done: Prepare VO WAD: {wad_name}')
        parsed.append([wad_name, wad, is_vo])
    # replace lang and write using parsed
    for lang in langs:
        # replace wad name and chunk hash inside wad
        for id in range(len(parsed)):
            wad_name, wad, is_vo = parsed[id]
            if not is_vo:
                continue
            # replace wad name
            new_wad_name = wad_name.split('.')
            new_wad_name[1] = lang
            parsed[id][0] = '.'.join(new_wad_name)
            # replace chunk hash
            for chunk in wad.chunks:
                if 'assets/sounds/wwise2016/vo/' in chunk.hash:
                    chunk_hash = chunk.hash.split('/')
                    chunk_hash[4] = lang
                    chunk.hash = '/'.join(chunk_hash)
        # convert parsed to wads
        for id in range(len(parsed)):
            wad_name, wad, is_vo = parsed[id]
            if not is_vo:
                continue
            wad_data = wad.write('', raw=True)
            with wad.stream('', 'rb+', raw=wad_data) as bs:
                for chunk in wad.chunks:
                    chunk.write_data(bs, chunk.id, chunk.hash, chunk.data)
                wad_data = bs.raw()
            wads[id] = wad_name, wad_data
        # write fantome out
        path = output_dir + f'/({lang}) ' + fantome_name
        write_fantome(path, info, image, wads)
        LOG(f'vo_helper: Done: Remake Fantomes: {path}')
    hash_manager.CustomHashes.free_wad_hashes()
    LOG(f'vo_helper: Done: Remake All Fantomes.')


def write_fantome(path, info, image, wads):
    with ZipFile(path, 'w') as zip:
        zip.writestr('META/info.json', json.dumps(info).encode('utf-8'))
        if image != None:
            zip.writestr('META/image.png', image)
        for wad_name, wad_data in wads:
            zip.writestr(wad_name, wad_data)


def prepare(_LOG):
    global LOG
    LOG = _LOG
    os.makedirs(local_dir, exist_ok=True)
    load_langs()
