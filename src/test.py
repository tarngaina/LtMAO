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
    from LtMAO.pyRitoFile import read_wad
    w = read_wad('D:/test/milio.wad.client')


db(test)
