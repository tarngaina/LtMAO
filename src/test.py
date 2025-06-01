from LtMAO import pyRitoFile

import os

wads = []
for root, dirs, files in os.walk('D:/Games/Riot Games/League of Legends/Game/DATA/FINAL'):
    for file in files:
        if file.endswith('.wad.client'):
            wad_f = os.path.join(root, file).replace('\\', '/')
            wads.append(wad_f)

for wad_f in wads:
    wad = pyRitoFile.wad.WAD().read(wad_f)
    with pyRitoFile.stream.BytesStream.reader(wad_f) as bs:
        for chunk in wad.chunks:
            chunk.read_data(bs) 
            if chunk.extension == 'bin':
                sig = pyRitoFile.bin.BIN().read(chunk.data, raw=True)
                if sig == 'PTCH':
                    print(chunk, sig)
                else:
                    print(f'skiped {chunk.hash}') 
            chunk.free_data()