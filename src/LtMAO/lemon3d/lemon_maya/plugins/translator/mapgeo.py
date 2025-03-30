from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

import os.path, random
from . import helper
from ..... import pyRitoFile
from .....pyRitoFile.structs import Vector, Matrix4

import logging

class MAPGEOTranslator(MPxFileTranslator):
    name = 'League of Legends: MAPGEO'
    extension = 'mapgeo'

    def __init__(self):
        MPxFileTranslator.__init__(self)

    def haveReadMethod(self):
        return True
    
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

    def reader(self, file, option, access):
        mapgeo_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
        # read mapgeo
        print(f'MAPGEO Importer: Read {mapgeo_path}')
        mapgeo = pyRitoFile.read_mapgeo(mapgeo_path)
        # load mapgeo
        helper.mirrorX(mapgeo=mapgeo)
        MAPGEO.scene_load(mapgeo)
        return True

    def writer(self, file, option, access):
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
        dismiss, mapgeo_export_options = MAPGEO.create_ui_mapgeo_export_options(mapgeo_path)
        if dismiss != 'Export':
            return False
        # dump mapgeo
        riot_mapgeo = None
        riot_mapgeo_path = mapgeo_export_options['riot_mapgeo_path']
        if riot_mapgeo_path != '':
            riot_mapgeo = pyRitoFile.read_mapgeo(riot_mapgeo_path)
        mapgeo = pyRitoFile.MAPGEO()
        dump_options = {
            'selected_group': selected_group,
            'version': int(mapgeo_export_options['version']),
            'riot_mapgeo': riot_mapgeo,
        }
        MAPGEO.scene_dump(mapgeo, dump_options)
        helper.mirrorX(mapgeo=mapgeo)
        pyRitoFile.write_mapgeo(mapgeo_path, mapgeo, version=dump_options['version'])
        return True

