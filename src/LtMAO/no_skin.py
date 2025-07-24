import json, os, os.path, zipfile, shutil, time
from . import lepath, hash_helper, pyRitoFile

def bin_hash(name):
    return f'{pyRitoFile.helper.FNV1a(name):08x}'


local_dir = './pref/no_skin'
cache_dir = f'{local_dir}/_cache'
skips_file = f'{local_dir}/SKIPS.json'
SKIPS = {}
FANTOME_META = {
    'Name': 'NO SKIN',
    'Author': 'tarngaina',
    'Version': '1.0',
    'Description': ''
}

def delete_cache():
    shutil.rmtree(cache_dir)


def load_skips():
    global SKIPS
    if os.path.exists(skips_file):
        with open(skips_file, 'r', encoding='utf-8') as f:
            SKIPS = json.load(f)
    else:
        SKIPS = {
            "_comment_general": [
                "Key starts with _ mean comment. What you put in here determine which characters and skins wont become skin0.bin (get skipped).",
                "example: azirsoldier: all mean all skinx.bin of azisoldier wont become skin0.bin."
            ],
            "_azirsoldier": "crash some game for no reason",
            "azirsoldier": "all",
            "_mel": "invisible particles",
            "mel": "all",
            "_aniviaiceblock": "some, but not all walls are invisible",
            "aniviaiceblock": "all",
            "_ekko": "true damage ekko become transparent",
            "ekko": [
                "skin19.bin",
                "skin20.bin",
                "skin21.bin",
                "skin22.bin",
                "skin23.bin",
                "skin24.bin",
                "skin25.bin",
                "skin26.bin",
                "skin27.bin"
            ],
            "_threshlantern": "crash some game for no reason",
            "threshlantern": [
                "skin11.bin"
            ]
        }


def save_skips():
    with open(skips_file, 'w+', encoding='utf-8') as f:
        json.dump(SKIPS, f, indent=4, ensure_ascii=False)
    print(f'no_skin: Finish: Write {skips_file}')


def get_skips():
    return json.dumps(SKIPS, indent=4)


def set_skips(text):
    try:
        global SKIPS
        SKIPS = json.loads(text)
    except:
        raise Exception('no_skin: Error: Set SKIPS: Invalid input.')


def mini_no_skin(skin0_file, otherskins_files):
    # rebuild hashes
    print(f'no_skin: Start: Rebuilding hashes')
    hash_helper.CustomHashes.read_hashes('hashes.binentries.txt')
    skin0_hashes = {}
    otherskins_hashes = {}
    for key, value in hash_helper.Storage.hashtables['hashes.binentries.txt'].items():
        if 'Characters/' in value and '/Skins/' in value:
            if not '/Root' in value:
                if '/Skin0' in value:
                    skin0_hashes[key] = value
                else:
                    otherskins_hashes[key] = value
    hash_helper.CustomHashes.free_hashes('hashes.binentries.txt')
    # read bins
    skin0_bin = pyRitoFile.bin.BIN().read(skin0_file)
    otherskins_bins = [pyRitoFile.bin.BIN().read(otherskins_file) for otherskins_file in otherskins_files]
    print(f'no_skin: Finish: Read BINs.')
    # skin0 bin
    base_scdp = None
    base_rr = None
    base_mrr = None
    for entry in skin0_bin.entries:
        if entry.type == hash_helper.Storage.bin_hashes['SkinCharacterDataProperties']:
            base_scdp = entry
            for field in entry.data:
                if field.hash == hash_helper.Storage.bin_hashes['mResourceResolver']:
                    base_mrr = field
                    break
        elif entry.type == hash_helper.Storage.bin_hashes['ResourceResolver']:
            base_rr = entry
    if base_scdp.hash not in skin0_hashes:
        raise Exception(f'no_skin: Error: Swap skin: {skin0_file} is not a skin0.bin.')
    # otherskins bin
    for i, otherskins_bin in enumerate(otherskins_bins):
        otherskins_file = otherskins_files[i]
        skin_scdp_hash = None
        skin_rr_hash = None
        for entry in otherskins_bin.entries:
            if entry.type == hash_helper.Storage.bin_hashes['SkinCharacterDataProperties']:
                skin_scdp_hash = entry.hash
                for field in entry.data:
                    if field.hash == hash_helper.Storage.bin_hashes['mResourceResolver']:
                        skin_rr_hash = field.data
                        break
                break
        if not skin_scdp_hash in otherskins_hashes:
            print(f'no_skin: Error: Swap skin: {otherskins_file} is not a specific skinX.bin.')
            continue
        # swapping
        base_scdp.hash = skin_scdp_hash
        if base_rr != None:
            base_rr.hash = skin_rr_hash
            base_mrr.data = skin_rr_hash
        # write file
        skin0_bin.write(otherskins_file)
    print(f'no_skin: Finish: Swap {len(otherskins_files)} skinX as skin0.')


