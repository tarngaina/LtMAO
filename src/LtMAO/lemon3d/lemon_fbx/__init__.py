import os, os.path
from . import skin, animation, helper
from ... import lepath, pyRitoFile
from fbx import (
    FbxManager, FbxImporter, FbxExporter, FbxIOSettings, FbxScene, FbxNode,
    FbxSkeleton, FbxMesh,
)

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
            fbx_meshes[helper.GetName(node)] = node_attribute
        elif type(node_attribute) == FbxSkeleton:
            fbx_joints[helper.GetName(node)] = node
    joint_count = len(fbx_joints)
    mesh_count = len(fbx_meshes)
    print(f'lemon_fbx: Joints: {joint_count}, Meshes: {mesh_count}')

    # dump skl
    skl, blender_armature_node_name, blender_armature_node_local_matrix = skin.SKL.dump_skl(fbx_joints)
    helper.mirrorX(skl=skl)
    skl.write(skl_path)
    print(f'lemon_fbx: Finish: Write SKL: {skl_path}')

    # dump skn
    skn = skin.SKN.dump_skn(fbx_meshes, skl, blender_armature_node_name, blender_armature_node_local_matrix)
    helper.mirrorX(skn=skn)
    skn.write(skn_path)
    print(f'lemon_fbx: Finish: Write SKN: {skn_path}')

    # dump anm
    anms = animation.ANM.dump_anm(fbx_scene, fbx_joints, blender_armature_node_local_matrix)
    os.makedirs(anm_path, exist_ok=True )
    for anm_name, anm in anms.items():
        helper.mirrorX(anm=anm)
        anm_file = lepath.join(anm_path, anm_name) + '.anm'
        anm.write(anm_file)
        print(f'lemon_fbx: Finish: Write ANM: {anm_file}')

    # boom boom bakudan
    fbx_importer.Destroy()
    print('lemon_fbx: Finish: Export Skin.') 

def skin_to_fbx(skl_path, skn_path, anm_path, fbx_path):
    # create scene
    fbx_manager = FbxManager()
    fbx_scene = FbxScene.Create(fbx_manager, 'export_scene')
    fbx_root_node = fbx_scene.GetRootNode()
    
    # build skl
    if skl_path != None and skl_path != '':
        skl = pyRitoFile.skl.SKL().read(skl_path)
        print(f'lemon_fbx: Finish: Read SKL: {skl_path}, Version: {skl.version}')
        helper.mirrorX(skl=skl)
        print(f'lemon_fbx: Joints: {len(skl.joints)}, Influences: {len(skl.influences)}')
        fbx_joint_nodes = skin.SKL.load_skl(fbx_root_node, fbx_scene, skl)
    else:
        skl = None
        fbx_joint_nodes = None

    # build skn
    skn = pyRitoFile.skn.SKN().read(skn_path)
    print(f'lemon_fbx: Finish: Read SKN: {skn_path}, Version: {skn.version}')
    helper.mirrorX(skn=skn)
    print(f'lemon_fbx: Indices: {len(skn.indices)}, Vertices: {len(skn.vertices)}, Submeshes: {len(skn.submeshes)}')
    skin.SKN.load_skn(fbx_root_node, fbx_scene, skn, skl, fbx_joint_nodes)

    # build anms
    if skl_path != None and skl_path != '':
        anm_files = []
        if os.path.isdir(anm_path):
            for file in os.listdir(anm_path):
                if file.endswith('.anm'):
                    anm_files.append(lepath.join(anm_path, file))
        anms = {}
        for anm_file in anm_files:
            anm = pyRitoFile.anm.ANM().read(anm_file)
            print(f'lemon_fbx: Finish: Read ANM: {anm_file}, Version: {anm.version}')
            helper.mirrorX(anm=anm)
            anms[anm_file] = anm
        print(f'lemon_fbx: Animations: {len(anms)}')
        animation.ANM.load_anm(fbx_scene, anms, fbx_joint_nodes)
    
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

