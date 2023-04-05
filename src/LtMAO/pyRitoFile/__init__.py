from LtMAO.pyRitoFile.skl import SKL, SKLJoint
from LtMAO.pyRitoFile.bin import BIN, BINEntry, BINPatch, BINField, BINType, BINEncoder


def read_skl(path):
    skl = SKL()
    skl.read(path)
    return skl


def read_bin(path):
    bin = BIN()
    bin.read(path)
    return bin


def write_bin(path, bin):
    bin.write(path)
