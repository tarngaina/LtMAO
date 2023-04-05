from LtMAO.pyRitoFile import BIN, BINEncoder
from json import dump

b = BIN()
b.read('D:/test/skin0.bin')
b.write('D:/test/rewrite_skin0.bin')
with open('D:/test/skin0.json', 'w+') as f:
    dump(b, f, indent=4, cls=BINEncoder)
