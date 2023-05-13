import json
import os
import os.path
import zipfile
import shutil
from LtMAO import hash_manager
from LtMAO import pyRitoFile


def bin_hash(name):
    return f'{pyRitoFile.hash.FNV1a(name):08x}'


LOG = print
cache_dir = f'./prefs/no_skin/_cache'
local_dir = './resources/no_skin'
skips_file = f'{local_dir}/SKIPS.json'
SKIPS = {}
FANTOME_META = {
    'Name': 'NO SKIN',
    'Author': 'tarngaina',
    'Version': '1.0',
    'Description': ''
}
PRE_BIN_HASH = {
    'SkinCharacterDataProperties': bin_hash('SkinCharacterDataProperties'),
    'ResourceResolver': bin_hash('ResourceResolver'),
    'mResourceResolver': bin_hash('mResourceResolver')
}


def delete_cache():
    shutil.rmtree(cache_dir)


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


def parse(champions_dir, output_dir):
    # filter wads
    files = os.listdir(champions_dir)
    wad_files = []
    for file in files:
        if file.endswith('.wad.client') and '_' not in file:
            wad_files.append(os.path.join(
                champions_dir, file).replace('\\', '/'))
    if len(wad_files) == 0:
        raise Exception(
            'no_skin: Failed: Create NO SKIN mod: Invalid Champions folder?')
    LOG(f'no_skin: Running: Create NO SKIN mod')
    swapped_chunks = []  # list of (chunk_hash, chunk_data)
    # read hashes
    hash_manager.read_wad_hashes()
    # rebuild smaller hash for faster comparsion
    LOG(f'no_skin: Running: Rebuilding hashes')
    hashtables = {}
    hashtables['hashes.game.txt'] = {}
    for key, value in hash_manager.HASHTABLES['hashes.game.txt'].items():
        if '.bin' in value and 'data/characters/' in value and '/skins/' in value and 'root.bin' not in value:
            hashtables['hashes.game.txt'][key] = value
    hash_manager.free_wad_hashes()
    # start parsing each wad
    for wad_file in wad_files:
        # read wad
        LOG(f'no_skin: Running: Parse: {wad_file}')
        wad = pyRitoFile.read_wad(wad_file)
        # only unhash skinx.bin with rebuild hashtables
        wad.un_hash(hashtables)
        # init data
        base_bin = {}  # base bin at character
        skin_bins = {}  # skin bins at character
        chunk_hashes = {}  # chunk hash of skins at character
        with wad.stream(wad_file, 'rb') as bs:
            # parse chunks in this wad -> out base_bin and skin_bins
            for chunk in wad.chunks:
                # filter skins bin (only unhash skinx.bin)
                if chunk.extension == 'bin':
                    # chunk.hash = 'data/character/<character>/skins/skinx.bin'
                    temp = chunk.hash.split('/')
                    character = temp[2]
                    skinx = temp[4]
                    # skip?
                    if character in SKIPS:
                        if SKIPS[character] == 'all' or skinx in SKIPS[character]:
                            continue
                    LOG(f'no_skin: Done: Parse: {character} {skinx}')
                    # read chunk
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
            LOG(f'no_skin: Done: Swap: {character}')
    # build new wad from swapped_chunks
    os.makedirs(cache_dir, exist_ok=True)
    wad_file = f'{cache_dir}/Annie.wad.client'
    wad = pyRitoFile.WAD()
    wad.chunks = [pyRitoFile.WADChunk.default()
                  for id in range(len(swapped_chunks))]
    wad.write(wad_file)
    with wad.stream(wad_file, 'rb+') as bs:
        for id, chunk in enumerate(wad.chunks):
            chunk.write_data(
                bs, id, swapped_chunks[id][0], swapped_chunks[id][1])
    # create fantome
    meta_dir = os.path.join(cache_dir, 'META')
    os.makedirs(meta_dir, exist_ok=True)
    info_file = os.path.join(meta_dir, 'info.json')
    with open(info_file, 'w+') as f:
        json.dump(FANTOME_META, f)
    fantome_file = os.path.join(
        output_dir,
        f'{FANTOME_META["Name"]} V{FANTOME_META["Version"]} by {FANTOME_META["Author"]}.fantome'
    )
    with zipfile.ZipFile(fantome_file, 'w') as z:
        z.write(info_file, 'META/info.json')
        z.write(wad_file, 'WAD/Annie.wad.client')
    delete_cache()
    LOG(f'no_skin: Done: Create Fantome: {fantome_file}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
    # ensure folder
    os.makedirs(local_dir, exist_ok=True)
    load_skips()
    save_skips()
