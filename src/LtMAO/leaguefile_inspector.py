from LtMAO.pyRitoFile import to_json, SKL, SKN, SO, BIN, WAD
from os import stat


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


def try_read(path, hashtables=None, ignore_error=False):
    try:
        obj = SKL()
        obj.read(path)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    try:
        obj = SKN()
        obj.read(path)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    try:
        obj = SO()
        obj.read_sco(path)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    try:
        obj = SO()
        obj.read_scb(path)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    try:
        obj = BIN()
        obj.read(path)
        obj.un_hash(hashtables)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    try:
        obj = WAD()
        obj.read(path)
        obj.un_hash(hashtables)
        return path, to_human(stat(path).st_size), to_json(obj)
    except:
        pass

    if ignore_error:
        return path, None, None
    raise Exception(
        'Failed: Try Read {path}: File is broken or not supported.')
