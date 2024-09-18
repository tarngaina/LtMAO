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
        a = pyRitoFile.read_mapgeo('D:/test/base_srx.mapgeo')
        pyRitoFile.write_mapgeo('D:/test/t.mapgeo', a, 17)
        
        b = pyRitoFile.read_mapgeo('D:/test/t.mapgeo')
        print('Done')

test()