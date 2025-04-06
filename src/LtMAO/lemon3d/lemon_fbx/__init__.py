from fbx import (
    FbxManager, FbxImporter, FbxExporter, FbxIOSettings, FbxScene, FbxNode,
    FbxSkeleton, FbxMesh, FbxSkin, FbxCluster, 
    FbxLayerElement, FbxSurfaceLambert, 
    FbxCriteria, FbxAnimStack, FbxAnimLayer, FbxAnimCurveDef, FbxTime, FbxTimeSpan, FbxGlobalSettings,
    FbxNull, FbxVector4, FbxVector4Array, FbxQuaternion, FbxDouble3, FbxVector2, FbxAMatrix,
)
from ...pyRitoFile import (
    SKL, SKLJoint, read_skl, read_skn,
    SKN, SKNVertex, SKNSubmesh, write_skl, write_skn,
    ANM, ANMTrack, ANMPose, read_anm, write_anm
)
from ...pyRitoFile.helper import Elf
from ...pyRitoFile.structs import Vector, Quaternion
import os, os.path
import math 
ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

def GetName(node):
    return ''.join(c if c in ALPHANUMERIC else f'FBXASC{ord(c):03}' for c in node.GetNameOnly().Buffer())


def mirrorX(skl=None, skn=None, anm=None):
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
    if anm != None:
        for track in anm.tracks:
            for time in track.poses:
                pose = track.poses[time]
                if pose.translate != None:
                    pose.translate.x = -pose.translate.x
                if pose.rotate != None:
                    pose.rotate.y = -pose.rotate.y
                    pose.rotate.z = -pose.rotate.z
    

def dump_skl(fbx_joints):
    # prepare
    joint_count = len(fbx_joints)
    if joint_count > 256:
        raise Exception(f'lemon_fbx: Error: Too many joints found: {joint_count}, max: 256')
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
    print(f'lemon_fbx: Finish: Read {joint_count} joints.')
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
                    print(f'lemon_fbx: Found blender armature/locator node: {blender_armature_node_name}')
                else:
                    if blender_armature_node_name != parent_node_name:
                        raise Exception('lemon_fbx: Error: Skeleton is grouped by multiple locator/blender armature node????')
                joint = skl.joints[joint_id]
                new_local_matrix = fbx_joint.EvaluateLocalTransform() * blender_armature_node_local_matrix
                translate, rotate, scale = new_local_matrix.GetT(), new_local_matrix.GetQ(), new_local_matrix.GetS()
                joint.local_translate = Vector(translate[0], translate[1], translate[2])
                joint.local_rotate = Quaternion(rotate[0], rotate[1], rotate[2], rotate[3])
                joint.local_scale = Vector(scale[0], scale[1], scale[2])
        else:
            skl.joints[joint_id].parent = -1      
    print(f'lemon_fbx: Finish: Dump SKL.')
    return skl, blender_armature_node_name, blender_armature_node_local_matrix


