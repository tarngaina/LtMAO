from io import BytesIO
from LtMAO.pyRitoFile.io import BinStream
from LtMAO.pyRitoFile.hash import FNV1a
from json import JSONEncoder


def bin_hash(name):
    return f'{FNV1a(name):08x}'


class SKNEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        else:
            return JSONEncoder.default(self, obj)


class SKNVertex:
    __slots__ = (
        'position', 'influences', 'weights', 'normal', 'uv',
        'color', 'tangent'
    )

    def __init__(self):
        self.position = None
        self.influences = None
        self.weights = None
        self.normal = None
        self.uv = None
        self.color = None
        self.tangent = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class SKNSubmesh:
    __slots__ = (
        'name', 'bin_hash',
        'vertex_start', 'vertex_count', 'index_start', 'index_count'
    )

    def __init__(self):
        self.name = None
        self.bin_hash = None
        self.vertex_start = None
        self.vertex_count = None
        self.index_start = None
        self.index_count = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class SKN:
    __slots__ = (
        'signature', 'version', 'flags',
        'bounding_box', 'bounding_sphere', 'vertex_type', 'vertex_size',
        'submeshes', 'indices', 'vertices'
    )

    def __init__(self):
        self.signature = None
        self.version = None
        self.flags = None
        self.bounding_box = None
        self.bounding_sphere = None
        self.vertex_type = None
        self.vertex_size = None
        self.submeshes = []
        self.indices = []
        self.vertices = []

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def read(self, path, raw=None):
        def IO(): return open(path, 'rb') if raw == None else BytesIO(raw)
        with IO() as f:
            bs = BinStream(f)

            self.signature, = bs.read_u32()
            if self.signature != 0x00112233:
                raise Exception(
                    f'Failed: Read SKN {path}: Wrong signature file: {hex(self.signature)}')
            self.signature = hex(self.signature)

            major, minor = bs.read_u16(2)
            self.version = float(f'{major}.{minor}')
            if major not in (0, 2, 4) and minor != 1:
                raise Exception(
                    f'Failed: Read SKN {path}: Unsupported file version: {major}.{minor}')

            if major == 0:
                # version 0 doesn't have submesh data
                index_count, vertex_count = bs.read_u32(2)

                submesh = SKNSubmesh()
                submesh.name = 'Base'
                submesh.name = bin_hash(submesh.name)
                submesh.vertex_start = 0
                submesh.vertex_count = vertex_count
                submesh.index_start = 0
                submesh.index_count = index_count
                self.submeshes.append(submesh)
            else:
                # read submeshes
                submesh_count, = bs.read_u32()
                self.submeshes = [SKNSubmesh() for i in range(submesh_count)]
                for i in range(submesh_count):
                    submesh = self.submeshes[i]
                    submesh.name, = bs.read_a_padded(64)
                    submesh.bin_hash = bin_hash(submesh.name)
                    submesh.vertex_start, submesh.vertex_count, submesh.index_start, submesh.index_count = bs.read_u32(
                        4)

                if major == 4:
                    self.flags, = bs.read_u32()

                index_count, vertex_count = bs.read_u32(2)
                # pad all this, cause we dont need
                if major == 4:
                    self.vertex_size, = bs.read_u32()
                    self.vertex_type, = bs.read_u32()
                    self.bounding_box = (bs.read_vec3()[0], bs.read_vec3()[0])
                    self.bounding_sphere = (
                        bs.read_vec3()[0], bs.read_f32()[0])

            # read unique indices
            indices = bs.read_u16(index_count)
            for i in range(0, index_count, 3):
                if indices[i] == indices[i+1] or indices[i+1] == indices[i+2] or indices[i+2] == indices[i]:
                    continue
                self.indices.extend(
                    (indices[i], indices[i+1], indices[i+2]))

            # read vertices
            self.vertices = [SKNVertex() for i in range(vertex_count)]
            for i in range(vertex_count):
                vertex = self.vertices[i]
                vertex.position, = bs.read_vec3()
                vertex.influences = bs.read_u8(4)
                vertex.weights = bs.read_f32(4)
                vertex.normal, = bs.read_vec3()
                vertex.uv, = bs.read_vec2()
                if self.vertex_type != None:
                    if self.vertex_type >= 1:
                        vertex.color = bs.read_u8(4)
                        if self.vertex_type == 2:
                            vertex.tangent, = bs.read_vec4()

    """def write(self, path):
        with open(path, 'wb') as f:
            bs = BinaryStream(f)

            bs.write_uint32(0x00112233)  # magic
            bs.write_uint16(1, 1)  # major, minor

            bs.write_uint32(len(self.submeshes))
            for submesh in self.submeshes:
                bs.write_padded_ascii(64, submesh.name)
                bs.write_uint32(
                    submesh.vertex_start, submesh.vertex_count, submesh.index_start, submesh.index_count)

            bs.write_uint32(len(self.indices), len(self.vertices))

            bs.write_uint16(*self.indices)

            for vertex in self.vertices:
                bs.write_vec3(vertex.position)
                bs.write_bytes(vertex.influences)
                bs.write_float(*vertex.weights)
                bs.write_vec3(vertex.normal)
                bs.write_vec2(vertex.uv)"""
