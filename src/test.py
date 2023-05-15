
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
    from LtMAO import pyRitoFile
    pyRitoFile.read_anm('D:/test3/v3.anm')
    pyRitoFile.read_anm('D:/test3/v4.anm')
    pyRitoFile.read_anm('D:/test3/v5.anm')
    pyRitoFile.read_anm('D:/test3/canm.anm')
