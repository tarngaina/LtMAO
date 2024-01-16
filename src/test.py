if __name__ == '__main__':
    from cProfile import Profile
    from pstats import Stats
    # profile
    def db(func):
        pr = Profile()
        pr.enable()

        func()

        pr.disable()
        stats = Stats(pr)
        stats.sort_stats('tottime').print_stats()

    def test():
        from LtMAO import hapiBin
        #hapiBin.test()
    
test()