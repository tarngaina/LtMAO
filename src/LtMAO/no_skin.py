import json
import pickle
import os
import os.path
from LtMAO import hash_manager
from LtMAO.pyRitoFile import read_wad, read_bin
from LtMAO.pyRitoFile.hash import FNV1a


def bin_hash(name):
    return f'{FNV1a(name):08x}'


LOG = print
config_file = './prefs/no_skin/config.json'
config = {}


def load_config():
    global config
    with open(config_file, 'r') as f:
        config = json.load(f)


def save_config():
    with open(config_file, 'w+') as f:
        json.dump(config, f, indent=4)


def start(champion_folder):
    # filter wads
    files = os.listdir(champion_folder)
    wad_paths = []
    for file in files:
        if file.endswith('.wad.client') and '_' not in file:
            wad_paths.append(file)

    hash_manager.read_wad_hashes()
    for wad_path in wad_paths:
        # read wad and unhash
        wad = read_wad(wad_path)
        wad.un_hash(hash_manager.HASHTABLES)

        # filter skins bins
        base_bin = None
        skin_bins = []
        for chunk in wad.chunks:
            if chunk.extension == 'bin':
                if 'data/character/' in chunk.hash and '/skins/' in chunk.hash:
                    if 'root.bin' not in chunk.hash:
                        chunk.read_data()
                        bin = read_bin('', raw=chunk.data)
                        if 'skin0.bin' in chunk.hash:
                            base_bin = bin
                        else:
                            skin_bins.append(base_bin)
                        chunk.free_data()

        # find base_bin hashes
        base_rr = next(
            (
                entry
                for entry in skin_bin.entries
                if entry.type == bin_hash('ResourceResolver')
            )
        )
        # replace skin_bin
        for skin_bin in skin_bins:
            skin_scdp_hash = next(
                (
                    entry.hash
                    for entry in skin_bin.entries
                    if entry.type == bin_hash('SkinCharacterDataProperties')
                )
            )
            skin_rr_hash = next(
                (
                    entry.hash
                    for entry in skin_bin.entries
                    if entry.type == bin_hash('ResourceResolver')
                )
            )
            if skin_scdp_hash == None:
                # invalid bins?
                continue
            # deepcopy base_bin -> skin_bin
            skin_bin = pickle.loads(pickle.dumps(base_bin))
            # now that skin_bin is base_bin
            # replace old skin_bin hash to this skin_bin
            skin_bin.hash = skin_scdp_hash
            if base_rr != None:
                skin_bin.hash = skin_rr_hash

    hash_manager.free_wad_hashes()


def prepare(_LOG):
    global LOG
    LOG = _LOG
    load_config()
    save_config()
