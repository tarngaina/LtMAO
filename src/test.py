from LtMAO import ritobin, pyRitoFile, file_inspector, hash_helper, tools


def db(func):
    import cProfile, pstats
    with cProfile.Profile() as profiler:
        func()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(15)

def test():
    from LtMAO import bumpath
    bum = bumpath.Bum()
    bum.add_source_dirs(['C:/test/aatrox.wad'])
    bum.source_bins[bumpath.unify_path('data/characters/aatrox/skins/skin0.bin')] = True
    bum.scan()
    bum.bum('C:/test/new folder', ignore_missing=True, combine_linked=True)

test()