def dump_skn(fbx_meshes, skl, blender_armature_node_name, blender_armature_node_local_matrix):
    def dump_mesh(mesh_name, fbx_mesh):
        print(f'lemon_fbx: Start:  Read {mesh_name}')   

        # check triangle
        is_triangle = fbx_mesh.IsTriangleMesh()
        print(f'lemon_fbx: Triangle mesh: {is_triangle}')
        if not is_triangle:
            raise Exception(f'lemon_fbx: Error: {mesh_name} is not a triangle mesh.')
        
        # get info
        indices = fbx_mesh.GetPolygonVertices()
        vertex_count = fbx_mesh.GetControlPointsCount()
        index_count = len(indices)
        face_count = index_count // 3
        print(f'lemon_fbx: Faces: {face_count}, Vertices: {vertex_count}, Indices: {index_count}')
        
        # mateiral faces - some fbx dont get sorted
        #-> sort it by value, also sort the indices too
        #-> save the old order for some stuff later
        #-> check shared vertex 
        #-> dump indices into each submesh
        #-> normalize submesh indices
        fbx_node = fbx_mesh.GetNode()
        material_count = fbx_node.GetMaterialCount()
        submesh_names = [GetName(fbx_node.GetMaterial(i)) for i in range(material_count)]
        submesh_indices = {submesh_name: [] for submesh_name in submesh_names}
        flag, material_faces = fbx_mesh.GetMaterialIndices()
        if not flag:
            raise Exception(f'lemon_fbx: Error: {mesh_name}: GetMaterialIndices()')
        if material_faces.GetCount() == 1:
            material_faces = [material_faces[0]] * face_count
        else:
            material_faces = [material_faces[i] for i in range(face_count)]
        parsed_material_faces = {material_id: [] for material_id in range(material_count)}
        for face_id in range(face_count):
            index1_id = face_id*3
            index2_id = face_id*3+1
            index3_id = face_id*3+2
            parsed_material_faces[material_faces[face_id]].append((
                index1_id, indices[index1_id],
                index2_id, indices[index2_id],
                index3_id, indices[index3_id]
            ))
        indices = []
        material_faces = []
        old_index_by_sorted_index = [0 for i in range(index_count)]
        temp_index_count = 0
        for material_id in range(material_count):
            for index1_id, index1, index2_id, index2, index3_id, index3 in parsed_material_faces[material_id]:
                material_faces.append(material_id)
                indices.extend((index1, index2, index3))
                old_index_by_sorted_index.extend((temp_index_count, temp_index_count+1, temp_index_count+2))
                temp_index_count+=3
        material_vertices = [-1] * vertex_count
        for face_id, material_id in enumerate(material_faces):
            for i in range(3):
                vertex = indices[face_id*3+i]
                if material_vertices[vertex] not in (-1, material_id):
                    raise Exception(f'lemon_fbx: Error: {mesh_name} contains vertices shared by multiple material.')
                material_vertices[vertex] = material_id
                submesh_indices[submesh_names[material_id]].append(vertex)
        for submesh_name in submesh_names:
            min_index = min(submesh_indices[submesh_name]) 
            submesh_indices[submesh_name] = [index - min_index for index in submesh_indices[submesh_name]]

        # positions -> transform to world position if blender armature node found
        vertex_positions = fbx_mesh.GetControlPoints()
        if blender_armature_node_name != None:
            vertex_positions = [blender_armature_node_local_matrix.MultT(vertex_position) for vertex_position in vertex_positions]
        # normals indices -> average vertex normals
        fbx_normals = FbxVector4Array()
        flag = fbx_mesh.GetPolygonVertexNormals(fbx_normals)
        if not flag:
            raise Exception(f'lemon_fbx: Error: {mesh_name}: GetPolygonVertexNormals()')
        vertex_normals = [[FbxVector4(0.0, 0.0, 0.0, 0.0), 0] for i in range(vertex_count)]
        for index, vertex in enumerate(indices): # this indices is sorted 
            vertex_normals[vertex][0] += fbx_normals[old_index_by_sorted_index[index]]
            vertex_normals[vertex][1] += 1
        vertex_normals = [s/c for s, c in vertex_normals]
        # weights indices -> vertex weights -> sort and prune 4+ (influence, weight)
        joint_ids_by_names = {}
        for joint in skl.joints:
            joint_ids_by_names[joint.name] = joint.id
        if fbx_mesh.GetDeformerCount() <= 0:
            raise Exception(f'lemon_fbx: Error: {mesh_name}: No deformer found. Mesh is not bound?')
        fbx_deformer = fbx_mesh.GetDeformer(0)
        if type(fbx_deformer) != FbxSkin:
           raise Exception(f'lemon_fbx: Error: {mesh_name}: Deformer is not FbxSkin? {type(fbx_deformer)}')
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
        # uv values
        flag, uvs = fbx_mesh.GetTextureUV()
        if not flag:
            raise Exception(f'lemon_fbx: Error: {mesh_name}: GetTextureUV()')
        # uv indices base on mapping mode
        vertex_uv_indices = [[] for i in range(vertex_count)]
        fbx_uv = fbx_mesh.GetElementUV(0)
        fbx_uv_mapping_mode = fbx_uv.GetMappingMode() 
        if fbx_uv_mapping_mode == FbxLayerElement.EMappingMode.eByControlPoint:
            # easy mapping mode, straight forward 1 vertex - 1 uv index
            for face_id in range(face_count):
                for i in range(0, 3):
                    index_id = face_id*3+i 
                    vertex = indices[index_id]
                    vertex_uv_indices[vertex].append(
                        (index_id, vertex)
                    )
        elif fbx_uv_mapping_mode == FbxLayerElement.EMappingMode.eByPolygonVertex:
            # this one 1 vertex could contains multiple uv indices
            for face_id in range(face_count):
                for i in range(0, 3):
                    index_id = face_id*3+i 
                    vertex = indices[index_id]
                    vertex_uv_indices[vertex].append(
                        (index_id, fbx_mesh.GetTextureUVIndex(face_id, i))
                    )
        else:
            # not yet support mapping mode
            # actually only 2 mapping mode above is needed because the rest is pepega for UVs?
            raise Exception(f'lemon_fbx: Error: {mesh_name}: Unsupported UV MappingMode: {fbx_uv_mapping_mode}')
        # dump vertex by uv index
        # -> first prepare normalized index by material
        # -> start dump each vertex with its uv indices
        # -> create new vertex if multiple uv index
        # -> replace indices of newly created vertex
        material_start_index = [0] * material_count
        for material_id in range(1, material_count):
            material_start_index[material_id] = material_start_index[material_id-1] + len(submesh_indices[submesh_names[material_id-1]])
        submesh_vertices = {submesh_name: [] for submesh_name in submesh_names}
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
                    new_index = len(submesh_vertices[submesh_names[material_id]]) 
                    new_index_at_uv_index[uv_index] = new_index
                    submesh_indices[submesh_names[material_id]][index_id] = new_index
                    submesh_vertices[submesh_names[material_id]].append(vertex)
                else:
                    submesh_indices[submesh_names[material_id]][index_id] = new_index_at_uv_index[uv_index]
        
        return submesh_indices, submesh_vertices, submesh_names
    
    # meshes
    # dump each mesh 
    # -> combine same submesh name first
    # -> combine into whole skn
    combined_submesh_indices = {}
    combined_submesh_vertices = {}
    combined_submesh_names = []
    for mesh_name, fbx_mesh in fbx_meshes.items():
        submesh_indices, submesh_vertices, submesh_names = dump_mesh(mesh_name, fbx_mesh)
        for submesh_name in submesh_names:
            if submesh_name not in combined_submesh_indices:
                combined_submesh_indices[submesh_name] = submesh_indices[submesh_name]
                combined_submesh_vertices[submesh_name] = submesh_vertices[submesh_name]
            else:
                max_index = max(combined_submesh_indices[submesh_name])+1
                combined_submesh_indices[submesh_name].extend(index+max_index for index in submesh_indices[submesh_name])
                combined_submesh_vertices[submesh_name].extend(submesh_vertices[submesh_name])
            if submesh_name not in combined_submesh_names:
                combined_submesh_names.append(submesh_name)
                
    # skn
    skn = SKN()
    skn.indices = combined_submesh_indices[combined_submesh_names[0]]
    skn.vertices = combined_submesh_vertices[combined_submesh_names[0]]
    submesh_count = len(combined_submesh_names)
    skn.submeshes = [SKNSubmesh() for i in range(submesh_count)]
    skn.submeshes[0].name = combined_submesh_names[0]
    skn.submeshes[0].index_start = 0
    skn.submeshes[0].index_count = len(combined_submesh_indices[combined_submesh_names[0]])
    skn.submeshes[0].vertex_start = 0
    skn.submeshes[0].vertex_count = len(combined_submesh_vertices[combined_submesh_names[0]])
    for submesh_id in range(1, submesh_count):
        max_index = max(skn.indices)+1
        skn.indices += [max_index + index for index in combined_submesh_indices[combined_submesh_names[submesh_id]]]
        skn.vertices += combined_submesh_vertices[combined_submesh_names[submesh_id]]
        submesh = skn.submeshes[submesh_id]
        previous_submesh = skn.submeshes[submesh_id-1]
        submesh.name = combined_submesh_names[submesh_id]
        submesh.index_start = previous_submesh.index_start + previous_submesh.index_count
        submesh.index_count = len(combined_submesh_indices[combined_submesh_names[submesh_id]])
        submesh.vertex_start = previous_submesh.vertex_start + previous_submesh.vertex_count
        submesh.vertex_count = len(combined_submesh_vertices[combined_submesh_names[submesh_id]])
    
    if len(skn.vertices) > 65535:
        raise Exception(f'lemon_fbx: Error: Too many vertices found: {len(skn.vertices)}, max allowed: 65535 vertices. (base on UVs)')
    print(f'lemon_fbx: Finish: Dump SKN.')
    return skn


