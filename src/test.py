
# profile
def db(func):
    from cProfile import Profile
    from pstats import Stats
    pr = Profile()
    pr.enable()

    func()

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(20)


if __name__ == '__main__':
    from LtMAO import hapiBin
    hapiBin.copy_vfx_colors('D:/test3/new.bin', 'D:/test3/old.bin')
