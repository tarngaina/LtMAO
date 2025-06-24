from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

import random
from . import helper
from ..... import pyRitoFile

class MAPGEOImporter(MPxFileTranslator):
    name = 'League of Legends: MAPGEO'
    extension = 'mapgeo'

    def __init__(self):
        MPxFileTranslator.__init__(self)

    def haveReadMethod(self):
        return True

    def defaultExtension(self):
        return self.extension

    def filter(self):
        return f'*.{self.extension}'
    
    def identifyFile(self, file, buffer, size):
        if file.fullName().endswith(f'.{self.extension}'):
            return MPxFileTranslator.kIsMyFileType
        return MPxFileTranslator.kNotMyFileType

    @classmethod
    def creator(cls):
        return asMPxPtr(cls())

    def reader(self, file, options, access):
        def read_cmd(file, options, access):
            mapgeo_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
            # read mapgeo
            print(f'MAPGEO Importer: Read {mapgeo_path}')
            mapgeo = pyRitoFile.mapgeo.MAPGEO().read(mapgeo_path)
            # load mapgeo
            helper.mirrorX(mapgeo=mapgeo)
            MAPGEO.scene_load(mapgeo)
            return True
    
        return helper.try_cmd(lambda: read_cmd(file, options, access))

class MAPGEOExporter(MPxFileTranslator):
    name = 'League of Legends: MAPGEO Export'
    extension = 'mapgeo'

    def __init__(self):
        MPxFileTranslator.__init__(self)
    
    def haveWriteMethod(self):
        return True

    def defaultExtension(self):
        return self.extension

    def filter(self):
        return f'*.{self.extension}'
    
    def identifyFile(self, file, buffer, size):
        if file.fullName().endswith(f'.{self.extension}'):
            return MPxFileTranslator.kIsMyFileType
        return MPxFileTranslator.kNotMyFileType

    @classmethod
    def creator(cls):
        return asMPxPtr(cls())

    def writer(self, file, options, access):
        def write_cmd(file, options, access):
            # check selected
            selections = MSelectionList()
            MGlobal.getActiveSelectionList(selections)
            if selections.isEmpty():
                raise helper.FunnyError('MAGPEO Exporter: Please select a group to export.')
            iterator = MItSelectionList(selections, MFn.kTransform)
            if iterator.isDone():
                raise helper.FunnyError(f'MAGPEO Exporter: Please select a group to export.')
            selected_dagpath = MDagPath()
            iterator.getDagPath(selected_dagpath)
            iterator.next()
            if not iterator.isDone():
                raise helper.FunnyError(f'MAGPEO Exporter: Please select only one group to export.')
            selected_group = MFnTransform(selected_dagpath)

            # export options
            mapgeo_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
            # dump mapgeo
            riot_mapgeo = None
            riot_mapgeo_path = helper.get_riot_path(mapgeo_path)
            if riot_mapgeo_path != '':
                riot_mapgeo = pyRitoFile.mapgeo.MAPGEO().read(riot_mapgeo_path)
            mapgeo = pyRitoFile.mapgeo.MAPGEO()
            options = {key: value for option in options.split(';') for key, value in (option.split('='), )}
            dump_options = {
                'selected_group': selected_group,
                'version': int(options['version']),
                'float16': False if options['float16'] == '0' else True,
                'riot_mapgeo': riot_mapgeo,
            }
            MAPGEO.scene_dump(mapgeo, dump_options)
            helper.mirrorX(mapgeo=mapgeo)
            mapgeo.write(mapgeo_path, float16=dump_options['float16'], version=dump_options['version'])
        
        return helper.try_cmd(lambda: write_cmd(file, options, access))