def dump_anm(fbx_scene, fbx_joints, blender_armature_node_local_matrix):
    # get fps
    fbx_global_settings = fbx_scene.GetSrcObject(FbxCriteria.ObjectType(FbxGlobalSettings.ClassId), 0)
    time_mode = fbx_global_settings.GetTimeMode()
    if time_mode == FbxTime.EMode.eFrames60:
        fps = 60.0   
    else:
        fps = 30.0
    anms = {}
    fbx_anim_stack_count = fbx_scene.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimStack.ClassId))
    print(f'lemon_fbx: Animation stacks: {fbx_anim_stack_count}')
    for anim_stack_id in range(fbx_anim_stack_count):
        fbx_anim_stack = fbx_scene.GetSrcObject(FbxCriteria.ObjectType(FbxAnimStack.ClassId), anim_stack_id)
        fbx_scene.SetCurrentAnimationStack(fbx_anim_stack)
        fbx_anim_stack_name = fbx_anim_stack.GetName().replace('|', '_')
        start = fbx_anim_stack.LocalStop.Get().GetSecondDouble()
        end = fbx_anim_stack.LocalStart.Get().GetSecondDouble()
        animation_time_range = start - end
        frame_range = int(animation_time_range * fps)
        fbx_time = FbxTime()
        tracks = {}
        for joint_name, fbx_joint in fbx_joints.items():
            parent_node = fbx_joint.GetParent()
            parent_is_blender_armature_node = False
            if type(parent_node.GetNodeAttribute()) == FbxNull:
                parent_is_blender_armature_node = True
            tracks[joint_name] = track = ANMTrack()
            track.joint_hash = Elf(joint_name)
            track.poses = {}
            for frame in range(1, frame_range+1, 1):
                track.poses[frame-1] = pose = ANMPose()
                time = frame / fps
                fbx_time.SetSecondDouble(time)
                fbx_local_matrix = fbx_joint.EvaluateLocalTransform(fbx_time) 
                if parent_is_blender_armature_node:
                    fbx_local_matrix = fbx_local_matrix * blender_armature_node_local_matrix
                translate, rotate, scale = fbx_local_matrix.GetT(), fbx_local_matrix.GetQ(), fbx_local_matrix.GetS()
                pose.translate = Vector(translate[0], translate[1], translate[2])
                pose.rotate = Quaternion(rotate[0], rotate[1], rotate[2], rotate[3])
                pose.scale = Vector(scale[0], scale[1], scale[2])
                if math.isnan(pose.rotate.x):
                    fbx_anim_evaluator = fbx_scene.GetAnimationEvaluator()
                    translate = fbx_anim_evaluator.GetNodeLocalTranslation(fbx_joint, fbx_time)
                    rotate = fbx_anim_evaluator.GetNodeLocalRotation(fbx_joint, fbx_time)
                    scale = fbx_anim_evaluator.GetNodeLocalScaling(fbx_joint, fbx_time)
                    fbx_local_matrix = FbxAMatrix()
                    fbx_local_matrix.SetTRS(translate, rotate, scale)
                    if parent_is_blender_armature_node:
                        fbx_local_matrix = fbx_local_matrix * blender_armature_node_local_matrix

                    translate = fbx_local_matrix.GetT()
                    rotate = fbx_local_matrix.GetQ()
                    scale = fbx_local_matrix.GetS()
                    pose.translate = Vector(translate[0], translate[1], translate[2])
                    pose.rotate = Quaternion(rotate[0], rotate[1], rotate[2], rotate[3])
                    pose.scale = Vector(scale[0], scale[1], scale[2])


        anm = ANM()
        anm.fps = fps
        anm.duration = frame_range
        anm.tracks = list(tracks.values())
        anms[fbx_anim_stack_name] = anm
        print(f'lemon_fbx: Finish: Dump ANM: Animation stack: {fbx_anim_stack_name}, Frame range: {frame_range}, FPS: {fps}')
    return anms       


