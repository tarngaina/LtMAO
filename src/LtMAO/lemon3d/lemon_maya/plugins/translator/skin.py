from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

import os.path
from . import helper
from ..... import pyRitoFile
from .....pyRitoFile.hash import Elf
from .....pyRitoFile.structs import Vector, Quaternion

LOG = print

class SKNTranslator(MPxFileTranslator):
    name = 'League of Legends: SKN'
    extension = 'skn'

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

    def reader(self, file, option, access):
        # import options
        skn_path = helper.ensure_path_extension(file.expandedFullName(), 'skn')
        dismiss, import_options = SKN.create_ui_skn_import_options(skn_path)
        if dismiss != 'Import': 
            return False
        # read skn
        skn = pyRitoFile.read_skn(skn_path)
        # fix skn name if need
        skn_name = skn_path.split('/')[-1].split('.')[0]
        if skn_name in '0123456789':
            skn_name = 'nf_'+self.name
        # load skeleton first if need
        group_transform = None
        skl = None
        if import_options['import_skeleton']:
            skl_path = import_options['skl_path']
            skl = pyRitoFile.read_skl(skl_path)
            skl.joints = [helper.LemonSKLJoint(**{key: getattr(joint, key) for key in joint.__slots__}) for joint in skl.joints]
            helper.mirrorX(skl=skl)
            group_transform = SKL.scene_load(skl, { 'skl_name': skn_name })
        # load skn
        helper.mirrorX(skn=skn)
        load_options = {
            'skn_name': skn_name,
            'group_transform': group_transform,
            'separated_mesh': import_options['import_separated_mesh'],
            'skl': skl
        }
        SKN.scene_load(skn, load_options)
        return True

class SKLTranslator(MPxFileTranslator):
    name = 'League of Legends: SKL'
    extension = 'skl'

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

    def reader(self, file, option, access):
        # read skl
        skl_path = helper.ensure_path_extension(file.expandedFullName(), 'skl')
        skl = pyRitoFile.read_skl(skl_path)
        skl.joints = [helper.LemonSKLJoint(**{key: getattr(joint, key) for key in joint.__slots__}) for joint in skl.joints]
        # fix skn name if need
        skl_name = skl_path.split('/')[-1].split('.')[0]
        if skl_name in '0123456789':
            skl_name = 'nf_'+self.name
        # load skl
        helper.mirrorX(skl=skl)
        load_options = {
            'skl_name': skl_name,
        }
        SKL.scene_load(skl, load_options)
        return True

class SkinTranslator(MPxFileTranslator):
    name = 'League of Legends: SKN & SKL'
    extension = 'skn'

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
        # check selected
        selections = MSelectionList()
        MGlobal.getActiveSelectionList(selections)
        if selections.isEmpty():
            raise helper.FunnyError('SKN Exporter: Please select a group of skinned meshes and joints.')
        if selections.length() > 1:
            raise helper.FunnyError('SKN Exporter: Too many selections.')
        selected_dagpath = MDagPath()
        selections.getDagPath(0, selected_dagpath)
        if selected_dagpath.apiType() != MFn.kTransform:
            raise helper.FunnyError('SKN Exporter: Selected object is not a group.')
        selected_group = MFnTransform(selected_dagpath)
        if selected_group.childCount() == 0:
            raise helper.FunnyError('SKN Exporter: Selected group is empty.')
        # export options
        skn_path = helper.ensure_path_extension(file.expandedFullName(), 'skn')
        skl_path = skn_path.replace('.skn', '.skl')
        dismiss, skn_export_options = SKN.create_ui_skn_export_options(skn_path, skl_path)
        if dismiss != 'Export':
            return False
        #  dump_skl
        riot_skl = None
        riot_skl_path = skn_export_options['riot_skl_path']
        if riot_skl_path != '':
            riot_skl = pyRitoFile.read_skl(riot_skl_path)
        dump_options = {
            'selected_group': selected_group,
            'riot_skl': riot_skl
        }
        skl = pyRitoFile.SKL()
        SKL.scene_dump(skl, dump_options)
        helper.mirrorX(skl=skl)
        # dump skn
        riot_skn = None
        riot_skn_path = skn_export_options['riot_skn_path']
        if riot_skn_path != '':
            riot_skn = pyRitoFile.read_skn(riot_skn_path)
        skn = pyRitoFile.SKN()
        dump_options = {
            'skl': skl,
            'selected_group': selected_group,
            'riot_skn': riot_skn
        }
        SKN.scene_dump(skn, dump_options)
        helper.mirrorX(skn=skn)
        pyRitoFile.write_skl(skl_path, skl)
        pyRitoFile.write_skn(skn_path, skn)
        
        return True

