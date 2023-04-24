import json
import pickle
import os
import os.path
from LtMAO import hash_manager
from LtMAO import pyRitoFile


def bin_hash(name):
    return f'{pyRitoFile.hash.FNV1a(name):08x}'


LOG = print
local_dir = './prefs/no_skin'
skips_file = f'{local_dir}/SKIPS.json'
config = {}


def load_skips():
    global config
    with open(skips_file, 'r') as f:
        config = json.load(f)


def save_skips():
    with open(skips_file, 'w+') as f:
        json.dump(config, f, indent=4)


def process(champion_folder):
    # filter wads
    files = os.listdir(champion_folder)
    wad_paths = []
    for file in files:
        if file.endswith('.wad.client') and '_' not in file:
            wad_paths.append(os.path.join(champion_folder, file))

    # list of (chunk_hash, chunk_data)
    chunk_prebuild = []

    hash_manager.read_wad_hashes()
    for wad_path in wad_paths:
        # read wad and unhash
        wad = pyRitoFile.read_wad(wad_path)
        wad.un_hash(hash_manager.HASHTABLES)
        # init data
        base_bin = {}  # base bin at character
        skin_bins = {}  # (chunk_hash, skin bins) at character
        bs = pyRitoFile.io.BinStream(open(wad_path, 'rb'))
        # parse chunks in this wad
        for chunk in wad.chunks:
            # filter skins bin
            if chunk.extension == 'bin':
                if 'data/characters/' in chunk.hash and '/skins/' in chunk.hash:
                    if 'root.bin' not in chunk.hash:
                        # chunk.hash = 'data/character/<char>/skins/...'
                        character = chunk.hash.split('/')[2]
                        chunk.read_data(bs)
                        bin = pyRitoFile.read_bin('', raw=chunk.data)
                        if character not in skin_bins:
                            skin_bins[character] = []
                        if 'skin0.bin' in chunk.hash:
                            base_bin[character] = bin
                        else:
                            skin_bins[character].append((chunk.hash, bin))
                        chunk.free_data()
        bs.close()

        # cache bin hash
        prebuild_bin_hash = {
            'SkinCharacterDataProperties': bin_hash('SkinCharacterDataProperties'),
            'ResourceResolver': bin_hash('ResourceResolver'),
        }
        # swap skins -> add to chunk_prebuild
        for char in base_bin:
            # find base_bin hashes
            base_scdp = None
            base_rr = None
            for entry in base_bin[char].entries:
                if entry.type == prebuild_bin_hash['SkinCharacterDataProperties']:
                    base_scdp = entry
                elif entry.type == prebuild_bin_hash['ResourceResolver']:
                    base_rr = entry
            print(base_scdp, base_rr)
            # replace skin_bin hashes on same base_bin
            # each time dump base_bin as chunk_data
            for chunk_hash, skin_bin in skin_bins[char]:
                skin_scdp_hash = None
                skin_rr_hash = None
                for entry in skin_bin.entries:
                    if entry.type == prebuild_bin_hash['SkinCharacterDataProperties']:
                        skin_scdp_hash = entry.hash
                    if entry.type == prebuild_bin_hash['ResourceResolver']:
                        skin_rr_hash = entry.hash
                base_scdp.hash = skin_scdp_hash
                if base_rr != None:
                    base_rr.hash = skin_rr_hash
                chunk_prebuild.append((
                    chunk_hash,
                    base_bin[char].write('', raw=True)
                ))
                LOG(f'Done: Swap: {chunk_hash}')
        break

    hash_manager.free_wad_hashes()

    # build wad from chunk_prebuild
    wad_path = './prefs/no_skin/Arhi.wad.client'
    wad = pyRitoFile.WAD()
    for id, (chunk_hash, chunk_data) in enumerate(chunk_prebuild):
        # create chunk infos
        chunk = pyRitoFile.WADChunk()
        chunk.build(id, chunk_hash, chunk_data)
        wad.chunks.append(chunk)
    wad.write(wad_path)
    bs = pyRitoFile.io.BinStream(open(wad_path, 'rb+'))
    for id, chunk in enumerate(wad.chunks):
        chunk.write_data(bs, chunk_prebuild[id][1])
    bs.close()


def prepare(_LOG):
    global LOG
    LOG = _LOG
    # ensure folder
    os.makedirs(local_dir, exist_ok=True)
    load_skips()
    save_skips()
