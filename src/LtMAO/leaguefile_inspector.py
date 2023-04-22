from LtMAO.pyRitoFile import to_json, read_skl, read_skn, read_sco, read_scb, read_bin, read_wad
from os import stat

LOG = print


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


def read_json(path, hashtables=None, ignore_error=False):
    fsize = to_human(stat(path).st_size)
    try:
        if path.endswith('.skl'):
            obj = read_skl(path)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            return path, fsize, to_json(obj)
        elif path.endswith('.skn'):
            obj = read_skn(path)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            return path, fsize, to_json(obj)
        elif path.endswith('.sco'):
            obj = read_sco(path)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            return path, fsize, to_json(obj)
        elif path.endswith('.scb'):
            obj = read_scb(path)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            return path, fsize, to_json(obj)
        elif path.endswith('.bin'):
            obj = read_bin(path)
            obj.un_hash(hashtables)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            return path, fsize, to_json(obj)
        elif path.endswith('.wad.client'):
            obj = read_wad(path)
            obj.un_hash(hashtables)
            LOG(f'Done: File Inspector: Read SKL: {path}')
            return path, fsize, to_json(obj)
    except Exception as e:
        if ignore_error:
            return path, fsize, None
        else:
            raise e
    return path, fsize, None


def prepare(_LOG):
    global LOG
    LOG = _LOG
