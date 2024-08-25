from ..pyRitoFile.skl import SKL, SKLJoint
from ..pyRitoFile.skn import SKN, SKNVertex, SKNSubmesh
from ..pyRitoFile.so import SO
from ..pyRitoFile.anm import ANM, ANMPose, ANMTrack, ANMErrorMetric
from ..pyRitoFile.mapgeo import MAPGEO
from ..pyRitoFile.bin import BIN, BINEntry, BINPatch, BINField, BINType, BINHelper, name_to_hex as bin_hash
from ..pyRitoFile.bnk import BNK, BNKObjectType
from ..pyRitoFile.wpk import WPK
from ..pyRitoFile.tex import TEX, TEXFormat
from ..pyRitoFile.wad import WAD, WADChunk, WADCompressionType, name_to_hex as wad_hash, guess_extension
from ..pyRitoFile import hash
from ..pyRitoFile import io
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
    good_types = [SKL, SKN, SO, ANM, MAPGEO, BIN, BNK, WPK, TEX, WAD]
    with open(path, 'w+') as f:
        for good_type in good_types:
            if isinstance(obj, good_type):
                dump(obj, f, indent=4, cls=PRFEncoder)


def to_json(obj):
    good_types = [SKL, SKN, SO, ANM, MAPGEO, BIN, BNK, WPK, TEX, WAD]
    for good_type in good_types:
        if isinstance(obj, good_type):
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

def write_anm(path, anm):
    anm.write(path)



def read_mapgeo(path, raw=None):
    mg = MAPGEO()
    mg.read(path, raw)
    return mg


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

def write_bnk(path, bnk, wem_datas):
    bnk.write(path, wem_datas)

def read_wpk(path, raw=None):
    wpk = WPK()
    wpk.read(path, raw)
    return wpk

def write_wpk(path, wpk, wem_datas):
    wpk.write(path, wem_datas)


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
