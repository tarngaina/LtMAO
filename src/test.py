from LtMAO import ritobin, pyRitoFile, file_inspector, hash_helper

ritobin.text_to_bin('D:/test/skin0.py', 'D:/test/a.bin')
hash_helper.Storage.read_bin_hashes()
file_inspector.inspect('D:/test/a.bin', hashtables=hash_helper.Storage.hashtables)
hash_helper.Storage.free_bin_hashes()