import os.path
from ... import pyRitoFile
from fbx import (
    FbxCriteria, FbxAnimStack, FbxAnimLayer, FbxAnimCurveDef, FbxTime, FbxTimeSpan, FbxGlobalSettings,
    FbxNull, FbxVector4, FbxQuaternion, FbxAMatrix
)

class ANM:
    @staticmethod
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

                joint_hash = pyRitoFile.helper.Elf(fbx_joint_node.GetName())
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
                        fbx_local_matrix = FbxAMatrix()
                        fbx_local_matrix.SetQ(FbxQuaternion(pose.rotate.x, pose.rotate.y, pose.rotate.z, pose.rotate.w))
                        rotate = fbx_local_matrix.GetR()
                        key_index = rotatex_curve.KeyAdd(fbx_time)
                        rotatex_curve.KeySetValue(key_index[0], rotate[0])
                        rotatex_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
                        key_index = rotatey_curve.KeyAdd(fbx_time)
                        rotatey_curve.KeySetValue(key_index[0], rotate[1])
                        rotatey_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)
                        key_index = rotatez_curve.KeyAdd(fbx_time)
                        rotatez_curve.KeySetValue(key_index[0], rotate[2])
                        rotatez_curve.KeySetInterpolation(key_index[0], FbxAnimCurveDef.EInterpolationType.eInterpolationLinear)


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


    @staticmethod
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
            fbx_anim_layer = fbx_anim_stack.GetMember(FbxCriteria.ObjectType(FbxAnimLayer.ClassId), 0)
            fbx_scene.SetCurrentAnimationStack(fbx_anim_stack)
            fbx_anim_stack_name = fbx_anim_stack.GetName().replace('|', '_')
            start = fbx_anim_stack.LocalStop.Get().GetSecondDouble()
            end = fbx_anim_stack.LocalStart.Get().GetSecondDouble()
            animation_time_range = start - end
            frame_range = int(animation_time_range * fps)
            fbx_time = FbxTime()
            tracks = []
            for joint_name, fbx_joint in fbx_joints.items():
                parent_node = fbx_joint.GetParent()
                parent_is_blender_armature_node = False
                if type(parent_node.GetNodeAttribute()) == FbxNull:
                    parent_is_blender_armature_node = True
                track = pyRitoFile.anm.ANMTrack()
                track.joint_hash = pyRitoFile.helper.Elf(joint_name)
                track.poses = {}

                translatex_curve = fbx_joint.LclTranslation.GetCurve(fbx_anim_layer, 'X', True);
                translatey_curve = fbx_joint.LclTranslation.GetCurve(fbx_anim_layer, 'Y', True);
                translatez_curve = fbx_joint.LclTranslation.GetCurve(fbx_anim_layer, 'Z', True);

                scalex_curve = fbx_joint.LclScaling.GetCurve(fbx_anim_layer, 'X', True);
                scaley_curve = fbx_joint.LclScaling.GetCurve(fbx_anim_layer, 'Y', True);
                scalez_curve = fbx_joint.LclScaling.GetCurve(fbx_anim_layer, 'Z', True);

                rotatex_curve = fbx_joint.LclRotation.GetCurve(fbx_anim_layer, 'X', True);
                rotatey_curve = fbx_joint.LclRotation.GetCurve(fbx_anim_layer, 'Y', True);
                rotatez_curve = fbx_joint.LclRotation.GetCurve(fbx_anim_layer, 'Z', True);

                for frame in range(1, frame_range+1, 1):
                    track.poses[frame-1] = pose = pyRitoFile.anm.ANMPose()
                    time = frame / fps
                    fbx_time.SetSecondDouble(time)
                    
                    translate = FbxVector4(
                        translatex_curve.Evaluate(fbx_time)[0],
                        translatey_curve.Evaluate(fbx_time)[0],
                        translatez_curve.Evaluate(fbx_time)[0]
                    )
                    rotate = FbxVector4(
                        rotatex_curve.Evaluate(fbx_time)[0], 
                        rotatey_curve.Evaluate(fbx_time)[0],
                        rotatez_curve.Evaluate(fbx_time)[0]
                    )
                    scale_x = scalex_curve.Evaluate(fbx_time)[0]
                    scale_y = scaley_curve.Evaluate(fbx_time)[0]
                    scale_z = scalez_curve.Evaluate(fbx_time)[0]
                    if scale_x == 0.0:
                        scale_x = 0.000001
                    if scale_y == 0.0:
                        scale_y = 0.000001
                    if scale_z == 0.0:
                        scale_z = 0.000001
                    scale = FbxVector4(scale_x, scale_y, scale_z)   
                    fbx_local_matrix = FbxAMatrix()
                    fbx_local_matrix.SetTRS(translate, rotate, scale)
                    if parent_is_blender_armature_node:
                        fbx_local_matrix = fbx_local_matrix * blender_armature_node_local_matrix
                    translate, rotate, scale = fbx_local_matrix.GetT(), fbx_local_matrix.GetQ(), fbx_local_matrix.GetS()
                    pose.translate = pyRitoFile.structs.Vector(translate[0], translate[1], translate[2])
                    pose.rotate = pyRitoFile.structs.Quaternion(rotate[0], rotate[1], rotate[2], rotate[3])
                    pose.scale = pyRitoFile.structs.Vector(scale[0], scale[1], scale[2])

                tracks.append(track)

            anm = pyRitoFile.anm.ANM()
            anm.fps = fps
            anm.duration = frame_range
            anm.tracks = tracks
            anms[fbx_anim_stack_name] = anm
            print(f'lemon_fbx: Finish: Dump ANM: Animation stack: {fbx_anim_stack_name}, Frame: {frame_range}, FPS: {fps}')
        return anms       
