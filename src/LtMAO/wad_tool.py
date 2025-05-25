from . import pyRitoFile
import os, json

def check_hashed_name(basename):
    try:
        int(basename, 16)
        return True
    except:
        return False


def unpack(wad_file, raw_dir, hashtables, filter=None):
    print(f'wad_tool: Start:  Unpack WAD: {wad_file}')
    # read wad
    wad = pyRitoFile.wad.WAD().read(wad_file)
    wad.un_hash(hashtables)
    hashed_files = {}
    # create dirs first
    with wad.stream(wad_file, 'rb') as bs:
        for chunk in wad.chunks:
            file_path = os.path.join(raw_dir, chunk.hash)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # actual extract
    with wad.stream(wad_file, 'rb') as bs:
        for chunk in wad.chunks:
            if filter != None and chunk.hash not in filter:
                continue
            # read chunk data first to get extension
            chunk.read_data(bs)
            # output file path of this chunk
            file_path = os.path.join(raw_dir, chunk.hash)
            # add extension to hashed file if know
            if check_hashed_name(chunk.hash) and chunk.extension != None:
                ext = f'.{chunk.extension}'
                if not file_path.endswith(ext):
                    file_path += ext
            file_path = file_path.replace('\\', '/')
            # hash data vfx bin 
            if os.path.dirname(file_path).endswith('data') and chunk.extension == 'bin':
                hashed_bin = os.path.join(raw_dir, pyRitoFile.wad.WADHasher.raw_to_hex(chunk.hash)+'.bin')
                hashed_files[os.path.basename(hashed_bin)] = chunk.hash
                file_path = hashed_bin
            # hash file same name with dir
            if os.path.exists(file_path) and os.path.isdir(file_path):
                hashed_file =  os.path.join(raw_dir, pyRitoFile.wad.WADHasher.raw_to_hex(chunk.hash))
                hashed_files[os.path.basename(hashed_file)] = chunk.hash
                file_path = hashed_file
            # write out chunk data to file
            with open(file_path, 'wb') as fo:
                fo.write(chunk.data)
            chunk.free_data()
            print(f'wad_tool: Finish: Unpack: {chunk.hash}')
    # remove empty dirs
    for root, dirs, files in os.walk(raw_dir, topdown=False):
        if len(os.listdir(root)) == 0:
            os.rmdir(root)
    # write hashed bins json
    if len(hashed_files) > 0:
        with open(os.path.join(raw_dir, 'hashed_files.json'), 'w+', encoding='utf-8') as f:
            json.dump(hashed_files, f, indent=4, ensure_ascii=False)


def pack(raw_dir, wad_file):
    print(f'wad_tool: Start:  Pack WAD: {raw_dir}')
    # create wad first with only infos
    chunk_datas = []
    chunk_hashes = []
    for root, dirs, files in os.walk(raw_dir):
        for file in files:
            # skip hashed bins json
            if file == 'hashed_files.json':
                continue
            # prepare chunk datas
            file_path = os.path.join(root, file).replace('\\', '/')
            chunk_datas.append(file_path)

            # check hashed files
            # hashed files are in root of the directory
            # and also be a valid hexadecimal int file name
            basename = os.path.basename(file)
            relative_path = os.path.relpath(file_path, raw_dir)
            if check_hashed_name(basename.split('.')[0]) and relative_path == basename:
                file_path = basename.split('.')[0]
                chunk_hashes.append(file_path)
            else:
                chunk_hashes.append(os.path.relpath(
                    file_path, raw_dir).replace('\\', '/'))
    # write wad
    wad = pyRitoFile.wad.WAD()
    wad.chunks = [pyRitoFile.wad.WADChunk.default()
                  for id in range(len(chunk_hashes))]
    wad.write(wad_file)
    # write wad chunk
    with wad.stream(wad_file, 'rb+') as bs:
        for id, chunk in enumerate(wad.chunks):
            with open(chunk_datas[id], 'rb') as f:
                chunk_data = f.read()
            chunk.write_data(bs, id, chunk_hashes[id], chunk_data, previous_chunks=wad.chunks[:id])
            chunk.free_data()
            print(f'wad_tool: Finish: Pack: {chunk.hash}')

