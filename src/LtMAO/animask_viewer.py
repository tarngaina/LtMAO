from LtMAO.pyRitoFile.hash import FNV1a
from LtMAO.pyRitoFile import BINHelper, bin_hash

PRE_BIN_HASH = {
    'animationGraphData': bin_hash('animationGraphData'),
    'mMaskDataMap': bin_hash('mMaskDataMap'),
    'mWeightList': bin_hash('mWeightList')
}


def get_weights(bin):
    mask_data = {}
    animationGraphData = BINHelper.find_item(
        items=bin.entries,
        compare_func=lambda entry: entry.type == PRE_BIN_HASH[
            'animationGraphData'] or bin_hash(entry.type) == PRE_BIN_HASH['animationGraphData']
    )
    if animationGraphData == None:
        raise Exception(
            'animask_viewer: Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = BINHelper.find_item(
        items=animationGraphData.data,
        compare_func=lambda field: field.hash == PRE_BIN_HASH[
            'mMaskDataMap'] or bin_hash(field.hash) == PRE_BIN_HASH['mMaskDataMap']
    )
    if mMaskDataMap == None:
        raise Exception(
            'animask_viewer: Failed: Get weights: No mMaskDataMap in this BIN.')
    for mask_name, MaskData in mMaskDataMap.data.items():
        mask_data[mask_name] = BINHelper.find_item(
            items=MaskData.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                'mWeightList'] or bin_hash(field.hash) == PRE_BIN_HASH['mWeightList'],
            return_func=lambda field: field.data
        )
    return mask_data


def set_weights(bin, mask_data):
    animationGraphData = BINHelper.find_item(
        items=bin.entries,
        compare_func=lambda entry: entry.type == PRE_BIN_HASH[
            'animationGraphData'] or bin_hash(entry.type) == PRE_BIN_HASH['animationGraphData']
    )
    if animationGraphData == None:
        raise Exception(
            'animask_viewer: Failed: Get weights: Not Animation BIN.')
    mMaskDataMap = BINHelper.find_item(
        items=animationGraphData.data,
        compare_func=lambda field: field.hash == PRE_BIN_HASH[
            'mMaskDataMap'] or bin_hash(field.hash) == PRE_BIN_HASH['mMaskDataMap']
    )
    if mMaskDataMap == None:
        raise Exception(
            'animask_viewer: Failed: Get weights: No mMaskDataMap in this BIN.')
    for mask_name, MaskData in mMaskDataMap.data.items():
        for field in MaskData.data:
            if field.hash == PRE_BIN_HASH['mWeightList'] or bin_hash(field.hash) == PRE_BIN_HASH['mWeightList']:
                field.data = mask_data[mask_name]
                break
