import json, os, os.path, zipfile, shutil, time
from . import hash_helper, pyRitoFile
from .hash_helper import cached_bin_hashes
from threading import Thread

def bin_hash(name):
    return f'{pyRitoFile.helper.FNV1a(name):08x}'


cache_dir = './pref/no_skin/_cache'
local_dir = './res/no_skin'
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
    with open(skips_file, 'r') as f:
        SKIPS = json.load(f)


def save_skips():
    with open(skips_file, 'w+') as f:
        json.dump(SKIPS, f, indent=4)
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
    for key, value in hash_helper.HASHTABLES['hashes.binentries.txt'].items():
        if 'Characters/' in value and '/Skins/' in value:
            if not '/Root' in value:
                if '/Skin0' in value:
                    skin0_hashes[key] = value
                else:
                    otherskins_hashes[key] = value
    hash_helper.CustomHashes.free_hashes('hashes.binentries.txt')
    # read bins
    skin0_bin = pyRitoFile.read_bin(skin0_file)
    otherskins_bins = [pyRitoFile.read_bin(otherskins_file) for otherskins_file in otherskins_files]
    print(f'no_skin: Finish: Read BINs.')
    # skin0 bin
    base_scdp = None
    base_rr = None
    base_mrr = None
    for entry in skin0_bin.entries:
        if entry.type == cached_bin_hashes['SkinCharacterDataProperties']:
            base_scdp = entry
            for field in entry.data:
                if field.hash == cached_bin_hashes['mResourceResolver']:
                    base_mrr = field
                    break
        elif entry.type == cached_bin_hashes['ResourceResolver']:
            base_rr = entry
    if base_scdp.hash not in skin0_hashes:
        raise Exception(f'no_skin: Error: Swap skin: {skin0_file} is not a skin0.bin.')
    # otherskins bin
    for i, otherskins_bin in enumerate(otherskins_bins):
        otherskins_file = otherskins_files[i]
        skin_scdp_hash = None
        skin_rr_hash = None
        for entry in otherskins_bin.entries:
            if entry.type == cached_bin_hashes['SkinCharacterDataProperties']:
                skin_scdp_hash = entry.hash
                for field in entry.data:
                    if field.hash == cached_bin_hashes['mResourceResolver']:
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
        pyRitoFile.write_bin(otherskins_file, skin0_bin)
    print(f'no_skin: Finish: Swap {len(otherskins_files)} skinX as skin0.')


def parse(champions_dir, output_dir, pool_size=4):
    # filter wads
    files = os.listdir(champions_dir)
    wad_files = []
    for file in files:
        if file.endswith('.wad.client') and '_' not in file:
            wad_files.append(os.path.join(
                champions_dir, file).replace('\\', '/'))
    if len(wad_files) == 0:
        raise Exception(
            'no_skin: Error: Create NO SKIN mod: Invalid Champions folder?')
    print(f'no_skin: Start: Create NO SKIN mod')
    swapped_chunks = []  # list of (chunk_hash, chunk_data)
    # read hashes
    hash_helper.read_wad_hashes()
    # rebuild smaller hash for faster comparsion
    print(f'no_skin: Start: Rebuilding hashes')
    hashtables = {}
    hashtables['hashes.game.txt'] = {}
    for key, value in hash_helper.HASHTABLES['hashes.game.txt'].items():
        if '.bin' in value and 'data/characters/' in value and '/skins/' in value and 'root.bin' not in value:
            hashtables['hashes.game.txt'][key] = value
    hash_helper.free_wad_hashes()
    # parse wad func
    def parse_wad(wad_file):    
        # read wad
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
                if entry.type == cached_bin_hashes['SkinCharacterDataProperties']:
                    base_scdp = entry
                    for field in entry.data:
                        if field.hash == cached_bin_hashes['mResourceResolver']:
                            base_mrr = field
                            break
                elif entry.type == cached_bin_hashes['ResourceResolver']:
                    base_rr = entry
            # replace skin_bin hashes on same base_bin
            # each time dump base_bin as chunk_data
            for id, skin_bin in enumerate(skin_bins[character]):
                # find skin scdp + rr hashes first
                skin_scdp_hash = None
                skin_rr_hash = None
                for entry in skin_bin.entries:
                    if entry.type == cached_bin_hashes['SkinCharacterDataProperties']:
                        skin_scdp_hash = entry.hash
                        for field in entry.data:
                            if field.hash == cached_bin_hashes['mResourceResolver']:
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
            print(f'no_skin: Finish: Swap: {character}')
    
    
    # pools stuffs
    pools = [None] * pool_size
    def work_cmd(target, pool_index):
        try:
            target()
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(f'no_skin: Error: {e}')
        pools[pool_index] = None
    # pool start
    target = len(wad_files)
    current = 0
    while current < target:
        for i in range(pool_size):
            if pools[i] == None:
                wad_file = wad_files[current]
                pools[i] = Thread(target=lambda: work_cmd(lambda: parse_wad(wad_file), i), daemon=True)
                pools[i].start()
                current += 1
        time.sleep(0.166)

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
            chunk.free_data()
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
    print(f'no_skin: Finish: Create Fantome: {fantome_file}')


def init():
    # ensure folder
    os.makedirs(local_dir, exist_ok=True)
    load_skips()