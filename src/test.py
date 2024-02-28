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
        src = 'D:/test/skin11.bin'
        from LtMAO import leaguefile_inspector, hash_manager
        hash_manager.read_all_hashes()
        path, size, type, json = leaguefile_inspector.read_lfi(
            src, hash_manager.HASHTABLES)
        dst = src + '.json'
        with open(dst, 'w+') as f:
            f.write(json if json != None else '{}')
        hash_manager.free_all_hashes()

    
test()