class SKN:
    @staticmethod
    def create_ui_skn_import_options(skn_path):
        # check skl path
        skl_path = skn_path.replace('.skn', '.skl')
        if not os.path.exists(skl_path):
            skl_path = ''
        skn_import_options = {
            'import_skeleton': True,
            'import_separated_mesh': True,
            'skl_path': skl_path
        }
        def ui_cmd():
            cmds.columnLayout()

            cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
            cmds.text(label='SKN Path:')
            cmds.text(label=skn_path, align='left', width=600)
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
            cmds.text(label='SKL Path:')
            skl_text = cmds.text(label=skl_path, align='left', width=600)
            def sklbrowse_cmd(text):
                skl_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='SKL(*.skl)',
                    caption='Select SKL file',
                    okCaption='Select'
                )
                if skl_path:
                    skl_path = skl_path[0].replace('\\', '/')
                    cmds.text(text, edit=True, label=skl_path)
                    skn_import_options['skl_path'] = skl_path
            cmds.button(label='Browse SKL', command=lambda e: sklbrowse_cmd(skl_text))
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=1)
            def set_value_cmd(key, value):
                skn_import_options[key] = value
            cmds.checkBoxGrp(
                vertical=True, 
                numberOfCheckBoxes=2, 
                columnWidth=[(1, 400), (2, 400)], 
                labelArray2=('Import with skeleton', 'Import mesh separated by materials.'),
                valueArray2=(skn_import_options['import_skeleton'], skn_import_options['import_separated_mesh']),
                onCommand1=lambda e: set_value_cmd('import_skeleton', True),
                offCommand1=lambda e: set_value_cmd('import_skeleton', False),
                onCommand2=lambda e: set_value_cmd('import_separated_mesh', True),
                offCommand2=lambda e: set_value_cmd('import_separated_mesh', False)
            )
            cmds.setParent('..')


            cmds.rowLayout(numberOfColumns=2)
            cmds.text(label='', w=700)
            cmds.button(label='Import', width=100, command=lambda e: cmds.layoutDialog(dismiss='Import'))

        return cmds.layoutDialog(title='SKN Import Options', ui=ui_cmd), skn_import_options
    
    @staticmethod
    def create_ui_skn_export_options(skn_path, skl_path):
        # check riot skn path
        riot_skn_path = os.path.join(
            os.path.dirname(skn_path), 
            f'riot_{os.path.basename(skn_path)}'
        ).replace('\\', '/')
        if not os.path.exists(riot_skn_path):
            riot_skn_path = os.path.join(
                os.path.dirname(skn_path),
                'riot.skn'
            ).replace('\\', '/')
        if not os.path.exists(riot_skn_path):
            riot_skn_path = ''
        # check riot skl path
        riot_skl_path = os.path.join(
            os.path.dirname(skl_path), 
            f'riot_{os.path.basename(skl_path)}'
        ).replace('\\', '/')
        if not os.path.exists(riot_skl_path):
            riot_skl_path = os.path.join(
                os.path.dirname(skl_path),
                'riot.skl'
            ).replace('\\', '/')
        if not os.path.exists(riot_skl_path):
            riot_skl_path = ''

        skn_export_options = {
            'riot_skn_path': riot_skn_path,
            'riot_skl_path': riot_skl_path
        }

        def ui_cmd():
            cmds.columnLayout()

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
            cmds.text(label='Riot SKN Path:')
            skn_text = cmds.text(label=riot_skn_path, align='left', width=600)
            def sknbrowse_cmd(text):
                skn_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='SKN(*.skn)',
                    caption='Select Riot SKN file',
                    okCaption='Select'
                )
                if skn_path:
                    skn_path = skn_path[0].replace('\\', '/')
                    cmds.text(text, edit=True, label=skn_path)
                    skn_export_options['riot_skn_path'] = skn_path
            cmds.button(label='Browse Riot SKN', command=lambda e: sknbrowse_cmd(skn_text))
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
            cmds.text(label='Riot SKL Path:')
            skl_text = cmds.text(label=riot_skl_path, align='left', width=600)
            def sklbrowse_cmd(text):
                skl_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='SKL(*.skl)',
                    caption='Select Riot SKL file',
                    okCaption='Select'
                )
                if skl_path:
                    skl_path = skl_path[0].replace('\\', '/')
                    cmds.text(text, edit=True, label=skl_path)
                    skn_export_options['riot_skl_path'] = skl_path
            cmds.button(label='Browse Riot SKL', command=lambda e: sklbrowse_cmd(skl_text))
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=2)
            cmds.text(label='', w=700)
            cmds.button(label='Export', width=100, command=lambda e: cmds.layoutDialog(dismiss='Export'))
        
        return cmds.layoutDialog(title='SKN Export Options', ui=ui_cmd), skn_export_options

    @staticmethod
    def scene_load(skn, load_options):
        def load_combined():
            vertex_count = len(skn.vertices)
            index_count = len(skn.indices)
            face_count = index_count // 3

            # create mesh
            vertices = MFloatPointArray(vertex_count)
            u_values = MFloatArray(vertex_count)
            v_values = MFloatArray(vertex_count)
            poly_count = MIntArray(face_count, 3)
            poly_indices = MIntArray(index_count)
            for i in range(vertex_count):
                vertex = skn.vertices[i]
                vertices[i].x = vertex.position.x
                vertices[i].y = vertex.position.y
                vertices[i].z = vertex.position.z
                u_values[i] = vertex.uv.x
                v_values[i] = 1.0 - vertex.uv.y
            for i in range(index_count):
                poly_indices[i] = skn.indices[i]

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

            # name
            skn_name = load_options['skn_name']
            mesh.setName(f'{skn_name}Shape')
            mesh_name = mesh.name()
            mesh_transform = MFnTransform(mesh.parent(0))
            mesh_transform.setName(f'mesh_{skn_name}')
            # add to group
            group_transform = load_options['group_transform']
            if group_transform == None:
                group_transform = MFnTransform()
                group_transform.create()
                group_transform.setName(f'group_{skn_name}')
            group_transform.addChild(mesh_transform.object())
            # materials
            skl = load_options['skl']
            for submesh in skn.submeshes:
                # check duplicate name node
                if skl != None:
                    match_joint = next(
                        (joint for joint in skl.joints if joint.name == submesh.name), None)
                    if match_joint != None:
                        submesh.name = submesh.name.lower()

                # lambert material
                lambert = MFnLambertShader()
                lambert.create()
                lambert.setName(submesh.name)
                lambert_name = lambert.name()
                # shading group
                face_start = submesh.index_start // 3
                face_end = (submesh.index_start + submesh.index_count) // 3
                # create renderable, independent shading group
                cmds.sets(
                    renderable=True,
                    noSurfaceShader=True,
                    empty=True,
                    name=f'{lambert_name}_SG'
                )
                # add submesh faces to shading group
                cmds.sets(
                    f'{mesh_name}.f[{face_start}:{face_end}]',
                    forceElement=f'{lambert_name}_SG',
                    e=True
                )
                # connect lambert to shading group
                cmds.connectAttr(
                    f'{lambert_name}.outColor',
                    f'{lambert_name}_SG.surfaceShader',
                    force=True
                )

            if skl != None:
                influence_count = len(skl.influences)
                mesh_dagpath = MDagPath()
                mesh.getPath(mesh_dagpath)

                # select mesh + joint
                selections = MSelectionList()
                selections.add(mesh_dagpath)
                for influence in skl.influences:
                    selections.add(skl.joints[influence].dagpath)
                MGlobal.selectCommand(selections)

                # bind selections
                cmds.skinCluster(
                    name=f'{skn_name}_skinCluster',
                    maximumInfluences=4,
                    toSelectedBones=True,
                )

                # get skin cluster
                in_mesh = mesh.findPlug('inMesh')
                plugs = MPlugArray()
                in_mesh.connectedTo(plugs, True, False)
                skin_cluster = MFnSkinCluster(plugs[0].node())
                skin_cluster_name = skin_cluster.name()

                # mask influence
                influences_dagpath = MDagPathArray()
                skin_cluster.influenceObjects(influences_dagpath)
                mask_influence = MIntArray(influence_count)
                for i in range(influence_count):
                    dagpath = skl.joints[skl.influences[i]].dagpath
                    match_j = next(j for j in range(influence_count)
                                    if dagpath == influences_dagpath[j])
                    if match_j != None:
                        mask_influence[i] = match_j

                # weights
                cmds.setAttr(f'{skin_cluster_name}.normalizeWeights', 0)
                component = MFnSingleIndexedComponent()
                # empty vertex_component = all vertices
                vertex_component = component.create(MFn.kMeshVertComponent)
                weights = MDoubleArray(vertex_count * influence_count)
                for i in range(vertex_count):
                    vertex = skn.vertices[i]
                    for j in range(4):
                        weight = vertex.weights[j]
                        influence = vertex.influences[j]
                        if weight > 0:
                            weights[i * influence_count + influence] = weight
                skin_cluster.setWeights(
                    mesh_dagpath, vertex_component, mask_influence, weights, False)
                cmds.setAttr(f'{skin_cluster_name}.normalizeWeights', 1)
                cmds.skinPercent(
                    skin_cluster_name,
                    mesh_name,
                    normalize=True
                )
            cmds.select(clear=True)
            # shud be final line
            mesh.updateSurface()

        def load_separated():
            # create group
            skn_name = load_options['skn_name']
            group_transform = load_options['group_transform']
            if group_transform == None:
                group_transform = MFnTransform()
                group_transform.create()
                group_transform.setName(f'group_{skn_name}')

            # init seperated meshes data
            shader_count = len(skn.submeshes)
            shader_vertices = {}
            shader_indices = {}
            shader_meshes = []
            for shader_index in range(shader_count):
                submesh = skn.submeshes[shader_index]
                shader_vertices[shader_index] = skn.vertices[submesh.vertex_start:
                                                                submesh.vertex_start+submesh.vertex_count]
                shader_indices[shader_index] = skn.indices[submesh.index_start:
                                                            submesh.index_start+submesh.index_count]
                min_vertex = min(shader_indices[shader_index])
                shader_indices[shader_index] = [
                    index-min_vertex for index in shader_indices[shader_index]]

            skl = load_options['skl']
            for shader_index in range(shader_count):
                vertex_count = len(shader_vertices[shader_index])
                index_count = len(shader_indices[shader_index])
                face_count = index_count // 3

                # create mesh
                vertices = MFloatPointArray(vertex_count)
                u_values = MFloatArray(vertex_count)
                v_values = MFloatArray(vertex_count)
                poly_count = MIntArray(face_count, 3)
                poly_indices = MIntArray(index_count)
                for i in range(vertex_count):
                    vertex = shader_vertices[shader_index][i]
                    vertices[i].x = vertex.position.x
                    vertices[i].y = vertex.position.y
                    vertices[i].z = vertex.position.z
                    u_values[i] = vertex.uv.x
                    v_values[i] = 1.0 - vertex.uv.y
                for i in range(index_count):
                    poly_indices[i] = shader_indices[shader_index][i]

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

                # save the MFnMesh to bind later
                shader_meshes.append(mesh)

                # name
                submesh = skn.submeshes[shader_index]
                mesh.setName(f'{skn_name}_{submesh.name}Shape')
                mesh_name = mesh.name()
                mesh_transform = MFnTransform(mesh.parent(0))
                mesh_transform.setName(
                    f'mesh_{submesh.name}')

                # add mesh to group
                group_transform.addChild(mesh_transform.object())

                # check duplicate name node
                if skl != None:
                    match_joint = next(
                        (joint for joint in skl.joints if joint.name == submesh.name), None)
                    if match_joint != None:
                        submesh.name = submesh.name.lower()

                # lambert material
                lambert = MFnLambertShader()
                lambert.create()
                lambert.setName(submesh.name)
                lambert_name = lambert.name()
                # create renderable, independent shading group
                cmds.sets(
                    renderable=True,
                    noSurfaceShader=True,
                    empty=True,
                    name=f'{lambert_name}_SG'
                )
                # add submesh faces to shading group
                cmds.sets(
                    f'{mesh_name}.f[0:{face_count}]',
                    forceElement=f'{lambert_name}_SG',
                    e=True
                )
                # connect lambert to shading group
                cmds.connectAttr(
                    f'{lambert_name}.outColor',
                    f'{lambert_name}_SG.surfaceShader',
                    force=True
                )

            if skl != None:
                for shader_index in range(shader_count):
                    # get mesh base on shader
                    mesh = shader_meshes[shader_index]
                    mesh_name = mesh.name()
                    influence_count = len(skl.influences)
                    mesh_dagpath = MDagPath()
                    mesh.getPath(mesh_dagpath)

                    # select mesh + joint
                    selections = MSelectionList()
                    selections.add(mesh_dagpath)
                    for influence in skl.influences:
                        selections.add(skl.joints[influence].dagpath)
                    MGlobal.selectCommand(selections)

                    # bind selections
                    cmds.skinCluster(
                        name=f'{mesh_name}_skinCluster',
                        maximumInfluences=4,
                        toSelectedBones=True,
                    )

                    # get skin cluster
                    in_mesh = mesh.findPlug('inMesh')
                    plugs = MPlugArray()
                    in_mesh.connectedTo(plugs, True, False)
                    skin_cluster = MFnSkinCluster(
                        plugs[0].node())
                    skin_cluster_name = skin_cluster.name()

                    # mask influence
                    influences_dagpath = MDagPathArray()
                    skin_cluster.influenceObjects(influences_dagpath)
                    mask_influence = MIntArray(influence_count)
                    for i in range(influence_count):
                        dagpath = skl.joints[skl.influences[i]].dagpath
                        match_j = next(j for j in range(
                            influence_count) if dagpath == influences_dagpath[j])
                        if match_j != None:
                            mask_influence[i] = match_j

                    # weights
                    cmds.setAttr(f'{skin_cluster_name}.normalizeWeights', 0)
                    component = MFnSingleIndexedComponent()
                    vertex_component = component.create(MFn.kMeshVertComponent)
                    vertex_count = len(shader_vertices[shader_index])
                    weights = MDoubleArray(vertex_count * influence_count)
                    for i in range(vertex_count):
                        vertex = shader_vertices[shader_index][i]
                        for j in range(4):
                            weight = vertex.weights[j]
                            influence = vertex.influences[j]
                            if weight > 0:
                                weights[i * influence_count +
                                        influence] = weight
                    skin_cluster.setWeights(
                        mesh_dagpath, vertex_component, mask_influence, weights, False)
                    cmds.skinPercent(
                        skin_cluster_name,
                        mesh_name,
                        normalize=True
                    )
                    cmds.setAttr(f'{skin_cluster_name}.normalizeWeights', 1)

            cmds.select(clear=True)
            # shud be final line
            for mesh in shader_meshes:
                mesh.updateSurface()

        if load_options['separated_mesh']:
            load_separated()
        else:
            load_combined()

    @staticmethod
    def scene_dump(skn, dump_options):
        skl = dump_options['skl']

        def dump_mesh(mesh):
            # get mesh DAG path
            mesh_dagpath = MDagPath()
            mesh.getPath(mesh_dagpath)
            mesh_vertex_count = mesh.numVertices()

            iterator = MItDependencyGraph(
                mesh.object(), MFn.kSkinClusterFilter, MItDependencyGraph.kUpstream)
            if iterator.isDone():
                raise helper.FunnyError(
                    f'SKN Expoter ({mesh.name()}): No skin cluster found, make sure you bound the skin.')
            skin_cluster = MFnSkinCluster(iterator.currentItem())

            # check holes
            hole_info = MIntArray()
            hole_vertices = MIntArray()
            mesh.getHoles(hole_info, hole_vertices)
            if hole_info.length() != 0:
                raise helper.FunnyError(
                    f'SKN Expoter ({mesh.name()}): Mesh contains {hole_info.length()} holes.')

            # get shader/materials
            shaders = MObjectArray()
            face_shader = MIntArray()
            instance = mesh_dagpath.instanceNumber() if mesh_dagpath.isInstanced() else 0
            mesh.getConnectedShaders(instance, shaders, face_shader)
            shader_count = shaders.length()
            # check no material assigned
            if shader_count < 1:
                raise helper.FunnyError(
                    f'SKN Expoter ({mesh.name()}): No material assigned to this mesh, please assign one.')
            # init shaders data to work on multiple shader
            shader_vertices = []
            shader_indices = []
            shader_names = []
            for i in range(shader_count):
                shader_vertices.append([])
                shader_indices.append([])
                # get shader name
                ss = MFnDependencyNode(
                    shaders[i]).findPlug('surfaceShader')
                plugs = MPlugArray()
                ss.connectedTo(plugs, True, False)
                shader_node = MFnDependencyNode(plugs[0].node())
                shader_names.append(shader_node.name())

            # iterator on faces - 1st
            # to get vertex_shader first base on face_shader
            # extra checking stuffs
            bad_faces = MIntArray()  # invalid triangulation polygon
            bad_faces2 = MIntArray()  # no material assigned
            bad_faces3 = MIntArray()  # no uv assigned
            bad_vertices = MIntArray()  # shared vertices
            vertex_shader = MIntArray(mesh_vertex_count, -1)
            iterator = MItMeshPolygon(mesh_dagpath)
            iterator.reset()
            while not iterator.isDone():
                # get shader of this face
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
                if not iterator.hasUVs():
                    if face_index not in bad_faces3:
                        bad_faces3.append(face_index)
                # get face vertices
                vertices = MIntArray()
                iterator.getVertices(vertices)
                face_vertex_count = vertices.length()
                # check if each vertex is shared by mutiple materials
                for i in range(face_vertex_count):
                    vertex = vertices[i]
                    if vertex_shader[vertex] not in (-1, shader_index):
                        if vertex not in bad_vertices:
                            bad_vertices.append(vertex)
                        continue
                    vertex_shader[vertex] = shader_index
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
                    f'SKN Expoter ({mesh.name()}): Mesh contains {bad_faces.length()} invalid triangulation faces, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history and rebind the skin, that might fix the problem.')
            if bad_faces2.length() > 0:
                component = MFnSingleIndexedComponent()
                face_component = component.create(
                    MFn.kMeshPolygonComponent)
                component.addElements(bad_faces2)
                selections = MSelectionList()
                selections.add(mesh_dagpath, face_component)
                MGlobal.selectCommand(selections)
                raise helper.FunnyError(
                    f'SKN Expoter ({mesh.name()}): Mesh contains {bad_faces2.length()} faces have no material assigned, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history and rebind the skin, that might fix the problem.')
            if bad_faces3.length() > 0:
                component = MFnSingleIndexedComponent()
                face_component = component.create(
                    MFn.kMeshPolygonComponent)
                component.addElements(bad_faces3)
                selections = MSelectionList()
                selections.add(mesh_dagpath, face_component)
                MGlobal.selectCommand(selections)
                raise helper.FunnyError(
                    f'SKN Expoter ({mesh.name()}): Mesh contains {bad_faces3.length()} faces have no UVs assigned, or, those faces UVs are not in first UV set (please check all UV set), those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history and rebind the skin, that might fix the problem.')
            if bad_vertices.length() > 0:
                component = MFnSingleIndexedComponent()
                vertex_component = component.create(
                    MFn.kMeshVertComponent)
                component.addElements(bad_vertices)
                selections = MSelectionList()
                selections.add(mesh_dagpath, vertex_component)
                MGlobal.selectCommand(selections)
                raise helper.FunnyError((
                    f'SKN Expoter ({mesh.name()}): Mesh contains {bad_vertices.length()} vertices are shared by mutiple materials, those vertices will be selected in scene.\n'
                    'Save/backup scene first, try one of following methods to fix:\n'
                    '1. Seperate all connected faces that shared those vertices.\n'
                    '2. Check and reassign correct material.\n'
                    '3. [not recommended] Try auto fix shared vertices button on shelf.\n',
                    '4. Combine all UVs into one using martin uv helper buttons in shelf and assign 1 material only to mesh.'
                    '\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history and rebind the skin, that might fix the problem.'
                ))

            # get weights of all vertices
            # empty vertex component = all vertices
            component = MFnSingleIndexedComponent()
            vertex_component = component.create(MFn.kMeshVertComponent)
            weights = MDoubleArray()
            util = MScriptUtil()
            ptr = util.asUintPtr()
            skin_cluster.getWeights(
                mesh_dagpath, vertex_component, weights, ptr)
            weight_influence_count = util.getUint(ptr)
            # map influence indices by skl joints
            influence_dagpaths = MDagPathArray()
            influence_count = skin_cluster.influenceObjects(influence_dagpaths)
            mask_influence = MIntArray(influence_count)
            joint_count = len(skl.joints)
            for i in range(influence_count):
                dagpath = influence_dagpaths[i]
                match_j = next(j for j in range(joint_count)
                               if dagpath == skl.joints[j].dagpath)
                if match_j != None:
                    mask_influence[i] = match_j
            # get all uvs
            u_values = MFloatArray()
            v_values = MFloatArray()
            mesh.getUVs(u_values, v_values)
            # iterator on vertices
            # to dump all new vertices base on unique uv
            iterator = MItMeshVertex(mesh_dagpath)
            iterator.reset()
            while not iterator.isDone():
                # get shader of this vertex
                vertex_index = iterator.index()
                shader_index = vertex_shader[vertex_index]
                if shader_index == -1:
                    # a strange vertex with no shader ?
                    # let say this vertex is alone and not in any face
                    # just ignore it?
                    iterator.next()
                    continue

                # influence and weight
                influences = [0, 0, 0, 0]
                vertex_weights = [0.0, 0.0, 0.0, 0.0]
                vertex_influences_weights = []
                for influence in range(weight_influence_count):
                    weight = weights[vertex_index *
                                     weight_influence_count + influence]
                    if weight > 0.001:
                        vertex_influences_weights.append((mask_influence[influence], weight))
                # prune 4+ influences 
                vertex_influences_weights.sort(key=lambda x: x[1])
                vertex_influences_weights = vertex_influences_weights[:4]
                for i in range(len(vertex_influences_weights)):
                    influences[i], vertex_weights[i] = vertex_influences_weights[i]
                # normalize weight
                weight_sum = sum(vertex_weights)
                if weight_sum > 0:
                    for i in range(4):
                        vertex_weights[i] /= weight_sum
                # position
                position = iterator.position(MSpace.kWorld)
                # average of normals of all faces connect to this vertex
                normals = MVectorArray()
                iterator.getNormals(normals)
                normal_count = normals.length()
                normal = MVector(0.0, 0.0, 0.0)
                for i in range(normal_count):
                    normal += normals[i]
                normal /= normal_count
                # unique uv
                uv_indices = MIntArray()
                iterator.getUVIndices(uv_indices)
                uv_count = uv_indices.length()
                if uv_count > 0:
                    seen = []
                    for i in range(uv_count):
                        uv_index = uv_indices[i]
                        if uv_index == -1:
                            continue
                        if uv_index not in seen:
                            seen.append(uv_index)
                            uv = Vector(
                                u_values[uv_index],
                                1.0 - v_values[uv_index]
                            )
                            # dump vertices
                            vertex = helper.LemonSKNVertex()
                            vertex.position = Vector(
                                position.x, position.y, position.z)
                            vertex.normal = Vector(
                                normal.x, normal.y, normal.z)
                            vertex.influences = bytes(influences)
                            vertex.weights = vertex_weights
                            vertex.uv = uv
                            vertex.uv_index = uv_index
                            vertex.new_index = len(
                                shader_vertices[shader_index])
                            shader_vertices[shader_index].append(vertex)
                else:
                    if vertex_index not in bad_vertices:
                        bad_vertices.append(vertex_index)
                iterator.next()

            # map new vertices base on uv_index
            map_vertices = {}
            for shader_index in range(shader_count):
                map_vertices[shader_index] = {}
                for vertex in shader_vertices[shader_index]:
                    map_vertices[shader_index][vertex.uv_index] = vertex.new_index
            # iterator on faces - 2nd
            # to dump indices:
            # - triangulated indices
            # - new indices base on new unique uv vertices
            iterator = MItMeshPolygon(mesh_dagpath)
            iterator.reset()
            while not iterator.isDone():
                # get shader of this face
                face_index = iterator.index()
                shader_index = face_shader[face_index]

                # get triangulated face indices
                points = MPointArray()
                indices = MIntArray()
                iterator.getTriangles(points, indices)
                face_index_count = indices.length()
                # get face vertices
                map_indices = {}
                vertices = MIntArray()
                iterator.getVertices(vertices)
                face_vertex_count = vertices.length()
                # map face indices by uv_index
                for i in range(face_vertex_count):
                    util = MScriptUtil()
                    ptr = util.asIntPtr()
                    iterator.getUVIndex(i, ptr)
                    uv_index = util.getInt(ptr)
                    map_indices[vertices[i]] = uv_index
                # map new indices by new vertices through uv_index
                # and add new indices
                new_indices = [
                    map_vertices[shader_index][map_indices[indices[i]]]
                    for i in range(face_index_count)
                ]
                shader_indices[shader_index].extend(new_indices)
                iterator.next()

            # return list of submeshes dumped out of this mesh
            submeshes = [helper.LemonSKNSubmesh() for i in range(shader_count)]
            for i in range(shader_count):
                submesh = submeshes[i]
                submesh.name = shader_names[i]
                submesh.indices = shader_indices[i]
                submesh.vertices = shader_vertices[i]
            return submeshes

        
        # dump all mesh of selected group
        submeshes = []
        selected_group = dump_options['selected_group']
        scene_meshes = helper.MIterator.list_all_meshes(selected_group)
        for scene_mesh in scene_meshes:
            submeshes += dump_mesh(MFnMesh(scene_mesh))

        # map submeshes by name
        map_submeshes = {}
        for submesh in submeshes:
            if submesh.name not in map_submeshes:
                map_submeshes[submesh.name] = []
            map_submeshes[submesh.name].append(submesh)
        # combine all submesh that has same name
        # save to SKN submeshes
        for submesh_name in map_submeshes:
            # check submesh name's length
            if len(submesh_name) > 64:
                raise helper.FunnyError(
                    f'SKN Exporter: Material name is too long: {submesh_name} with {len(submesh_name)} chars, max allowed: 64 chars.')
            combined_submesh = helper.LemonSKNSubmesh()
            combined_submesh.name = submesh_name
            previous_max_index = 0
            for submesh in map_submeshes[submesh_name]:
                combined_submesh.vertices += submesh.vertices
                if previous_max_index > 0:
                    previous_max_index += 1
                combined_submesh.indices.extend(
                    index + previous_max_index for index in submesh.indices)
                previous_max_index = max(combined_submesh.indices)
            skn.submeshes.append(combined_submesh)

        # calculate SKN indices, vertices and update SKN submeshes data
        # for first submesh
        skn.submeshes[0].index_start = 0
        skn.submeshes[0].index_count = len(skn.submeshes[0].indices)
        skn.indices += skn.submeshes[0].indices
        skn.submeshes[0].vertex_start = 0
        skn.submeshes[0].vertex_count = len(skn.submeshes[0].vertices)
        skn.vertices += skn.submeshes[0].vertices
        # for the rest if more than 1 submeshes
        submesh_count = len(skn.submeshes)
        if submesh_count > 1:
            index_start = skn.submeshes[0].index_count
            vertex_start = skn.submeshes[0].vertex_count
            for i in range(1, submesh_count):
                skn.submeshes[i].index_start = index_start
                skn.submeshes[i].index_count = len(skn.submeshes[i].indices)
                max_index = max(skn.submeshes[i-1].indices)
                skn.submeshes[i].indices = [
                    index + max_index+1 for index in skn.submeshes[i].indices]
                skn.indices.extend(skn.submeshes[i].indices)

                skn.submeshes[i].vertex_start = vertex_start
                skn.submeshes[i].vertex_count = len(
                    skn.submeshes[i].vertices)
                skn.vertices.extend(skn.submeshes[i].vertices)

                index_start += skn.submeshes[i].index_count
                vertex_start += skn.submeshes[i].vertex_count

        # sort submesh to match riot.skn submeshes order
        riot_skn = dump_options['riot_skn']
        if riot_skn != None:
            LOG(
                'SKN Exporter: Found riot.skn, sorting materials...')

            new_submeshes = []
            submesh_count = len(skn.submeshes)
            # for adding extra material at the end of list
            flags = [True] * submesh_count

            # find riot submesh in scene
            for riot_submesh in riot_skn.submeshes:
                riot_submesh_name = riot_submesh.name.lower()
                found = False
                for i in range(submesh_count):
                    if flags[i] and skn.submeshes[i].name.lower() == riot_submesh_name:
                        new_submeshes.append(skn.submeshes[i])
                        LOG(
                            f'SKN Exporter: Found material: {skn.submeshes[i].name}')
                        flags[i] = False
                        found = True
                        break

                # submesh that not found
                if not found:
                    LOG(
                        f'SKN Exporter: Missing riot material: {riot_submesh.name}')

            # add extra/addtional materials to the end of list
            for i in range(submesh_count):
                if flags[i]:
                    new_submeshes.append(skn.submeshes[i])
                    flags[i] = False
                    LOG(
                        f'SKN Exporter: New material: {skn.submeshes[i].name}')

            # assign new list
            skn.submeshes = new_submeshes

        # check limit vertices
        vertices_count = len(skn.vertices)
        if vertices_count > 65535:
            raise helper.FunnyError(
                f'SKN Exporter: Too many vertices found: {vertices_count}, max allowed: 65535 vertices. (base on UVs)')

        # check limit submeshes
        submesh_count = len(skn.submeshes)
        if submesh_count > 32:
            raise helper.FunnyError(
                f'SKN Exporter: Too many materials assigned: {submesh_count}, max allowed: 32 materials.')

