import os
import os.path

def join(path, *paths):
    return os.path.join(path, *paths).replace('\\', '/')

def abs(path):
    return os.path.abspath(path).replace('\\', '/')

def rel(path, start):
    return os.path.relpath(path, start).replace('\\', '/')

def ext(path, old, new):
    return path.removesuffix(old) + new

def walk(path, fitler_func, topdown=True):
    res = []
    for root, dirs, files in os.walk(path, topdown):
        for file in files:
            if fitler_func(file):
                res.append(join(root, file))
    return res
