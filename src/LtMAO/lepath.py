import os.path

def join(path, *paths):
    return os.path.join(path, *paths).replace('\\', '/')

def ext(path, old, new):
    return path.removesuffix(old) + new