class SKL:
    @staticmethod
    def scene_load(skl, load_options):
        # group of meshes
        skl_name = load_options['skl_name']
        group_transform = MFnTransform()
        group_transform.create()
        group_transform.setName(f'group_{skl_name}')

        # find joint existed in scene
        iterator = MItDag(MItDag.kDepthFirst, MFn.kJoint)
        while not iterator.isDone():
            dagpath = MDagPath()
            iterator.getPath(dagpath)
            ik_joint = MFnIkJoint(dagpath)
            joint_name = ik_joint.name()
            match_joint = next(
                (joint for joint in skl.joints if joint.name == joint_name), None)
            if match_joint != None:
                match_joint.dagpath = dagpath
            iterator.next()

        # create joint if not existed
        # set transform
        for joint_id, joint in enumerate(skl.joints):
            if joint.dagpath == None:
                # create if not existed
                ik_joint = MFnIkJoint()
                ik_joint.create()
                ik_joint.setName(joint.name)
                joint.dagpath = MDagPath()
                ik_joint.getPath(joint.dagpath)
            else:
                # get the existed joint
                ik_joint = MFnIkJoint(joint.dagpath)
            # add custom attribute: Riot ID
            if not cmds.attributeQuery(
                'riotid',
                exists=True,
                node=joint.name
            ):
                cmds.addAttr(
                    joint.name,
                    longName='riotid',
                    niceName='Riot ID',
                    attributeType='byte',
                    minValue=0, 
                    maxValue=255, 
                    defaultValue=joint_id
                )
            cmds.setAttr(f'{joint.name}.riotid', joint_id)
            # set transform
            ik_joint.set(helper.MayaTransformMatrix.compose(
                joint.local_translate, joint.local_rotate, joint.local_scale, MSpace.kWorld
            ))
            # add to group
            group_transform.addChild(ik_joint.object())

        # link parent
        for joint in skl.joints:
            if joint.parent > -1:
                parent_node = MFnIkJoint(skl.joints[joint.parent].dagpath)
                child_node = MFnIkJoint(joint.dagpath)
                if not parent_node.isParentOf(child_node.object()):
                    parent_node.addChild(child_node.object())
        
        return group_transform
    
    @staticmethod
    def scene_dump(skl, dump_options):
        selected_group = dump_options['selected_group']
        scene_joints = helper.MIterator.list_all_joints(selected_group)
        for scene_joint in scene_joints:
            joint = helper.LemonSKLJoint()
            ik_joint = MFnIkJoint(scene_joint)
            # dagpath, name, transform
            joint.dagpath = MDagPath()
            ik_joint.getPath(joint.dagpath)
            joint.name = ik_joint.name()
            joint.hash = Elf(joint.name)
            joint.radius = 2.1
            joint.local_translate, joint.local_rotate, joint.local_scale = helper.MayaTransformMatrix.decompose(
                MTransformationMatrix(ik_joint.transformationMatrix()),
                MSpace.kTransform
            )
            joint.ibind_translate, joint.ibind_rotate, joint.ibind_scale = helper.MayaTransformMatrix.decompose(
                MTransformationMatrix(joint.dagpath.inclusiveMatrixInverse()),
                MSpace.kWorld
            )
            skl.joints.append(joint)

        # riot skl
        riot_skl = dump_options['riot_skl']
        if riot_skl != None:
            # sort joints with riot skl
            LOG('SKL Expoter: Found riot.skl, sorting joints...')

            new_joints = []
            joint_count = len(skl.joints)
            riot_joint_count = len(riot_skl.joints)
            # for adding extra joint at the end of list
            flags = [True] * joint_count

            # find riot joint in scene
            for riot_joint in riot_skl.joints:
                riot_joint_name = riot_joint.name.lower()
                found = False
                for i in range(joint_count):
                    if flags[i] and skl.joints[i].name.lower() == riot_joint_name:
                        new_joints.append(skl.joints[i])
                        flags[i] = False
                        found = True
                        break
                # if not found riot join in current scene -> not enough joints to match riot joints -> bad
                # fill empty joint
                if not found:
                    LOG(
                        f'SKL Exporter: Missing riot joint: {riot_joint.name}')
                    joint = helper.LemonSKLJoint()
                    joint.dagpath = None
                    joint.name = riot_joint.name
                    joint.hash = Elf(joint.name)
                    joint.parent = -1
                    joint.radius = 2.1
                    joint.local_translation = Vector(0.0, 0.0, 0.0)
                    joint.local_rotation = Quaternion(0.0, 0.0, 0.0, 1.0)
                    joint.local_scale = Vector(0.0, 0.0, 0.0)
                    joint.iglobal_translation = Vector(0.0, 0.0, 0.0)
                    joint.iglobal_rotation = Quaternion(0.0, 0.0, 0.0, 1.0)
                    joint.iglobal_scale = Vector(0.0, 0.0, 0.0)
                    new_joints.append(joint)

            # joint in scene = riot joint: good
            # joint in scene < riot joint: bad, might not work
            new_joint_count = len(new_joints)
            if new_joint_count < riot_joint_count:
                LOG(
                    f'SKL Exporter: Missing {riot_joint_count - new_joint_count} joints compared to riot.skl, joints order might be wrong.')
            else:
                LOG(
                    f'SKL Exporter: Successfully matched {new_joint_count} joints with riot.skl.')

            # add extra/addtional joints to the end of list
            # animation layer weight value for those joint will auto be 1.0
            for i in range(joint_count):
                if flags[i]:
                    new_joints.append(skl.joints[i])
                    flags[i] = False
                    LOG(
                        f'SKL Exporter: New joints: {skl.joints[i].name}')

            # assign new list
            skl.joints = new_joints
        else:
            # sort joint with riot ID attribute
            new_joints = []
            joint_count = len(skl.joints)
            riot_joints = [None]*joint_count
            other_joints = []
            flags = [True] * joint_count

            # get riot joints through ID attribute
            for joint in skl.joints:
                try:
                    attribute_exists = cmds.attributeQuery(
                        'riotid',
                        exists=True,
                        node=joint.name
                    )
                except:
                    # there are case that we fail to check extra attribute
                    # ex: 2 same name joints have different parent (or this is rito fault?)
                    # just count as new joint and move on
                    other_joints.append(joint)
                    continue

                # if joint doesnt have attribute -> new joint
                if not attribute_exists:
                    other_joints.append(joint)
                    continue
                id = cmds.getAttr(f'{joint.name}.riotid')
                # if id out of range -> bad joint
                if id < 0 or id >= joint_count:
                    other_joints.append(joint)
                    continue
                # if duplicated ID -> bad joint
                if riot_joints[id] != None:
                    other_joints.append(joint)
                    continue
                riot_joints[id] = joint

            # add good joints first
            new_joints = [joint for joint in riot_joints if joint != None]
            # add new/bad joints at the end
            new_joints.extend(joint for joint in other_joints)
            skl.joints = new_joints

        # link parent
        joint_count = len(skl.joints)
        for joint in skl.joints:
            if joint.dagpath == None:
                continue
            ik_joint = MFnIkJoint(joint.dagpath)
            if ik_joint.parentCount() == 1 and ik_joint.parent(0).apiType() == MFn.kJoint:
                # get parent dagpath of this joint node
                parent_dagpath = MDagPath()
                MFnIkJoint(ik_joint.parent(0)).getPath(parent_dagpath)
                # find parent id by parent dagpath
                match_id = next((id for id in range(
                    joint_count) if skl.joints[id].dagpath == parent_dagpath), None)
                if match_id != None:
                    joint.parent = match_id
            else:
                # must be batman
                joint.parent = -1

        # check limit joint
        joint_count = len(skl.joints)
        if joint_count > 256:
            raise helper.FunnyError(
                f'SKL Exporter: Too many joints found: {joint_count}, max allowed: 256 joints.')