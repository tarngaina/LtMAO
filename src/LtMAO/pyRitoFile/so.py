from io import BytesIO, StringIO
from ..pyRitoFile.io import BinStream
from ..pyRitoFile.structs import Vector
from enum import Enum

class SOFlag(Enum):
    HasVcp = 1
    HasLocalOriginLocatorAndPivot = 2

    def __json__(self):
        return self.name


class SO:
    __slots__ = (
        'signature', 'version', 'flags', 'name',
        'central', 'pivot', 'bounding_box', 'material', 'vertex_type',
        'indices', 'positions', 'uvs', 'colors'
    )

    def __init__(self, signature=None, version=None, flags=None, name=None, central=None, pivot=None, bounding_box=None, material=None, vertex_type=None, indices=None, positions=None, uvs=None, colors=None):
        self.signature = signature
        self.version = version
        self.flags = flags
        self.name = name
        self.central = central
        self.pivot = pivot
        self.bounding_box = bounding_box
        self.material = material
        self.vertex_type = vertex_type
        self.indices = indices
        self.positions = positions
        self.uvs = uvs
        self.colors = colors

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def stream(self, path, mode, raw=None):
        if raw != None:
            if raw == True:  # the bool True value
                return BinStream(BytesIO())
            else:
                return BinStream(BytesIO(raw))
        return BinStream(open(path, mode))

    def stream_sco(self, path, mode, raw=None):
        if raw != None:
            if raw == True:  # the bool True value
                return StringIO()
            else:
                return StringIO(raw.decode('ascii'))
        return open(path, mode)

    def stream_scb(self, path, mode, raw=None):
        if raw != None:
            if raw == True:  # the bool True value
                return BinStream(BytesIO())
            else:
                return BinStream(BytesIO(raw))
        return BinStream(open(path, mode))

    def read_sco(self, path, raw=None):
        with self.stream_sco(path, 'r', raw) as f:
            lines = f.readlines()
            lines = [line[:-1] for line in lines]

            self.signature = lines[0]
            if self.signature != '[ObjectBegin]':
                raise Exception(
                    f'pyRitoFile: Failed: Read SCO {path}: Wrong file signature: {self.signature}')

            index = 1  # skip magic
            len1234 = len(lines)
            self.indices = []
            self.positions = []
            self.uvs = []
            while index < len1234:
                inp = lines[index].split()
                if len(inp) == 0:  # cant split, definitely not voldemort
                    index += 1
                    continue
                if inp[0] == 'Name=':
                    self.name = inp[1]

                elif inp[0] == 'CentralPoint=':
                    self.central = Vector(
                        float(inp[1]), float(inp[2]), float(inp[3]))

                elif inp[0] == 'PivotPoint=':
                    self.pivot = Vector(
                        float(inp[1]), float(inp[2]), float(inp[3]))

                elif inp[0] == 'Verts=':
                    vertex_count = int(inp[1])
                    for i in range(index+1, index+1 + vertex_count):
                        inp2 = lines[i].split()
                        self.positions.append(Vector(
                            float(inp2[0]), float(inp2[1]), float(inp2[2])))
                    index = i+1
                    continue

                elif inp[0] == 'Faces=':
                    face_count = int(inp[1])
                    for i in range(index+1, index+1 + face_count):
                        inp2 = lines[i].replace('\t', ' ').split()

                        # skip bad faces
                        face = (int(inp2[1]), int(inp2[2]), int(inp2[3]))
                        if face[0] == face[1] or face[1] == face[2] or face[2] == face[0]:
                            continue
                        self.indices.extend(face)

                        self.material = inp2[4]

                        # u v, u v, u v
                        self.uvs.append(
                            Vector(float(inp2[5]), float(inp2[6])))
                        self.uvs.append(
                            Vector(float(inp2[7]), float(inp2[8])))
                        self.uvs.append(
                            Vector(float(inp2[9]), float(inp2[10])))

                    index = i+1
                    continue

                index += 1

    def write_sco(self, path, raw=None):
        with self.stream_sco(path, 'w', raw) as f:
            f.write('[ObjectBegin]\n')  # magic
            f.write(f'Name= {self.name}\n') # name
            # central
            f.write(
                f'CentralPoint= {self.central.x:.4f} {self.central.y:.4f} {self.central.z:.4f}\n') \
            # pivot
            if self.pivot != None:
                f.write(
                    f'PivotPoint= {self.pivot.x:.4f} {self.pivot.y:.4f} {self.pivot.z:.4f}\n')
            # positions
            f.write(f'Verts= {len(self.positions)}\n')
            for position in self.positions:
                f.write(f'{position.x:.4f} {position.y:.4f} {position.z:.4f}\n')
            # faces
            face_count = len(self.indices) // 3
            f.write(f'Faces= {face_count}\n')
            for i in range(face_count):
                index = i * 3
                f.write('3\t')
                f.write(f' {self.indices[index]:>5}')
                f.write(f' {self.indices[index+1]:>5}')
                f.write(f' {self.indices[index+2]:>5}')
                f.write(f'\t{self.material:>20}\t')
                f.write(f'{self.uvs[index].x:.12f} {self.uvs[index].y:.12f} ')
                f.write(
                    f'{self.uvs[index+1].x:.12f} {self.uvs[index+1].y:.12f} ')
                f.write(
                    f'{self.uvs[index+2].x:.12f} {self.uvs[index+2].y:.12f}\n')
            f.write('[ObjectEnd]')
            return f.getvalue() if raw else None

    def read_scb(self, path, raw=None):
        with self.stream_scb(path, 'rb', raw) as bs:
            self.signature, = bs.read_a(8)
            if self.signature != 'r3d2Mesh':
                raise Exception(
                    f'pyRitoFile: Failed: Read SCB {path}: Wrong file signature: {self.signature}')

            major, minor = bs.read_u16(2)
            self.version = float(f'{major}.{minor}')
            if major not in (3, 2) and minor != 1:
                raise Exception(
                    f'pyRitoFile: Failed: Read SCB {path}: Unsupported file version: {major}.{minor}')

            self.name, = bs.read_a_padded(128)
            vertex_count, face_count, self.flags = bs.read_u32(3)
            self.flags = SOFlag(self.flags)

            # bouding box
            self.bounding_box = (bs.read_vec3()[0], bs.read_vec3()[0])

            if major == 3 and minor == 2:
                self.vertex_type, = bs.read_u32()

            self.positions = bs.read_vec3(vertex_count)
            if self.vertex_type != None:
                if self.vertex_type >= 1:
                    self.colors = [bs.read_u8(4) for i in range(vertex_count)]

            self.central, = bs.read_vec3()
            self.indices = []
            self.uvs = []
            for i in range(face_count):
                face = bs.read_u32(3)
                if face[0] == face[1] or face[1] == face[2] or face[2] == face[0]:
                    continue
                self.indices.extend(face)

                self.material, = bs.read_a_padded(64)

                uvs = bs.read_f32(6)

                # u u u, v v v
                self.uvs.append(Vector(uvs[0], uvs[3]))
                self.uvs.append(Vector(uvs[1], uvs[4]))
                self.uvs.append(Vector(uvs[2], uvs[5]))

    def write_scb(self, path, raw=None):
        def get_bounding_box():
            min = Vector(float("inf"), float("inf"), float("inf"))
            max = Vector(float("-inf"), float("-inf"), float("-inf"))
            for position in self.positions:
                if min.x > position.x:
                    min.x = position.x
                if min.y > position.y:
                    min.y = position.y
                if min.z > position.z:
                    min.z = position.z
                if max.x < position.x:
                    max.x = position.x
                if max.y < position.y:
                    max.y = position.y
                if max.z < position.z:
                    max.z = position.z
            return min, max
        
        with self.stream_scb(path, 'wb', raw) as bs:
            # signature, version
            bs.write_a('r3d2Mesh')  
            bs.write_u16(3, 2)  
            # name but nothing is fine
            bs.write_a_padded('', 128)  
            # position count, face count, flags
            face_count = len(self.indices) // 3
            bs.write_u32(len(self.positions), face_count, self.flags.value)
            bs.write_vec3(*get_bounding_box()) # bounding box
            bs.write_u32(0)  # vertex color
            # positions
            bs.write_vec3(*self.positions)
            # central
            bs.write_vec3(self.central)
            # faces 
            for i in range(face_count):
                index = i * 3
                bs.write_u32(
                    self.indices[index], self.indices[index+1], self.indices[index+2])

                bs.write_a_padded(self.material, 64)
                # u u u, v v v
                bs.write_f32(
                    self.uvs[index].x, self.uvs[index +
                                                1].x, self.uvs[index+2].x,
                    self.uvs[index].y, self.uvs[index+1].y, self.uvs[index+2].y
                )