from LtMAO.pyRitoFile.skl import SKL, SKLJoint, SKLEncoder
from LtMAO.pyRitoFile.skn import SKN, SKNEncoder
from LtMAO.pyRitoFile.so import SO, SOEncoder
from LtMAO.pyRitoFile.bin import BIN, BINEntry, BINPatch, BINField, BINType, BINEncoder, BINHelper
from LtMAO.pyRitoFile.bnk import BNK
from LtMAO.pyRitoFile.wad import WAD, WADChunk, WADCompressionType, WADEncoder
from LtMAO.pyRitoFile import hash
from LtMAO.pyRitoFile import io
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


def read_skl(path, raw=None):
    skl = SKL()
    skl.read(path, raw)
    return skl


def write_skl(path, skl):
    skl.write(path)


def read_skn(path, raw=None):
    skn = SKN()
    skn.read(path, raw)
    return skn


def write_skn(path, skn):
    skn.write(path)


def read_sco(path, raw=None):
    so = SO()
    so.read_sco(path, raw)
    return so


def write_sco(path, so):
    so.write_sco(path)


def read_scb(path, raw=None):
    so = SO()
    so.read_scb(path, raw)
    return so


def write_scb(path, so):
    so.write_scb(path)


def read_bin(path, raw=None):
    bin = BIN()
    bin.read(path, raw)
    return bin


def write_bin(path, bin):
    bin.write(path)


def read_wad(path, raw=None):
    wad = WAD()
    wad.read(path, raw)
    return wad


def write_wad(path, wad):
    wad.write(path)
