from LtMAO.cdtb_hashes import CDTB
from LtMAO import pyRitoFile

CDTB.LOG = print
CDTB.sync_all()

b = pyRitoFile.read_bin('D:/test/skin0.bin')
b.un_hash(CDTB.HASHTABLES)
