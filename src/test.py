from cProfile import Profile
from pstats import Stats

import xxhash


# profile
def db(func):
    pr = Profile()
    pr.enable()

    func()

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(20)


def test():
    print(xxhash.xxh64(
        'assets/challenges/config/00_crystals/challengecrystal_borderversion_bronze.ls_c2.tex').hexdigest())


db(test)
