import os, os.path, traceback, json
from . import hash_helper, pyRitoFile

def parse_bin(bin, *, existing_files=[]):
    bin_hash = pyRitoFile.bin.BINHasher.raw_to_hex
    temp_hashes = [
        hash_helper.Storage.bin_hashes[text] for text in (
            'SkinCharacterDataProperties', 'StaticMaterialDef', 'GearSkinUpgrade', 'VfxSystemDefinitionData'
        )
    ]

    def parse_entry(entry):
        mentioned_files = []
        missing_files = []

        def parse_value(value, value_type):
            if value_type == pyRitoFile.bin.BINType.STRING:
                value = value.lower()
                if 'assets/' in value or 'data/' in value:
                    if value not in mentioned_files:
                        mentioned_files.append(value)
            elif value_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                for v in value.data:
                    parse_value(v, value_type)
            elif value_type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                for f in value.data:
                    parse_field(f)

        def parse_field(field):
            if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                for v in field.data:
                    parse_value(v, field.value_type)
            elif field.type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                for f in field.data:
                    parse_field(f)
            elif field.type == pyRitoFile.bin.BINType.MAP:
                for key, value in field.data.items():
                    parse_value(key, field.key_type)
                    parse_value(value, field.value_type)
            elif field.type == pyRitoFile.bin.BINType.OPTION and field.value_type == pyRitoFile.bin.BINType.STRING:
                parse_value(field.data, field.value_type)
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
    existing_files = [os.path.relpath(file_path, path).replace(
        '\\', '/') for file_path in full_files]
    # parsing
    print(f'pyntex: Start:  Read bin hashes')
    hash_helper.Storage.read_bin_hashes()
    for i, full_file in enumerate(full_files):
        if full_file.endswith('.bin'):
            try:
                bin = pyRitoFile.bin.BIN().read(full_file)
                bin.un_hash(hash_helper.Storage.hashtables)
                result = parse_bin(bin, existing_files=existing_files)
                if len(result) > 0:
                    res[existing_files[i]] = result
                    print(f'pyntex: Finish: Parse {full_file}')
            except Exception as e:
                print(f'pyntex: Error: Parse {full_file}: {e}')
                print(traceback.format_exc())
    hash_helper.Storage.free_bin_hashes()
    # write json out
    json_file = path + '.pyntex.json'
    with open(json_file, 'w+', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    print(f'pyntex: Finish: Write {json_file}')


def parse_wad(path):
    res = {}
    # read wad
    print(f'pyntex: Start:  Read wad hashes')
    hash_helper.Storage.read_wad_hashes()
    wad = pyRitoFile.wad.WAD().read(path)
    wad.un_hash(hash_helper.Storage.hashtables)
    hash_helper.Storage.free_wad_hashes()
    # rehash the data/ bins
    for chunk in wad.chunks:
        if chunk.extension == 'bin':
            if os.path.dirname(chunk.hash) == 'data':
                chunk.hash = pyRitoFile.wad.WADHasher.raw_to_hex(chunk.hash) + '.bin'
    # list all chunk hashes
    chunk_hashes = []
    for chunk in wad.chunks:
        chunk_hashes.append(chunk.hash)
    # parsing
    print(f'pyntex: Start:  Read bin hashes')
    hash_helper.Storage.read_bin_hashes()
    with wad.stream(path, 'rb') as bs:
        for chunk in wad.chunks:
            chunk.read_data(bs)
            if chunk.extension == 'bin':
                try:
                    bin = pyRitoFile.bin.BIN().read('', raw=chunk.data)
                    bin.un_hash(hash_helper.Storage.hashtables)
                    result = parse_bin(bin, existing_files=chunk_hashes)
                    if len(result) > 0:
                        res[chunk.hash] = result
                        print(f'pyntex: Finish: Parse {chunk.hash}')
                except Exception as e:
                    print(f'pyntex: Error: Parse {chunk.hash}: {e}')
                    print(traceback.format_exc())
            chunk.free_data()
    hash_helper.Storage.free_bin_hashes()
    # write json out
    json_file = path + '.pyntex.json'
    with open(json_file, 'w+', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    print(f'pyntex: Finish: Write {json_file}')


def parse(path):
    if os.path.isdir(path):
        parse_dir(path)
    else:
        if path.endswith('.wad.client'):
            parse_wad(path)

