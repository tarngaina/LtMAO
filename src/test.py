from cProfile import Profile
from pstats import Stats


# profile
def db(func):
    pr = Profile()
    pr.enable()

    func()

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(20)


def test():
    import pickle
    from LtMAO import pyRitoFile

    p = pickle.dumps(pyRitoFile.read_bin('D:/test/skin0.bin'))
    bin = pickle.loads(p)
    print(pyRitoFile.to_json(bin))


db(test)
