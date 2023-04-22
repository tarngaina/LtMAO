import requests
import os
import os.path
import json
from threading import Thread
from LtMAO.pyRitoFile import read_wad, read_bin, read_skn, read_skl
from LtMAO.pyRitoFile.hash import FNV1a

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


def read_all():
    CustomHashes.read_all()


def free_all():
    CustomHashes.free_all()


def HASH_SEPARATOR(filename):
    # space separator in hashes txt
    # use this to skip using split()
    return 16 if filename in WAD_HASHES else 8


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


class CDTB:
    # for syncing CDTB hashes
    local_dir = './prefs/hashes/cdtb_hashes'

    def local_file(
        filename): return f'{CDTB.local_dir}/{filename}'

    def github_file(
        filename): return f'https://raw.githubusercontent.com/CommunityDragon/CDTB/master/cdragontoolbox/{filename}'
    etag_path = f'{local_dir}/etag.json'
    ETAG = {}

    @staticmethod
    def sync_hashes(*filenames):
        for filename in filenames:
            local_file = CDTB.local_file(filename)
            github_file = CDTB.github_file(filename)
            # GET request
            get = requests.get(github_file, stream=True)
            get.raise_for_status()
            # get etag and compare, new etag = sync
            etag_local = CDTB.ETAG.get(filename, None)
            etag_github = get.headers['Etag']
            if etag_local == None or etag_local != etag_github or not os.path.exists(local_file):
                # set etag
                CDTB.ETAG[filename] = etag_github
                # download file
                bytes_downloaded = 0
                chunk_size = 1024**2
                with open(local_file, 'wb') as f:
                    for chunk in get.iter_content(chunk_size):
                        bytes_downloaded += len(chunk)
                        LOG(
                            f'Downloading: {github_file}: {to_human(bytes_downloaded)}')
                        f.write(chunk)
                combine_custom_hashes(filename)
            LOG(f'Done: Sync hash: {local_file}')

    @staticmethod
    def sync_all():
        # read etags
        CDTB.ETAG = {}
        if os.path.exists(CDTB.etag_path):
            with open(CDTB.etag_path, 'r') as f:
                CDTB.ETAG = json.load(f)
        CDTB.sync_hashes(*ALL_HASHES)
        # write etags
        with open(CDTB.etag_path, 'w+') as f:
            json.dump(CDTB.ETAG, f, indent=4)


