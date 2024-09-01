from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

import os.path
from . import helper
from ..... import pyRitoFile
from .....pyRitoFile.structs import Vector
LOG = print

class SCOTranslator(MPxFileTranslator):
    name = 'League of Legends: SCO'
    extension = 'sco'

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
        sco_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
        # read sco
        so = pyRitoFile.read_sco(sco_path)
        so.name = helper.get_name_from_path(sco_path)
        # load so
        helper.mirrorX(so=so)
        SO.scene_load(so, {})
        return True

    def writer(self, file, option, access):
        # check selected
        selections = MSelectionList()
        MGlobal.getActiveSelectionList(selections)
        iterator = MItSelectionList(selections, MFn.kMesh)
        if iterator.isDone():
            raise helper.FunnyError(
                f'SO Exporter: Please select a mesh to export.')
        mesh_dagpath = MDagPath()
        iterator.getDagPath(mesh_dagpath)
        iterator.next()
        if not iterator.isDone():
            raise helper.FunnyError(
                f'SO Exporter: Please select only one mesh to export.')
        selected_mesh = MFnMesh(mesh_dagpath)
        # export options
        sco_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
        dismiss, sco_export_options = SO.create_ui_sco_export_options(sco_path)
        if dismiss != 'Export':
            return False
        so = pyRitoFile.SO()
        riot_so = None
        riot_sco_path = sco_export_options['riot_sco_path']
        if riot_sco_path != '':
            riot_so = pyRitoFile.read_sco(riot_sco_path)
        dump_options = {
            'selected_mesh': selected_mesh,
            'riot_so': riot_so
        }
        SO.scene_dump(so, dump_options)
        helper.mirrorX(so=so)
        pyRitoFile.write_sco(sco_path, so)
        return True
    

class SCBTranslator(MPxFileTranslator):
    name = 'League of Legends: SCB'
    extension = 'scb'

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
        scb_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
        # read scb
        so = pyRitoFile.read_scb(scb_path)
        so.name = helper.get_name_from_path(scb_path)
        # load so
        helper.mirrorX(so=so)
        SO.scene_load(so, {})
        return True

    def writer(self, file, option, access):
        # check selected
        selections = MSelectionList()
        MGlobal.getActiveSelectionList(selections)
        iterator = MItSelectionList(selections, MFn.kMesh)
        if iterator.isDone():
            raise helper.FunnyError(
                f'SO Exporter: Please select a mesh to export.')
        mesh_dagpath = MDagPath()
        iterator.getDagPath(mesh_dagpath)
        iterator.next()
        if not iterator.isDone():
            raise helper.FunnyError(
                f'SO Exporter: Please select only one mesh to export.')
        selected_mesh = MFnMesh(mesh_dagpath)
        # export options
        scb_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
        dismiss, scb_export_options = SO.create_ui_scb_export_options(scb_path)
        if dismiss != 'Export':
            return False
        so = pyRitoFile.SO()
        riot_so = None
        riot_scb_path = scb_export_options['riot_scb_path']
        if riot_scb_path != '':
            riot_so = pyRitoFile.read_scb(riot_scb_path)
        dump_options = {
            'selected_mesh': selected_mesh,
            'riot_so': riot_so
        }
        SO.scene_dump(so, dump_options)
        helper.mirrorX(so=so)
        pyRitoFile.write_scb(scb_path, so)
        return True


