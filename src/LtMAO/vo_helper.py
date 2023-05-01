import os
from zipfile import ZipFile
import json
from LtMAO import pyRitoFile, hash_manager


LOG = print
local_dir = './resources/vo_helper'
regions_file = f'{local_dir}/regions.json'
REGIONS = {}


def load_regions():
    global REGIONS
    with open(regions_file, 'r') as f:
        REGIONS = json.load(f)


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
    if info == None:
        raise Exception(
            f'Failed: Read FANTOME: {path}: This file does not contains META/info.json.'
        )
    return info, image, wads


def make_fantome(fantome_name, output_dir, info, image, wads):
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
        parsed.append([wad_name, wad, is_vo])
    # replace region and write using parsed
    for region in REGIONS:
        # replace wad name and chunk hash inside wad
        for id in range(len(parsed)):
            wad_name, wad, is_vo = parsed[id]
            if not is_vo:
                continue
            # replace wad name
            new_wad_name = wad_name.split('.')
            new_wad_name[1] = region
            parsed[id][0] = '.'.join(new_wad_name)
            # replace chunk hash
            for chunk in wad.chunks:
                if 'assets/sounds/wwise2016/vo/' in chunk.hash:
                    chunk_hash = chunk.hash.split('/')
                    chunk_hash[4] = region
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
        path = output_dir + f'/({region}) ' + fantome_name
        write_fantome(path, info, image, wads)
        LOG(f'Done: Make VO Fantomes: {path}')
    hash_manager.CustomHashes.free_wad_hashes()


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
    load_regions()
