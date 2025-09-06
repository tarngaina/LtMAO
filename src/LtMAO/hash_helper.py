try: 
    import requests
except: 
    print('Warning: hash_helper failed to import requests.')
import os, os.path, json, traceback
from . import lepath, pyRitoFile, setting

def get_hash_separator(filename):
    # space separator in hashes txt
    # use this to skip using split()
    return 16 if filename in WAD_HASHES else 8


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]

class Bin_Hashes(dict):
    def __getitem__(self, key):
        if key in self.keys():
            return super().__getitem__(key)
        else:
            super().__setitem__(key, pyRitoFile.bin.BINHasher.raw_to_hex(key))
            return super().__getitem__(key)


BIN_HASHES = (
    'hashes.binentries.txt',
    'hashes.binhashes.txt',
    'hashes.bintypes.txt',
    'hashes.binfields.txt'
)
WAD_HASHES = (
    'hashes.game.txt',
    'hashes.lcu.txt',
)
ALL_HASHES = BIN_HASHES + WAD_HASHES

class Storage:
    hashtables = {key: {} for key in ALL_HASHES}
    bin_hashes = Bin_Hashes()

    def read_all_hashes(): CustomHashes.read_all_hashes()
    def read_wad_hashes(): CustomHashes.read_wad_hashes()
    def read_bin_hashes(): CustomHashes.read_bin_hashes()
    def free_all_hashes(): CustomHashes.free_all_hashes()
    def free_wad_hashes(): CustomHashes.free_wad_hashes()
    def free_bin_hashes(): CustomHashes.free_bin_hashes()


class CDTBHashes:
    # for syncing CDTB hashes
    local_dir = './pref/hashes/cdtb_hashes'

    def local_file(filename):
        return f'{CDTBHashes.local_dir}/{filename}'

    def remote_file(filename):
        # return f'https://raw.githubusercontent.com/CommunityDragon/CDTB/master/cdragontoolbox/{filename}'
        return f'https://raw.communitydragon.org/data/hashes/lol/{filename}'
    
    def calculate_size():
        total_size = 0
        for root, dirs, files in os.walk(CDTBHashes.local_dir):
            for file in files:
                total_size += os.path.getsize(lepath.join(root, file))
        return to_human(total_size)

    etag_path = f'{local_dir}/etag.json'
    ETAG = {}

    @staticmethod
    def sync_hashes(*filenames):
        for filename in filenames:
            try:
                local_file = CDTBHashes.local_file(filename)
                remote_file = CDTBHashes.remote_file(filename)
                # GET request
                get = requests.get(remote_file, stream=True)
                get.raise_for_status()
                # get etag and compare, new etag = sync
                etag_local = CDTBHashes.ETAG.get(filename, None)
                etag_remote = get.headers['ETag']
                if etag_local == None or etag_local != etag_remote or not os.path.exists(local_file):
                    # set etag
                    CDTBHashes.ETAG[filename] = etag_remote
                    # download file
                    bytes_downloaded = 0
                    chunk_size = 1024**2*5
                    bytes_downloaded_log = 0
                    bytes_downloaded_log_limit = 1024**2
                    with open(local_file, 'wb') as f:
                        for chunk in get.iter_content(chunk_size):
                            chunk_length = len(chunk)
                            bytes_downloaded += chunk_length
                            f.write(chunk)
                            bytes_downloaded_log += chunk_length
                            if bytes_downloaded_log > bytes_downloaded_log_limit:
                                print(
                                    f'hash_helper: Downloading: {remote_file}: {to_human(bytes_downloaded)}')
                                bytes_downloaded_log = 0
                print(f'hash_helper: Finish: Sync hash: {local_file}')
            except Exception as e:
                print(f'hash_helper: Error: Sync hash: {filename}: {e}')
                print(traceback.format_exc())
            CustomHashes.combine_custom_hashes(filename)
        print(f'hash_helper: Finish: Sync all hashes.')

    @staticmethod
    def sync_all():
        # read etags
        CDTBHashes.ETAG = {}
        if os.path.exists(CDTBHashes.etag_path):
            with open(CDTBHashes.etag_path, 'r', encoding='utf-8') as f:
                CDTBHashes.ETAG = json.load(f)
        CDTBHashes.sync_hashes(*ALL_HASHES)
        # write etags
        with open(CDTBHashes.etag_path, 'w+', encoding='utf-8') as f:
            json.dump(CDTBHashes.ETAG, f, indent=4, ensure_ascii=False)


