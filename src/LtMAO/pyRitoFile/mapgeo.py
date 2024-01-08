from io import BytesIO
from ..pyRitoFile.io import BinStream
from ..pyRitoFile.structs import Vector, Matrix4

from enum import Enum

class MAPGEOSubmesh:
    __slots__ = (
        'name', 'hash',
        'index_start', 'index_count',
        'min_vertex', 'max_vertex'
    )

    def __init__(self):
        self.name = None
        self.hash = None
        self.index_start = None
        self.index_count = None
        self.min_vertex = None
        self.max_vertex = None
    
    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

class MAPGEOVertex:
    __slots__ = (
        'position', 'normal', 'diffuse_uv', 'lightmap_uv', 'color'
    )

    def __init__(self):
        self.position = None
        self.normal = None
        self.diffuse_uv = None
        self.lightmap_uv = None
        self.color = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

class MAPGEOModel:
    __slots__ = (
        'name',
        'vertex_buffer_count', 'vertex_description_id', 'vertex_buffer_ids', 'vertex_count', 'vertices', 
        'index_buffer_id', 'index_count', 'indices',
        'layer', 'is_bush', 'bucket_hash',
        'submeshes',
        'bounding_box', 'matrix', 
        'lightmap', 'lightmap_scale_offset'
    )

    def __init__(self):
        self.name = None
        self.vertex_buffer_count = None
        self.vertex_description_id = None
        self.vertex_buffer_ids = None
        self.vertex_count = None
        self.vertices = []
        self.index_buffer_id = None
        self.index_count = None
        self.indices = []
        self.layer = None
        self.is_bush = None
        self.bucket_hash = None
        self.submeshes = None
        self.bounding_box = None
        self.matrix = None
        self.lightmap = None
        self.lightmap_scale_offset = None

    def __json__(self):
        return {key: getattr(self, key) if key != 'vertices' else getattr(self, key)[:-1] for key in self.__slots__}
    
class MAPGEOVertexElementName(Enum):
    Position = 0
    BlendWeight = 1
    Normal = 2
    FogCoordinate = 3
    PrimaryColor = 4
    SecondaryColor = 5
    BlendIndex = 6
    Texcoord0 = 7
    Texcoord1 = 8
    Texcoord2 = 9
    Texcoord3 = 10
    Texcoord4 = 11
    Texcoord5 = 12
    Texcoord6 = 13
    Texcoord7 = 14
    Tangent = 15

    def __json__(self):
        return self.name
    
class MAPGEOVertexElementFormat(Enum):
    X_Float32 = 0
    XY_Float32 = 1
    XYZ_Float32 = 2
    XYZW_Float32 = 3
    BGRA_Packed8888 = 4
    ZYXW_Packed8888 = 5
    RGBA_Packed8888 = 6
    XYZW_Packed8888 = 7
    Unknown_8_Bytes = 8

    def __json__(self):
        return self.name
   
class MAPGEOVertexElement:
    __slots__ = ('name', 'format')

    def __init__(self):
        self.name = None
        self.format = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}
    
class MAPGEOVertexUsage(Enum):
    Static = 0
    Dynamic = 1
    Stream = 2

    def __json__(self):
        return self.name

class MAPGEOVertexDescription:
    __slots__ = ('usage','elements')

    def __init__(self):
        self.usage = None
        self.elements = []

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

