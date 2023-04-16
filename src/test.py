
from LtMAO import pyRitoFile
from LtMAO.cdtb_hashes import CDTB

CDTB.sync_all()
CDTB.read_hashes('hashes.game.txt')
b = pyRitoFile.read_wad('D:/test/Milio.wad.client')
b.un_hash(CDTB.HASHTABLES)
pyRitoFile.write_json('D:/test/milio.json', b)
CDTB.free_all()