class ExtractedHashes:
    # extracted hash
    local_dir = './pref/hashes/extracted_hashes'

    def local_file(filename): 
        return f'{ExtractedHashes.local_dir}/{filename}'

    @staticmethod
    def calculate_size():
        total_size = 0
        for root, dirs, files in os.walk(ExtractedHashes.local_dir):
            for file in files:
                total_size += os.path.getsize(lepath.join(root, file))
        return to_human(total_size)
    
    @staticmethod
    def clear_extract_hashes(*filenames):
        for filename in filenames:
            eh_file = ExtractedHashes.local_file(filename)
            if os.path.exists(eh_file):
                os.remove(lepath.abs(eh_file))
        print('hash_helper: Finish: Clear Extract Hashes.')
    
    @staticmethod
    def extract(*file_paths):
        wad_hash = pyRitoFile.wad.WADHasher.raw_to_hex
        start_game_path = [
            'assets/', 
            'clientstates/',
            'data/',
            'levels/',
            'maps/',
            'uiautoatlas/',
            'ux/'
        ]

        hashtables = {
            'hashes.binentries.txt': {},
            'hashes.binhashes.txt': {},
            'hashes.game.txt': {}
        }
        def extract_skn(path, raw=False):
            try:
                # extract submesh hash <-> submesh name
                skn = pyRitoFile.skn.SKN().read(path, raw)
                for submesh in skn.submeshes:
                    hashtables['hashes.binhashes.txt'][submesh.bin_hash] = submesh.name
                    print(f'hash_helper: Finish: Extract: {submesh.name}')
            except Exception as e:
                print(f'hash_helper: Error: {e}')
                print(traceback.format_exc())
                

        def extract_skl(path, raw=False):
            try:
                # extract joint hash <-> joint name
                skl = pyRitoFile.skl.SKL().read(path, raw)
                for joint in skl.joints:
                    hashtables['hashes.binhashes.txt'][joint.bin_hash] = joint.name
                    print(f'hash_helper: Finish: Extract: {joint.name}')
            except Exception as e:
                print(f'hash_helper: Error: {e}')
                print(traceback.format_exc())

        def extract_bin(path, raw=False):
            def extract_file_value(value, value_type):
                if value_type == pyRitoFile.bin.BINType.STRING:
                    value = value.lower()
                    if any(value.startswith(prefix) for prefix in start_game_path):
                        hashtables['hashes.game.txt'][wad_hash(
                            value)] = value
                        print(f'hash_helper: Finish: Extract: {value}')
                        if value.endswith('.dds'):
                            temp = value.split('/')
                            basename = temp[-1]
                            dirname = '/'.join(temp[:-1])
                            value2x = f'{dirname}/2x_{basename}'
                            value4x = f'{dirname}/4x_{basename}'
                            hashtables['hashes.game.txt'][wad_hash(
                                value2x)] = value2x
                            hashtables['hashes.game.txt'][wad_hash(
                                value4x)] = value4x
                        elif value.endswith('.bin'):
                            valuepy = lepath.ext(value, '.bin', '.py')
                            hashtables['hashes.game.txt'][wad_hash(valuepy)] = valuepy
                elif value_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                    for v in value.data:
                        extract_file_value(v, value_type)
                elif value_type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                    if value.data != None:
                        for f in value.data:
                            extract_file_field(f)

            def extract_file_field(field):
                if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                    for v in field.data:
                        extract_file_value(v, field.value_type)
                elif field.type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                    if field.data != None:
                        for f in field.data:
                            extract_file_field(f)
                elif field.type == pyRitoFile.bin.BINType.MAP:
                    for key, value in field.data.items():
                        extract_file_value(key, field.key_type)
                        extract_file_value(value, field.value_type)
                elif field.type == pyRitoFile.bin.BINType.OPTION and field.value_type == pyRitoFile.bin.BINType.STRING:
                    if field.data != None:
                        extract_file_value(field.data, field.value_type)
                else:
                    extract_file_value(field.data, field.type)

            try:
                bin = pyRitoFile.bin.BIN().read(path, raw)
                # extract VfxSystemDefinitionData <-> particlePath
                VfxSystemDefinitionDatas = bin.get_items(lambda entry: entry.type == Storage.bin_hashes['VfxSystemDefinitionData'])
                for VfxSystemDefinitionData in VfxSystemDefinitionDatas:
                    particlePaths = VfxSystemDefinitionData.get_items(lambda field: field.hash == Storage.bin_hashes['particlePath'])
                    if len(particlePaths) > 0:
                        hashtables['hashes.binentries.txt'][VfxSystemDefinitionData.hash] = particlePaths[0].data
                        print(f'hash_helper: Finish: Extract: {particlePaths[0].data}')
                # extract StaticMaterialDef <-> name
                StaticMaterialDefs = bin.get_items(lambda entry: entry.type == Storage.bin_hashes['StaticMaterialDef'])
                for StaticMaterialDef in StaticMaterialDefs:
                    names = StaticMaterialDef.get_items(lambda field: field.hash == Storage.bin_hashes['name'])
                    if len(names) > 0:
                        hashtables['hashes.binentries.txt'][StaticMaterialDef.hash] = names[0].data
                        print(f'hash_helper: Finish: Extract: {names[0].data}')
                # extract file hashes
                for entry in bin.entries:
                    for field in entry.data:
                        extract_file_field(field)
                for link in bin.links:
                    extract_file_value(link, pyRitoFile.bin.BINType.STRING)
            except Exception as e:
                print(f'hash_helper: Error: {e}')
                print(traceback.format_exc())
                
        def extract_wad(path):
            wad = pyRitoFile.wad.WAD().read(path)
            with pyRitoFile.stream.BytesStream.reader(path) as bs:
                for chunk in wad.chunks:
                    chunk.read_data(bs)
                    if chunk.extension == 'skn':
                        extract_skn(chunk.data, raw=True)
                    elif chunk.extension == 'skl':
                        extract_skl(chunk.data, raw=True)
                    elif chunk.extension == 'bin':
                        extract_bin(chunk.data, raw=True)
                    chunk.free_data()
            

        # extract hashes base on file types
        for file_path in file_paths:
            if file_path.endswith('.wad.client'):
                extract_wad(file_path)
            elif file_path.endswith('.skn'):
                extract_skn(file_path)
            elif file_path.endswith('.skl'):
                extract_skl(file_path)
            elif file_path.endswith('.bin'):
                extract_bin(file_path)
        # write out hashes txt
        for filename, hashtable in hashtables.items():
            local_file = ExtractedHashes.local_file(filename)
            sep = get_hash_separator(filename)
            # read existed extracted hashes
            if os.path.exists(local_file):
                with open(local_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        hashtable[line[:sep]] = line[sep+1:-1]
            # write
            with open(local_file, 'w+', encoding='utf-8') as f:
                f.writelines(
                    f'{key} {value}\n'
                    for key, value in sorted(
                        hashtable.items(), key=lambda item: item[1]
                    )
                )
            print(f'hash_helper: Finish: Extract: {local_file}')
            CustomHashes.combine_custom_hashes(filename)


class CustomHashes:
    # combine with CDTB and extracted hashes
    # use for all functions in this app
    local_dir = './pref/hashes/custom_hashes'

    def local_file(filename): 
        return f'{CustomHashes.local_dir}/{filename}'
    
    def calculate_size():
        total_size = 0
        for root, dirs, files in os.walk(CustomHashes.local_dir):
            for file in files:
                total_size += os.path.getsize(lepath.join(root, file))
        return to_human(total_size)

    @staticmethod
    def read_hashes(*filenames):
        for filename in filenames:
            local_file = CustomHashes.local_file(filename)
            # safe check
            if os.path.exists(local_file):
                # read hashes
                with open(local_file, 'r', encoding='utf-8') as f:
                    sep = get_hash_separator(filename)
                    for line in f:
                        Storage.hashtables[filename][line[:sep]] = line[sep+1:-1]

    @staticmethod
    def write_hashes(*filenames):
        for filename in filenames:
            local_file = CustomHashes.local_file(filename)
            # write combined hashes
            with open(local_file, 'w+', encoding='utf-8') as f:
                f.writelines(
                    f'{key} {value}\n'
                    for key, value in sorted(
                        Storage.hashtables[filename].items(), key=lambda item: item[1]
                    )
                )

    @staticmethod
    def read_bin_hashes():
        CustomHashes.read_hashes(*BIN_HASHES)

    @staticmethod
    def read_wad_hashes():
        CustomHashes.read_hashes(*WAD_HASHES)

    @staticmethod
    def read_all_hashes():
        CustomHashes.read_hashes(*ALL_HASHES)

    @staticmethod
    def free_hashes(*filenames):
        for filename in filenames:
            Storage.hashtables[filename] = {}

    @staticmethod
    def free_bin_hashes(*filenames):
        CustomHashes.free_hashes(*BIN_HASHES)

    @staticmethod
    def free_wad_hashes(*filenames):
        CustomHashes.free_hashes(*WAD_HASHES)

    @staticmethod
    def free_all_hashes():
        CustomHashes.free_hashes(*ALL_HASHES)

    @staticmethod
    def combine_custom_hashes(*filenames):
        for filename in filenames:
            hashtable = {}
            cdtb_file = CDTBHashes.local_file(filename)
            ex_file = ExtractedHashes.local_file(filename)
            ch_file = CustomHashes.local_file(filename)
            sep = get_hash_separator(filename)
            # read cdtb hashes
            if os.path.exists(cdtb_file):
                with open(cdtb_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        hashtable[line[:sep]] = line[sep+1:-1]
            # read extracted hashes
            if os.path.exists(ex_file):
                with open(ex_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        hashtable[line[:sep]] = line[sep+1:-1]
            # read existed custom hashes
            if os.path.exists(ch_file):
                with open(ch_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        hashtable[line[:sep]] = line[sep+1:-1]
            # write combined hashes
            with open(ch_file, 'w+', encoding='utf-8') as f:
                f.writelines(
                    f'{key} {value}\n'
                    for key, value in sorted(
                        hashtable.items(), key=lambda item: item[1]
                    )
                )
            print(f'hash_helper: Finish: Update: {ch_file}')

    @staticmethod
    def reset_custom_hashes(*filenames):
        for filename in filenames:
            cdtb_file = CDTBHashes.local_file(filename)
            ch_file = CustomHashes.local_file(filename)
            # copy file from cdtb
            with open(cdtb_file, 'rb') as f:
                data = f.read()
            with open(ch_file, 'wb+') as f:
                f.write(data)
        print('hash_helper: Finish: Reset Custom Hashes to CDTB Hashes.')

def init():
    # load setting first
    CDTBHashes.local_dir = setting.get('CDTBHashes.local_dir', CDTBHashes.local_dir)
    ExtractedHashes.local_dir = setting.get('ExtractedHashes.local_dir', ExtractedHashes.local_dir)
    CustomHashes.local_dir = setting.get('CustomHashes.local_dir', CustomHashes.local_dir)
    # ensure folder
    os.makedirs(CDTBHashes.local_dir, exist_ok=True)
    os.makedirs(ExtractedHashes.local_dir, exist_ok=True)
    os.makedirs(CustomHashes.local_dir, exist_ok=True)
