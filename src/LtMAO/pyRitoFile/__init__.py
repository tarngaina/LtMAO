from LtMAO.pyRitoFile.skl import SKL, SKLJoint, SKLEncoder
from LtMAO.pyRitoFile.skn import SKN, SKNEncoder
from LtMAO.pyRitoFile.so import SO, SOEncoder
from LtMAO.pyRitoFile.bin import BIN, BINEntry, BINPatch, BINField, BINType, BINEncoder
from LtMAO.pyRitoFile.bnk import BNK
from LtMAO.pyRitoFile.wad import WAD, WADEncoder
from json import dump, dumps


def write_json(path, obj):
    with open(path, 'w+') as f:
        if isinstance(obj, SKL):
            dump(obj, f, indent=4, cls=SKLEncoder)
        elif isinstance(obj, SKN):
            dump(obj, f, indent=4, cls=SKNEncoder)
        elif isinstance(obj, SO):
            dump(obj, f, indent=4, cls=SKNEncoder)
        elif isinstance(obj, BIN):
            dump(obj, f, indent=4, cls=BINEncoder)
        elif isinstance(obj, WAD):
            dump(obj, f, indent=4, cls=WADEncoder)


def to_json(obj):
    if isinstance(obj, SKL):
        return dumps(obj, indent=4, cls=SKLEncoder)
    elif isinstance(obj, SKN):
        return dumps(obj, indent=4, cls=SKNEncoder)
    elif isinstance(obj, SO):
        return dumps(obj, indent=4, cls=SOEncoder)
    elif isinstance(obj, BIN):
        return dumps(obj, indent=4, cls=BINEncoder)
    elif isinstance(obj, WAD):
        return dumps(obj, indent=4, cls=WADEncoder)


def read_skl(path):
    skl = SKL()
    skl.read(path)
    return skl


def write_skl(path, skl):
    skl.write(path)


def read_skn(path):
    skn = SKN()
    skn.read(path)
    return skn


def write_skn(path, skn):
    skn.write(path)


def read_sco(path):
    so = SO()
    so.read_sco(path)
    return so


def write_sco(path, so):
    so.write_sco(path)


def read_scb(path):
    so = SO()
    so.read_scb(path)
    return so


def write_scb(path, so):
    so.write_scb(path)


def read_bin(path):
    bin = BIN()
    bin.read(path)
    return bin


def write_bin(path, bin):
    bin.write(path)


def read_wad(path):
    wad = WAD()
    wad.read(path)
    return wad


def write_wad(path, wad):
    wad.write(path)
