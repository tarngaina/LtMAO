from LtMAO.pyRitoFile import to_json, SKL, BIN
from os import stat


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


def try_read(path):
    try:
        obj = SKL()
        obj.read(path)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    try:
        obj = BIN()
        obj.read(path)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    raise Exception(
        'Failed: Try Read {path}: File is broken or not supported.')
