from LtMAO import pyRitoFile
from LtMAO import hash_manager
from LtMAO import ext_tools
import os

LOG = print


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


def read_json(path, hashtables=None, ignore_error=False):
    json = None
    try:
        if path.endswith('.skl'):
            obj = pyRitoFile.read_skl(path)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            json = pyRitoFile.to_json(obj)
        elif path.endswith('.skn'):
            obj = pyRitoFile.read_skn(path)
            LOG(f'Done: File Inspector: Read SKN: {path}')
            json = pyRitoFile.to_json(obj)
        elif path.endswith('.sco'):
            obj = pyRitoFile.read_sco(path)
            LOG(f'Done: File Inspector: Read SCO: {path}')
            json = pyRitoFile.to_json(obj)
        elif path.endswith('.scb'):
            obj = pyRitoFile.read_scb(path)
            LOG(f'Done: File Inspector: Read SCB: {path}')
            json = pyRitoFile.to_json(obj)
        elif path.endswith('.bin'):
            obj = pyRitoFile.read_bin(path)
            obj.un_hash(hashtables)
            LOG(f'Done: File Inspector: Read BIN: {path}')
            json = pyRitoFile.to_json(obj)
        elif path.endswith('.wad.client'):
            obj = pyRitoFile.read_wad(path)
            obj.un_hash(hashtables)
            # read chunk data to guess extension (incase poor unhash)
            with obj.stream(path, 'rb') as bs:
                for chunk in obj.chunks:
                    chunk.read_data(bs)
                    chunk.free_data()
            LOG(f'Done: File Inspector: Read WAD: {path}')
            json = pyRitoFile.to_json(obj)
    except Exception as e:
        if not ignore_error:
            raise e
    return path, to_human(os.stat(path).st_size), json


def read_ritobin(path, ignore_error=False):
    json = None
    try:
        ext_tools.RITOBIN.run(
            path,
            dir_hashes=hash_manager.CustomHashes.local_dir
        )
        py_file = '.'.join(path.split('.bin')[:-1]) + '.py'
        with open(py_file, 'r') as f:
            json = f.read()
        os.remove(py_file)
        LOG(f'Done: File Inspector: Read BIN: {path}')
    except Exception as e:
        if not ignore_error:
            raise e
    return path, to_human(os.stat(path).st_size), json


def prepare(_LOG):
    global LOG
    LOG = _LOG