class ExtractedHashes:
    # extracted hash
    local_dir = './prefs/hashes/extracted_hashes'
    def local_file(filename): return f'{ExtractedHashes.local_dir}/{filename}'

    def extract(*file_paths):
        def bin_hash(name):
            return f'{FNV1a(name):08x}'

        hashtables = {
            'hashes.binentries.txt': {},
            'hashes.binhashes.txt': {}
        }
        pre_bin_hashes = {
            'VfxSystemDefinitionData': bin_hash('VfxSystemDefinitionData'),
            'particlePath': bin_hash('particlePath'),
            'StaticMaterialDef': bin_hash('StaticMaterialDef'),
            'name': bin_hash('name')
        }

        def extract_skn(skn):
            # extract submesh hash <-> submesh name
            for submesh in skn.submeshes:
                hashtables['hashes.binhashes.txt'][submesh.bin_hash] = submesh.name

        def extract_skl(skl):
            # extract joint hash <-> joint name
            for joint in skl.joints:
                hashtables['hashes.binhashes.txt'][joint.bin_hash] = joint.name

        def extract_bin(bin):
            for entry in bin.entries:
                # extract VfxSystemDefinitionData <-> particlePath
                if entry.type == pre_bin_hashes['VfxSystemDefinitionData']:
                    particle_path_field = next((field for field in entry.data if field.hash == pre_bin_hashes[
                        'particlePath']), None)
                    if particle_path_field != None:
                        hashtables['hashes.binentries.txt'][entry.hash] = particle_path_field.data
                # extract StaticMaterialDef <-> name
                elif entry.type == pre_bin_hashes['StaticMaterialDef']:
                    name_field = next((field for field in entry.data if field.hash == pre_bin_hashes[
                        'name']), None)
                    if name_field != None:
                        hashtables['hashes.binentries.txt'][entry.hash] = name_field.data

        # extract hashes base on file types
        for file_path in file_paths:
            if file_path.endswith('.wad.client'):
                wad = read_wad(file_path, read_data=True)
                for chunk in wad.chunks:
                    if chunk.extension == 'skn':
                        try:
                            extract_skn(read_skn('', raw=chunk.data))
                            LOG(f'Done: Extract Hashes: {chunk.hash}.{chunk.extension}')
                        except:
                            LOG(
                                f'Failed: Extract Hashes: Skipped {chunk.hash}.{chunk.extension}')
                    elif chunk.extension == 'skl':
                        try:
                            extract_skl(read_skl('', raw=chunk.data))
                            LOG(f'Done: Extract Hashes: {chunk.hash}.{chunk.extension}')
                        except:
                            LOG(
                                f'Failed: Extract Hashes: Skipped {chunk.hash}.{chunk.extension}')
                    elif chunk.extension == 'bin':
                        try:
                            extract_bin(read_bin('', raw=chunk.data))
                            LOG(f'Done: Extract Hashes: {chunk.hash}.{chunk.extension}')
                        except:
                            LOG(
                                f'Failed: Extract Hashes: Skipped {chunk.hash}.{chunk.extension}')
                    # free memory
                    chunk.data = None
            elif file_path.endswith('.skn'):
                try:
                    extract_skn(read_skn(file_path))
                    LOG(f'Done: Extract Hashes: {file_path}')
                except:
                    LOG(
                        f'Failed: Extract Hashes: Skipped {file_path}')
            elif file_path.endswith('.skl'):
                try:
                    extract_skl(read_skl(file_path))
                    LOG(f'Done: Extract Hashes: {file_path}')
                except:
                    LOG(
                        f'Failed: Extract Hashes: Skipped {file_path}')
            elif file_path.endswith('.bin'):
                try:
                    extract_bin(read_bin(file_path))
                    LOG(f'Done: Extract Hashes: {file_path}')
                except:
                    LOG(
                        f'Failed: Extract Hashes: Skipped {file_path}')
            LOG(f'Done: Extract Hashes: {file_path}')
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
            LOG(f'Done: Extract: {local_file}')
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
    def read_binhashes():
        CustomHashes.read_hashes(*BIN_HASHES)

    @staticmethod
    def read_wadhashes():
        CustomHashes.read_hashes(*WAD_HASHES)

    @staticmethod
    def read_all():
        CustomHashes.read_hashes(*ALL_HASHES)

    @staticmethod
    def free_hashes(*filenames):
        for filename in filenames:
            del HASHTABLES[filename]

    @staticmethod
    def free_binhashes(*filenames):
        CustomHashes.free_hashes(*BIN_HASHES)

    @staticmethod
    def free_wadhashes(*filenames):
        CustomHashes.free_hashes(*WAD_HASHES)

    @staticmethod
    def free_all():
        CustomHashes.free_hashes(*ALL_HASHES)


def combine_custom_hashes(*filenames):
    for filename in filenames:
        hashtable = {}
        cdtb_file = CDTB.local_file(filename)
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
        LOG(f'Done: Update: {ch_file}')


def prepare(_LOG):
    # function need to call first
    def prepare_cmd():
        global LOG
        LOG = _LOG
        # ensure folder
        if not os.path.exists(CDTB.local_dir):
            os.makedirs(CDTB.local_dir)
        if not os.path.exists(ExtractedHashes.local_dir):
            os.makedirs(ExtractedHashes.local_dir)
        if not os.path.exists(CustomHashes.local_dir):
            os.makedirs(CustomHashes.local_dir)
        # sync CDTB hashesh
        CDTB.sync_all()

    Thread(target=prepare_cmd, daemon=True).start()
