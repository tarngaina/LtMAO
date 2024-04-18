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
    
    def testWriteSkn4_1():
        from LtMAO.pyRitoFile.skn import SKN
        from requests import get
        
        skn = SKN()
        skn_bytes = get('https://raw.communitydragon.org/latest/game/assets/characters/akali/skins/base/akali.skn').content
        skn.read(path='', raw=skn_bytes)
        output_bytes: bytes = skn.write('akali2.skn', raw=True)
        output_bytes = output_bytes + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        print(skn_bytes == output_bytes)  # True yay :D
    
#test()
testWriteSkn4_1()