def fbx_to_skin(fbx_path, skl_path, skn_path, anm_path):
    # io & load scene
    fbx_manager = FbxManager()
    fbx_importer = FbxImporter.Create(fbx_manager, 'importer')
    fbx_importer.Initialize(fbx_path)
    major, minor, revision = fbx_importer.GetFileVersion()
    fbx_scene = FbxScene.Create(fbx_manager, 'scene')
    fbx_importer.Import(fbx_scene)
    print(f'lemon_fbx: Finish: Read FBX: {fbx_path}')
    print(f'lemon_fbx: FBX Version: {major}.{minor}.{revision}')

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
    print(f'lemon_fbx: Joints: {joint_count}, Meshes: {mesh_count}')

    # dump skl
    skl, blender_armature_node_name, blender_armature_node_local_matrix = dump_skl(fbx_joints)
    mirrorX(skl=skl)
    write_skl(skl_path, skl)
    print(f'lemon_fbx: Finish: Write SKL: {skl_path}')

    # dump skn
    skn = dump_skn(fbx_meshes, skl, blender_armature_node_name, blender_armature_node_local_matrix)
    mirrorX(skn=skn)
    write_skn(skn_path, skn)
    print(f'lemon_fbx: Finish: Write SKN: {skn_path}')

    # dump anm
    anms = dump_anm(fbx_scene, fbx_joints, blender_armature_node_local_matrix)
    os.makedirs(anm_path, exist_ok=True )
    for anm_name, anm in anms.items():
        mirrorX(anm=anm)
        anm_file = os.path.join(anm_path, anm_name).replace('\\', '/') + '.anm'
        write_anm(anm_file, anm)
        print(f'lemon_fbx: Finish: Write ANM: {anm_file}')

    # boom boom bakudan
    fbx_importer.Destroy()
    print('lemon_fbx: Finish: FBX to SKIN.')