class MAPGEO:
    @staticmethod
    def scene_load(mapgeo):
        # ensure far clip plane, to see whole map
        cmds.setAttr('perspShape.farClipPlane', 300000)
        # layers
        layer_models = {}
        for i in range(8):
            layer_models[i] = []
        # bushes
        bush_models = []

        # map submeshes by name
        submesh_names = []
        for model in mapgeo.models:
            for submesh in model.submeshes:
                if submesh.name == '-missing@environment-':
                    submesh.name = 'missing_environment'
                submesh.name = submesh.name.replace('/', '__')
                if submesh.name not in submesh_names:
                    submesh_names.append(submesh.name)

        # create shared material
        for submesh_name in submesh_names:
            # material
            material = MFnStandardSurfaceShader()
            material.create()
            material.setName(submesh_name)
            material.setSpecular(0.0)
            material_name = material.name()
            # create renderable, independent shading group
            cmds.sets(
                renderable=True,
                noSurfaceShader=True,
                empty=True,
                name=f'{material_name}_SG'
            )
            # connect material to shading group
            cmds.connectAttr(
                f'{material_name}.outColor',
                f'{material_name}_SG.surfaceShader',
                force=True
            )

        # the group of all meshes, the name of this group = map ID, for example: Map11, Map12
        group_transform = MFnTransform()
        group_transform.create()
        group_name = 'MapID'
        for model in mapgeo.models:
            print(f'MAPGEO Importer: Loading {model.name}')

            vertex_count = len(model.vertices)
            index_count = len(model.indices)
            face_count = index_count // 3

            # create mesh
            vertices = MFloatPointArray(vertex_count)
            u_values = MFloatArray(vertex_count)
            v_values = MFloatArray(vertex_count)
            poly_count = MIntArray(face_count, 3)
            poly_indices = MIntArray(index_count)
            for i in range(vertex_count):
                vertex = model.vertices[i]
                position = vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Position]
                vertices[i].x = position.x
                vertices[i].y = position.y
                vertices[i].z = position.z
                diffuse_uv = vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord0]
                u_values[i] = diffuse_uv.x
                v_values[i] = 1.0 - diffuse_uv.y
            for i in range(index_count):
                poly_indices[i] = model.indices[i]

            mesh = MFnMesh()
            mesh.create(
                vertex_count,
                face_count,
                vertices,
                poly_count,
                poly_indices,
                u_values,
                v_values
            )
            mesh.assignUVs(
                poly_count, poly_indices
            )

            # name and transform
            mesh.setName(f'{model.name}Shape')
            mesh_name = mesh.name()
            transform = MFnTransform(mesh.parent(0))
            transform.setName(model.name)
            transform_name = transform.name()
            matrix = MMatrix()
            matrix_list = [value for value in model.matrix]
            MScriptUtil.createMatrixFromList(matrix_list, matrix)
            transform.set(MTransformationMatrix(matrix))

            lightmap_flag = model.baked_light.path not in (None, '')
            # lightmap uv
            if lightmap_flag:
                temp_lightmap = model.baked_light.path.split('/')
                short_lightmap = temp_lightmap[-1]
                full_lightmap = '__'.join(temp_lightmap[:-1])
                group_name = f'lm_{full_lightmap}'

                mesh.createUVSetWithName(short_lightmap)
                lightmap_u_values = MFloatArray(vertex_count)
                lightmap_v_values = MFloatArray(vertex_count)
                for i in range(vertex_count):
                    vertex = model.vertices[i]
                    lightmap_uv = vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord7]
                    lightmap_u_values[i] = lightmap_uv.x * model.baked_light.scale[0] + model.baked_light.offset[0]
                    lightmap_v_values[i] = 1.0-(lightmap_uv.y * model.baked_light.scale[1] + model.baked_light.offset[1])

                mesh.setUVs(
                    lightmap_u_values, lightmap_v_values, short_lightmap
                )
                mesh.assignUVs(
                    poly_count, poly_indices, short_lightmap
                )

            # color
            if pyRitoFile.mapgeo.MAPGEOVertexElementName.PrimaryColor in model.vertices[0].value:
                colors = MColorArray(vertex_count, MColor(1.0, 1.0, 1.0, 1.0))
                vertex_indices = MIntArray(vertex_count)
                for i in range(vertex_count):
                    vertex_indices[i] = i
                    color = vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.PrimaryColor]
                    colors[i].b = color[0] / 255.0
                    colors[i].g = color[1] / 255.0
                    colors[i].r = color[2] / 255.0
                    colors[i].a = color[3] / 255.0
                mesh.setVertexColors(colors, vertex_indices)

            for submesh in model.submeshes:
                material_name = submesh.name
                # shading group
                face_start = submesh.index_start // 3
                face_end = (submesh.index_start + submesh.index_count) // 3
                # add submesh faces to shading group
                cmds.sets(
                    f'{mesh_name}.f[{face_start}:{face_end}]',
                    forceElement=f'{material_name}_SG',
                    e=True
                )

            mesh.updateSurface()

            # convert layer in byte to 8 char binary string, example: 10101010
            # from RIGHT to LEFT, if the char at index 3 is '1' -> the object appear on layer index 3
            # default for no layer data: 11111111
            layer = f'{model.layer.value:08b}'[::-1]

            # add the model to the layer data, where it belong to
            for i in range(8):
                if layer[i] == '1':
                    layer_models[i].append(transform_name)

            # sets bush
            if pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord5 in model.vertices[0].value:
                bush_models.append(transform_name)
            # extra attributes
            # create bucket hash attribute
            if not cmds.attributeQuery(
                'buckethash',
                exists=True,
                node=transform_name
            ):
                if model.bucket_grid_hash == None:
                    model.bucket_grid_hash = 0
                cmds.addAttr(
                    transform_name,
                    longName='buckethash',
                    niceName='Bucket Grid Hash',
                    dataType='string'
                )
            cmds.setAttr(f'{transform_name}.buckethash', f"{model.bucket_grid_hash:08x}", type='string')
            # create render flags attribute
            if not cmds.attributeQuery(
                'renderflags',
                exists=True,
                node=transform_name
            ):
                if model.render == None:
                    model.render = 0
                cmds.addAttr(
                    transform_name,
                    longName='renderflags',
                    niceName='Render Flags',
                    attributeType='byte'
                )
            cmds.setAttr(f'{transform_name}.renderflags', model.render)

            # add object to group
            group_transform.addChild(transform.object())

        group_transform.setName(group_name)

        # clear select before create setss
        cmds.select(clear=True)

        # check/create set and assign mesh to set
        for i in range(8):
            if not cmds.objExists(f'set{i+1}'):
                cmds.sets(name=f'set{i+1}') 
            cmds.sets(
                *layer_models[i],
                addElement=f'set{i+1}'
            )

        # create bush set
        if not cmds.objExists('setBushes'):
            cmds.sets(name='setBushes') 
        cmds.sets(
            *bush_models,
            addElement='setBushes'
        )
        cmds.select(clear=True)
        
    @staticmethod
    def scene_dump(mapgeo, dump_options):
        version = dump_options['version'] 

        group_transform = dump_options['selected_group']
        group_name = group_transform.name()
        # auto freeze selected group transform
        cmds.makeIdentity(
            group_name,
            apply=True,
            translate=1,
            rotate=1,
            scale=1,
            normal=0,
            preserveNormals=1
        )
        # layer
        layer_models = {}
        for i in range(8):
            if not cmds.objExists(f'set{i+1}'):
                raise helper.FunnyError(
                    f'MAGPEO Exporter: There is no set{i+1} in scene. Please create 8 sets as 8 layers of mapgeo.\n'
                    'How to create a set:\n'
                    '1. [recommended] Use create layers(set) buttons on the shelf.\n'
                    '2. Maya toolbar -> Create -> Sets -> Set.'
                )
            layer_models[i] = cmds.sets(f'set{i+1}', query=True)
            if layer_models[i] == None: layer_models[i] = []

        # bush
        if not cmds.objExists('setBushes'):
            raise helper.FunnyError(
                f'MAGPEO Exporter: There is no setBushes in scene. Please create a set for bushes.\n'
                'How to create a set:\n'
                '1. [recommended] Use create setBushes buttons on the shelf.\n'
                '2. Maya toolbar -> Create -> Sets -> Set.'
            )
        bush_models = cmds.sets('setBushes', query=True)
        if bush_models == None: bush_models = []

        # const define
        NO_COLOR = MColor(-1.0, -1.0, -1.0, -1.0)
        # iterator all meshes in group transform
        mapgeo.models = []
        mesh_dagpath = MDagPath()
        iteratorMesh = MItDag()
        iteratorMesh.reset(group_transform.object(), MItDag.kDepthFirst, MFn.kMesh)
        while not iteratorMesh.isDone():
            iteratorMesh.getPath(mesh_dagpath)
            mesh = MFnMesh(mesh_dagpath)
            model = pyRitoFile.mapgeo.MAPGEOModel()

            # name and transform
            transform = MFnTransform(mesh.parent(0))
            model.name = transform.name()
            print(f'MAGPEO Exporter: Dumping {model.name}')
            matrix = transform.transformationMatrix()
            model.matrix = pyRitoFile.structs.Matrix4(*[matrix(i, j) for i in range(4) for j in range(4)])

            # layer
            model.layer = ''.join(
                ['1' if model.name in layer_models[7-i] else '0' for i in range(8)])
            model.layer = pyRitoFile.mapgeo.MAPGEOLayer(int(model.layer, 2))
            # bush
            model.is_bush = True if model.name in bush_models else False
            # bucket hash
            if cmds.attributeQuery(
                'buckethash',
                exists=True,
                node=model.name
            ):
                try:
                    model.bucket_grid_hash = int(cmds.getAttr(f'{model.name}.buckethash'), 16)
                except:
                    model.bucket_grid_hash = 0
            else:
                model.bucket_grid_hash = 0
            # render flags
            if cmds.attributeQuery(
                'renderflags',
                exists=True,
                node=model.name
            ):
                try:
                    model.render = int(cmds.getAttr(f'{model.name}.renderflags'))
                except:
                    model.render = 0
            else:
                model.render = 0
            # disable backface culling
            model.disable_backface_culling = False
            # get shader/materials
            shaders = MObjectArray()
            face_shader = MIntArray()
            instance = mesh_dagpath.instanceNumber() if mesh_dagpath.isInstanced() else 0
            mesh.getConnectedShaders(instance, shaders, face_shader)
            shader_count = shaders.length()
            if shader_count < 1:
                raise helper. FunnyError(
                    f'MAGPEO Exporter ({mesh.name()}): No material assigned to this mesh, please assign one.')

            shader_indices = [[] for i in range(shader_count)]

            # get all UV sets
            uv_names = []
            mesh.getUVSetNames(uv_names)
            # first uv set = diffuse
            # second uv set = lightmap
            # ignore other sets
            lightmap_flag = False
            if len(uv_names) > 1:
                model.baked_light = pyRitoFile.mapgeo.MAPGEOChannel()
                if group_name.startswith('lm_'):
                    model.baked_light.path = group_name.replace('lm_', '').replace('__', '/')+'/'+uv_names[1]
                else:
                    model.baked_light.path = f'ASSETS/Maps/Lightmaps/Maps/MapGeometry/{group_name}/Base/{uv_names[1]}'
                lightmap_flag = True

            # iterator on faces - 1st
            # dump original triangle indices
            # extra checking stuffs
            bad_faces = MIntArray()  # invalid triangulation polygon
            bad_faces2 = MIntArray()  # no material assigned
            bad_faces3 = MIntArray()  # no uv assigned
            points = MPointArray()
            indices = MIntArray()
            vertices = MIntArray()
            iterator = MItMeshPolygon(mesh_dagpath)
            iterator.reset()
            while not iterator.isDone():
                face_index = iterator.index()
                shader_index = face_shader[face_index]

                # check valid triangulation
                if not iterator.hasValidTriangulation():
                    if face_index not in bad_faces:
                        bad_faces.append(face_index)
                # check face with no material assigned
                if shader_index == -1:
                    if face_index not in bad_faces2:
                        bad_faces2.append(face_index)
                # check if face has no UVs
                if not iterator.hasUVs(uv_names[0]):
                    if face_index not in bad_faces3:
                        bad_faces3.append(face_index)

                # get triangulated face indices & face vertices
                iterator.getTriangles(points, indices)
                iterator.getVertices(vertices)

                # map this face indices by uv_index
                util = MScriptUtil()
                ptr = util.asIntPtr()
                map_indices = {}
                for i in range(vertices.length()):
                    iterator.getUVIndex(i, ptr, uv_names[0])
                    uv_index = util.getInt(ptr)
                    map_indices[vertices[i]] = uv_index

                # add mapped indices
                shader_indices[shader_index].extend(
                    map_indices[indices[i]] for i in range(indices.length()))
                iterator.next()

            if bad_faces.length() > 0:
                component = MFnSingleIndexedComponent()
                face_component = component.create(
                    MFn.kMeshPolygonComponent)
                component.addElements(bad_faces)
                selections = MSelectionList()
                selections.add(mesh_dagpath, face_component)
                MGlobal.selectCommand(selections)
                raise helper.FunnyError(
                    f'MAPGEO Exporter ({mesh.name()}): Mesh contains {bad_faces.length()} invalid triangulation faces, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history, that might fix the problem.')
            if bad_faces2.length() > 0:
                component = MFnSingleIndexedComponent()
                face_component = component.create(
                    MFn.kMeshPolygonComponent)
                component.addElements(bad_faces2)
                selections = MSelectionList()
                selections.add(mesh_dagpath, face_component)
                MGlobal.selectCommand(selections)
                raise helper.FunnyError(
                    f'MAPGEO Exporter ({mesh.name()}): Mesh contains {bad_faces2.length()} faces have no material assigned, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history, that might fix the problem.')
            if bad_faces3.length() > 0:
                component = MFnSingleIndexedComponent()
                face_component = component.create(
                    MFn.kMeshPolygonComponent)
                component.addElements(bad_faces3)
                selections = MSelectionList()
                selections.add(mesh_dagpath, face_component)
                MGlobal.selectCommand(selections)
                raise helper.FunnyError(
                    f'MAPGEO Exporter ({mesh.name()}): Mesh contains {bad_faces3.length()} faces have no UVs assigned, or, those faces UVs are not in first UV set, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history, that might fix the problem.')

            # get uv values
            u_values = MFloatArray()
            v_values = MFloatArray()
            mesh.getUVs(u_values, v_values, uv_names[0])
            if lightmap_flag:
                lightmap_u_values = MFloatArray()
                lightmap_v_values = MFloatArray()
                mesh.getUVs(lightmap_u_values,
                            lightmap_v_values, uv_names[1])
                lightmap_uv_count = lightmap_u_values.length()
                bad_lightmap_mesh = False
            # iterator on vertices
            # to dump all new vertices base on uv_index
            normals = MVectorArray()
            uv_indices = MIntArray()
            iterator = MItMeshVertex(mesh_dagpath)
            iterator.reset()
            model.vertices = []
            while not iterator.isDone():
                # get unique uv
                iterator.getUVIndices(uv_indices)
                uv_count = uv_indices.length()
                if uv_count == 0:
                    continue
                seen = []
                for i in range(uv_count):
                    uv_index = uv_indices[i]
                    if uv_index == -1:
                        continue
                    if uv_index not in seen:
                        seen.append(uv_index)
                        vertex = helper.LemonMAPGEOVertex()
                        vertex.value = {}

                        # position
                        pos = iterator.position(MSpace.kTransform)
                        position = pyRitoFile.structs.Vector(pos.x, pos.y, pos.z)
                        vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Position] = position

                        # bush vertex animation 
                        if model.is_bush:
                            bush_animated_vertex = pyRitoFile.structs.Vector(
                                random.uniform(-0.005, 0.005) * position.x + position.x,
                                random.uniform(-0.005, 0.005) * position.y + position.y,
                                random.uniform(-0.005, 0.005) * position.z + position.z
                            )
                            vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord5] = bush_animated_vertex

                        # average of normals of all faces connect to this vertex
                        iterator.getNormals(normals)
                        normal_count = normals.length()
                        normal = pyRitoFile.structs.Vector(0.0, 0.0, 0.0)
                        for i in range(normal_count):
                            normal.x += normals[i].x
                            normal.y += normals[i].y
                            normal.z += normals[i].z
                        normal.x /= normal_count
                        normal.y /= normal_count
                        normal.z /= normal_count
                        vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Normal] = normal

                        # uv
                        diffuse_uv = pyRitoFile.structs.Vector(
                            u_values[uv_index],
                            1.0 - v_values[uv_index]
                        )
                        vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord0] = diffuse_uv
                        if lightmap_flag:
                            if uv_index >= 0 and uv_index < lightmap_uv_count:
                                if lightmap_u_values[uv_index] != None and lightmap_v_values[uv_index] != None:
                                    lightmap_uv = pyRitoFile.structs.Vector(
                                        lightmap_u_values[uv_index],
                                        1.0 - lightmap_v_values[uv_index]
                                    )
                                    vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord7] = lightmap_uv
                                else:
                                    bad_lightmap_mesh = True
                            else:
                                bad_lightmap_mesh = True
                        vertex.uv_index = uv_index

                        # color
                        color = MColor()
                        iterator.getColor(color)
                        if color != NO_COLOR:
                            color = (
                                int(color.b * 255.0),
                                int(color.g * 255.0),
                                int(color.r * 255.0),
                                int(color.a * 255.0)
                            )
                            vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.PrimaryColor] = color

                        model.vertices.append(vertex)
                iterator.next()

            if lightmap_flag:
                if bad_lightmap_mesh:
                    print(f'MAPGEO Exporter ({mesh.name()}): This mesh contains a vertex that has diffuse UV but no lightmap UV.')

            # sort vertices by uv_index
            model.vertices.sort(key=lambda vertex: vertex.uv_index)

            # create MAPGEOModel data
            index_start = 0
            model.indices = []
            model.submeshes = [pyRitoFile.mapgeo.MAPGEOSubmesh() for i in range(shader_count)]
            for shader_index in range(shader_count):
                # get shader name
                ss = MFnDependencyNode(
                    shaders[shader_index]).findPlug('surfaceShader')
                plugs = MPlugArray()
                ss.connectedTo(plugs, True, False)
                shader_node = MFnDependencyNode(plugs[0].node())

                index_count = len(shader_indices[shader_index])

                # dump MAPGEO data: submeshes, indices and vertices
                submesh = model.submeshes[shader_index]
                submesh.name = shader_node.name()
                if submesh.name == 'missing_environment':
                    submesh.name = '-missing@environment-'
                submesh.name = submesh.name.replace('__', '/')
                submesh.index_start = index_start
                submesh.index_count = index_count
                submesh.min_vertex = min(shader_indices[shader_index])
                submesh.max_vertex = max(shader_indices[shader_index])
                model.indices.extend(shader_indices[shader_index])

                index_start += index_count

            # extra stuffs
            model.texture_overrides = []
            model.texture_overrides_scale_offset = [0.0, 0.0, 0.0, 0.0]
            
            # check limit vertices
            vertices_count = max(model.indices)
            if vertices_count > 65535:
                raise helper.FunnyError(
                    f'MAPGEO Exporter ({mesh.name()}): Too many vertices found: {vertices_count}, max allowed: 65535 vertices.')

            # check limit submeshes
            submesh_count = len(model.submeshes)
            if submesh_count > 64:
                raise helper.FunnyError(
                    f'MAPGEO Exporter ({mesh.name()}): Too many materials assigned on this mesh: {submesh_count}, max allowed: 64 materials on each mesh.')
            mapgeo.models.append(model)


            iteratorMesh.next()

        if len(mapgeo.models) == 0:
            raise helper.FunnyError(
                f'MAPGEO Exporter ({group_name}): There is no mesh inside this group.')
        
        mapgeo.texture_overrides = []

        riot_mapgeo = dump_options['riot_mapgeo']
        if riot_mapgeo != None:
            print('MAPGEO Exporter (riot.mapgeo): Found riot.mapgeo, copying original data...')
            mapgeo.texture_overrides = riot_mapgeo.texture_overrides
            mapgeo.bucket_grids = riot_mapgeo.bucket_grids
            mapgeo.planar_reflectors = riot_mapgeo.planar_reflectors
        else:
            print('MAPGEO Exporter : No riot.mapgeo found, map can be crashed due to missing original data...')
