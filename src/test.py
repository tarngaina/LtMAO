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
        d =  pyRitoFile.read_anm('D:/test/kaisa_spell1.anm')
        pyRitoFile.write_anm('D:/test/t.anm', d )
        pyRitoFile.read_anm('D:/test/t.anm')

test()