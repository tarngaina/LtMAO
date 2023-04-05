from LtMAO.pyRitoFile.hash import FNV1a


def get_weights(bin):
    mask_data = {}

    entry = bin.entries[0]
    if entry.type != FNV1a('animationGraphData'):
        raise Exception(
            'Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = next(
        (field for field in entry.fields if field.hash == FNV1a('mMaskDataMap')), None)
    if mMaskDataMap == None:
        raise Exception(
            'Failed: Get weights: No mMaskDataMap in this BIN.')
    for key in mMaskDataMap.values:
        for field in mMaskDataMap.values[key].values:
            if field.hash == FNV1a('mWeightList'):
                mask_data[key] = field.values

    return mask_data


def set_weights(bin, mask_data):
    entry = bin.entries[0]
    if entry.type != FNV1a('animationGraphData'):
        raise Exception(
            'Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = next(
        (field for field in entry.fields if field.hash == FNV1a('mMaskDataMap')), None)
    if mMaskDataMap == None:
        raise Exception(
            'Failed: Get weights: No mMaskDataMap in this BIN.')
    for key in mMaskDataMap.values:
        for field in mMaskDataMap.values[key].values:
            if field.hash == FNV1a('mWeightList'):
                field.values = mask_data[key]
