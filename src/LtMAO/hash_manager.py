import requests
import os
import os.path
import json
from threading import Thread
import traceback
from . import pyRitoFile, setting

LOG = print
BIN_HASHES = (
    'hashes.binentries.txt',
    'hashes.binfields.txt',
    'hashes.bintypes.txt',
    'hashes.binhashes.txt'
)
WAD_HASHES = (
    'hashes.game.txt',
    'hashes.lcu.txt',
)
ALL_HASHES = BIN_HASHES + WAD_HASHES
HASHTABLES = {key: {} for key in ALL_HASHES}


def read_all_hashes(): CustomHashes.read_all_hashes()
def read_wad_hashes(): CustomHashes.read_wad_hashes()
def read_bin_hashes(): CustomHashes.read_bin_hashes()
def free_all_hashes(): CustomHashes.free_all_hashes()
def free_wad_hashes(): CustomHashes.free_wad_hashes()
def free_bin_hashes(): CustomHashes.free_bin_hashes()

class CACHED_BIN_HASHES(dict):
    def __getitem__(self, key):
        if key in self.keys():
            return super().__getitem__(key)
        else:
            super().__setitem__(key, pyRitoFile.bin_hash(key))
            return super().__getitem__(key)
        
cached_bin_hashes = CACHED_BIN_HASHES()

def HASH_SEPARATOR(filename):
    # space separator in hashes txt
    # use this to skip using split()
    return 16 if filename in WAD_HASHES else 8


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


class CDTBHashes:
    # for syncing CDTB hashes
    local_dir = './prefs/hashes/cdtb_hashes'

    def local_file(filename):
        return f'{CDTBHashes.local_dir}/{filename}'

    def remote_file(filename):
        # return f'https://raw.githubusercontent.com/CommunityDragon/CDTB/master/cdragontoolbox/{filename}'
        return f'https://raw.communitydragon.org/data/hashes/lol/{filename}'

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
                                LOG(
                                    f'hash_manager: Downloading: {remote_file}: {to_human(bytes_downloaded)}')
                                bytes_downloaded_log = 0
                LOG(f'hash_manager: Done: Sync hash: {local_file}')
            except Exception as e:
                LOG(f'hash_manager: Failed: Sync hash: {filename}: {e}')
                LOG(traceback.format_exc())
            combine_custom_hashes(filename)
        LOG(f'hash_manager: Done: Sync all hashes.')

    @staticmethod
    def sync_all():
        # read etags
        CDTBHashes.ETAG = {}
        if os.path.exists(CDTBHashes.etag_path):
            with open(CDTBHashes.etag_path, 'r') as f:
                CDTBHashes.ETAG = json.load(f)
        CDTBHashes.sync_hashes(*ALL_HASHES)
        # write etags
        with open(CDTBHashes.etag_path, 'w+') as f:
            json.dump(CDTBHashes.ETAG, f, indent=4)


