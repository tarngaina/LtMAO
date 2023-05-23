
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
    b = pyRitoFile.read_bnk('D:/test3/events.bnk')
    pyRitoFile.write_json('D:/test3/events.json', b)
