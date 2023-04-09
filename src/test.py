from LtMAO import pyRitoFile


skl1 = pyRitoFile.read_skl('d:/test/neeko.skl')
pyRitoFile.write_json('d:/test/neeko.skl.json', skl1)
pyRitoFile.write_skl('d:/test/neeko_new.skl', skl1)

"""
skl2 = pyRitoFile.read_skl('d:/test/jhin.skl')
pyRitoFile.write_json('d:/test/jhin.skl.json', skl2)
pyRitoFile.write_skl('d:/test/jhin_new.skl', skl2)

bin = pyRitoFile.read_bin('d:/test/skin0.bin')
pyRitoFile.write_json('d:/test/skin0.bin.json', bin)
pyRitoFile.write_bin('d:/test/skin0_new.bin', bin)"""