class ExtractedHashes:
    # extracted hash
    local_dir = './prefs/hashes/extracted_hashes'
    def local_file(filename): return f'{ExtractedHashes.local_dir}/{filename}'

    def extract(*file_paths):
        wad_hash = pyRitoFile.wad_hash

        hashtables = {
            'hashes.binentries.txt': {},
            'hashes.binhashes.txt': {},
            'hashes.game.txt': {}
        }
        def extract_skn(file_path, raw=None):
            try:
                # extract submesh hash <-> submesh name
                if raw == None:
                    skn = pyRitoFile.read_skn(file_path)
                else:
                    skn = pyRitoFile.read_skn('', raw)
                for submesh in skn.submeshes:
                    hashtables['hashes.binhashes.txt'][submesh.bin_hash] = submesh.name
                LOG(f'hash_manager: Done: Extract Hashes: {file_path}')
            except Exception as e:
                LOG(f'hash_manager: Failed: Extract Hashes: {file_path}: {e}')
                LOG(traceback.format_exc())

        def extract_skl(file_path, raw=None):
            try:
                # extract joint hash <-> joint name
                if raw == None:
                    skl = pyRitoFile.read_skl(file_path)
                else:
                    skl = pyRitoFile.read_skl('', raw)
                for joint in skl.joints:
                    hashtables['hashes.binhashes.txt'][joint.bin_hash] = joint.name
                LOG(f'hash_manager: Done: Extract Hashes: {file_path}')
            except Exception as e:
                LOG(f'hash_manager: Failed: Extract Hashes: {file_path}: {e}')
                LOG(traceback.format_exc())

        def extract_bin(file_path, raw=None):
            def extract_file_value(value, value_type):
                if value_type == pyRitoFile.BINType.String:
                    value = value.lower()
                    if 'assets/' in value or 'data/' in value:
                        hashtables['hashes.game.txt'][wad_hash(
                            value)] = value
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
                elif value_type in (pyRitoFile.BINType.List, pyRitoFile.BINType.List2):
                    for v in value.data:
                        extract_file_value(v, value_type)
                elif value_type in (pyRitoFile.BINType.Embed, pyRitoFile.BINType.Pointer):
                    for f in value.data:
                        extract_file_field(f)

            def extract_file_field(field):
                if field.type in (pyRitoFile.BINType.List, pyRitoFile.BINType.List2):
                    for v in field.data:
                        extract_file_value(v, field.value_type)
                elif field.type in (pyRitoFile.BINType.Embed, pyRitoFile.BINType.Pointer):
                    for f in field.data:
                        extract_file_field(f)
                elif field.type == pyRitoFile.BINType.Map:
                    for key, value in field.data.items():
                        extract_file_value(key, field.key_type)
                        extract_file_value(value, field.value_type)
                else:
                    extract_file_value(field.data, field.type)

            try:
                if raw == None:
                    bin = pyRitoFile.read_bin(file_path)
                else:
                    bin = pyRitoFile.read_bin('', raw)
                for entry in bin.entries:
                    # extract VfxSystemDefinitionData <-> particlePath
                    if entry.type == cached_bin_hashes['VfxSystemDefinitionData']:
                        particlePath = pyRitoFile.BINHelper.find_item(
                            items=entry.data,
                            compare_func=lambda field: field.hash == cached_bin_hashes['particlePath']
                        )
                        if particlePath != None:
                            hashtables['hashes.binentries.txt'][entry.hash] = particlePath.data
                    # extract StaticMaterialDef <-> name
                    elif entry.type == cached_bin_hashes['StaticMaterialDef']:
                        name = pyRitoFile.BINHelper.find_item(
                            items=entry.data,
                            compare_func=lambda field: field.hash == cached_bin_hashes['name']
                        )
                        if name != None:
                            hashtables['hashes.binentries.txt'][entry.hash] = name.data
                # extract file hashes
                for entry in bin.entries:
                    for field in entry.data:
                        extract_file_field(field)
                for link in bin.links:
                    extract_file_value(link, pyRitoFile.BINType.String)

                LOG(f'hash_manager: Done: Extract Hashes: {file_path}')
            except Exception as e:
                LOG(f'hash_manager: Failed: Extract Hashes: {file_path}: {e}')
                LOG(traceback.format_exc())

        def extract_wad(file_path):
            try:
                wad = pyRitoFile.read_wad(file_path)
                with wad.stream(file_path, 'rb') as bs:
                    for chunk in wad.chunks:
                        chunk.read_data(bs)
                        if chunk.extension == 'skn':
                            extract_skn(
                                f'{chunk.hash}.{chunk.extension}', chunk.data)
                        elif chunk.extension == 'skl':
                            extract_skl(
                                f'{chunk.hash}.{chunk.extension}', chunk.data)
                        elif chunk.extension == 'bin':
                            extract_bin(
                                f'{chunk.hash}.{chunk.extension}', chunk.data)
                        chunk.free_data()
                LOG(f'hash_manager: Done: Extract Hashes: {file_path}')
            except Exception as e:
                LOG(f'hash_manager: Failed: Extract Hashes: {file_path}: {e}')
                LOG(traceback.format_exc())

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
            sep = HASH_SEPARATOR(filename)
            # read existed extracted hashes
            if os.path.exists(local_file):
                with open(local_file, 'r') as f:
                    for line in f:
                        hashtable[line[:sep]] = line[sep+1:-1]
            # write
            with open(local_file, 'w+') as f:
                f.writelines(
                    f'{key} {value}\n'
                    for key, value in sorted(
                        hashtable.items(), key=lambda item: item[1]
                    )
                )
            LOG(f'hash_manager: Done: Extract: {local_file}')
            combine_custom_hashes(filename)