class MAPGEO:
    __slots__ = (
        'signature', 'version',
        'baked_terrain_sampler1', 'baked_terrain_sampler2',
        'vertex_descriptions',
        'models'
    )
    
    def __init__(self):
        self.signature = None
        self.version = None
        self.baked_terrain_sampler1 = None
        self.baked_terrain_sampler2 = None
        self.vertex_descriptions = []
        self.models = []

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
            self.signature, = bs.read_a(4)
            if self.signature != 'OEGM':
                raise Exception(
                    f'pyRitoFile: Failed: Read MAPGEO {path}: Wrong signature file: {self.signature}')
            self.version, = bs.read_u32()
            if self.version not in (5, 6, 7, 9, 11, 12, 13, 14, 15):
                raise Exception(
                    f'pyRitoFile: Failed: Read MAPGEO {path}: Unsupported file version: {self.version}')

            use_seperate_point_lights = False
            if self.version < 7:
                use_seperate_point_lights, = bs.read_b()

            if self.version >= 9:
                self.baked_terrain_sampler1 = bs.read(bs.read_u32()[0]).decode('ascii')
                if self.version >= 11:
                    self.baked_terrain_sampler2 = bs.read(bs.read_u32()[0]).decode('ascii')

            # vertex descriptions
            vd_count, = bs.read_u32()
            self.vertex_descriptions = [MAPGEOVertexDescription() for i in range(vd_count)]
            for i in range(vd_count):
                vertex_description = self.vertex_descriptions[i]
                vertex_description.usage = MAPGEOVertexUsage(bs.read_u32()[0])
                element_count, = bs.read_u32()
                unpacked_u32s = bs.read_u32(element_count * 2)
                vertex_description.elements = [MAPGEOVertexElement() for j in range(element_count)]
                for j in range(element_count):
                    vertex_description.elements[j].name = MAPGEOVertexElementName(unpacked_u32s[j*2])
                    vertex_description.elements[j].format = MAPGEOVertexElementFormat(unpacked_u32s[j*2+1])
                bs.pad(8 * (15 - element_count))  # pad empty vertex descriptions

            # vertex buffers 
            # -> can not read now because need vertex descriptions 
            # -> save offset instead
            vertex_buffer_count, = bs.read_u32()
            vbos = [None]*vertex_buffer_count
            for i in range(vertex_buffer_count):
                if self.version >= 13:
                    bs.pad(1)  # layer
                vb_size, = bs.read_u32()
                vbos[i] = bs.tell()
                bs.pad(vb_size)
        
            # index buffers
            # -> can straight read because its just int array
            index_buffer_count, = bs.read_u32()
            ibs = [None]*index_buffer_count
            for i in range(index_buffer_count):
                if self.version >= 13:
                    bs.pad(1)  # layer
                ib_size, = bs.read_u32()
                ibs[i] = bs.read_u16(ib_size // 2)

            # for skip reading same vertex buffer
            unpacked_vbs = [None]*vertex_buffer_count
            format_convert_values = {
                # mapgeo vertex: (python struct format, bytes size, unpacked items size)
                MAPGEOVertexElementFormat.X_Float32: ('f', 4, 1),  
                MAPGEOVertexElementFormat.XY_Float32: ('2f', 8, 2),  
                MAPGEOVertexElementFormat.XYZ_Float32: ('3f', 12, 3), 
                MAPGEOVertexElementFormat.XYZW_Float32: ('4f', 16, 4),  
                MAPGEOVertexElementFormat.BGRA_Packed8888: ('4B', 4, 4), 
                MAPGEOVertexElementFormat.ZYXW_Packed8888: ('4B', 4, 4), 
                MAPGEOVertexElementFormat.RGBA_Packed8888: ('4B', 4, 4), 
                MAPGEOVertexElementFormat.XYZW_Packed8888: ('4B', 4, 4),  
                MAPGEOVertexElementFormat.Unknown_8_Bytes: ('2f', 8, 2)  
            }
            # read models
            model_count, = bs.read_u32()
            self.models = [MAPGEOModel() for i in range(model_count)]
            for model_id, model in enumerate(self.models):
                # model name
                if self.version < 12:
                    model.name = bs.read_ascii(bs.read_int32())
                else:
                    model.name = f'MapGeo_Instance_{model_id}'
                # model vertices
                model.vertex_count, model.vertex_buffer_count, model.vertex_description_id = bs.read_u32(3)
                # read vertex buffer into unpacked vbs
                model.vertex_buffer_ids = bs.read_i32(model.vertex_buffer_count)
                for i, vertex_buffer_id in enumerate(model.vertex_buffer_ids):
                    vertex_description = self.vertex_descriptions[model.vertex_description_id+i]
                    # skip unpacked vertex buffers
                    if unpacked_vbs[vertex_buffer_id] != None:
                        continue
                    unpacked_vbs[vertex_buffer_id] = []
                    # vertex python format & size through vertex descriptions of single vertex (yes only 1)
                    vertex_python_format = ''
                    vertex_byte_size = 0
                    for element in vertex_description.elements:
                        vertex_python_format += format_convert_values[element.format][0]
                        vertex_byte_size += format_convert_values[element.format][1]
                    # save the current offset (we are in middle of model reading)
                    # jump to vertex buffers place through saved vertex buffer offset
                    return_offset = bs.tell()
                    bs.seek(vbos[vertex_buffer_id])
                    # read whole vertex buffers with vertex format & size
                    # every vertex use same format so just multiply with vertex count
                    unpacked_vbs[vertex_buffer_id] = bs.read_fmt(
                        fmt = vertex_python_format*model.vertex_count,
                        fmt_size = vertex_byte_size*model.vertex_count
                    )
                    # return to model reading after read vertices
                    bs.seek(return_offset)
                # now with unpacked vbs, set values for vertex
                model.vertices = [MAPGEOVertex() for i in range(model.vertex_count)]
                for i, vertex_buffer_id in enumerate(model.vertex_buffer_ids):
                    vertex_description = self.vertex_descriptions[model.vertex_description_id+i]
                    unpacked_vb = unpacked_vbs[vertex_buffer_id]
                    current_index = 0
                    for vertex in model.vertices:
                        for element in vertex_description.elements:
                            if element.name == MAPGEOVertexElementName.Position:
                                vertex.position = Vector(
                                    unpacked_vb[current_index],
                                    unpacked_vb[current_index+1],
                                    unpacked_vb[current_index+2]
                                )
                            elif element.name == MAPGEOVertexElementName.PrimaryColor:
                                vertex.color = (
                                    unpacked_vb[current_index],
                                    unpacked_vb[current_index+1],
                                    unpacked_vb[current_index+2],
                                    unpacked_vb[current_index+3],
                                )
                            elif element.name == MAPGEOVertexElementName.Texcoord0:
                                vertex.diffuse_uv = Vector(
                                    unpacked_vb[current_index],
                                    unpacked_vb[current_index+1]
                                )
                            elif element.name == MAPGEOVertexElementName.Texcoord7:
                                vertex.lightmap_uv = Vector(
                                    unpacked_vb[current_index],
                                    unpacked_vb[current_index+1]
                                )
                            current_index += format_convert_values[element.format][2]

                # model indices
                model.index_count, model.index_buffer_id = bs.read_u32(2)
                model.indices = ibs[model.index_buffer_id]
                # layer
                model.layer = 255
                if self.version >= 13:
                    model.layer, = bs.read_u8()
                
                # bucket hash
                if self.version >= 15:
                    model.bucket_hash, = bs.read_u32()

                # submeshes
                submesh_count, = bs.read_u32()
                model.submeshes = [MAPGEOSubmesh() for i in range(submesh_count)]
                for submesh in model.submeshes:
                    submesh.hash, = bs.read_u32()
                    submesh.name, = bs.read_a(bs.read_u32()[0])
                    submesh.index_start, submesh.index_count, submesh.min_vertex, submesh.max_vertex = bs.read_u32(
                        4)

                if self.version != 5:
                    # flip normals
                    bs.pad(1)

                # bounding box
                model.bounding_box = (bs.read_vec3()[0], bs.read_vec3()[0])

                # transform matrix
                model.matrix, = bs.read_mtx4()

                # quality: 1, 2, 4, 8, 16
                # all quality = 1|2|4|8|16 = 31
                bs.pad(1)

                # layer - below version 13
                if self.version >= 7 and self.version <= 12:
                    model.layer, = bs.read_u8()

                # bush - version 14
                if self.version >= 14:
                    model.is_bush, = bs.read_b()

                if self.version >= 11:
                    # render flag
                    bs.pad(1)

                if use_seperate_point_lights and self.version < 7:
                    # pad seperated point light
                    bs.pad(12)

                if self.version < 9:
                    # pad 9 light probes
                    bs.pad(108)

                # lightmap
                model.lightmap, = bs.read_a(bs.read_u32()[0])
                # lightmap so (scale & offset)
                # real lightmap uv = lightmap uv * lightmap scale + lightmap offset
                model.lightmap_scale_offset = bs.read_f32(4)

                if self.version >= 9:
                    # baked light
                    bs.pad(bs.read_u32()[0])
                    # baked light so
                    bs.pad(16)

                    if self.version >= 12:
                        # baked paint
                        bs.pad(bs.read_u32()[0])
                        # baked paint so
                        bs.pad(16)

            return
            # for modded file with no bucket grid, planar reflector: stop reading
            current = bs.tell()
            end = bs.end()
            if current == end:
                return

            # there is no reason to read bucket grids below suporting version
            if version >= 15:
                # bucket grids
                bucket_grid_count = bs.read_uint32()
                self.bucket_grids = [MAPGEOBucketGrid() for i in range(bucket_grid_count)]
                for i in range(bucket_grid_count):
                    # hash
                    self.bucket_grids[i].hash = bs.read_uint32()
                    # min/max x/z(16), max out stick x/z(8), bucket size x/z(8)
                    self.bucket_grids[i].header = bs.read_bytes(32)
                    bucket_size = bs.read_uint16()
                    self.bucket_grids[i].no_bucket = bs.read_byte()[0]
                    self.bucket_grids[i].bucket_flag = bs.read_byte()[0]
                    vertex_count, index_count = bs.read_uint32(2)
                    if self.bucket_grids[i].no_bucket == 0:
                        self.bucket_grids[i].vertices = bs.read_bytes(12*vertex_count)
                        self.bucket_grids[i].indices = bs.read_bytes(2*index_count)
                        # max stick out x/z(8)
                        # start index + base vertex(8)
                        # inside face count + sticking out face count(4)
                        self.bucket_grids[i].buckets = bs.read_bytes(
                            20*bucket_size*bucket_size)
                        if self.bucket_grids[i].bucket_flag >= 1:
                            # if first bit = 1, read face flags
                            self.bucket_grids[i].face_flags = bs.read_bytes(
                                index_count//3)

                self.planar_reflector = MAPGEOPlanarReflector()
                pr_count = bs.read_uint32()
                self.planar_reflector.prs = [None]*pr_count
                for i in range(pr_count):
                    self.planar_reflector.prs[i] = (
                        # matrix4 transform of viewpoint?
                        bs.read_bytes(64),
                        # 2 vec3 position to indicate the plane
                        bs.read_bytes(24),
                        # vec3 normal, direction of plane
                        bs.read_bytes(12)
                    )