import json
import os
import os.path
from LtMAO import hash_manager
from LtMAO import pyRitoFile
import threading
import time

tk_widget = None


def bin_hash(name):
    return f'{pyRitoFile.hash.FNV1a(name):08x}'


PRE_BIN_HASH = {
    'SkinCharacterDataProperties': bin_hash('SkinCharacterDataProperties'),
    'ResourceResolver': bin_hash('ResourceResolver'),
    'mResourceResolver': bin_hash('mResourceResolver')
}


LOG = print
local_dir = './resources/no_skin'
skips_file = f'{local_dir}/SKIPS.json'
SKIPS = {}


def load_skips():
    global SKIPS
    with open(skips_file, 'r') as f:
        SKIPS = json.load(f)


def save_skips():
    with open(skips_file, 'w+') as f:
        json.dump(SKIPS, f, indent=4)


def get_skips():
    return json.dumps(SKIPS, indent=4)


def set_skips(text):
    try:
        global SKIPS
        SKIPS = json.loads(text)
    except:
        raise Exception('Failed: Update SKIPS: Invalid input.')


def parse(champion_folder):
    # filter wads
    files = os.listdir(champion_folder)
    wad_paths = []
    for file in files:
        if file.endswith('.wad.client') and '_' not in file:
            wad_paths.append(os.path.join(
                champion_folder, file).replace('\\', '/'))
    if len(wad_paths) == 0:
        raise Exception(
            'Failed: Create NO SKIN mod: Invalid Champions folder?')
    LOG(f'Running: Create NO SKIN mod')
    swapped_chunks = []
    # read hashes
    hash_manager.read_wad_hashes()
    for wad_path in wad_paths:
        # read wad
        LOG(f'Running: Parse: {wad_path}')
        wad = pyRitoFile.read_wad(wad_path)
        wad.un_hash(hash_manager.HASHTABLES)
        # init data
        base_bin = {}  # base bin at character
        skin_bins = {}  # skin bins at character
        chunk_hashes = {}  # chunk hash of skins at character
        bs = pyRitoFile.io.BinStream(open(wad_path, 'rb'))
        # parse chunks in this wad -> out base_bin and skin_bins
        for chunk in wad.chunks:
            # filter skins bin
            if chunk.extension == 'bin':
                if 'data/characters/' in chunk.hash and '/skins/' in chunk.hash:
                    if 'root.bin' not in chunk.hash:
                        # chunk.hash = 'data/character/<character>/skins/skinx.bin'
                        temp = chunk.hash.split('/')
                        character = temp[2]
                        skinx = temp[4]
                        # skip?
                        if character in SKIPS:
                            if SKIPS[character] == 'all' or skinx in SKIPS[character]:
                                continue
                        LOG(f'Done: Parse: {character} {skinx}')
                        chunk.read_data(bs)
                        bin = pyRitoFile.read_bin('', raw=chunk.data)
                        chunk.free_data()
                        if 'skin0.bin' in chunk.hash:
                            # found base bin
                            base_bin[character] = bin
                        else:
                            # found skin bin
                            if character not in skin_bins:
                                skin_bins[character] = []
                            skin_bins[character].append(bin)
                            # found chunk hash of skin bin
                            if character not in chunk_hashes:
                                chunk_hashes[character] = []
                            chunk_hashes[character].append(chunk.hash)
        bs.close()
        # swap skins -> save by chunk
        for character in base_bin:
            # there is character that only has skin0.bin, skip them
            if character not in skin_bins:
                continue
            # find base_bin hashes
            base_scdp = None
            base_rr = None
            base_mrr = None
            for entry in base_bin[character].entries:
                if entry.type == PRE_BIN_HASH['SkinCharacterDataProperties']:
                    base_scdp = entry
                    for field in entry.data:
                        if field.hash == PRE_BIN_HASH['mResourceResolver']:
                            base_mrr = field
                            break
                elif entry.type == PRE_BIN_HASH['ResourceResolver']:
                    base_rr = entry
            # replace skin_bin hashes on same base_bin
            # each time dump base_bin as chunk_data
            for id, skin_bin in enumerate(skin_bins[character]):
                # find skin scdp + rr hashes first
                skin_scdp_hash = None
                skin_rr_hash = None
                for entry in skin_bin.entries:
                    if entry.type == PRE_BIN_HASH['SkinCharacterDataProperties']:
                        skin_scdp_hash = entry.hash
                        for field in entry.data:
                            if field.hash == PRE_BIN_HASH['mResourceResolver']:
                                skin_rr_hash = field.data
                                break
                        break
                # swapping
                base_scdp.hash = skin_scdp_hash
                if base_rr != None:
                    base_rr.hash = skin_rr_hash
                    base_mrr.data = skin_rr_hash

                # create WAD chunk
                swapped_chunks.append(
                    (chunk_hashes[character][id], base_bin[character].write('', raw=True)))
            LOG(f'Done: Swap: {character}')
    hash_manager.free_wad_hashes()
    # build wad from swapped_chunks
    out_wad_path = './prefs/no_skin/Annie.wad.client'
    out_wad = pyRitoFile.WAD()
    for id in range(len(swapped_chunks)):
        # create chunk infos
        chunk = pyRitoFile.WADChunk()
        chunk.id = id
        chunk.hash = swapped_chunks[id][0]
        chunk.duplicated = False
        chunk.subchunk_start = 0
        chunk.subchunk_count = 0
        out_wad.chunks.append(chunk)
    # write wad info
    wad.write(out_wad_path)
    # write chunk data
    bs = pyRitoFile.io.BinStream(open(out_wad_path, 'rb+'))
    for id, chunk in enumerate(wad.chunks):
        chunk.write_data(bs, swapped_chunks[id][1])
    bs.close()


def prepare(_LOG):
    global LOG
    LOG = _LOG
    # ensure folder
    os.makedirs(local_dir, exist_ok=True)
    load_skips()
    save_skips()
