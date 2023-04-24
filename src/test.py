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
    from LtMAO import no_skin, pyRitoFile
    no_skin.process(
        r'C:\Riot Games\League of Legends\Game\DATA\FINAL\Champions')
    # bin = pyRitoFile.read_bin('D:/test/skin1.bin')
    # bin.write('D:/test/skin1_rewrite.bin')


db(test)
