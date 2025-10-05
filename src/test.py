import cProfile, pstats
from LtMAO import pyRitoFile, file_inspector


def db(func):
    with cProfile.Profile() as profile:
        func()
    stats = pstats.Stats(profile)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(20)

def test3():
    b = pyRitoFile.mapgeo.MAPGEO().read('D:/a.mapgeo')
    file_inspector.write_json('D:/test/a.json', b)
    
db(test3)