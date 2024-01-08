from fbx import *
from .pyRitoFile import SKL, SKLJoint, SKN, SKNVertex, SKNSubmesh, read_skl, read_skn, write_skl, write_skn
from .pyRitoFile.hash import Elf
from .pyRitoFile.structs import Vector, Quaternion
import string

ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
LOG = print


def GetName(node):
    return ''.join(c if c in ALPHANUMERIC else f'FBXASC{ord(c):03}' for c in node.GetNameOnly().Buffer())


def mirrorX(skl = None, skn = None):
    if skl != None:
        for joint in skl.joints:
            joint.local_translate.x = -joint.local_translate.x
            joint.local_rotate.y = -joint.local_rotate.y
            joint.local_rotate.z = -joint.local_rotate.z
            joint.ibind_translate.x = -joint.ibind_translate.x
            joint.ibind_rotate.y = -joint.ibind_rotate.y
            joint.ibind_rotate.z = -joint.ibind_rotate.z
    if skn != None:
        for vertex in skn.vertices:
            vertex.position.x = -vertex.position.x
            if vertex.normal != None:
                vertex.normal.y = -vertex.normal.y
                vertex.normal.z = -vertex.normal.z
    

def dump_skl(fbx_joints):
    # prepare
    joint_count = len(fbx_joints)
    if joint_count > 256:
        raise Exception(f'lol2fbx: Faield: Too many joints found: {joint_count}, max: 256')
    skl = SKL()
    skl.joints = [SKLJoint() for i in range(joint_count)]
    # dump joint infos
    for joint_id, (joint_name, fbx_joint) in enumerate(fbx_joints.items()):
        # name and stuffs
        joint = skl.joints[joint_id]
        joint.id = joint_id
        joint.name = joint_name
        joint.parent = -1
        joint.hash = Elf(joint_name)
        joint.radius = 2.1
        # local transform
        fbx_local_matrix = fbx_joint.EvaluateLocalTransform()
        translate, rotate, scale = fbx_local_matrix.GetT(), fbx_local_matrix.GetQ(), fbx_local_matrix.GetS()
        joint.local_translate = Vector(translate[0], translate[1], translate[2])
        joint.local_rotate = Quaternion(rotate[0], rotate[1], rotate[2], rotate[3])
        joint.local_scale = Vector(scale[0], scale[1], scale[2])
        # inverse bind transform
        fbx_ibind_matrix = fbx_joint.EvaluateGlobalTransform().Inverse()
        translate, rotate, scale = fbx_ibind_matrix.GetT(), fbx_ibind_matrix.GetQ(), fbx_ibind_matrix.GetS()
        joint.ibind_translate = Vector(translate[0], translate[1], translate[2])
        joint.ibind_rotate = Quaternion(rotate[0], rotate[1], rotate[2], rotate[3])
        joint.ibind_scale = Vector(scale[0], scale[1], scale[2])
    LOG(f'lol2fbx: Done: Read {joint_count} joints.')
    # link parent
    blender_armature_node_name = None
    blender_armature_node_local_matrix = None
    for joint_id, (joint_name, fbx_joint) in enumerate(fbx_joints.items()):
        parent_node = fbx_joint.GetParent()
        parent_node_name = GetName(parent_node)
        if parent_node != None:
            # normal parent
            if type(parent_node.GetNodeAttribute()) == FbxSkeleton:
                for i in range(joint_count):
                    if skl.joints[i].name == parent_node_name:
                        skl.joints[joint_id].parent = i
                        break
            # blender fbx always export a locator/armature/fbxnull node at top skeleton
            # -> ungroup that node
            # -> by get the nodes transform, multiply to all the childs
            elif type(parent_node.GetNodeAttribute()) == FbxNull:
                if blender_armature_node_name == None:
                    blender_armature_node_name = parent_node_name
                    blender_armature_node_local_matrix = parent_node.EvaluateLocalTransform()
                    LOG(f'lol2fbx: Found blender armature/locator node: {blender_armature_node_name}')
                else:
                    if blender_armature_node_name != parent_node_name:
                        raise Exception('lol2fbx: Failed: Skeleton is grouped by multiple locator/blender armature node????')
                joint = skl.joints[joint_id]
                new_local_matrix = fbx_joint.EvaluateLocalTransform() * blender_armature_node_local_matrix
                translate, rotate, scale = new_local_matrix.GetT(), new_local_matrix.GetQ(), new_local_matrix.GetS()
                joint.local_translate = Vector(translate[0], translate[1], translate[2])
                joint.local_rotate = Quaternion(rotate[0], rotate[1], rotate[2], rotate[3])
                joint.local_scale = Vector(scale[0], scale[1], scale[2])
        else:
            skl.joints[joint_id].parent = -1      
    LOG(f'lol2fbx: Done: Dump SKL.')
    return skl, blender_armature_node_name, blender_armature_node_local_matrix


