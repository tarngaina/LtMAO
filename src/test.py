from LtMAO import ritobin, pyRitoFile, file_inspector, hash_helper, tools


def db(func):
    import cProfile, pstats
    with cProfile.Profile() as profiler:
        func()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(15)

def test():
    from LtMAO.lemon3d import lemon_blender

    lemon_blender.set_startup_py(r'C:\Program Files\Blender Foundation\Blender 4.5\4.5', r'C:\LtMAO')

    

test()