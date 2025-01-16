from io import BytesIO
from .stream import BinStream
from .ermmm import FNV1a
from enum import IntEnum

def bin_hash(name):
    return f'{FNV1a(name):08x}'


class SKNVertexType(IntEnum):
    BASIC = 0
    COLOR = 1
    TANGENT = 2

    def __json__(self):
        return self.name


class SKNVertex:
    __slots__ = (
        'position', 'influences', 'weights', 'normal', 'uv',
        'color', 'tangent'
    )

    def __init__(self, position=None, influences=None, weights=None, normal=None, uv=None, color=None, tangent=None):
        self.position = position
        self.influences = influences
        self.weights = weights
        self.normal = normal
        self.uv = uv
        self.color = color
        self.tangent = tangent

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class SKNSubmesh:
    __slots__ = (
        'name', 'bin_hash',
        'vertex_start', 'vertex_count', 'index_start', 'index_count'
    )

    def __init__(self, name=None, bin_hash=None, vertex_start=None, vertex_count=None, index_start=None, index_count=None):
        self.name = name
        self.bin_hash = bin_hash
        self.vertex_start = vertex_start
        self.vertex_count = vertex_count
        self.index_start = index_start
        self.index_count = index_count

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class SKN:
    __slots__ = (
        'signature', 'version', 'flags',
        'bounding_box', 'bounding_sphere', 'vertex_type', 'vertex_size',
        'submeshes', 'indices', 'vertices'
    )

    def __init__(self, signature=None, version=None, flags=None, bounding_box=None, bounding_sphere=None, vertex_type=None, vertex_size=None, submeshes=None, indices=None, vertices=None):
        self.signature = signature
        self.version = version
        self.flags = flags
        self.bounding_box = bounding_box
        self.bounding_sphere = bounding_sphere
        self.vertex_type = vertex_type
        self.vertex_size = vertex_size
        self.submeshes = submeshes
        self.indices = indices
        self.vertices = vertices

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def stream(self, path, mode, raw=None):
        if raw != None:
            if raw == True:  # the bool True value
                return BinStream(BytesIO())
            else:
                return BinStream(BytesIO(raw))
        return BinStream(open(path, mode))

    def read(self, path, raw=None):
        with self.stream(path, 'rb', raw) as bs:
            self.signature, = bs.read_u32()
            if self.signature != 0x00112233:
                raise Exception(
                    f'pyRitoFile: Failed: Read SKN {path}: Wrong signature file: {hex(self.signature)}')
            self.signature = hex(self.signature)

            major, minor = bs.read_u16(2)
            self.version = float(f'{major}.{minor}')
            if major not in (0, 2, 4) and minor != 1:
                raise Exception(
                    f'pyRitoFile: Failed: Read SKN {path}: Unsupported file version: {major}.{minor}')
            
            if major == 0:
                # version 0 doesn't have submesh data
                index_count, vertex_count = bs.read_u32(2)

                submesh = SKNSubmesh()
                submesh.name = 'Base'
                submesh.bin_hash = bin_hash(submesh.name)
                submesh.vertex_start = 0
                submesh.vertex_count = vertex_count
                submesh.index_start = 0
                submesh.index_count = index_count
                self.submeshes = [submesh]
            else:
                # read submeshes
                submesh_count, = bs.read_u32()
                self.submeshes = [SKNSubmesh() for i in range(submesh_count)]
                for submesh in self.submeshes:
                    submesh.name, = bs.read_s_padded(64)
                    submesh.bin_hash = bin_hash(submesh.name)
                    submesh.vertex_start, submesh.vertex_count, submesh.index_start, submesh.index_count = bs.read_u32(
                        4)

                if major == 4:
                    self.flags, = bs.read_u32()

                index_count, vertex_count = bs.read_u32(2)
                if major == 4:
                    self.vertex_size, = bs.read_u32()
                    self.vertex_type, = bs.read_u32()
                    if not self.vertex_type in (0, 1, 2):
                        raise Exception(f'pyRitoFile: Failed: Read SKN {path}: Invalid vertex_type: {self.vertex_type}')
                    self.vertex_type = SKNVertexType(self.vertex_type)
                    self.bounding_box = (bs.read_vec3()[0], bs.read_vec3()[0])
                    self.bounding_sphere = (
                        bs.read_vec3()[0], bs.read_f32()[0])
                    
            if index_count % 3 > 0:
                raise Exception(f'pyRitoFile: Failed: Read SKN {path}: Bad indices data: {index_count}')

            # read unique indices
            indices = bs.read_u16(index_count)
            self.indices = []
            for i in range(0, index_count, 3):
                if indices[i] == indices[i+1] or indices[i+1] == indices[i+2] or indices[i+2] == indices[i]:
                    continue
                self.indices.extend(
                    (indices[i], indices[i+1], indices[i+2]))

            # read vertices
            self.vertices = [SKNVertex() for i in range(vertex_count)]
            for vertex in self.vertices:
                vertex.position, = bs.read_vec3()
                vertex.influences = bs.read_u8(4)
                vertex.weights = bs.read_f32(4)
                vertex.normal, = bs.read_vec3()
                vertex.uv, = bs.read_vec2()
                if self.vertex_type in (SKNVertexType.COLOR, SKNVertexType.TANGENT):
                    vertex.color = bs.read_u8(4)
                    if self.vertex_type == SKNVertexType.TANGENT:
                        vertex.tangent, = bs.read_vec4()

    def write(self, path, raw=None):
        with self.stream(path, 'wb', raw) as bs:
            # magic, version
            bs.write_u32(0x00112233)
            if self.version != None and self.version >= 4:
                bs.write_u16(4, 1)
            else:
                bs.write_u16(1, 1)
                self.version = 1.1
            # submesh
            bs.write_u32(len(self.submeshes))
            for submesh in self.submeshes:
                bs.write_s_padded(submesh.name, 64)
                bs.write_u32(
                    submesh.vertex_start, submesh.vertex_count, submesh.index_start, submesh.index_count)
            if self.version >= 4:
                bs.write_u32(self.flags)
            # stuffs
            bs.write_u32(len(self.indices), len(self.vertices))
            if self.version >= 4:
                bs.write_u32(self.vertex_size, self.vertex_type.value)
                bs.write_vec3(*self.bounding_box)
                bs.write_vec3(self.bounding_sphere[0])
                bs.write_f32(self.bounding_sphere[1])
             # indices vertices
            bs.write_u16(*self.indices)
            for vertex in self.vertices:
                bs.write_vec3(vertex.position)
                bs.write_u8(*vertex.influences)
                bs.write_f32(*vertex.weights)
                bs.write_vec3(vertex.normal)
                bs.write_vec2(vertex.uv)
                if self.vertex_type in (SKNVertexType.COLOR, SKNVertexType.TANGENT):
                    bs.write_u8(*vertex.color)
                    if self.vertex_type == SKNVertexType.TANGENT:
                        bs.write_vec4(vertex.tangent)

            return bs.raw() if raw else None
