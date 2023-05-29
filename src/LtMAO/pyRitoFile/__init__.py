from LtMAO.pyRitoFile.skl import SKL, SKLJoint
from LtMAO.pyRitoFile.skn import SKN
from LtMAO.pyRitoFile.so import SO
from LtMAO.pyRitoFile.anm import ANM, ANMPose, ANMTrack, ANMErrorMetric
from LtMAO.pyRitoFile.bin import BIN, BINEntry, BINPatch, BINField, BINType, BINHelper, name_to_hex as bin_hash
from LtMAO.pyRitoFile.bnk import BNK, BNKSection, BNKSectionData, BNKObject, BNKObjectData, BNKObjectType, BNKWem
from LtMAO.pyRitoFile.tex import TEX, TEXFormat
from LtMAO.pyRitoFile.wad import WAD, WADChunk, WADCompressionType, name_to_hex as wad_hash, guess_extension
from LtMAO.pyRitoFile import hash
from LtMAO.pyRitoFile import io
from json import dump, dumps, JSONEncoder


class PRFEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, bytes):
            return str(obj.hex(' ').upper())
        else:
            return JSONEncoder.default(self, obj)


def write_json(path, obj):
    with open(path, 'w+') as f:
        if isinstance(obj, SKL):
            dump(obj, f, indent=4, cls=PRFEncoder)
        elif isinstance(obj, SKN):
            dump(obj, f, indent=4, cls=PRFEncoder)
        elif isinstance(obj, SO):
            dump(obj, f, indent=4, cls=PRFEncoder)
        elif isinstance(obj, ANM):
            dump(obj, f, indent=4, cls=PRFEncoder)
        elif isinstance(obj, BIN):
            dump(obj, f, indent=4, cls=PRFEncoder)
        elif isinstance(obj, BNK):
            dump(obj, f, indent=4, cls=PRFEncoder)
        elif isinstance(obj, TEX):
            dump(obj, f, indent=4, cls=PRFEncoder)
        elif isinstance(obj, WAD):
            dump(obj, f, indent=4, cls=PRFEncoder)


def to_json(obj):
    if isinstance(obj, SKL):
        return dumps(obj, indent=4, cls=PRFEncoder)
    elif isinstance(obj, SKN):
        return dumps(obj, indent=4, cls=PRFEncoder)
    elif isinstance(obj, SO):
        return dumps(obj, indent=4, cls=PRFEncoder)
    elif isinstance(obj, ANM):
        return dumps(obj, indent=4, cls=PRFEncoder)
    elif isinstance(obj, BIN):
        return dumps(obj, indent=4, cls=PRFEncoder)
    elif isinstance(obj, BNK):
        return dumps(obj, indent=4, cls=PRFEncoder)
    elif isinstance(obj, TEX):
        return dumps(obj, indent=4, cls=PRFEncoder)
    elif isinstance(obj, WAD):
        return dumps(obj, indent=4, cls=PRFEncoder)


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


def read_scb(path, raw=None):
    so = SO()
    so.read_scb(path, raw)
    return so


def read_anm(path, raw=None):
    anm = ANM()
    anm.read(path, raw)
    return anm


def read_bin(path, raw=None):
    bin = BIN()
    bin.read(path, raw)
    return bin


def write_bin(path, bin):
    bin.write(path)


def read_bnk(path, raw=None):
    bnk = BNK()
    bnk.read(path, raw)
    return bnk


def read_tex(path, raw=None):
    tex = TEX()
    tex.read(path, raw)
    return tex


def read_wad(path, raw=None):
    wad = WAD()
    wad.read(path, raw)
    return wad


def write_wad(path, wad):
    wad.write(path)
