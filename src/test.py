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
        from LtMAO import pyRitoFile
        parser = bnk_tool.BNKParser(
            'D:/test/kaisa_base_sfx_audio.bnk',
            'D:/test/kaisa_base_sfx_events.bnk',
            'D:/test/skin0.bin'
        )
        parser.unpack(parser.get_cache_dir())
        parser.pack('D:/test/t.bnk')

        parser = bnk_tool.BNKParser(
            'D:/test/t.wpk',
            'D:/test/kaisa_base_vo_events.bnk',
            'D:/test/skin0.bin'
        )
    
test()