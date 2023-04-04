class Vector:
    __slots__ = ('x', 'y', 'z', 'w')

    def __init__(self, x, y, z=None, w=None):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __iter__(self):
        yield self.x
        yield self.y
        if self.z != None:
            yield self.z
        if self.w != None:
            yield self.w

    def __json__(self):
        return [v for v in self]


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

    def __json__(self):
        return [v for v in self]