def load_skl(fbx_root_node, fbx_scene, skl):
    # create joints
    # -> set joint's local transform
    fbx_joint_nodes = {}
    for joint_id, joint in enumerate(skl.joints):
        fbx_joint_node = FbxNode.Create(fbx_scene, f'{joint.name}')
        fbx_joint = FbxSkeleton.Create(fbx_scene, 'joint_{joint.name}')
        fbx_joint.SetSkeletonType(FbxSkeleton.EType.eLimbNode)
        fbx_joint_node.SetNodeAttribute(fbx_joint)
        fbx_root_node.AddChild(fbx_joint_node)
        local_rotate = FbxVector4()
        local_rotate.SetXYZ(FbxQuaternion(joint.local_rotate.x, joint.local_rotate.y, joint.local_rotate.z, joint.local_rotate.w))
        fbx_joint_node.LclTranslation.Set(FbxDouble3(joint.local_translate.x, joint.local_translate.y, joint.local_translate.z))
        fbx_joint_node.LclRotation.Set(FbxDouble3(local_rotate[0], local_rotate[1], local_rotate[2]))
        fbx_joint_node.LclScaling.Set(FbxDouble3(joint.local_scale.x, joint.local_scale.y, joint.local_scale.z))
        fbx_joint_nodes[joint_id] = fbx_joint_node
    # link joint parents
    for joint_id, joint in enumerate(skl.joints):
        if joint.parent != -1:
            fbx_joint_nodes[joint.parent].AddChild(fbx_joint_nodes[joint_id])
    print(f'lemon_fbx: Finish: Load SKL.')
    return fbx_joint_nodes


