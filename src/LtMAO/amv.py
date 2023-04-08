from LtMAO.pyRitoFile.hash import bin_hash


def get_weights(bin):
    mask_data = {}

    entry = bin.entries[0]
    if entry.type != bin_hash('animationGraphData'):
        raise Exception(
            'Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = next(
        (field for field in entry.fields if field.hash == bin_hash('mMaskDataMap')), None)
    if mMaskDataMap == None:
        raise Exception(
            'Failed: Get weights: No mMaskDataMap in this BIN.')
    for key in mMaskDataMap.values:
        for field in mMaskDataMap.values[key].values:
            if field.hash == bin_hash('mWeightList'):
                mask_data[key] = field.values

    return mask_data


def set_weights(bin, mask_data):
    entry = bin.entries[0]
    if entry.type != bin_hash('animationGraphData'):
        raise Exception(
            'Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = next(
        (field for field in entry.fields if field.hash == bin_hash('mMaskDataMap')), None)
    if mMaskDataMap == None:
        raise Exception(
            'Failed: Get weights: No mMaskDataMap in this BIN.')
    for key in mMaskDataMap.values:
        for field in mMaskDataMap.values[key].values:
            if field.hash == bin_hash('mWeightList'):
                field.values = mask_data[key]
