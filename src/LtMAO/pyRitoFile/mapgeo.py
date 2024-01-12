from io import BytesIO
from ..pyRitoFile.io import BinStream
from ..pyRitoFile.structs import Vector, Matrix4
from enum import Enum
from flags import Flags

class MAPGEOChannel:
    __slots__ = ('name', 'scale', 'offset')

    def __init__(self):
        self.name = None
        self.scale = None
        self.offset = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}
    
class MAPGEORender(Flags):
    Decal = 1 << 0
    UseEnvironmentDistortionEffectBuffer  = 1 << 1
    RenderOnlyIfEyeCandyOn = 1 << 2
    RenderOnlyIfEyeCandyOff = 1 << 3

    def __json__(self):
        return self.to_simple_str()

class MAPGEOQuality(Flags):
    VeryLow = 1 << 0
    Low = 1 << 1
    Medium = 1 << 2
    High = 1 << 3
    VeryHigh = 1 << 4

    def __json__(self):
        return self.to_simple_str()

class MAPGEOLayer(Flags):
    Layer1 = 1 << 0
    Layer2 = 1 << 1
    Layer3 = 1 << 2
    Layer4 = 1 << 3
    Layer5 = 1 << 4
    Layer6 = 1 << 5
    Layer7 = 1 << 6
    Layer8 = 1 << 7

    def __json__(self):
        return self.to_simple_str()

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
    __slots__ = ('value')

    def __init__(self):
        self.value = {}

    def __json__(self):
        return self.value

class MAPGEOModel:
    __slots__ = (
        'name',
        'vertex_buffer_count', 'vertex_description_id', 'vertex_buffer_ids', 'vertex_count', 'vertices', 
        'index_buffer_id', 'index_count', 'indices',
        'layer', 'quality', 'disable_backface_culling', 'is_bush', 'render', 'point_light', 'light_probe', 
        'bucket_grid_hash', 'submeshes',
        'bounding_box', 'matrix', 
        'baked_light', 'stationary_light', 'baked_paint'
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
        self.quality = None
        self.disable_backface_culling = None
        self.is_bush = None
        self.render = None
        self.point_light = None
        self.light_probe = None
        self.bucket_grid_hash = None
        self.submeshes = None
        self.bounding_box = None
        self.matrix = None
        self.baked_light = None
        self.stationary_light = None
        self.baked_paint = None

    def __json__(self):
        d = {key: getattr(self, key) for key in self.__slots__}
        d['vertices'] = ('write only first vertex to save memory', d['vertices'][0])
        d['indices'] = ('not write to save memory')
        return d
    
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
    XY_Float32_2 = 8

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

class MAPGEOHelper:
    MAPGEO_FORMAT_TO_PYTHON_VALUES = {
        # mapgeo vertex format: (python struct format, bytes size, unpacked items size, unpacked type)
        MAPGEOVertexElementFormat.X_Float32: ('f', 4, 1, float),  
        MAPGEOVertexElementFormat.XY_Float32: ('2f', 8, 2, Vector),  
        MAPGEOVertexElementFormat.XYZ_Float32: ('3f', 12, 3, Vector), 
        MAPGEOVertexElementFormat.XYZW_Float32: ('4f', 16, 4, Vector),  
        MAPGEOVertexElementFormat.BGRA_Packed8888: ('4B', 4, 4, tuple), 
        MAPGEOVertexElementFormat.ZYXW_Packed8888: ('4B', 4, 4, tuple), 
        MAPGEOVertexElementFormat.RGBA_Packed8888: ('4B', 4, 4, tuple), 
        MAPGEOVertexElementFormat.XYZW_Packed8888: ('4B', 4, 4, tuple),  
        MAPGEOVertexElementFormat.XY_Float32_2: ('2f', 8, 2, Vector)  
    }

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
                self.baked_terrain_sampler1, = bs.read_a(bs.read_u32()[0])
                if self.version >= 11:
                    self.baked_terrain_sampler2, = bs.read_a(bs.read_u32()[0])

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

            # read models
            unpacked_vbs = [None]*vertex_buffer_count # for skip reading same vertex buffer
            model_count, = bs.read_u32()
            self.models = [MAPGEOModel() for i in range(model_count)]
            for model_id, model in enumerate(self.models):
                # model name
                if self.version < 12:
                    model.name = bs.read_a(bs.read_i32()[0])
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
                        python_format, byte_size, _, _ = MAPGEOHelper.MAPGEO_FORMAT_TO_PYTHON_VALUES[element.format]
                        vertex_python_format += python_format
                        vertex_byte_size += byte_size
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
                            _, _, unpacked_item_size, unpacked_type = MAPGEOHelper.MAPGEO_FORMAT_TO_PYTHON_VALUES[element.format]
                            unpacked_item_value = (unpacked_vb[current_index+i] for i in range(unpacked_item_size))
                            vertex.value[element.name.name] = unpacked_type(*unpacked_item_value) if unpacked_type is not tuple else unpacked_type(unpacked_item_value)
                            current_index += unpacked_item_size

                # model indices
                model.index_count, model.index_buffer_id = bs.read_u32(2)
                model.indices = ibs[model.index_buffer_id]

                # layer - above or version 13
                if self.version >= 13:
                    model.layer = MAPGEOLayer(bs.read_u8()[0])
                
                # bucket grid hash
                if self.version >= 15:
                    model.bucket_grid_hash, = bs.read_u32()

                # submeshes
                submesh_count, = bs.read_u32()
                model.submeshes = [MAPGEOSubmesh() for i in range(submesh_count)]
                for submesh in model.submeshes:
                    submesh.hash, = bs.read_u32()
                    submesh.name, = bs.read_a(bs.read_u32()[0])
                    submesh.index_start, submesh.index_count, submesh.min_vertex, submesh.max_vertex = bs.read_u32(
                        4)

                if self.version != 5:
                    model.disable_backface_culling, = bs.read_b()

                # bounding box
                model.bounding_box = (bs.read_vec3()[0], bs.read_vec3()[0])

                # transform matrix
                model.matrix, = bs.read_mtx4()

                # quality 
                model.quality = MAPGEOQuality(bs.read_u8()[0])

                # layer - below version 13
                if self.version >= 7 and self.version <= 12:
                    model.layer = MAPGEOLayer(bs.read_u8()[0])

                # is_bush - version 14
                if self.version >= 14:
                    model.is_bush, = bs.read_b()

                # render flag
                if self.version >= 11:
                    model.render = MAPGEORender(bs.read_u8()[0])

                # point light
                if self.version < 7 and use_seperate_point_lights:
                    model.point_light, = bs.read_vec3()

                if self.version < 9:
                    # light probes
                    # 27 floats, 9 for each RGB channel
                    model.light_probe = (bs.read_f32(9), bs.read_f32(9), bs.read_f32(9))

                # lightmap
                model.baked_light = MAPGEOChannel()
                model.baked_light.name, = bs.read_a(bs.read_u32()[0])
                model.baked_light.scale = bs.read_f32(2)
                model.baked_light.offset = bs.read_f32(2)

                if self.version >= 9:
                    model.stationary_light = MAPGEOChannel()
                    model.stationary_light.name, = bs.read_a(bs.read_u32()[0])
                    model.stationary_light.scale = bs.read_f32(2)
                    model.stationary_light.offset = bs.read_f32(2)

                    if self.version >= 12:
                        model.baked_paint = MAPGEOChannel()
                        model.baked_paint.name, = bs.read_a(bs.read_u32()[0])
                        model.baked_paint.scale = bs.read_f32(2)
                        model.baked_paint.offset = bs.read_f32(2)

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