def dump_skn(fbx_meshes, materials, skl, blender_armature_node_name, blender_armature_node_local_matrix):
    def dump_mesh(mesh_name, fbx_mesh):
        LOG(f'lol2fbx: Running: Read {mesh_name}')

        # check triangle
        is_triangle = fbx_mesh.IsTriangleMesh()
        LOG(f'lol2fbx: Triangle mesh: {is_triangle}')
        if not is_triangle:
            raise Exception(f'lol2fbx: Failed: {mesh_name} is not a triangle mesh.')
        
        # get info
        indices = fbx_mesh.GetPolygonVertices()
        vertex_count = fbx_mesh.GetControlPointsCount()
        index_count = len(indices)
        face_count = index_count // 3
        LOG(f'lol2fbx: Faces: {face_count}, Vertices: {vertex_count}, Indices: {index_count}')
        
        # mateiral faces (auto sort?) 
        #-> check shared vertex 
        #-> dump indices into each submesh
        #-> normalize submesh indices
        submesh_indices = [[] for i in range(material_count)]
        flag, material_faces = fbx_mesh.GetMaterialIndices()
        if not flag:
            raise Exception(f'lol2fbx: Failed: {mesh_name}: GetMaterialIndices()')
        if material_faces.GetCount() == 1:
            material_faces = [material_faces[0] for i in range(face_count)]
        material_vertices = [-1 for i in range(vertex_count)]
        for face_id, material_id in enumerate(material_faces):
            for i in range(3):
                vertex = indices[face_id*3+i]
                if material_vertices[vertex] not in (-1, material_id):
                    raise Exception(f'lol2fbx: Failed: {mesh_name} contains vertices shared by multiple material.')
                material_vertices[vertex] = material_id
                submesh_indices[material_id].append(vertex)
        for material_id in range(material_count):
            min_index = min(submesh_indices[material_id]) 
            submesh_indices[material_id] = [index - min_index for index in submesh_indices[material_id]]

        # positions -> transform to world position if blender armature node found
        vertex_positions = fbx_mesh.GetControlPoints()
        if blender_armature_node_name != None:
            vertex_positions = [blender_armature_node_local_matrix.MultT(vertex_position) for vertex_position in vertex_positions]
        # normals indices -> average vertex normals
        fbx_normals = FbxVector4Array()
        flag = fbx_mesh.GetPolygonVertexNormals(fbx_normals)
        if not flag:
            raise Exception(f'lol2fbx: Failed: {mesh_name}: GetPolygonVertexNormals()')
        vertex_normals = [[FbxVector4(0.0, 0.0, 0.0, 0.0), 0] for i in range(vertex_count)]
        for index, vertex in enumerate(indices):
            vertex_normals[vertex][0] += fbx_normals[index]
            vertex_normals[vertex][1] += 1
        vertex_normals = [s/c for s, c in vertex_normals]
        # weights indices -> vertex weights -> sort and prune 4+ (influence, weight)
        joint_ids_by_names = {}
        for joint in skl.joints:
            joint_ids_by_names[joint.name] = joint.id
        if fbx_mesh.GetDeformerCount() <= 0:
            raise Exception(f'lol2fbx: Failed: {mesh_name}: No deformer found. Mesh is not bound?')
        fbx_deformer = fbx_mesh.GetDeformer(0)
        if type(fbx_deformer) != FbxSkin:
            raise Exception(f'lol2fbx: Failed: {mesh_name}: Deformer is not FbxSkin?')
        fbx_clusters = [fbx_deformer.GetCluster(i) for i in range(fbx_deformer.GetClusterCount())]
        vertex_influences_weights = [[] for i in range(vertex_count)] 
        for fbx_cluster in fbx_clusters:
            influence_id = joint_ids_by_names[GetName(fbx_cluster.GetLink())]
            fbx_weight_vertices = fbx_cluster.GetControlPointIndices()
            fbx_weight_values = fbx_cluster.GetControlPointWeights() 
            for vertex_id in range(len(fbx_weight_vertices)):
                vertex_influences_weights[fbx_weight_vertices[vertex_id]].append((influence_id, fbx_weight_values[vertex_id]))
        for i in range(vertex_count):
            if len(vertex_influences_weights[i]) > 4:
                vertex_influences_weights[i].sort(key=lambda x: x[1])
                vertex_influences_weights[i] = vertex_influences_weights[i][:4]
                sum_weight = sum(weight for influence, weight in vertex_influences_weights[i])
                for j, (influence, weight) in enumerate(vertex_influences_weights[i]):
                    vertex_influences_weights[i][j] = (influence, weight/sum_weight)
        vertex_influences = [[] for i in range(vertex_count)]
        vertex_weights = [[] for i in range(vertex_count)]
        for i in range(vertex_count):
            for influence, weight in vertex_influences_weights[i]:
                vertex_influences[i].append(influence)
                vertex_weights[i].append(weight)
            fill_zero = [0 for j in range(4 - len(vertex_influences[i]))]
            vertex_influences[i] += fill_zero 
            vertex_weights[i] += fill_zero
        # uv indices 
        material_start_index = [0 for i in range(material_count)]
        for material_id in range(1, material_count):
            material_start_index[material_id] = material_start_index[material_id-1] + len(submesh_indices[material_id-1])
        flag, uvs = fbx_mesh.GetTextureUV()
        if not flag:
            raise Exception('lol2fbx: Failed: {mesh_name}: GetTextureUV()')
        vertex_uv_indices = [[] for i in range(vertex_count)]
        for face_id in range(face_count):
            for i in range(0, 3):
                index_id = face_id*3+i 
                vertex = indices[index_id]
                vertex_uv_indices[vertex].append(
                    (index_id, fbx_mesh.GetTextureUVIndex(face_id, i))
                )

        # dump vertex by uv index
        # -> create new vertex if multiple uv index
        # -> replace indices of newly created vertex
        submesh_vertices = [[] for i in range(len(materials))]
        for i in range(vertex_count):
            material_id = material_vertices[i]
            seen_uv_indices = []
            new_index_at_uv_index = {}
            for index_id, uv_index in vertex_uv_indices[i]:
                index_id -= material_start_index[material_id]
                if uv_index not in seen_uv_indices:
                    seen_uv_indices.append(uv_index)
                    vertex = SKNVertex()
                    # position
                    vertex.position = Vector(vertex_positions[i][0], vertex_positions[i][1], vertex_positions[i][2])
                    # normal
                    vertex.normal = Vector(vertex_normals[i][0], vertex_normals[i][1], vertex_normals[i][2])
                    # influence + weight
                    vertex.influences = vertex_influences[i]
                    vertex.weights = vertex_weights[i]
                    # uvs
                    vertex.uv = Vector(uvs[uv_index][0], 1-uvs[uv_index][1])
                    new_index = len(submesh_vertices[material_id]) 
                    new_index_at_uv_index[uv_index] = new_index
                    submesh_indices[material_id][index_id] = new_index
                    submesh_vertices[material_id].append(vertex)
                else:
                    submesh_indices[material_id][index_id] = new_index_at_uv_index[uv_index]
        
        return submesh_indices, submesh_vertices
    # meshes
    # dump each mesh -> combine indices, vertices
    material_count = len(materials)
    combined_submesh_indices = [[] for i in range(material_count)]
    combined_submesh_vertices = [[] for i in range(material_count)]
    material_count = len(materials)               
    for mesh_name, fbx_mesh in fbx_meshes.items():
        submesh_indices, submesh_vertices = dump_mesh(mesh_name, fbx_mesh)
        for material_id in range(material_count):
            max_index = max(combined_submesh_indices[material_id], default=-1)+1
            combined_submesh_indices[material_id].extend(
                index+max_index for index in submesh_indices[material_id]
            )
            combined_submesh_vertices[material_id].extend(submesh_vertices[material_id])

    # skn
    skn = SKN()
    skn.indices = combined_submesh_indices[0]
    skn.vertices = combined_submesh_vertices[0]
    skn.submeshes = [SKNSubmesh() for i in range(material_count)]
    skn.submeshes[0].name = GetName(materials[0])
    skn.submeshes[0].index_start = 0
    skn.submeshes[0].index_count = len(combined_submesh_indices[0])
    skn.submeshes[0].vertex_start = 0
    skn.submeshes[0].vertex_count = len(combined_submesh_vertices[0])
    for material_id in range(1, material_count):
        max_index = max(skn.indices)+1
        skn.indices += [max_index + index for index in combined_submesh_indices[material_id]]
        skn.vertices += combined_submesh_vertices[material_id]
        submesh = skn.submeshes[material_id]
        previous_submesh = skn.submeshes[material_id-1]
        submesh.name = GetName(materials[material_id])
        submesh.index_start = previous_submesh.index_start + previous_submesh.index_count
        submesh.index_count = len(combined_submesh_indices[material_id])
        submesh.vertex_start = previous_submesh.vertex_start + previous_submesh.vertex_count
        submesh.vertex_count = len(combined_submesh_vertices[material_id])
    
    if len(skn.vertices) > 65535:
        raise Exception(f'lol2fbx: Failed Too many vertices found: {len(skn.vertices)}, max allowed: 65535 vertices. (base on UVs)')

    return skn

