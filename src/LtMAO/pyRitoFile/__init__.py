from LtMAO.pyRitoFile.skl import SKL, SKLJoint, SKLEncoder
from LtMAO.pyRitoFile.bin import BIN, BINEntry, BINPatch, BINField, BINType, BINEncoder
from LtMAO.pyRitoFile.bnk import BNK
from json import dump, dumps


def write_json(path, obj):
    with open(path, 'w+') as f:
        if isinstance(obj, SKL):
            dump(obj, f, indent=4, cls=SKLEncoder)
        elif isinstance(obj, BIN):
            dump(obj, f, indent=4, cls=BINEncoder)


def to_json(obj):
    if isinstance(obj, SKL):
        return dumps(obj, indent=4, cls=SKLEncoder)
    elif isinstance(obj, BIN):
        return dumps(obj, indent=4, cls=BINEncoder)


def read_skl(path):
    skl = SKL()
    skl.read(path)
    return skl


def write_skl(path, skl):
    skl.write(path)


def read_bin(path):
    bin = BIN()
    bin.read(path)
    return bin


def write_bin(path, bin):
    bin.write(path)
