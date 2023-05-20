from LtMAO import pyRitoFile

LOG = print


def dds2tex(dds_path, tex_path=None):
    # prepare path
    if tex_path == None:
        tex_path = dds_path.split('.dds')[0] + '.tex'
    LOG(
        f'Ritoddstex: Running: tex2dds: Convert {dds_path} to {tex_path}')
    # read dds header
    with pyRitoFile.io.BinStream(open(dds_path, 'rb')) as bs:
        signature, = bs.read_u32()
        if signature != 0x20534444:
            raise Exception(
                f'Ritoddstex: Failed: dds2tex: Wrong signature DDS file: {signature}')
        uints = bs.read_u32(31)
        dds_header = {
            'dwSize': uints[0],
            'dwFlags': uints[1],
            'dwHeight': uints[2],
            'dwWidth': uints[3],
            'dwPitchOrLinearSize': uints[4],
            'dwDepth': uints[5],
            'dwMipMapCount': uints[6],
            'dwReserved1': uints[7:7+11],
            'ddspf':  {
                'dwSize': uints[18],
                'dwFlags': uints[19],
                'dwFourCC': uints[20],
                'dwRGBBitCount': uints[21],
                'dwRBitMask': uints[22],
                'dwGBitMask': uints[23],
                'dwBBitMask': uints[24],
                'dwABitMask': uints[25],
            },
            'dwCaps': uints[26],
            'dwCaps2': uints[27],
            'dwCaps3': uints[28],
            'dwCaps4': uints[29],
            'dwReserved2': uints[30],
        }
        dds_pixel_format = dds_header['ddspf']
        dds_data = bs.read(-1)
    # prepare tex header
    tex = pyRitoFile.TEX()
    tex.width = dds_header['dwWidth']
    tex.height = dds_header['dwHeight']
    if dds_pixel_format['dwFourCC'] == int('DXT1'.encode('ascii')[::-1].hex(), 16):
        tex.format = pyRitoFile.TEXFormat.DXT1
    elif dds_pixel_format['dwFourCC'] == int('DXT5'.encode('ascii')[::-1].hex(), 16):
        tex.format = pyRitoFile.TEXFormat.DXT5
    elif (dds_pixel_format['dwFlags'] & 0x00000041) == 0x00000041:
        if dds_pixel_format['dwRGBBitCount'] != 32 or dds_pixel_format['dwRBitMask'] != 0x000000ff or dds_pixel_format['dwGBitMask'] != 0x0000ff00 or dds_pixel_format['dwBBitMask'] != 0x00ff0000 or dds_pixel_format['dwABitMask'] != 0xff000000:
            raise Exception(
                f'Ritoddstex: Failed: dds2tex: DDS file is not in exact RGBA8 format.')
        tex.format = pyRitoFile.TEXFormat.RGBA8
    else:
        raise Exception(
            f'Ritoddstex: Failed: dds2tex: Unsupported DDS format: {dds_pixel_format["dwFourCC"]}')
    if dds_header['dwMipMapCount'] > 1:
        expected_dwMipMapCount = 32 - \
            len(f'{max(dds_header["dwWidth"], dds_header["dwHeight"]):032b}'.split(
                '1', 1)[0])
        if dds_header['dwMipMapCount'] != expected_dwMipMapCount:
            raise Exception(
                f'Ritoddstex: Failed: dds2tex: Wrong DDS mipmap count: {dds_header["dwMipMapCount"]}, expected: {expected_dwMipMapCount}'
            )
        tex.mipmaps = True
    # prepare tex data
    if tex.mipmaps:
        # if mipmaps and supported format
        if tex.format in (pyRitoFile.TEXFormat.DXT1, pyRitoFile.TEXFormat.DXT1_):
            block_size = 4
            bytes_per_block = 8
        elif tex.format == pyRitoFile.TEXFormat.DXT5:
            block_size = 4
            bytes_per_block = 16
        else:
            block_size = 1
            bytes_per_block = 4
        mipmap_count = dds_header['dwMipMapCount']
        current_offset = 0
        for i in range(mipmap_count):
            current_width = max(tex.width // (1 << i), 1)
            current_height = max(tex.height // (1 << i), 1)
            block_width = (current_width +
                           block_size - 1) // block_size
            block_height = (current_height +
                            block_size - 1) // block_size
            current_size = bytes_per_block * block_width * block_height
            tex.data.append(
                dds_data[current_offset:current_offset+current_size])
            current_offset += current_size
        # mipmap in dds file is reversed to tex file
        tex.data = tex.data[::-1]
    else:
        tex.data = [dds_data]
    # write tex file
    tex.write(tex_path)
    LOG(
        f'Ritoddstex: Done: tex2dds: Write {tex_path}')


def tex2dds(tex_path, dds_path=None):
    # prepare path
    if dds_path == None:
        dds_path = tex_path.split('.tex')[0] + '.dds'
    LOG(
        f'Ritoddstex: Running: tex2dds: Convert {tex_path} to {dds_path}')
    # read tex
    tex = pyRitoFile.read_tex(tex_path)
    # prepare dds header
    dds_pixel_format = {
        'dwSize': 32,
        'dwFlags': 0,
        'dwFourCC': 0,
        'dwRGBBitCount': 0,
        'dwRBitMask': 0,
        'dwGBitMask': 0,
        'dwBBitMask': 0,
        'dwABitMask': 0,
    }
    if tex.format in (pyRitoFile.TEXFormat.DXT1, pyRitoFile.TEXFormat.DXT1_):
        dds_pixel_format['dwFourCC'] = int(
            'DXT1'.encode('ascii')[::-1].hex(), 16)
        dds_pixel_format['dwFlags'] = 0x00000004
    elif tex.format == pyRitoFile.TEXFormat.DXT5:
        dds_pixel_format['dwFourCC'] = int(
            'DXT5'.encode('ascii')[::-1].hex(), 16)
        dds_pixel_format['dwFlags'] = 0x00000004
    elif tex.format == pyRitoFile.TEXFormat.RGBA8:
        dds_pixel_format['dwFlags'] = 0x00000041
        dds_pixel_format['dwRGBBitCount'] = 32
        dds_pixel_format['dwRBitMask'] = 0x000000ff
        dds_pixel_format['dwGBitMask'] = 0x0000ff00
        dds_pixel_format['dwBBitMask'] = 0x00ff0000
        dds_pixel_format['dwABitMask'] = 0xff000000
    else:
        raise Exception(
            f'Ritoddstex: Failed: tex2dds: Unsupported TEX format: {tex.format}')
    dds_header = {
        'dwSize': 124,
        'dwFlags': 0x00001007,
        'dwHeight': tex.height,
        'dwWidth': tex.width,
        'dwPitchOrLinearSize': 0,
        'dwDepth': 0,
        'dwMipMapCount': 0,
        'dwReserved1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'ddspf': dds_pixel_format,
        'dwCaps': 0x00001000,
        'dwCaps2': 0,
        'dwCaps3': 0,
        'dwCaps4': 0,
        'dwReserved2': 0,
    }
    if tex.mipmaps:
        dds_header['dwFlags'] |= 0x00020000
        dds_header['dwCaps'] |= 0x00400008
        dds_header['dwMipMapCount'] = len(tex.data)
    # write dds file
    with pyRitoFile.io.BinStream(open(dds_path, 'wb')) as bs:
        # signature
        bs.write_u32(0x20534444)
        # header
        bs.write_u32(dds_header['dwSize'])
        bs.write_u32(dds_header['dwFlags'])
        bs.write_u32(dds_header['dwHeight'])
        bs.write_u32(dds_header['dwWidth'])
        bs.write_u32(dds_header['dwPitchOrLinearSize'])
        bs.write_u32(dds_header['dwDepth'])
        bs.write_u32(dds_header['dwMipMapCount'])
        bs.write_u32(*dds_header['dwReserved1'])
        # pixel format
        bs.write_u32(dds_pixel_format['dwSize'])
        bs.write_u32(dds_pixel_format['dwFlags'])
        bs.write_u32(dds_pixel_format['dwFourCC'])
        bs.write_u32(dds_pixel_format['dwRGBBitCount'])
        bs.write_u32(dds_pixel_format['dwRBitMask'])
        bs.write_u32(dds_pixel_format['dwGBitMask'])
        bs.write_u32(dds_pixel_format['dwBBitMask'])
        bs.write_u32(dds_pixel_format['dwABitMask'])
        # continue header
        bs.write_u32(dds_header['dwCaps'])
        bs.write_u32(dds_header['dwCaps2'])
        bs.write_u32(dds_header['dwCaps3'])
        bs.write_u32(dds_header['dwCaps4'])
        bs.write_u32(dds_header['dwReserved2'])
        if tex.mipmaps:
            # mipmap in tex file is reversed to dds file
            for block_data in reversed(tex.data):
                bs.write(block_data)
        else:
            bs.write(tex.data[0])
    LOG(
        f'Ritoddstex: Done: tex2dds: Write {dds_path}')