class SO:
    @staticmethod
    def create_ui_sco_export_options(sco_path):
        # check riot sco path
        riot_sco_path = os.path.join(
            os.path.dirname(sco_path), 
            f'riot_{os.path.basename(sco_path)}'
        ).replace('\\', '/')
        if not os.path.exists(riot_sco_path):
            riot_sco_path = os.path.join(
                os.path.dirname(sco_path),
                'riot.sco'
            ).replace('\\', '/')
        if not os.path.exists(riot_sco_path):
            riot_sco_path = ''
        sco_export_options = {
            'riot_sco_path': riot_sco_path
        }

        def ui_cmd():
            cmds.columnLayout()

            cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
            cmds.text(label='SCO Path:')
            cmds.text(label=sco_path, align='left', width=600)
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
            cmds.text(label='Riot SCO Path:')
            sco_text = cmds.text(label=riot_sco_path, align='left', width=600)
            def scobrowse_cmd(text):
                sco_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='SCO(*.sco)',
                    caption='Select Riot SCO file',
                    okCaption='Select'
                )
                if sco_path:
                    sco_path = sco_path[0].replace('\\', '/')
                    cmds.text(text, edit=True, label=sco_path)
                    sco_export_options['riot_sco_path'] = sco_path
            cmds.button(label='Browse Riot SCO', command=lambda e: scobrowse_cmd(sco_text))
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=2)
            cmds.text(label='', w=700)
            def dismiss(result):
                cmds.layoutDialog(dismiss=result)
            cmds.button(label='Export', width=100, command=lambda e: dismiss('Export'))
        
        return cmds.layoutDialog(title='SCO Export Options', ui=ui_cmd), sco_export_options

    @staticmethod
    def create_ui_scb_export_options(scb_path):
        # check riot scb path
        riot_scb_path = os.path.join(
            os.path.dirname(scb_path), 
            f'riot_{os.path.basename(scb_path)}'
        ).replace('\\', '/')
        if not os.path.exists(riot_scb_path):
            riot_scb_path = os.path.join(
                os.path.dirname(scb_path),
                'riot.scb'
            ).replace('\\', '/')
        if not os.path.exists(riot_scb_path):
            riot_scb_path = ''
        scb_export_options = {
            'riot_scb_path': riot_scb_path
        }

        def ui_cmd():
            cmds.columnLayout()

            cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
            cmds.text(label='SCB Path:')
            cmds.text(label=scb_path, align='left', width=600)
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
            cmds.text(label='Riot SCB Path:')
            scb_text = cmds.text(label=riot_scb_path, align='left', width=600)
            def scbbrowse_cmd(text):
                scb_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='SCB(*.scb)',
                    caption='Select Riot SCB file',
                    okCaption='Select'
                )
                if scb_path:
                    scb_path = scb_path[0].replace('\\', '/')
                    cmds.text(text, edit=True, label=scb_path)
                    scb_export_options['riot_scb_path'] = scb_path
            cmds.button(label='Browse Riot SCB', command=lambda e: scbbrowse_cmd(scb_text))
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=2)
            cmds.text(label='', w=700)
            def dismiss(result):
                cmds.layoutDialog(dismiss=result)
            cmds.button(label='Export', width=100, command=lambda e: dismiss('Export'))
        
        return cmds.layoutDialog(title='SCB Export Options', ui=ui_cmd), scb_export_options

    @staticmethod
    def scene_load(so, load_options):
        vertex_count = len(so.positions)
        index_count = len(so.indices)
        face_count = index_count // 3

        # create mesh
        vertices = MFloatPointArray(vertex_count)
        u_values = MFloatArray(index_count)
        v_values = MFloatArray(index_count)
        poly_count = MIntArray(face_count, 3)
        poly_indices = MIntArray(index_count)
        uv_indices = MIntArray(index_count)
        for i in range(vertex_count):
            vertex = so.positions[i]
            vertices[i].x = vertex.x-so.central.x
            vertices[i].y = vertex.y-so.central.y
            vertices[i].z = vertex.z-so.central.z
        for i in range(index_count):
            u_values[i] = so.uvs[i].x
            v_values[i] = 1.0 - so.uvs[i].y
            poly_indices[i] = so.indices[i]
            uv_indices[i] = i

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
            poly_count, uv_indices
        )

        # name + central
        mesh.setName(so.name)
        mesh_name = mesh.name()
        transform = MFnTransform(mesh.parent(0))
        transform.setName(f'mesh_{so.name}')
        transform.setTranslation(
            MVector(so.central.x, so.central.y, so.central.z),
            MSpace.kTransform
        )

        # material
        # lambert material
        lambert = MFnLambertShader()
        lambert.create()
        lambert.setName(so.material)
        lambert_name = lambert.name()
        # shading group
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

        # use a joint for pivot
        if so.pivot != None:
            ik_joint = MFnIkJoint()
            ik_joint.create()
            ik_joint.setName(f'pivot_{so.name}')
            ik_joint.setTranslation(
                MVector(
                    so.central.x - so.pivot.x,
                    so.central.y - so.pivot.y,
                    so.central.z - so.pivot.z
                ),
                MSpace.kTransform
            )

            # bind pivot with mesh
            pivot_dagpath = MDagPath()
            ik_joint.getPath(pivot_dagpath)
            mesh_dagpath = MDagPath()
            mesh.getPath(mesh_dagpath)
            selections = MSelectionList()
            selections.add(mesh_dagpath)
            selections.add(pivot_dagpath)
            MGlobal.selectCommand(selections)
            # bind selections
            cmds.skinCluster(
                name=f'{so.name}_skinCluster',
                maximumInfluences=1,
                toSelectedBones=True,
            )

        cmds.select(clear=True)
        mesh.updateSurface()

    @staticmethod
    def scene_dump(so, dump_options):
        mesh = dump_options['selected_mesh']
        mesh_dagpath = MDagPath()
        mesh.getPath(mesh_dagpath)

        # get name
        so.name = mesh.name()

        # central point: translation of mesh
        transform = MFnTransform(mesh.parent(0))
        central_translation = transform.getTranslation(MSpace.kTransform)
        so.central = Vector(
            central_translation.x, central_translation.y, central_translation.z)

        # check hole
        hole_info = MIntArray()
        hole_vertex = MIntArray()
        mesh.getHoles(hole_info, hole_vertex)
        if hole_info.length() > 0:
            raise helper.FunnyError(f'SO Expoter ({mesh.name()}): Mesh contains holes.')

        # SCO only: find pivot joint through skin cluster
        iterator = MItDependencyGraph(
            mesh.object(), MFn.kSkinClusterFilter, MItDependencyGraph.kUpstream)
        if not iterator.isDone():
            skin_cluster = MFnSkinCluster(iterator.currentItem())
            influences_dagpath = MDagPathArray()
            influence_count = skin_cluster.influenceObjects(
                influences_dagpath)
            if influence_count > 1:
                raise helper.FunnyError(
                    f'SO Expoter ({mesh.name()}): More than 1 joint bound with this mesh, can not determine which one is pivot joint.')
            ik_joint = MFnTransform(influences_dagpath[0])
            joint_translation = ik_joint.getTranslation(MSpace.kTransform)
            so.pivot = Vector(
                so.central.x - joint_translation.x,
                so.central.y - joint_translation.y,
                so.central.z - joint_translation.z
            )

        # dumb vertices
        vertex_count = mesh.numVertices()
        points = MFloatPointArray()
        mesh.getPoints(points, MSpace.kWorld)
        so.positions = [Vector(points[i].x, points[i].y, points[i].z)
                         for i in range(vertex_count)]
        so.indices = []
        so.uvs = []
        # dump uvs outside loop
        u_values = MFloatArray()
        v_values = MFloatArray()
        mesh.getUVs(u_values, v_values)
        # iterator on faces
        # to dump face indices and UVs
        # extra checking
        bad_faces = MIntArray()  # invalid triangulation face
        bad_faces2 = MIntArray()  # no UV face
        iterator = MItMeshPolygon(mesh_dagpath)
        iterator.reset()
        while not iterator.isDone():
            face_index = iterator.index()

            # check valid triangulation
            if not iterator.hasValidTriangulation():
                if face_index not in bad_faces:
                    bad_faces.append(face_index)
            # check if face has no UVs
            if not iterator.hasUVs():
                if face_index not in bad_faces2:
                    bad_faces2.append(face_index)

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
            # dump indices and uvs
            for i in range(face_index_count):
                index = indices[i]
                so.indices.append(index)
                uv_index = map_indices[index]
                so.uvs.append(Vector(
                    u_values[uv_index],
                    1.0 - v_values[uv_index]
                ))
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
                f'SO Expoter ({mesh.name()}): Mesh contains {bad_faces.length()} invalid triangulation faces, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history, that might fix the problem.')
        if bad_faces2.length() > 0:
            component = MFnSingleIndexedComponent()
            face_component = component.create(
                MFn.kMeshPolygonComponent)
            component.addElements(bad_faces2)
            selections = MSelectionList()
            selections.add(mesh_dagpath, face_component)
            MGlobal.selectCommand(selections)
            raise helper.FunnyError(
                f'SO Expoter ({mesh.name()}): Mesh contains {bad_faces2.length()} faces have no UVs assigned, or, those faces UVs are not in current UV set, those faces will be selected in scene.\nBonus: If there is nothing selected (or they are invisible) after this error message, consider to delete history, that might fix the problem.')

        # get shader
        instance = mesh_dagpath.instanceNumber() if mesh_dagpath.isInstanced() else 0
        shaders = MObjectArray()
        face_shader = MIntArray()
        mesh.getConnectedShaders(instance, shaders, face_shader)
        if shaders.length() > 1:
            raise helper.FunnyError(
                f'SO Expoter ({mesh.name()}): More than 1 material assigned to this mesh.')
        # material name
        if shaders.length() > 0:
            ss = MFnDependencyNode(
                shaders[0]).findPlug('surfaceShader')
            plugs = MPlugArray()
            ss.connectedTo(plugs, True, False)
            material = MFnDependencyNode(plugs[0].node())
            so.material = material.name()
            if len(so.material) > 64:
                raise helper.FunnyError(
                    f'SO Expoter ({mesh.name()}): Material name is too long: {so.material} with {len(so.material)} chars, max allowed: 64 chars.')
        else:
            # its only allow 1 material anyway
            so.material = 'lambert69'
        
        # set flags
        so.flags = pyRitoFile.SOFlag.HasLocalOriginLocatorAndPivot
        # export base on riot file
        riot_so = dump_options['riot_so']
        if riot_so != None:
            so.central = riot_so.central
            so.pivot = riot_so.pivot
            so.flags = riot_so.flags
            LOG('SO Expoter: Found riot.so (scb/sco), updated central, pivot, flags.')