def load_skn(fbx_root_node, fbx_scene, skn, skl, fbx_joint_nodes):
    fbx_lamberts = {}
    for submesh in skn.submeshes:
        fbx_lamberts[submesh.name] = FbxSurfaceLambert.Create(fbx_scene, submesh.name)
    for submesh_id, submesh in enumerate(skn.submeshes): 
        submesh_vertices = skn.vertices[submesh.vertex_start:submesh.vertex_start+submesh.vertex_count]
        submesh_indices = skn.indices[submesh.index_start:submesh.index_start+submesh.index_count]
        min_index = min(submesh_indices)
        submesh_indices = [index-min_index for index in submesh_indices]

        # create mesh
        fbx_mesh_node = FbxNode.Create(fbx_scene, f'mesh_{submesh.name}')
        fbx_mesh = FbxMesh.Create(fbx_scene, f'shape_{submesh.name}')
        fbx_mesh_node.SetNodeAttribute(fbx_mesh)
        fbx_root_node.AddChild(fbx_mesh_node)
    
        # set vertex position
        vertex_count = len(submesh_vertices)
        fbx_mesh.InitControlPoints(vertex_count)
        for vertex_id, vertex in enumerate(submesh_vertices):
            fbx_mesh.SetControlPointAt(FbxVector4(vertex.position.x, vertex.position.y, vertex.position.z), vertex_id)
   
        # create materials
        fbx_material = fbx_mesh.CreateElementMaterial()
        fbx_material.SetMappingMode(FbxLayerElement.EMappingMode.eByPolygon)
        fbx_material.SetReferenceMode(FbxLayerElement.EReferenceMode.eIndexToDirect)
        fbx_mesh_node.AddMaterial(fbx_lamberts[submesh.name])
    
        # create faces on each material
        index_count = len(submesh_indices)
        for index in range(0, index_count, 3):
            fbx_mesh.BeginPolygon(0)
            fbx_mesh.AddPolygon(submesh_indices[index])
            fbx_mesh.AddPolygon(submesh_indices[index+1])
            fbx_mesh.AddPolygon(submesh_indices[index+2])
            fbx_mesh.EndPolygon()   
        # set uvs
        fbx_diffuse_uv = fbx_mesh.CreateElementUV('DiffuseUV')
        fbx_diffuse_uv.SetMappingMode(FbxLayerElement.EMappingMode.eByControlPoint)
        fbx_diffuse_uv.SetReferenceMode(FbxLayerElement.EReferenceMode.eDirect)
        uvs = fbx_diffuse_uv.GetDirectArray()
        for vertex in submesh_vertices:
            uvs.Add(FbxVector2(vertex.uv.x, 1-vertex.uv.y))
        # set normals - doesnt work?
        fbx_normal = fbx_mesh.CreateElementNormal()
        fbx_normal.SetMappingMode(FbxLayerElement.EMappingMode.eByControlPoint)
        fbx_normal.SetReferenceMode(FbxLayerElement.EReferenceMode.eDirect)
        normals = fbx_normal.GetDirectArray()
        for vertex in submesh_vertices:
            normals.Add(FbxVector4(vertex.normal.x, vertex.normal.y, vertex.normal.z))  
        
        # set weights 
        # -> create skin 
        # -> create cluster 
        # -> set cluster weights, and transform link matrix (why?)
        fbx_skin = FbxSkin.Create(fbx_scene, 'skinned_mesh')
        fbx_skin.SetSkinningType(FbxSkin.EType.eBlend)
        fbx_mesh.AddDeformer(fbx_skin)
        weight_vertices = {influence: [] for influence in skl.influences}
        weight_values =  {influence: [] for influence in skl.influences}
        for vertex_id, vertex in enumerate(submesh_vertices):
            for i in range(4):
                influence_id = vertex.influences[i]
                weight = vertex.weights[i]
                if weight > 0.0:
                    weight_vertices[skl.influences[influence_id]].append(vertex_id)
                    weight_values[skl.influences[influence_id]].append(weight)
        for influence in skl.influences:
            fbx_cluster = FbxCluster.Create(fbx_scene, f'cluster_{influence}')
            fbx_cluster.SetLink(fbx_joint_nodes[influence])
            fbx_cluster.SetLinkMode(FbxCluster.ELinkMode.eTotalOne)
            weight_vertex_value_count = len(weight_vertices[influence]) 
            for i in range(weight_vertex_value_count):
                fbx_cluster.AddControlPointIndex(weight_vertices[influence][i], weight_values[influence][i])
            fbx_cluster.SetTransformLinkMatrix(fbx_joint_nodes[influence].EvaluateGlobalTransform())
            fbx_skin.AddCluster(fbx_cluster)
        
        print(f'lemon_fbx: Finish: Load submesh: {submesh.name}, Indices: {len(submesh_indices)}, Vertices: {len(submesh_vertices)}')
    print(f'lemon_fbx: Finish: Load SKN.')


