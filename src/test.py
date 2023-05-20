
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
    from PIL import Image
    with Image.open('D:/test3/test.dds') as img:
        print(img.width)
        print(img.height)
