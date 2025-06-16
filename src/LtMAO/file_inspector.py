from . import pyRitoFile
import json

class FIEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, bytes):
            return str(obj.hex(' ').upper())
        else:
            return json.JSONEncoder.default(self, obj)

def write_json(path, obj):
    for good_type in (
        pyRitoFile.skl.SKL, 
        pyRitoFile.skn.SKN, 
        pyRitoFile.so.SO, 
        pyRitoFile.anm.ANM,
        pyRitoFile.mapgeo.MAPGEO, 
        pyRitoFile.bin.BIN, 
        pyRitoFile.bnk.BNK, 
        pyRitoFile.wpk.WPK, 
        pyRitoFile.tex.TEX, 
        pyRitoFile.wad.WAD
    ):
        if isinstance(obj, good_type):
            with open(path, 'w+', encoding='utf-8') as f:
                json.dump(obj, f, indent=4, ensure_ascii=False, cls=FIEncoder)

def inspect(path, hashtables=None):
    with open(path, 'rb') as f:
        data = f.read(20)
    file_type = pyRitoFile.wad.WADExtensioner.guess_extension(data)
    if file_type == 'skl':
        obj = pyRitoFile.skl.SKL().read(path)
        print(f'file_inspector: Finish: Read SKL: {path}')
    elif file_type == 'skn':
        obj = pyRitoFile.skn.SKN().read(path)
        print(f'file_inspector: Finish: Read SKN: {path}')
    elif file_type == 'sco':
        obj = pyRitoFile.so.SO().read_sco(path)
        print(f'file_inspector: Finish: Read SCO: {path}')
    elif file_type == 'scb':
        obj = pyRitoFile.so.SO().read_scb(path)
        print(f'file_inspector: Finish: Read SCB: {path}')
    elif file_type == 'anm':
        obj = pyRitoFile.anm.ANM().read(path)
        print(f'file_inspector: Finish: Read ANM: {path}')
    elif file_type == 'mapgeo':
        obj = pyRitoFile.mapgeo.MAPGEO().read(path)
        print( f'file_inspector: Finish: Read MAPGEO: {path}')
    elif file_type == 'bin':
        obj = pyRitoFile.bin.BIN().read(path)
        obj.un_hash(hashtables)
        print(f'file_inspector: Finish: Read BIN: {path}')
    elif file_type == 'bnk':
        obj = pyRitoFile.bnk.BNK().read(path)
        print(f'file_inspector: Finish: Read BNK: {path}')
    elif file_type == 'wpk':
        obj = pyRitoFile.wpk.WPK().read(path)
        print(f'file_inspector: Finish: Read WPK: {path}')
    elif file_type == 'tex':
        obj = pyRitoFile.tex.TEX().read(path)
        print(f'file_inspector: Finish: Read TEX: {path}')
    elif file_type == 'wad':
        obj = pyRitoFile.wad.WAD().read(path)
        obj.un_hash(hashtables)
        # read chunk data to guess extension (incase poor unhash)
        with pyRitoFile.stream.BytesStream.reader(path) as bs:
            for chunk in obj.chunks:
                chunk.read_data(bs)
                chunk.free_data()
        print(f'file_inspector: Finish: Read WAD: {path}')
    else:
        raise Exception(f'file_inspector: Error: Read: {path}: Unknown file type')
    json_file = path + '.json'
    write_json(json_file, obj)
    print(f'file_inspector: Finish: Write Json: {json_file}')