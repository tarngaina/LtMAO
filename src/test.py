if __name__ == '__main__':
    from LtMAO import pyRitoFile
    b = pyRitoFile.read_mapgeo('D:/test/test.mapgeo')
    print(dir(b))