def load_anm(fbx_scene, anms, fbx_joint_nodes):
    # set 30 fps
    fbx_global_settings = fbx_scene.GetSrcObject(FbxCriteria.ObjectType(FbxGlobalSettings.ClassId), 0)
    fbx_global_settings.SetTimeMode(FbxTime.EMode.eFrames30)
    for anm_file, anm in anms.items():
        fbx_anim_stack_name = os.path.basename(anm_file).split('.anm')[0]
        fbx_anim_stack = FbxAnimStack.Create(fbx_scene, fbx_anim_stack_name)
        fbx_anim_layer = FbxAnimLayer.Create(fbx_scene, 'Layer0')
        fbx_anim_stack.AddMember(fbx_anim_layer)
        start = FbxTime()
        start.SetSecondDouble(0.0)
        end = FbxTime()
        end.SetSecondDouble(anm.duration / anm.fps)
        fbx_time_span = FbxTimeSpan()
        fbx_time_span.Set(start, end)
        fbx_anim_stack.SetLocalTimeSpan(fbx_time_span)

        fbx_time = FbxTime()
        tracks = {}
        for track in anm.tracks:
            tracks[track.joint_hash] = track
        for joint_id, fbx_joint_node in fbx_joint_nodes.items():
            translatex_curve = fbx_joint_node.LclTranslation.GetCurve(fbx_anim_layer, 'X', True);
            translatey_curve = fbx_joint_node.LclTranslation.GetCurve(fbx_anim_layer, 'Y', True);
            translatez_curve = fbx_joint_node.LclTranslation.GetCurve(fbx_anim_layer, 'Z', True);

            scalex_curve = fbx_joint_node.LclScaling.GetCurve(fbx_anim_layer, 'X', True);
            scaley_curve = fbx_joint_node.LclScaling.GetCurve(fbx_anim_layer, 'Y', True);
            scalez_curve = fbx_joint_node.LclScaling.GetCurve(fbx_anim_layer, 'Z', True);

            rotatex_curve = fbx_joint_node.LclRotation.GetCurve(fbx_anim_layer, 'X', True);
            rotatey_curve = fbx_joint_node.LclRotation.GetCurve(fbx_anim_layer, 'Y', True);
            rotatez_curve = fbx_joint_node.LclRotation.GetCurve(fbx_anim_layer, 'Z', True);


            joint_hash = Elf(fbx_joint_node.GetName())
            if joint_hash not in tracks:
                continue
            track = tracks[joint_hash]
            
            translatex_curve.KeyModifyBegin()
            translatey_curve.KeyModifyBegin()
            translatez_curve.KeyModifyBegin()
            scalex_curve.KeyModifyBegin()
            scaley_curve.KeyModifyBegin()
            scalez_curve.KeyModifyBegin()
            rotatex_curve.KeyModifyBegin()
            rotatey_curve.KeyModifyBegin()
            rotatez_curve.KeyModifyBegin()

            # frame 0 as bind pose first
            fbx_time.SetSecondDouble(0.0)

            translate = fbx_joint_node.LclTranslation.Get()
            key_index = translatex_curve.KeyAdd(fbx_time)
            translatex_curve.KeySetValue(key_index[0], translate[0])
            translatex_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
            key_index = translatey_curve.KeyAdd(fbx_time)
            translatey_curve.KeySetValue(key_index[0], translate[1])
            translatey_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
            key_index = translatez_curve.KeyAdd(fbx_time)
            translatez_curve.KeySetValue(key_index[0], translate[2])
            translatez_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)

            rotate = fbx_joint_node.LclRotation.Get()
            fbx_time.SetSecondDouble(0.0)           
            key_index = rotatex_curve.KeyAdd(fbx_time)
            rotatex_curve.KeySetValue(key_index[0], rotate[0])
            rotatex_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationCubic)
            key_index = rotatey_curve.KeyAdd(fbx_time)
            rotatey_curve.KeySetValue(key_index[0], rotate[1])
            rotatey_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationCubic)
            key_index = rotatez_curve.KeyAdd(fbx_time)
            rotatez_curve.KeySetValue(key_index[0], rotate[2])
            rotatez_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationCubic)

            scale = fbx_joint_node.LclScaling.Get()
            fbx_time.SetSecondDouble(0.0)           
            key_index = scalex_curve.KeyAdd(fbx_time)
            scalex_curve.KeySetValue(key_index[0], scale[0])
            scalex_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
            key_index = scaley_curve.KeyAdd(fbx_time)
            scaley_curve.KeySetValue(key_index[0], scale[1])
            scaley_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
            key_index = scalez_curve.KeyAdd(fbx_time)
            scalez_curve.KeySetValue(key_index[0], scale[2])
            scalez_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)

            # the animations
            for frame in track.poses:
                pose = track.poses[frame]
                fbx_time.SetSecondDouble((frame+1) / anm.fps)           
                if pose.translate != None:
                    key_index = translatex_curve.KeyAdd(fbx_time)
                    translatex_curve.KeySetValue(key_index[0], pose.translate.x)
                    translatex_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
                    key_index = translatey_curve.KeyAdd(fbx_time)
                    translatey_curve.KeySetValue(key_index[0], pose.translate.y)
                    translatey_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
                    key_index = translatez_curve.KeyAdd(fbx_time)
                    translatez_curve.KeySetValue(key_index[0], pose.translate.z)
                    translatez_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)

                if pose.scale != None:
                    key_index = scalex_curve.KeyAdd(fbx_time)
                    scalex_curve.KeySetValue(key_index[0], pose.scale.x)
                    scalex_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
                    key_index = scaley_curve.KeyAdd(fbx_time)
                    scaley_curve.KeySetValue(key_index[0], pose.scale.y)
                    scaley_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
                    key_index = scalez_curve.KeyAdd(fbx_time)
                    scalez_curve.KeySetValue(key_index[0], pose.scale.z)
                    scalez_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
                
                if pose.rotate != None:
                    rotate = FbxVector4()
                    rotate.SetXYZ(FbxQuaternion(pose.rotate.x, pose.rotate.y, pose.rotate.z, pose.rotate.w))
                
                    key_index = rotatex_curve.KeyAdd(fbx_time)
                    rotatex_curve.KeySetValue(key_index[0], rotate[0])
                    rotatex_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationCubic)
                    key_index = rotatey_curve.KeyAdd(fbx_time)
                    rotatey_curve.KeySetValue(key_index[0], rotate[1])
                    rotatey_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationCubic)
                    key_index = rotatez_curve.KeyAdd(fbx_time)
                    rotatez_curve.KeySetValue(key_index[0], rotate[2])
                    rotatez_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationCubic)


            translatex_curve.KeyModifyEnd()
            translatey_curve.KeyModifyEnd()
            translatez_curve.KeyModifyEnd()
            scalex_curve.KeyModifyEnd()
            scaley_curve.KeyModifyEnd()
            scalez_curve.KeyModifyEnd()
            rotatex_curve.KeyModifyEnd()
            rotatey_curve.KeyModifyEnd()
            rotatez_curve.KeyModifyEnd()

        print(f'lemon_fbx: Finish: Load animation stack: {fbx_anim_stack_name}')


