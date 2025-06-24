from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

from . import helper
from ..... import pyRitoFile

class SCOImporter(MPxFileTranslator):
    name = 'League of Legends: SCO'
    extension = 'sco'

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
            sco_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
            # read sco
            so = pyRitoFile.so.SO().read_sco(sco_path)
            so.name = helper.get_name_from_path(sco_path)
            # load so
            helper.mirrorX(so=so)
            SO.scene_load(so, {})
            return True
    
        return helper.try_cmd(lambda: read_cmd(file, options, access))

class SCOExporter(MPxFileTranslator):
    name = 'League of Legends: SCO Export'
    extension = 'sco'

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
            so = pyRitoFile.so.SO()
            dump_options = {
                'selected_mesh': selected_mesh,
            }
            SO.scene_dump(so, dump_options)
            helper.mirrorX(so=so)
            so.write_sco(sco_path)
            return True

        return helper.try_cmd(lambda: write_cmd(file, options, access))
    
class SCBImporter(MPxFileTranslator):
    name = 'League of Legends: SCB'
    extension = 'scb'

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
            scb_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
            # read scb
            so = pyRitoFile.so.SO().read_scb(scb_path)
            so.name = helper.get_name_from_path(scb_path)
            # load so
            helper.mirrorX(so=so)
            SO.scene_load(so, {})
            return True
        
        return helper.try_cmd(lambda: read_cmd(file, options, access))

class SCBExporter(MPxFileTranslator):
    name = 'League of Legends: SCB Export'
    extension = 'scb'

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
            so = pyRitoFile.so.SO()
            dump_options = {
                'selected_mesh': selected_mesh,
                'scb_flags': pyRitoFile.so.SOFlag.HasVcp if 'HasVcp' in options else pyRitoFile.so.SOFlag.HasLocalOriginLocatorAndPivot
            }
            SO.scene_dump(so, dump_options)
            helper.mirrorX(so=so)
            so.write_scb(scb_path)
            return True

        return helper.try_cmd(lambda: write_cmd(file, options, access))
    
class SO:
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
        material = MFnStandardSurfaceShader()
        material.create()
        material.setName(so.material)
        material.setSpecular(0.0)
        material_name = material.name()
        # shading group
        # create renderable, independent shading group
        cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f'{material_name}_SG'
        )
        # add submesh faces to shading group
        cmds.sets(
            f'{mesh_name}.f[0:{face_count}]',
            forceElement=f'{material_name}_SG',
            e=True
        )
        # connect material to shading group
        cmds.connectAttr(
            f'{material_name}.outColor',
            f'{material_name}_SG.surfaceShader',
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
        so.central = pyRitoFile.structs.Vector(
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
            so.pivot = pyRitoFile.structs.Vector(
                so.central.x - joint_translation.x,
                so.central.y - joint_translation.y,
                so.central.z - joint_translation.z
            )

        # dumb vertices
        vertex_count = mesh.numVertices()
        points = MFloatPointArray()
        mesh.getPoints(points, MSpace.kWorld)
        so.positions = [pyRitoFile.structs.Vector(points[i].x, points[i].y, points[i].z)
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
                so.uvs.append(pyRitoFile.structs.Vector(
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
            so.material = 'standardSurface69'
        
        # set flags
        so.flags = pyRitoFile.so.SOFlag.HasLocalOriginLocatorAndPivot
        if 'scb_flags' in dump_options:
            so.flags = dump_options['scb_flags']