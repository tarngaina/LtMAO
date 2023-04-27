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
    from LtMAO import wad_tool
    wad_tool.pack('D:/test/test', 'D:/test/test.wad.client')


if __name__ == '__main__':
    db(test)