def skin_to_fbx(skl_path, skn_path, anm_path, fbx_path):
    # create scene
    fbx_manager = FbxManager()
    fbx_scene = FbxScene.Create(fbx_manager, 'export_scene')
    fbx_root_node = fbx_scene.GetRootNode()
    
    # build skl
    skl = read_skl(skl_path)
    print(f'lemon_fbx: Finish: Read SKL: {skl_path}, Version: {skl.version}')
    mirrorX(skl=skl)
    print(f'lemon_fbx: Joints: {len(skl.joints)}, Influences: {len(skl.influences)}')
    fbx_joint_nodes = load_skl(fbx_root_node, fbx_scene, skl)

    # build skn
    skn = read_skn(skn_path)
    print(f'lemon_fbx: Finish: Read SKN: {skn_path}, Version: {skn.version}')
    mirrorX(skn=skn)
    print(f'lemon_fbx: Indices: {len(skn.indices)}, Vertices: {len(skn.vertices)}, Submeshes: {len(skn.submeshes)}')
    load_skn(fbx_root_node, fbx_scene, skn, skl, fbx_joint_nodes)

    # build anms
    anm_files = []
    if os.path.isdir(anm_path):
        for file in os.listdir(anm_path):
            if file.endswith('.anm'):
                anm_files.append(os.path.join(anm_path, file).replace('\\', '/'))
    anms = {}
    for anm_file in anm_files:
        anm = read_anm(anm_file)
        print(f'lemon_fbx: Finish: Read ANM: {anm_file}, Version: {anm.version}')
        mirrorX(anm=anm)
        anms[anm_file] = anm
    print(f'lemon_fbx: Animations: {len(anms)}')
    load_anm(fbx_scene, anms, fbx_joint_nodes)
    
    # io & save scene
    fbx_ios = FbxIOSettings.Create(fbx_manager, 'ios')
    fbx_manager.SetIOSettings(fbx_ios)
    fbx_exporter = FbxExporter.Create(fbx_manager, 'exporter')
    fbx_exporter.Initialize(fbx_path)
    fbx_exporter.Export(fbx_scene)
    print(f'lemon_fbx: Finish: Write FBX: {fbx_path}')

    # boom boom bakudan
    fbx_exporter.Destroy()
    print('lemon_fbx: Finish: SKIN to FBX.')