def full_no_skin(champions_dir, output_dir):
    start_time = time.time()
    # filter wads
    files = os.listdir(champions_dir)
    wad_files = []
    for file in files:
        if file.endswith('.wad.client') and '_' not in file:
            wad_files.append(lepath.join(
                champions_dir, file))
    if len(wad_files) == 0:
        raise Exception(
            'no_skin: Error: Create NO SKIN mod: Invalid Champions folder?')
    print(f'no_skin: Start: Create NO SKIN mod')
    swapped_chunks = []  # list of (chunk_hash, chunk_data)
    # read hashes
    hash_helper.Storage.read_wad_hashes()
    # rebuild smaller hash for faster comparsion
    print(f'no_skin: Start: Rebuilding hashes')
    hashtables = {}
    hashtables['hashes.game.txt'] = {}
    for key, value in hash_helper.Storage.hashtables['hashes.game.txt'].items():
        if '.bin' in value and 'data/characters/' in value and '/skins/' in value and 'root.bin' not in value:
            hashtables['hashes.game.txt'][key] = value
    hash_helper.Storage.free_wad_hashes()
    # parse wad func
    for wad_file in wad_files:
        # read wad
        wad = pyRitoFile.wad.WAD().read(wad_file)
        # only unhash skinx.bin with rebuild hashtables
        wad.un_hash(hashtables)
        # init data
        base_bin = {}  # base bin at character
        skin_bins = {}  # skin bins at character
        chunk_hashes = {}  # chunk hash of skins at character
        with pyRitoFile.stream.BytesStream.reader(wad_file) as bs:
            # parse chunks in this wad -> out base_bin and skin_bins
            for chunk in wad.chunks:
                # filter skins bin (only unhash skinx.bin)
                if chunk.extension == 'bin':
                    # chunk.hash = 'data/character/{character}/skins/{skinx}'
                    temp = chunk.hash.split('/')
                    character = temp[2]
                    skinx = temp[4]
                    # skip?
                    if character in SKIPS:
                        if SKIPS[character] == 'all' or skinx in SKIPS[character]:
                            continue
                    # read chunk
                    chunk.read_data(bs)
                    bin = pyRitoFile.bin.BIN().read(chunk.data, raw=True)
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
                if entry.type == hash_helper.Storage.bin_hashes['SkinCharacterDataProperties']:
                    base_scdp = entry
                    for field in entry.data:
                        if field.hash == hash_helper.Storage.bin_hashes['mResourceResolver']:
                            base_mrr = field
                            break
                elif entry.type == hash_helper.Storage.bin_hashes['ResourceResolver']:
                    base_rr = entry
            # replace skin_bin hashes on same base_bin
            # each time dump base_bin as chunk_data
            for id, skin_bin in enumerate(skin_bins[character]):
                # find skin scdp + rr hashes first
                skin_scdp_hash = None
                skin_rr_hash = None
                for entry in skin_bin.entries:
                    if entry.type == hash_helper.Storage.bin_hashes['SkinCharacterDataProperties']:
                        skin_scdp_hash = entry.hash
                        for field in entry.data:
                            if field.hash == hash_helper.Storage.bin_hashes['mResourceResolver']:
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
            print(f'no_skin: Finish: {character}: Swap {len(skin_bins[character])} skinX to skin0.')

    # build new wad from swapped_chunks
    os.makedirs(cache_dir, exist_ok=True)
    wad_file = f'{cache_dir}/Zyra.wad.client'
    wad = pyRitoFile.wad.WAD()
    wad.chunks = [pyRitoFile.wad.WADChunk.default()
                  for id in range(len(swapped_chunks))]
    wad.write(wad_file)
    with pyRitoFile.stream.BytesStream.updater(wad_file) as bs:
        for id, chunk in enumerate(wad.chunks):
            chunk.write_data(
                bs, id, swapped_chunks[id][0], swapped_chunks[id][1])
            chunk.free_data()
    # create fantome
    meta_dir = lepath.join(cache_dir, 'META')
    os.makedirs(meta_dir, exist_ok=True)
    info_file = lepath.join(meta_dir, 'info.json')
    with open(info_file, 'w+', encoding='utf-8') as f:
        json.dump(FANTOME_META, f, indent=4, ensure_ascii=False)
    fantome_file = lepath.join(
        output_dir,
        f'{FANTOME_META["Name"]} V{FANTOME_META["Version"]} by {FANTOME_META["Author"]}.fantome'
    )
    with zipfile.ZipFile(fantome_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(info_file, 'META/info.json')
        z.write(wad_file, 'WAD/Annie.wad.client')
    delete_cache()
    end_time = time.time()
    print(f'no_skin: Finish: Create Fantome: {fantome_file} with {end_time-start_time:.2g} seconds')


def init():
    # ensure folder
    os.makedirs(local_dir, exist_ok=True)
    load_skips()