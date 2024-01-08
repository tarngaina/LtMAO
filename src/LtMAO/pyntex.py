import os
import os.path
from . import pyRitoFile, hash_manager
import json

LOG = print

PRE_BIN_HASH = {
    'SkinCharacterDataProperties': pyRitoFile.bin_hash('SkinCharacterDataProperties'),
    'StaticMaterialDef': pyRitoFile.bin_hash('StaticMaterialDef'),
    'GearSkinUpgrade': pyRitoFile.bin_hash('GearSkinUpgrade'),
    'VfxSystemDefinitionData': pyRitoFile.bin_hash('VfxSystemDefinitionData')
}


def parse_bin(bin, *, existing_files=[]):
    bin_hash = pyRitoFile.bin_hash
    wad_hash = pyRitoFile.wad_hash
    temp_hashes = PRE_BIN_HASH.values()

    def parse_entry(entry):
        mentioned_files = []
        missing_files = []

        def parse_value(value, value_type):
            if value_type == pyRitoFile.BINType.String:
                value = value.lower()
                if 'assets/' in value or 'data/' in value:
                    if value not in mentioned_files:
                        mentioned_files.append(value)
            elif value_type in (pyRitoFile.BINType.List, pyRitoFile.BINType.List2):
                for v in value.data:
                    parse_value(v, value_type)
            elif value_type in (pyRitoFile.BINType.Embed, pyRitoFile.BINType.Pointer):
                for f in value.data:
                    parse_field(f)

        def parse_field(field):
            if field.type in (pyRitoFile.BINType.List, pyRitoFile.BINType.List2):
                for v in field.data:
                    parse_value(v, field.value_type)
            elif field.type in (pyRitoFile.BINType.Embed, pyRitoFile.BINType.Pointer):
                for f in field.data:
                    parse_field(f)
            elif field.type == pyRitoFile.BINType.Map:
                for key, value in field.data.items():
                    parse_value(key, field.key_type)
                    parse_value(value, field.value_type)
            else:
                parse_value(field.data, field.type)

        for field in entry.data:
            parse_field(field)

        if len(existing_files) > 0:
            missing_files = [
                file for file in mentioned_files if file not in existing_files]

        dic = {}
        dic['hash'] = entry.hash
        dic['types'] = entry.type
        dic['mentioned_files'] = mentioned_files
        if len(missing_files) > 0:
            dic['missing_files'] = missing_files
        return dic

    results = []
    for entry in bin.entries:
        if bin_hash(entry.type) in temp_hashes:
            results.append(parse_entry(entry))
    return results


def parse_dir(path):
    res = {}
    # list all files
    full_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            full_files.append(os.path.join(root, file).replace('\\', '/'))
    full_files.sort()
    rel_files = [os.path.relpath(file_path, path).replace(
        '\\', '/') for file_path in full_files]
    # parsing
    LOG(f'pyntex: Running: Read bin hashes')
    hash_manager.read_bin_hashes()
    for id, full_file in enumerate(full_files):
        if full_file.endswith('.bin'):
            try:
                bin = pyRitoFile.read_bin(full_file)
                bin.un_hash(hash_manager.HASHTABLES)
                result = parse_bin(bin, existing_files=rel_files)
                if len(result) > 0:
                    res[rel_files[id]] = result
                    LOG(f'pyntex: Done: Parse {full_file}')
            except Exception as e:
                LOG(f'pyntex: Failed: Parse {full_file}: {e}')
    hash_manager.free_bin_hashes()
    # write json out
    json_file = path + '.pyntex.json'
    with open(json_file, 'w+') as f:
        json.dump(res, f, indent=4)
    LOG(f'pyntex: Done: Write {json_file}')


def parse_wad(path):
    res = {}
    # read wad
    LOG(f'pyntex: Running: Read wad hashes')
    hash_manager.read_wad_hashes()
    wad = pyRitoFile.read_wad(path)
    wad.un_hash(hash_manager.HASHTABLES)
    hash_manager.free_wad_hashes()
    # rehash the data/ bins
    for chunk in wad.chunks:
        if chunk.extension == 'bin':
            if os.path.dirname(chunk.hash) == 'data':
                chunk.hash = pyRitoFile.wad_hash(chunk.hash) + '.bin'
    # list all chunk hashes
    chunk_hashes = []
    for chunk in wad.chunks:
        chunk_hashes.append(chunk.hash)
    # parsing
    LOG(f'pyntex: Running: Read bin hashes')
    hash_manager.read_bin_hashes()
    with wad.stream(path, 'rb') as bs:
        for chunk in wad.chunks:
            chunk.read_data(bs)
            if chunk.extension == 'bin':
                try:
                    bin = pyRitoFile.read_bin('', raw=chunk.data)
                    bin.un_hash(hash_manager.HASHTABLES)
                    result = parse_bin(bin, existing_files=chunk_hashes)
                    if len(result) > 0:
                        res[chunk.hash] = result
                        LOG(f'pyntex: Done: Parse {chunk.hash}')
                except Exception as e:
                    LOG(f'pyntex: Failed: Parse {chunk.hash}: {e}')
            chunk.free_data()
    hash_manager.free_bin_hashes()
    # write json out
    json_file = path + '.pyntex.json'
    with open(json_file, 'w+') as f:
        json.dump(res, f, indent=4)
    LOG(f'pyntex: Done: Write {json_file}')


def parse(path):
    if os.path.isdir(path):
        parse_dir(path)
    else:
        if path.endswith('.wad.client'):
            parse_wad(path)


def prepare(_LOG):
    global LOG
    LOG = _LOG
