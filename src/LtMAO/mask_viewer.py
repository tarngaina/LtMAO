from . import hash_helper

def find_mMaskDataMap(bin):
    animationGraphDatas = bin.get_items(lambda entry: entry.type == hash_helper.Storage.bin_hashes['animationGraphData'])
    for animationGraphData in animationGraphDatas:
        mMaskDataMaps = animationGraphData.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['mMaskDataMap'])
        if len(mMaskDataMaps) == 0:
            raise Exception(
                'mask_viewer: Error: No mMaskDataMap in this BIN.')
        else:
            return mMaskDataMaps[0]
    raise Exception('mask_viewer: Error: Not Animation BIN.')

def get_weights(bin):
    mask_data = {}
    mMaskDataMap = find_mMaskDataMap(bin)
    for mask_name, MaskData in mMaskDataMap.data.items():
        mWeightLists = MaskData.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['mWeightList'])
        if len(mWeightLists) > 0:
            mask_data[mask_name] = mWeightLists[0].data
    return mask_data


def set_weights(bin, mask_data):
    mMaskDataMap = find_mMaskDataMap(bin)
    for mask_name, MaskData in mMaskDataMap.data.items():
        mWeightLists = MaskData.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['mWeightList'])
        if len(mWeightLists) > 0:
            mWeightLists[0].data = mask_data[mask_name]
