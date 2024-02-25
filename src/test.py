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
        from LtMAO import hash_manager
        hash_manager.read_wad_hashes()
        new_hashtables = {}
        for hash, value in hash_manager.HASHTABLES['hashes.game.txt'].items():
            if 'assets/sounds/wwise2016/vo' in value:
                new_hashtables[hash]=value
        
        f = open('D:/LtMAO/resources/vo_helper/old_vo_hashes.game.txt', 'w+')
        f.write(
            '\n'.join(hash + ' ' + value for hash, value in new_hashtables.items())
        )
        f.close()



    
test()