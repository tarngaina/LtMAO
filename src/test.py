from LtMAO import ritobin, hash_helper, pyRitoFile

hash_helper.Storage.read_bin_hashes()
ritobin.bin_to_text('D:/test/bloom.materials.bin', hashtables=hash_helper.Storage.hashtables)
hash_helper.Storage.free_bin_hashes()
