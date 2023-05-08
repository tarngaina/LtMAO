from LtMAO import pyRitoFile
from LtMAO import hash_manager
import os
from json import dump

LOG = print


def check_hashed_name(basename):
    try:
        int(basename, 16)
        return True
    except:
        return False


def unpack(wad_file, raw_dir):
    LOG(f'Running: Unpack WAD: {wad_file}')
    # read wad
    hash_manager.read_wad_hashes()
    wad = pyRitoFile.read_wad(wad_file)
    wad.un_hash(hash_manager.HASHTABLES)
    hash_manager.free_wad_hashes()
    hashed_bins = {}
    with wad.stream(wad_file, 'rb') as bs:
        for chunk in wad.chunks:
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
            chunk.read_data(bs)
            with open(file_path, 'wb') as fo:
                fo.write(chunk.data)
            chunk.free_data()
            LOG(f'Done: Unpack: {chunk.hash}')
    if len(hashed_bins) > 0:
        with open(os.path.join(raw_dir, 'hashed_bins.json'), 'w+') as f:
            dump(hashed_bins, f, indent=4)


def pack(raw_dir, wad_file):
    LOG(f'Running: Pack WAD: {raw_dir}')
    # create wad first with only infos
    chunk_datas = []
    chunk_hashes = []
    for root, dirs, files in os.walk(raw_dir):
        for id, file in enumerate(files):
            # prepare chunk datas
            file_path = os.path.join(root, file).replace('\\', '/')
            chunk_datas.append(file_path)
            # prepare chunk hash: remove extension of hashed file
            # example: 6bff35087d62f95d.bin -> 6bff35087d62f95d
            basename = file.split('.')[0]
            if check_hashed_name(basename):
                file = basename
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
            chunk.write_data(bs, id, chunk_hashes[id], chunk_data)
            chunk.free_data()
            LOG(f'Done: Packed: {chunk.hash}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