class MAPGEO:
    @staticmethod
    def create_ui_mapgeo_export_options(mapgeo_path):
        # check riot mapgeo path
        riot_mapgeo_path = os.path.join(
            os.path.dirname(mapgeo_path), 
            f'riot_{os.path.basename(mapgeo_path)}'
        ).replace('\\', '/')
        if not os.path.exists(riot_mapgeo_path):
            riot_mapgeo_path = os.path.join(
                os.path.dirname(mapgeo_path),
                'riot.mapgeo'
            ).replace('\\', '/')
        if not os.path.exists(riot_mapgeo_path):
            riot_mapgeo_path = ''

        if not cmds.optionVar(exists='lemon3d_mapgeo_version'):
            cmds.optionVar(sv=('lemon3d_mapgeo_version', '17'), default=True)
        mapgeo_export_options = {
            'version': cmds.optionVar(query='lemon3d_mapgeo_version'),
            'riot_mapgeo_path': riot_mapgeo_path
        } 
        def set_value_cmd(key, value):
            mapgeo_export_options[key] = value


        def ui_cmd():
            cmds.columnLayout()

            cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
            cmds.text(label='MAPGEO Path:')
            cmds.text(label=mapgeo_path, align='left', width=600)
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=1, adjustableColumn=1)
            def change_cmd(item):
                set_value_cmd('version', item)
                cmds.optionVar(sv=('lemon3d_mapgeo_version', item))
            option_menu = cmds.optionMenu(label='Version: ', changeCommand=change_cmd)
            cmds.menuItem(label = '17')
            cmds.menuItem(label = '13')
            cmds.optionMenu(option_menu, edit=True, value=mapgeo_export_options['version'])
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=3)
            cmds.text(label='Riot MAPGEO Path:')
            mapgeo_text = cmds.text(label=riot_mapgeo_path, align='left', width=600)
            def mapgeobrowse_cmd(text):
                mapgeo_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='MAPGEO(*.mapgeo)',
                    caption='Select Riot MAPGEO file',
                    okCaption='Select'
                )
                if mapgeo_path:
                    mapgeo_path = mapgeo_path[0].replace('\\', '/')
                    cmds.text(text, edit=True, label=mapgeo_path)
                    mapgeo_export_options['riot_mapgeo_path'] = mapgeo_path
            cmds.button(label='Browse Riot MAPGEO', command=lambda e: mapgeobrowse_cmd(mapgeo_text))
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=2)
            cmds.text(label='', w=700)
            def dismiss(result):
                cmds.layoutDialog(dismiss=result)
            cmds.button(label='Export', width=100, command=lambda e: dismiss('Export'))
        
        return cmds.layoutDialog(title='ANM Export Options', ui=ui_cmd), mapgeo_export_options

    @staticmethod
    def scene_load(mapgeo):
        # ensure far clip plane, to see whole map
        cmds.setAttr('perspShape.farClipPlane', 300000)
        # render with alpha cut
        cmds.setAttr('hardwareRenderingGlobals.transparencyAlgorithm', 5)
        # layers
        layer_models = {}
        for i in range(8):
            layer_models[i] = []
        # bushes
        bush_models = []
        # baron models
        baron_models = []

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
                position = vertex.value[pyRitoFile.MAPGEOVertexElementName.Position.name]
                vertices[i].x = position.x
                vertices[i].y = position.y
                vertices[i].z = position.z
                diffuse_uv = vertex.value[pyRitoFile.MAPGEOVertexElementName.Texcoord0.name]
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
                    lightmap_uv = vertex.value[pyRitoFile.MAPGEOVertexElementName.Texcoord7.name]
                    lightmap_u_values[i] = lightmap_uv.x * model.baked_light.scale[0] + model.baked_light.offset[0]
                    lightmap_v_values[i] = 1.0-(lightmap_uv.y * model.baked_light.scale[1] + model.baked_light.offset[1])

                mesh.setUVs(
                    lightmap_u_values, lightmap_v_values, short_lightmap
                )
                mesh.assignUVs(
                    poly_count, poly_indices, short_lightmap
                )

            # color
            if pyRitoFile.MAPGEOVertexElementName.PrimaryColor.name in model.vertices[0].value:
                colors = MColorArray(vertex_count, MColor(1.0, 1.0, 1.0, 1.0))
                vertex_indices = MIntArray(vertex_count)
                for i in range(vertex_count):
                    vertex_indices[i] = i
                    color = vertex.value[pyRitoFile.MAPGEOVertexElementName.PrimaryColor.name]
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
            if model.is_bush:
                bush_models.append(transform_name)

            # extra attributes
            # create bucket hash attribute (for baron related stuff)
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
                    niceName='Bucket Hash',
                    dataType='string'
                )
            cmds.setAttr(f'{transform_name}.buckethash', f"{model.bucket_grid_hash:08x}", type='string')
            # baron models
            if model.bucket_grid_hash > 0:
                baron_models.append(transform_name)
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
    
        # create baron set
        if not cmds.objExists('setBaron'):
            cmds.sets(name='setBaron') 
        cmds.sets(
            *baron_models,
            addElement='setBaron'
        )
        cmds.select(clear=True)

    @staticmethod
    def scene_dump(mapgeo, dump_options):
        version = dump_options['version'] 

        group_transform = dump_options['selected_group']
        group_name = group_transform.name()
        group_dagpath = MDagPath()
        group_transform.getPath(group_dagpath)
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
        mesh_dagpath = MDagPath()
        iteratorMesh = MItDag(MItDag.kDepthFirst, MFn.kMesh)
        iteratorMesh.reset(group_transform.object())
        mapgeo.models = []
        while not iteratorMesh.isDone():
            iteratorMesh.getPath(mesh_dagpath)
            if mesh_dagpath == group_dagpath:
                iteratorMesh.next()
                continue
            if mesh_dagpath.apiType() != MFn.kMesh:
                iteratorMesh.next()
                continue
            mesh = MFnMesh(mesh_dagpath)
            model = pyRitoFile.MAPGEOModel()

            # name and transform
            transform = MFnTransform(mesh.parent(0))
            model.name = transform.name()
            print(f'MAGPEO Exporter: Dumping {model.name}')
            matrix = transform.transformationMatrix()
            model.matrix = Matrix4(*[matrix(i, j) for i in range(4) for j in range(4)])

            # layer
            model.layer = ''.join(
                ['1' if model.name in layer_models[7-i] else '0' for i in range(8)])
            model.layer = pyRitoFile.MAPGEOLayer(int(model.layer, 2))
            # bush
            model.is_bush = True if model.name in bush_models else False
            # baron bucket hash
            try:
                if cmds.attributeQuery(
                    'buckethash',
                    exists=True,
                    node=model.name
                ):
                    model.bucket_grid_hash = int(cmds.getAttr(f'{model.name}.buckethash'), 16)
            except:
                model.bucket_grid_hash = 0
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
                model.baked_light = pyRitoFile.MAPGEOChannel()
                if group_name.startswith('riot_'):
                    model.baked_light.path = group_name.replace('riot_', '').replace('__', '/')+'/'+uv_names[1]
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
                raise FunnyError(
                    f'MAPGEO Exporter ({mesh.name()}): Mesh contains {bad_faces.length()} invalid triangulation faces, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history, that might fix the problem.')
            if bad_faces2.length() > 0:
                component = MFnSingleIndexedComponent()
                face_component = component.create(
                    MFn.kMeshPolygonComponent)
                component.addElements(bad_faces2)
                selections = MSelectionList()
                selections.add(mesh_dagpath, face_component)
                MGlobal.selectCommand(selections)
                raise FunnyError(
                    f'MAPGEO Exporter ({mesh.name()}): Mesh contains {bad_faces2.length()} faces have no material assigned, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history, that might fix the problem.')
            if bad_faces3.length() > 0:
                component = MFnSingleIndexedComponent()
                face_component = component.create(
                    MFn.kMeshPolygonComponent)
                component.addElements(bad_faces3)
                selections = MSelectionList()
                selections.add(mesh_dagpath, face_component)
                MGlobal.selectCommand(selections)
                raise FunnyError(
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
                        position = Vector(pos.x, pos.y, pos.z)
                        vertex.value[pyRitoFile.MAPGEOVertexElementName.Position.name] = position

                        # bush vertex animation 
                        if version > 13 and model.is_bush:
                            bush_vertex_animation = Vector(
                                random.uniform(-0.005, 0.005) * position.x + position.x,
                                random.uniform(-0.005, 0.005) * position.y + position.y,
                                random.uniform(-0.005, 0.005) * position.z + position.z
                            )
                            vertex.value[pyRitoFile.MAPGEOVertexElementName.Texcoord5.name] = bush_vertex_animation

                        # average of normals of all faces connect to this vertex
                        iterator.getNormals(normals)
                        normal_count = normals.length()
                        normal = Vector(0.0, 0.0, 0.0)
                        for i in range(normal_count):
                            normal.x += normals[i].x
                            normal.y += normals[i].y
                            normal.z += normals[i].z
                        normal.x /= normal_count
                        normal.y /= normal_count
                        normal.z /= normal_count
                        vertex.value[pyRitoFile.MAPGEOVertexElementName.Normal.name] = normal

                        # uv
                        
                        diffuse_uv = Vector(
                            u_values[uv_index],
                            1.0 - v_values[uv_index]
                        )
                        vertex.value[pyRitoFile.MAPGEOVertexElementName.Texcoord0.name] = diffuse_uv
                        if lightmap_flag:
                            if uv_index >= 0 and uv_index < lightmap_uv_count:
                                if lightmap_u_values[uv_index] != None and lightmap_v_values[uv_index] != None:
                                    lightmap_uv = Vector(
                                        lightmap_u_values[uv_index],
                                        1.0 - lightmap_v_values[uv_index]
                                    )
                                    vertex.value[pyRitoFile.MAPGEOVertexElementName.Texcoord7.name] = lightmap_uv
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
                            vertex.value[pyRitoFile.MAPGEOVertexElementName.PrimaryColor.name] = color

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
            model.submeshes = [pyRitoFile.MAPGEOSubmesh() for i in range(shader_count)]
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
        riot_mapgeo = dump_options['riot_mapgeo']
        if riot_mapgeo != None:
            print('MAPGEO Exporter (riot.mapgeo): Found riot.mapgeo, copying bucket grids...')
            mapgeo.bucket_grids = riot_mapgeo.bucket_grids
            mapgeo.planar_reflectors = riot_mapgeo.planar_reflectors
        else:
            print('MAPGEO Exporter : No riot.mapgeo found, map can be crashed due to missing bucket grids...')
