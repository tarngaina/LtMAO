from io import BytesIO, StringIO
from LtMAO.pyRitoFile.io import BinStream
from LtMAO.pyRitoFile.structs import Vector


class SO:
    __slots__ = (
        'signature', 'version', 'flags', 'name',
        'central', 'pivot', 'bounding_box', 'material', 'vertex_type',
        'indices', 'positions', 'uvs', 'colors'
    )

    def __init__(self):
        self.signature = None
        self.version = None
        self.flags = None
        self.name = None
        self.central = None
        self.pivot = None
        self.bounding_box = None
        self.material = None
        self.vertex_type = None
        self.indices = []
        self.positions = []
        self.uvs = []
        self.colors = []

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

            # bouding box
            self.bounding_box = (bs.read_vec3()[0], bs.read_vec3()[0])

            if major == 3 and minor == 2:
                self.vertex_type, = bs.read_u32()

            self.positions = bs.read_vec3(vertex_count)
            if self.vertex_type != None:
                if self.vertex_type >= 1:
                    self.colors = [bs.read_u8(4) for i in range(vertex_count)]

            self.central, = bs.read_vec3()
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


"""
    def write_sco(self, path):
        with open(path, 'w') as f:
            f.write('[ObjectBegin]\n')  # magic

            f.write(f'Name= {self.name}\n')
            f.write(
                f'CentralPoint= {self.central.x:.4f} {self.central.y:.4f} {self.central.z:.4f}\n')
            if self.pivot != None:
                f.write(
                    f'PivotPoint= {self.pivot.x:.4f} {self.pivot.y:.4f} {self.pivot.z:.4f}\n')

            # vertices
            f.write(f'Verts= {len(self.vertices)}\n')
            for position in self.vertices:
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

    def write_scb(self, path):
        # dump bb after flip
        def get_bounding_box():
            min = Vector(float("inf"), float("inf"), float("inf"))
            max = Vector(float("-inf"), float("-inf"), float("-inf"))
            for vertex in self.vertices:
                if min.x > vertex.x:
                    min.x = vertex.x
                if min.y > vertex.y:
                    min.y = vertex.y
                if min.z > vertex.z:
                    min.z = vertex.z
                if max.x < vertex.x:
                    max.x = vertex.x
                if max.y < vertex.y:
                    max.y = vertex.y
                if max.z < vertex.z:
                    max.z = vertex.z
            return min, max

        with open(path, 'wb') as f:
            bs = BinaryStream(f)

            bs.write_ascii('r3d2Mesh')  # magic
            bs.write_uint16(3, 2)  # major, minor

            bs.write_padded_ascii(128, '')  # well

            face_count = len(self.indices) // 3
            bs.write_uint32(len(self.vertices), face_count)

            # flags:
            # 1 - vertex color
            # 2 - local origin locator and pivot
            bs.write_uint32(self.scb_flag)

            # bounding box
            bs.write_vec3(*get_bounding_box())

            bs.write_uint32(0)  # vertex color

            # vertices
            bs.write_vec3(*self.vertices)

            # central
            bs.write_vec3(self.central)

            # faces - easy peasy squeezy last part
            for i in range(face_count):
                index = i * 3
                bs.write_uint32(
                    self.indices[index], self.indices[index+1], self.indices[index+2])

                bs.write_padded_ascii(64, self.material)

                # u u u, v v v
                bs.write_float(
                    self.uvs[index].x, self.uvs[index +
                                                1].x, self.uvs[index+2].x,
                    self.uvs[index].y, self.uvs[index+1].y, self.uvs[index+2].y
                )

"""
