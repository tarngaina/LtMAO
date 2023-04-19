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
    hashes = {}
    with open(f'./prefs/hashes/morehashes/hashes.game.txt', 'r') as f:
        for line in f:
            key, value = line[:-1].split()
            hashes[key] = value


def test2():
    hashes = {}
    with open(f'./prefs/hashes/morehashes/hashes.game.txt', 'r') as f:
        for line in f:
            key, value = line[:16], line[17:-1]
            hashes[key] = value


db(test)
db(test2)
