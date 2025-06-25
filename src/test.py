from LtMAO import ritobin, pyRitoFile, file_inspector, hash_helper, tools


def db(func):
    import cProfile, pstats
    with cProfile.Profile() as profiler:
        func()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(15)

def test():
    hash_helper.Storage.read_all_hashes()
    ritobin.bin_to_text('D:/test/map11.bin', 'D:/test/map11.py', hash_helper.Storage.hashtables)
    
    ritobin.text_to_bin('D:/test/map11.py', 'D:/test/a.bin')
    ritobin.bin_to_text('D:/test/a.bin', 'D:/test/a.py', hash_helper.Storage.hashtables)
    hash_helper.Storage.free_all_hashes()
test()