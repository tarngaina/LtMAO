from .pyRitoFile.ermmm import FNV1a
from .pyRitoFile import BINHelper, bin_hash
from .hash_manager import cached_bin_hashes


def find_mMaskDataMap(bin):
    animationGraphData = BINHelper.find_item(
        items=bin.entries,
        compare_func=lambda entry: entry.type == cached_bin_hashes[
            'animationGraphData'] or bin_hash(entry.type) == cached_bin_hashes['animationGraphData']
    )
    if animationGraphData == None:
        raise Exception(
            'animask_viewer: Failed: Find mMaskDataMap: Not Animation BIN.')
    mMaskDataMap = BINHelper.find_item(
        items=animationGraphData.data,
        compare_func=lambda field: field.hash == cached_bin_hashes[
            'mMaskDataMap'] or bin_hash(field.hash) == cached_bin_hashes['mMaskDataMap']
    )
    if mMaskDataMap == None:
        raise Exception(
            'animask_viewer: Failed: Find mMaskDataMap: No mMaskDataMap in this BIN.')
    return mMaskDataMap


def get_weights(bin):
    mask_data = {}
    mMaskDataMap = find_mMaskDataMap(bin)
    for mask_name, MaskData in mMaskDataMap.data.items():
        mask_data[mask_name] = BINHelper.find_item(
            items=MaskData.data,
            compare_func=lambda field: field.hash == cached_bin_hashes[
                'mWeightList'] or bin_hash(field.hash) == cached_bin_hashes['mWeightList'],
            return_func=lambda field: field.data
        )
    return mask_data


def set_weights(bin, mask_data):
    mMaskDataMap = find_mMaskDataMap(bin)
    for mask_name, MaskData in mMaskDataMap.data.items():
        for field in MaskData.data:
            if field.hash == cached_bin_hashes['mWeightList'] or bin_hash(field.hash) == cached_bin_hashes['mWeightList']:
                field.data = mask_data[mask_name]
                break
