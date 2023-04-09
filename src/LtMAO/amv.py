from LtMAO.pyRitoFile.hash import bin_hash


def get_weights(bin):
    mask_data = {}

    entry = bin.entries[0]
    if entry.type != bin_hash('animationGraphData'):
        raise Exception(
            'Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = next(
        (data for data in entry.data if data.hash == bin_hash('mMaskDataMap')), None)
    if mMaskDataMap == None:
        raise Exception(
            'Failed: Get weights: No mMaskDataMap in this BIN.')
    for key in mMaskDataMap.data:
        for field in mMaskDataMap.data[key].data:
            if field.hash == bin_hash('mWeightList'):
                mask_data[key] = field.data

    return mask_data


def set_weights(bin, mask_data):
    entry = bin.entries[0]
    if entry.type != bin_hash('animationGraphData'):
        raise Exception(
            'Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = next(
        (data for data in entry.data if data.hash == bin_hash('mMaskDataMap')), None)
    if mMaskDataMap == None:
        raise Exception(
            'Failed: Get weights: No mMaskDataMap in this BIN.')
    for key in mMaskDataMap.data:
        for field in mMaskDataMap.data[key].data:
            if field.hash == bin_hash('mWeightList'):
                field.data = mask_data[key]
