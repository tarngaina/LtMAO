import os, os.path, json, traceback
from . import lepath, hash_helper, pyRitoFile

def unify_path(path):
    # if the path is straight up hex
    # ex: ec9584b0506c2abb -> ec9584b0506c2abb
    if pyRitoFile.wad.WADHasher.is_hash(path):
        return path
    # if the path is hashed file 
    # ex: ec9584b0506c2abb.bin -> ec9584b0506c2abb
    basename = path.split('.')[0]
    if pyRitoFile.wad.WADHasher.is_hash(basename):
        return basename
    # if the path is pure raw
    # ex: data/effects.bin -> ec9584b0506c2abb
    return pyRitoFile.wad.WADHasher.raw_to_hex(path)

def check_if_path_in_there(path, there):
    path = unify_path(path)
    for f in there:
        if path == unify_path(f):
            return True
    return False    

def checK_if_path_is_same(path1, path2):
    return unify_path(path1) == unify_path(path2)

def parse_bin(bin, *, existing_files={}):
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
                if value.data != None:
                    for f in value.data:
                        parse_field(f)

        def parse_field(field):
            if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                for v in field.data:
                    parse_value(v, field.value_type)
            elif field.type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                if field.data != None:
                    for f in field.data:
                        parse_field(f)
            elif field.type == pyRitoFile.bin.BINType.MAP:
                for key, value in field.data.items():
                    parse_value(key, field.key_type)
                    parse_value(value, field.value_type)
            elif field.type == pyRitoFile.bin.BINType.OPTION and field.value_type == pyRitoFile.bin.BINType.STRING:
                if field.data != None:
                    parse_value(field.data, field.value_type)
            else:
                parse_value(field.data, field.type)

        for field in entry.data:
            parse_field(field)

        if len(existing_files) > 0:   
            for file in mentioned_files:
                if check_if_path_in_there(file, existing_files):
                    existing_files[file] = False
                    if file.endswith('.dds'):
                        splits = file.split('/')
                        dds2x = '/'.join(splits[:-1] + ['2x_' + splits[-1]])
                        dds4x = '/'.join(splits[:-1] + ['4x_' + splits[-1]])
                        if dds2x in existing_files:
                            existing_files[dds2x] = False
                        if dds4x in existing_files:
                            existing_files[dds4x] = False
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
        dic = parse_entry(entry)
        if len(dic['mentioned_files']) > 0:
            results.append(dic)
    return results


def parse_dir(path, delete_junk_files=False):
    res = {}
    # list all files
    full_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            full_files.append(lepath.join(root, file).lower())
    full_files.sort()
    existing_files = {
        lepath.rel(file_path, path): True 
        for file_path in full_files
    }
    short_files = list(existing_files.keys())
    # parsing
    print(f'pyntex: Start:  Read bin hashes')
    hash_helper.Storage.read_bin_hashes()
    for full_file_index, full_file in enumerate(full_files):
        if full_file.endswith('.bin'):
            try:
                bin = pyRitoFile.bin.BIN().read(full_file)
                bin.un_hash(hash_helper.Storage.hashtables)
                result = parse_bin(bin, existing_files=existing_files)
                if len(result) > 0:
                    res[short_files[full_file_index]] = result
                    print(f'pyntex: Finish: Parse {full_file}')
                existing_files[short_files[full_file_index]] = False
            except Exception as e:
                print(f'pyntex: Error: {e}')
                print(traceback.format_exc())
    hash_helper.Storage.free_bin_hashes()
    if 'hashed_files.json' in existing_files:
        existing_files['hashed_files.json'] = False
    res['junk_files'] = [file for file in existing_files if existing_files[file]]
    if delete_junk_files:
        for file in res['junk_files']:
            full_file = lepath.join(path, file)
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
    # list all chunk hashes
    chunk_hashes = {chunk.hash: True for chunk in wad.chunks}
    # parsing
    print(f'pyntex: Start:  Read bin hashes')
    hash_helper.Storage.read_bin_hashes()
    with pyRitoFile.stream.BytesStream.reader(path) as bs:
        for chunk in wad.chunks:
            chunk.read_data(bs)
            if chunk.extension == 'bin':
                try:
                    bin = pyRitoFile.bin.BIN().read(chunk.data, raw=True)
                    bin.un_hash(hash_helper.Storage.hashtables)
                    result = parse_bin(bin, existing_files=chunk_hashes)
                    if len(result) > 0:
                        res[chunk.hash] = result
                        print(f'pyntex: Finish: Parse {chunk.hash}')
                    chunk_hashes[chunk.hash] = False
                except Exception as e:
                    print(f'pyntex: Error: {e}')
                    print(traceback.format_exc())
            chunk.free_data()
    hash_helper.Storage.free_bin_hashes()
    res['junk_files'] = [file for file in chunk_hashes if chunk_hashes[file]]
    if delete_junk_files:
        # write temp wad
        chunk_hashes_to_write = [file for file in chunk_hashes if not chunk_hashes[file]]
        temp_path = path + '.pyntextemp'
        temp = pyRitoFile.wad.WAD()
        temp.chunks = [pyRitoFile.wad.WADChunk.default()
                    for id in range(len(chunk_hashes_to_write))]
        temp.write(temp_path)
        # write temp chunk
        with pyRitoFile.stream.BytesStream.reader(path) as bs, pyRitoFile.stream.BytesStream.updater(temp_path) as bs_temp:
            for id, temp_chunk in enumerate(temp.chunks):
                chunk = wad.get_items(lambda chunk: checK_if_path_is_same(chunk.hash, chunk_hashes_to_write[id]))[0]
                chunk.read_data(bs)
                temp_chunk.write_data(bs_temp, id, chunk.hash, chunk.data, previous_chunks=temp.chunks[:id])
                chunk.free_data()
                temp_chunk.free_data()
                print(f'pyntex: Finish: Rebuild {temp_chunk.hash}')
        # replace temp as new wad
        os.remove(path)
        os.rename(temp_path, path)
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

