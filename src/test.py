from LtMAO.pyRitoFile import BIN


b = BIN()
b.read('D:/test/first.bin')
b.write('D:/test/second.bin')

c = BIN()
c.read('D:/test/second.bin')
