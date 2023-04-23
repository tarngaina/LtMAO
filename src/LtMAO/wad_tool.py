from LtMAO import pyRitoFile
from LtMAO import hash_manager

LOG = print


def unpack(wad_path, raw_path):
    hash_manager.read_wad_hashes()
    wad = pyRitoFile.read_wad(wad_path)
    wad.un_hash(hash_manager.HASHTABLES)
    pyRitoFile.WADHelper.unpack(wad, raw=raw_path, LOG=LOG)
    hash_manager.free_wad_hashes()


def pack(raw_path, wad_path):
    pass


def prepare(_LOG):
    global LOG
    LOG = _LOG
