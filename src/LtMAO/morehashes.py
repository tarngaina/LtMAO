import os
import os.path
from LtMAO.pyRitoFile import read_wad, read_bin, read_skn, read_skl
from LtMAO.pyRitoFile.hash import FNV1a


LOG = print


def bin_hash(name):
    return f'{FNV1a(name):08x}'


def local_file(filename): return f'./prefs/ctdb_hashes/{filename}'


def extract(*file_paths):
    hashtables = {
        'morehashes.binentries.txt': {},
        'morehashes.binhashes.txt': {}
    }
    pre_hashes = {
        'VfxSystemDefinitionData': bin_hash('VfxSystemDefinitionData'),
        'particlePath': bin_hash('particlePath'),
        'StaticMaterialDef': bin_hash('StaticMaterialDef'),
        'name': bin_hash('name')
    }

    def extract_skn(skn):
        for submesh in skn.submeshes:
            if submesh.bin_hash not in hashtables['morehashes.binhashes.txt']:
                hashtables['morehashes.binhashes.txt'][submesh.bin_hash] = submesh.name

    def extract_skl(skl):
        for joint in skl.joints:
            if joint.bin_hash not in hashtables['morehashes.binhashes.txt']:
                hashtables['morehashes.binhashes.txt'][joint.bin_hash] = joint.name

    def extract_bin(bin):
        for entry in bin.entries:
            # extract VfxSystemDefinitionData <-> particlePath
            if entry.type == pre_hashes['VfxSystemDefinitionData']:
                particle_path_field = next((field for field in entry.data if field.hash == pre_hashes[
                    'particlePath']), None)
                if particle_path_field != None:
                    hash = entry.hash
                    name = particle_path_field.data
                    if hash not in hashtables['morehashes.binentries.txt']:
                        hashtables['morehashes.binentries.txt'][hash] = name
            # extract StaticMaterialDef <-> name
            elif entry.type == pre_hashes['StaticMaterialDef']:
                name_field = next((field for field in entry.data if field.hash == pre_hashes[
                    'name']), None)
                if name_field != None:
                    hash = entry.hash
                    name = name_field.data
                    if hash not in hashtables['morehashes.binentries.txt']:
                        hashtables['morehashes.binentries.txt'][hash] = name

    # extract hashes base on file types
    for file_path in file_paths:
        if file_path.endswith('.wad.client'):
            wad = read_wad(file_path)
            for chunk in wad.chunks:
                if chunk.extension == 'bin':
                    extract_bin(read_bin('', raw=chunk.data))
                elif chunk.extension == 'skn':
                    extract_skn(read_skn('', raw=chunk.data))
                elif chunk.extension == 'skl':
                    extract_skl(read_skl('', raw=chunk.data))
        elif file_path.endswith('.bin'):
            extract_bin(read_bin(file_path))
        elif file_path.endswith('.skn'):
            # extract hashes <-> material name
            extract_skn(read_skn(file_path))
        elif file_path.endswith('.skl'):
            # extract hashes <-> joint name
            extract_skl(read_skl(file_path))
        LOG(f'Done: Extract Hashes: {file_path}')

    for filename, hashes in hashtables.items():
        # read old saved hashes, combine with new hashes
        if os.path.exists(local_file(filename)):
            with open(local_file(filename), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line[:-1].split()
                    hash = line[0]
                    name = line[1]
                    if hash not in hashtables[filename]:
                        hashtables[filename][hash] = name

        with open(local_file(filename), 'w+') as f:
            f.write(''.join(f'{hash} {name}\n' for hash,
                    name in sorted(hashes.items(), key=lambda kv: kv[1])))
        LOG(f'Done: Update: {filename}')
