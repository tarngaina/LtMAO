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
        from LtMAO import bnk_tool
        parser = bnk_tool.BNKParser(
            'D:/test/kaisa_base_vo_audio.wpk',
            'D:/test/kaisa_base_vo_events.bnk',
            ''
        )
        parser.unpack('D:/test')

    
test()