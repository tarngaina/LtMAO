if __name__ == '__main__':
    
    # profile
    def db(func):
        from cProfile import Profile
        from pstats import Stats

        pr = Profile()
        pr.enable()

        func()

        pr.disable()
        stats = Stats(pr)
        stats.sort_stats('tottime').print_stats()

    def test():
        from LtMAO import pyRitoFile
        pyRitoFile.write_sco('D:/test/t.sco', pyRitoFile.read_sco('D:/test/test.sco'))
        pyRitoFile.write_scb('D:/test/t.scb', pyRitoFile.read_scb('D:/test/test.scb'))

test()