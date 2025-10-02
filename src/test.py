from LtMAO import ritobin, pyRitoFile, file_inspector, hash_helper, tools


def db(func):
    import cProfile, pstats
    with cProfile.Profile() as profiler:
        func()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(15)

def test():
    #ritobin.bin_to_text('C:/test/bloom.materials.bin', 'C:/test/bloom.materials.py')
    ritobin.text_to_bin( 'C:/test/bloom.materials.py', 'C:/test/a.bin')
    

db(test)