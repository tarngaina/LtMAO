from . import pyRitoFile

def to_json(path, hashtables=None):
    json = {}
    with open(path, 'rb') as f:
        data = f.read(20)
    file_type = pyRitoFile.guess_extension(data)
    if file_type == 'skl':
        obj = pyRitoFile.read_skl(path)
        print(f'file_inspector: Finish: Read SKL: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'skn':
        obj = pyRitoFile.read_skn(path)
        print(f'file_inspector: Finish: Read SKN: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'sco':
        obj = pyRitoFile.read_sco(path)
        print(f'file_inspector: Finish: Read SCO: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'scb':
        obj = pyRitoFile.read_scb(path)
        print(f'file_inspector: Finish: Read SCB: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'anm':
        obj = pyRitoFile.read_anm(path)
        print(f'file_inspector: Finish: Read ANM: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'mapgeo':
        obj = pyRitoFile.read_mapgeo(path)
        print( f'file_inspector: Finish: Read MAPGEO: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'bin':
        obj = pyRitoFile.read_bin(path)
        obj.un_hash(hashtables)
        print(f'file_inspector: Finish: Read BIN: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'bnk':
        obj = pyRitoFile.read_bnk(path)
        print(f'file_inspector: Finish: Read BNK: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'wpk':
        obj = pyRitoFile.read_wpk(path)
        print(f'file_inspector: Finish: Read WPK: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'tex':
        obj = pyRitoFile.read_tex(path)
        print(f'file_inspector: Finish: Read TEX: {path}')
        json = pyRitoFile.to_json(obj)
    elif file_type == 'wad':
        obj = pyRitoFile.read_wad(path)
        obj.un_hash(hashtables)
        # read chunk data to guess extension (incase poor unhash)
        with obj.stream(path, 'rb') as bs:
            for chunk in obj.chunks:
                chunk.read_data(bs)
                chunk.free_data()
        print(f'file_inspector: Finish: Read WAD: {path}')
        json = pyRitoFile.to_json(obj)
    else:
        raise Exception(
            f'file_inspector: Error: Read: {path}: Unknown file type')
    return json