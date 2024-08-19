from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

from . import helper
from ..... import pyRitoFile

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
        # read skn
        skn_path = helper.ensure_path_extension(file.expandedFullName(), 'skn')
        import_options = SKN.create_ui_skn_import_options(skn_path)
        skn = pyRitoFile.read_skn(skn_path)
        # fix skn name if need
        skn_name = skn_path.split('/')[-1].split('.')[0]
        if skn_name in '0123456789':
            skn_name = 'nf_'+self.name
        # load skeleton first if need
        group_transform = None
        skl = None
        joint_dagpaths = None
        if import_options['import_skeleton']:
            skl_path = skn_path.replace('.skn', '.skl')
            skl = pyRitoFile.read_skl(skl_path)
            helper.mirrorX(skl=skl)
            group_transform, joint_dagpaths = SKL.scene_load(skl, { 'skl_name': skn_name })
        # load skn
        helper.mirrorX(skn=skn)
        load_options = {
            'skn_name': skn_name,
            'group_transform': group_transform,
            'separated_mesh': import_options['import_separated_mesh'],
            'skl': skl,
            'joint_dagpaths': joint_dagpaths
        }
        SKN.scene_load(skn, load_options)
        return True


class SKN:
    @staticmethod
    def create_ui_skn_import_options(skn_path):
        skn_import_options = {
            'import_skeleton': True,
            'import_separated_mesh': True
        }
        def ui_cmd():
            cmds.columnLayout()

            cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
            cmds.text(label='SKN Path:')
            cmds.text(label=skn_path, width=600)
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
            cmds.text(label='SKL Path:')
            skl_path = skn_path.replace('.skn', '.skl')
            skl_text = cmds.text(label=skl_path, width=600)
            def sklbrowse_cmd(text):
                skl_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='SKL(*.skl)',
                    caption='Select SKL file',
                    okCaption='Select'
                )
                if skl_path:
                    cmds.text(text, edit=True, label=skl_path[0])
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
            cmds.button(label='OK', width=100, command=lambda e: cmds.layoutDialog(dismiss='OK'))

        cmds.layoutDialog(title='SKN Import Options', ui=ui_cmd)
        return skn_import_options

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
            skl, joint_dagpaths = load_options['skl'], load_options['joint_dagpaths']
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
                    selections.add(joint_dagpaths[influence])
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
                    dagpath = joint_dagpaths[skl.influences[i]]
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

            skl, joint_dagpaths = load_options['skl'], load_options['joint_dagpaths']
            
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
                        selections.add(joint_dagpaths[influence])
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
                        dagpath = joint_dagpaths[skl.influences[i]]
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


class SKLTranslator(MPxFileTranslator):
    name = 'League of Legends: SKL'
    extension = 'skl'

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
        skl_path = helper.ensure_path_extension(file.expandedFullName(), 'skl')
        skl = pyRitoFile.read_skl(skl_path)
        # fix skn name if need
        skl_name = skl_path.split('/')[-1].split('.')[0]
        if skl_name in '0123456789':
            skl_name = 'nf_'+self.name
        helper.mirrorX(skl=skl)
        load_options = {
            'skl_name': skl_name,
        }
        SKL.scene_load(skl, load_options)
        return True
    
    def writer(self, file, option, access):
        return True


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
        joint_dagpaths = [None] * len(skl.joints)
        for joint_id, joint in enumerate(skl.joints):
            if joint_dagpaths[joint_id] == None:
                # create if not existed
                ik_joint = MFnIkJoint()
                ik_joint.create()
                ik_joint.setName(joint.name)
                joint_dagpaths[joint_id] = MDagPath()
                ik_joint.getPath(joint_dagpaths[joint_id])
            else:
                # get the existed joint
                ik_joint = MFnIkJoint(joint_dagpaths[joint_id])
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
            ik_joint.set(helper.MayaTransform.compose(
                joint.local_translate, joint.local_rotate, joint.local_scale, MSpace.kWorld
            ))
            # add to group
            group_transform.addChild(ik_joint.object())

        # link parent
        for joint_id, joint in enumerate(skl.joints):
            if joint.parent > -1:
                parent_node = MFnIkJoint(joint_dagpaths[joint.parent])
                child_node = MFnIkJoint(joint_dagpaths[joint_id])
                if not parent_node.isParentOf(child_node.object()):
                    parent_node.addChild(child_node.object())
        
        return group_transform, joint_dagpaths