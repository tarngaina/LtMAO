from . import pyRitoFile
import os
import json

LOG = print


def check_hashed_name(basename):
    try:
        int(basename, 16)
        return True
    except:
        return False


def unpack(wad_file, raw_dir, hashtables, filter=None):
    LOG(f'wad_tool: Running: Unpack WAD: {wad_file}')
    # read wad
    wad = pyRitoFile.read_wad(wad_file)
    wad.un_hash(hashtables)
    hashed_bins = {}
    with wad.stream(wad_file, 'rb') as bs:
        for chunk in wad.chunks:
            if filter != None and chunk.hash not in filter:
                continue
            # read chunk data first to get extension
            chunk.read_data(bs)
            # output file path of this chunk
            file_path = os.path.join(raw_dir, chunk.hash)
            # add extension to file path if know
            if chunk.extension != None:
                ext = f'.{chunk.extension}'
                if not file_path.endswith(ext):
                    file_path += ext
            file_path = file_path.replace('\\', '/')
            # handle hashed bin
            if os.path.dirname(file_path).endswith('data') and chunk.extension == 'bin':
                hashed_bin = os.path.join(
                    raw_dir, pyRitoFile.wad_hash(chunk.hash)+'.bin')
                hashed_bins[os.path.basename(
                    hashed_bin)] = 'data/'+os.path.basename(file_path)
                file_path = hashed_bin
            # ensure folder of this file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # write out chunk data to file
            with open(file_path, 'wb') as fo:
                fo.write(chunk.data)
            chunk.free_data()
            LOG(f'wad_tool: Done: Unpack: {chunk.hash}')
    # write hashed bins json
    if len(hashed_bins) > 0:
        with open(os.path.join(raw_dir, 'hashed_bins.json'), 'w+') as f:
            json.dump(hashed_bins, f, indent=4)


def pack(raw_dir, wad_file):
    LOG(f'wad_tool: Running: Pack WAD: {raw_dir}')
    # create wad first with only infos
    chunk_datas = []
    chunk_hashes = []
    for root, dirs, files in os.walk(raw_dir):
        for file in files:
            # skip hashed bins json
            if file == 'hashed_bins.json':
                continue
            # prepare chunk datas
            file_path = os.path.join(root, file).replace('\\', '/')
            chunk_datas.append(file_path)
            # check hashed files
            # by remove extension: 6bff35087d62f95d.bin -> 6bff35087d62f95d
            basename = os.path.basename(file).split('.')[0]

            # not r'/assets/' in file_path
            # Ignoring the check for hashes inside of assets
            # For example that thing would think that a file assets/.../.../face.tex is a hash
            # Since "face" is indeed a valid hash
            # Also, never saw hashed files inside of assets path unless u really cooked
            if check_hashed_name(basename) and not r'/assets/' in file_path:
                file_path = basename
                chunk_hashes.append(file_path)
            else:
                chunk_hashes.append(os.path.relpath(
                    file_path, raw_dir).replace('\\', '/'))
    # write wad
    wad = pyRitoFile.WAD()
    wad.chunks = [pyRitoFile.WADChunk.default()
                  for id in range(len(chunk_hashes))]
    wad.write(wad_file)
    # write wad chunk
    with wad.stream(wad_file, 'rb+') as bs:
        for id, chunk in enumerate(wad.chunks):
            with open(chunk_datas[id], 'rb') as f:
                chunk_data = f.read()
            chunk.write_data(bs, id, chunk_hashes[id], chunk_data, previous_chunks=wad.chunks[:id])
            chunk.free_data()
            LOG(f'wad_tool: Done: Pack: {chunk.hash}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