class CustomHashes:
    # combine with CDTB and extracted hashes
    # use for all functions in this app
    local_dir = './prefs/hashes/custom_hashes'
    def local_file(filename): return f'{CustomHashes.local_dir}/{filename}'

    @staticmethod
    def read_hashes(*filenames):
        for filename in filenames:
            local_file = CustomHashes.local_file(filename)
            # safe check
            if os.path.exists(local_file):
                # read hashes
                with open(local_file, 'r') as f:
                    sep = HASH_SEPARATOR(filename)
                    for line in f:
                        HASHTABLES[filename][line[:sep]] = line[sep+1:-1]

    @staticmethod
    def write_hashes(*filenames):
        for filename in filenames:
            local_file = CustomHashes.local_file(filename)
            # write combined hashes
            with open(local_file, 'w+') as f:
                f.writelines(
                    f'{key} {value}\n'
                    for key, value in sorted(
                        HASHTABLES[filename].items(), key=lambda item: item[1]
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
            HASHTABLES[filename] = {}

    @staticmethod
    def free_bin_hashes(*filenames):
        CustomHashes.free_hashes(*BIN_HASHES)

    @staticmethod
    def free_wad_hashes(*filenames):
        CustomHashes.free_hashes(*WAD_HASHES)

    @staticmethod
    def free_all_hashes():
        CustomHashes.free_hashes(*ALL_HASHES)


def combine_custom_hashes(*filenames):
    for filename in filenames:
        hashtable = {}
        cdtb_file = CDTBHashes.local_file(filename)
        ex_file = ExtractedHashes.local_file(filename)
        ch_file = CustomHashes.local_file(filename)
        sep = HASH_SEPARATOR(filename)
        # read cdtb hashes
        if os.path.exists(cdtb_file):
            with open(cdtb_file, 'r') as f:
                for line in f:
                    hashtable[line[:sep]] = line[sep+1:-1]
        # read extracted hashes
        if os.path.exists(ex_file):
            with open(ex_file, 'r') as f:
                for line in f:
                    hashtable[line[:sep]] = line[sep+1:-1]
        # read existed custom hashes
        if os.path.exists(ch_file):
            with open(ch_file, 'r') as f:
                for line in f:
                    hashtable[line[:sep]] = line[sep+1:-1]
        # write combined hashes
        with open(ch_file, 'w+') as f:
            f.writelines(
                f'{key} {value}\n'
                for key, value in sorted(
                    hashtable.items(), key=lambda item: item[1]
                )
            )
        LOG(f'hash_manager: Done: Update: {ch_file}')


def reset_custom_hashes(*filenames):
    for filename in filenames:
        cdtb_file = CDTBHashes.local_file(filename)
        ch_file = CustomHashes.local_file(filename)
        # copy file from cdtb
        with open(cdtb_file, 'rb') as f:
            data = f.read()
        with open(ch_file, 'wb+') as f:
            f.write(data)


def prepare(_LOG):
    global LOG
    LOG = _LOG
    # load setting first
    CDTBHashes.local_dir = setting.get('CDTBHashes.local_dir', CDTBHashes.local_dir)
    ExtractedHashes.local_dir = setting.get('ExtractedHashes.local_dir', ExtractedHashes.local_dir)
    CustomHashes.local_dir = setting.get('CustomHashes.local_dir', CustomHashes.local_dir)
    # ensure folder
    os.makedirs(CDTBHashes.local_dir, exist_ok=True)
    os.makedirs(ExtractedHashes.local_dir, exist_ok=True)
    os.makedirs(CustomHashes.local_dir, exist_ok=True)
    Thread(target=CDTBHashes.sync_all, daemon=True).start()
