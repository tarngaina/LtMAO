from LtMAO import ritobin, pyRitoFile, file_inspector, hash_helper, tools


def db(func):
    import cProfile, pstats
    with cProfile.Profile() as profiler:
        func()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(15)

def test():
    from LtMAO import lepath

    print(lepath.ext('D:/test/a.wad.client', 'wad.client', 'wad'))
   
test()