def fbx_to_skin(fbx_path, skl_path='', skn_path=''):
    # io & load scene
    fbx_manager = FbxManager()
    fbx_importer = FbxImporter.Create(fbx_manager, 'importer')
    fbx_importer.Initialize(fbx_path)
    major, minor, revision = fbx_importer.GetFileVersion()
    LOG(f'lol2fbx: Fbx File: {fbx_path}')
    LOG(f'lol2fbx: Version: {major}.{minor}.{revision}\n')
    fbx_scene = FbxScene.Create(fbx_manager, 'scene')
    fbx_importer.Import(fbx_scene)
    fbx_importer.Destroy()

    # nodes
    fbx_nodes = [fbx_scene.GetNode(i) for i in range(fbx_scene.GetNodeCount())]

    # get meshes and joints
    fbx_meshes = {}
    fbx_joints = {}
    for node in fbx_nodes:
        node_attribute = node.GetNodeAttribute()
        if type(node_attribute) == FbxMesh:
            fbx_meshes[GetName(node)] = node_attribute
        elif type(node_attribute) == FbxSkeleton:
            fbx_joints[GetName(node)] = node
    joint_count = len(fbx_joints)
    mesh_count = len(fbx_meshes)
    LOG(f'lol2fbx: Joints: {joint_count}, Meshes: {mesh_count}\n')

    skl, blender_armature_node_name, blender_armature_node_local_matrix = dump_skl(fbx_joints)
    materials = [fbx_scene.GetMaterial(i) for i in range(fbx_scene.GetMaterialCount())]
    LOG(f'lol2fbx: Scene materials: {len(materials)}')
    skn = dump_skn(fbx_meshes, materials, skl, blender_armature_node_name, blender_armature_node_local_matrix)

    # mirror X before write
    mirrorX(skl, skn)
    
    # write file out after dump
    if skl_path != None:
        skl_path = fbx_path.replace('.fbx', '.skl')
    write_skl(skl_path, skl)
    LOG(f'lol2fbx: Done: Write SKL')
    if skn_path != None:
        skn_path = fbx_path.replace('.fbx', '.skn')
    write_skn(skn_path, skn)
    LOG(f'lol2fbx: Done: Write SKN')


def prepare(_LOG):
    global LOG
    LOG = _LOG
