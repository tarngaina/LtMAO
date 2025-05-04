from LtMAO import ritobin, hash_helper, pyRitoFile

hash_helper.read_bin_hashes()
ritobin.bin_to_text('D:/test/skin0.bin', hashtables=hash_helper.HASHTABLES)
hash_helper.free_bin_hashes()