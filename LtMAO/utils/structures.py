class Vector:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield self.x
        yield self.y
        if self.z != None:
            yield self.z


class Quaternion:
    __slots__ = ('x', 'y', 'z', 'w')

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
        yield self.w
