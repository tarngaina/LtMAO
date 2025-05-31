import os, os.path, json
from . import hash_helper, pyRitoFile

def parse_bin(bin, *, existing_files={}):
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
            for file in mentioned_files:
                if file in existing_files:
                    existing_files[file] = False
                else:
                    missing_files.append(file)     

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


def parse_dir(path, delete_junk_files=False):
    res = {}
    # list all files
    full_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            full_files.append(os.path.join(root, file).replace('\\', '/'))
    full_files.sort()
    existing_files = {
        os.path.relpath(file_path, path).replace('\\', '/'): True 
        for file_path in full_files
    }
    short_files = list(existing_files.keys())
    # parsing
    print(f'pyntex: Start:  Read bin hashes')
    hash_helper.Storage.read_bin_hashes()
    for full_file_index, full_file in enumerate(full_files):
        if full_file.endswith('.bin'):
            bin = pyRitoFile.bin.BIN().read(full_file)
            bin.un_hash(hash_helper.Storage.hashtables)
            result = parse_bin(bin, existing_files=existing_files)
            if len(result) > 0:
                res[short_files[full_file_index]] = result
                print(f'pyntex: Finish: Parse {full_file}')
            existing_files[short_files[full_file_index]] = False
    hash_helper.Storage.free_bin_hashes()
    if 'hashed_files.json' in existing_files:
        existing_files['hashed_files.json'] = False
    res['junk_files'] = [file for file in existing_files if existing_files[file]]
    if delete_junk_files:
        for file in res['junk_files']:
            full_file = os.path.join(path, file).replace('\\', '/')
            os.remove(full_file)
            print(f'pyntex: Finish: Remove {full_file}')
        # remove empty dirs
        for root, dirs, files in os.walk(path, topdown=False):
            if len(os.listdir(root)) == 0:
                os.rmdir(root)
    else:
        # write json out
        json_file = path + '.pyntex.json'
        with open(json_file, 'w+', encoding='utf-8') as f:
            json.dump(res, f, indent=4, ensure_ascii=False)
        print(f'pyntex: Finish: Write {json_file}')


def parse_wad(path, delete_junk_files=False):
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
    chunk_hashes = {chunk.hash: True for chunk in wad.chunks}
    # parsing
    print(f'pyntex: Start:  Read bin hashes')
    hash_helper.Storage.read_bin_hashes()
    with wad.stream(path, 'rb') as bs:
        for chunk in wad.chunks:
            chunk.read_data(bs)
            if chunk.extension == 'bin':
                bin = pyRitoFile.bin.BIN().read('', raw=chunk.data)
                bin.un_hash(hash_helper.Storage.hashtables)
                result = parse_bin(bin, existing_files=chunk_hashes)
                if len(result) > 0:
                    res[chunk.hash] = result
                    print(f'pyntex: Finish: Parse {chunk.hash}')
                chunk_hashes[chunk.hash] = False
            chunk.free_data()
    hash_helper.Storage.free_bin_hashes()
    res['junk_files'] = [file for file in chunk_hashes if chunk_hashes[file]]
    if delete_junk_files:
        # write wad2 temp
        chunks_to_write = [file for file in chunk_hashes if not chunk_hashes[file]]
        wad2_path = path + '.temp'
        wad2 = pyRitoFile.wad.WAD()
        wad2.chunks = [pyRitoFile.wad.WADChunk.default()
                    for id in range(len(chunks_to_write))]
        wad2.write(wad2_path)
        # write wad2 chunk
        with wad2.stream(wad2_path, 'rb+') as bs2:
            with wad.stream(path, 'rb') as bs:
                for id, chunk2 in enumerate(wad2.chunks):
                    chunk_hash_to_write = chunks_to_write[id]
                    # find chunk data 
                    for chunk in wad.chunks:
                        if chunk.hash == chunk_hash_to_write:
                            chunk.read_data(bs)
                            chunk_data = chunk.data
                            chunk.free_data()
                            break
                    chunk2.write_data(bs2, id, chunk_hash_to_write, chunk_data, previous_chunks=wad2.chunks[:id])
                    chunk2.free_data()
                    print(f'pyntex: Finish: Rebuild {chunk2.hash}')
        # replace temp as new wad
        os.remove(path)
        os.rename(wad2_path, path)
    else:
        # write json out
        json_file = path + '.pyntex.json'
        with open(json_file, 'w+', encoding='utf-8') as f:
            json.dump(res, f, indent=4, ensure_ascii=False)
        print(f'pyntex: Finish: Write {json_file}')


def parse(path, delete_junk_files=False):
    if os.path.isdir(path):
        parse_dir(path, delete_junk_files)
    else:
        if path.endswith('.wad.client'):
            parse_wad(path, delete_junk_files)

