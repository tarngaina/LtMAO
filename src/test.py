
# profile
def db(func):
    from cProfile import Profile
    from pstats import Stats
    pr = Profile()
    pr.enable()

    func()

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(20)


if __name__ == '__main__':

    from LtMAO import wad_tool
    with open('D:/test3/skin0.bin', 'rb') as f:
        bin_data = f.read()
        wad_bytes = wad_tool.pack_v2(
            [
                bin_data,
                bin_data
            ],
            [
                f'data/characters/briar/skins/skin0.bin',
                f'data/characters/briar/animations/skin1.bin'
            ]
        )
        with open('D:/test3/wadout.wad.client', 'wb+') as f:
            f.write(wad_bytes)
