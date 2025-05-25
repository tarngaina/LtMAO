from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

from . import helper
from ..... import pyRitoFile


class ANMImporter(MPxFileTranslator):
    name = 'League of Legends: ANM'
    extension = 'anm'

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
            # import options
            anm_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
            # read anm
            anm = pyRitoFile.anm.ANM().read(anm_path)
            anm.tracks = helper.convert_pyRitoFile_objects_to_Lemon(anm.tracks, helper.LemonANMTrack)
            # load anm
            helper.mirrorX(anm=anm)
            load_options = {
                'reset_channel': False if 'reset_channel=0' in options else True
            }
            ANM.scene_load(anm, load_options)
            return True
    
        return helper.try_cmd(lambda: read_cmd(file, options, access))

class ANMExporter(MPxFileTranslator):
    name = 'League of Legends: ANM Export'
    extension = 'anm'

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
            # export options
            anm_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
            anm = pyRitoFile.anm.ANM()
            ANM.scene_dump(anm, {})
            helper.mirrorX(anm=anm)
            anm.write(anm_path)
            return True

        return helper.try_cmd(lambda: write_cmd(file, options, access))


class ANM:
    @staticmethod
    def scene_load(anm, load_options):
        # ensure scene fps
        if anm.fps > 59:
            MTime.setUIUnit(MTime.kNTSCField)
        else:
            MTime.setUIUnit(MTime.kNTSCFrame)

        ui_unit = MTime.uiUnit()
        time0 = MTime(0.0, ui_unit)

        # get current time
        current = MAnimControl.currentTime().value()

        # reset channel
        if load_options['reset_channel']:
            cmds.delete(all=True, channels=True)
            cmds.currentTime(0)
            current = 0.0  # reset current

        # ensure animation range
        end = anm.duration 
        MAnimControl.setMinMaxTime(time0, MTime(current+end, ui_unit))
        MAnimControl.setAnimationStartEndTime(
            time0, MTime(current+end, ui_unit))
        MAnimControl.setPlaybackSpeed(1.0)

        # file's joints that found in scene
        scene_tracks = []
        # attribute name for getting curve
        attributes = [
            'tx', 'ty', 'tz',
            'rx', 'ry', 'rz',
            'sx', 'sy', 'sz'
        ]
        # loop through all ik joint in scenes
        iterator = MItDag(MItDag.kDepthFirst, MFn.kJoint)
        dagpath = MDagPath()
        while not iterator.isDone():
            iterator.getPath(dagpath)
            ik_joint = MFnIkJoint(dagpath)
            joint_name = ik_joint.name()

            # find file's joints that match this scene's joint's name
            match_track = next(
                (track for track in anm.tracks if track.joint_hash == pyRitoFile.helper.Elf(joint_name)), None)
            if match_track != None:
                match_track.joint_name = joint_name
                match_track.ik_joint = ik_joint
                for attr in attributes:
                    match_track.curve_times[attr] = MTimeArray()
                    match_track.curve_values[attr] = MDoubleArray()
                scene_tracks.append(match_track)
            iterator.next()

        if len(scene_tracks) == 0:
            raise helper.FunnyError(
                'ANM Importer: No matched joints found in scene, please import SKL first before import ANM.')

        # bind current pose to frame 0 - very helpful if its bind pose
        # this also create the curves so dont need to call MFnAnimCurve.create()
        joint_names = [track.joint_name for track in scene_tracks]
        cmds.currentTime(0)
        cmds.setKeyframe(
            joint_names,
            breakdown=False,
            hierarchy='none',
            controlPoints=False,
            shape=False,
            attribute=('translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ')
        )

        # get global times
        times = []
        for track in scene_tracks:
            for time in track.poses:
                if time not in times:
                    times.append(time)
        # fill gloal times
        for track in scene_tracks:
            for time in times:
                if time not in track.poses:
                    track.poses[time] = None
        # MTime instance at time  (dict comp)
        mtimes = {time: MTime(current + time + 1, ui_unit)
                  for time in times}

        # build curve data
        for time in times:
            for track in scene_tracks:
                pose = track.poses[time]
                if pose != None:
                    mtime = mtimes[time]
                    if pose.translate != None:
                        track.curve_times['tx'].append(mtime)
                        track.curve_values['tx'].append(pose.translate.x)
                        track.curve_times['ty'].append(mtime)
                        track.curve_values['ty'].append(pose.translate.y)
                        track.curve_times['tz'].append(mtime)
                        track.curve_values['tz'].append(pose.translate.z)

                    if pose.rotate != None:
                        euler = MQuaternion(
                            pose.rotate.x, pose.rotate.y, pose.rotate.z, pose.rotate.w
                        ).asEulerRotation()
                        track.curve_times['rx'].append(mtime)
                        track.curve_values['rx'].append(euler.x)
                        track.curve_times['ry'].append(mtime)
                        track.curve_values['ry'].append(euler.y)
                        track.curve_times['rz'].append(mtime)
                        track.curve_values['rz'].append(euler.z)

                    if pose.scale != None:
                        track.curve_times['sx'].append(mtime)
                        track.curve_values['sx'].append(pose.scale.x)
                        track.curve_times['sy'].append(mtime)
                        track.curve_values['sy'].append(pose.scale.y)
                        track.curve_times['sz'].append(mtime)
                        track.curve_values['sz'].append(pose.scale.z)

        # set keys on curve
        for track in scene_tracks:
            joint_node = track.ik_joint.object()
            dep = MFnDependencyNode(joint_node)

            for attr in attributes:
                # plug=node.attribute: example: tx_plug=Root.tX
                attr_plug = dep.findPlug(attr)
                # get/create curve for this attribute
                MFnAnimCurve(attr_plug).addKeys(
                    track.curve_times[attr],
                    track.curve_values[attr]
                )

        # get all rotaion curves
        track_rotate_curves = []
        for track in scene_tracks:
            track_rotate_curves += [f'{track.joint_name}.rotateX', f'{track.joint_name}.rotateY', f'{track.joint_name}.rotateZ']
        # quat slerp all rotation curve
        cmds.rotationInterpolation(
            track_rotate_curves,
            convert='quaternionSlerp'
        )
        if not load_options['reset_channel']:
            # if continous animation, quat slerp will break next anm so we roll back
            cmds.rotationInterpolation(
                track_rotate_curves,
                convert='none'
            )
        MAnimControl.setCurrentTime(MAnimControl.animationEndTime())

    @staticmethod
    def scene_dump(anm, dump_options):
        # get joint in scene
        anm.tracks = []
        iterator = MItDag(MItDag.kDepthFirst, MFn.kJoint)
        dagpath = MDagPath()
        while not iterator.isDone():
            # dag path
            iterator.getPath(dagpath)

            # track data
            track = helper.LemonANMTrack()
            track.ik_joint = MFnIkJoint(dagpath)
            track.joint_name = track.ik_joint.name()
            track.joint_hash = pyRitoFile.helper.Elf(track.joint_name)
            track.poses = {}
            anm.tracks.append(track)

            iterator.next()

        # dump fps
        ui_unit = MTime.uiUnit()
        fps = MTime(1, MTime.kSeconds).asUnits(ui_unit)
        anm.fps = 60.0 if fps > 59 else 30.0

        # dump from frame 1 to frame end
        # if its not then well, its the ppl fault, not mine. haha suckers
        start = int(MAnimControl.animationStartTime().value())
        end = int(MAnimControl.animationEndTime().value())
        anm.duration = abs(end-start)

        for frame in range(anm.duration):
            MAnimControl.setCurrentTime(MTime(start+1+frame, ui_unit))
            for track in anm.tracks:

                pose = pyRitoFile.anm.ANMPose()
                # translate
                translate = track.ik_joint.getTranslation(MSpace.kTransform)
                pose.translate = pyRitoFile.structs.Vector(
                    translate.x, translate.y, translate.z)
                # scale
                util = MScriptUtil()
                util.createFromDouble(0.0, 0.0, 0.0)
                ptr = util.asDoublePtr()
                track.ik_joint.getScale(ptr)
                pose.scale = pyRitoFile.structs.Vector(
                    util.getDoubleArrayItem(ptr, 0),
                    util.getDoubleArrayItem(ptr, 1),
                    util.getDoubleArrayItem(ptr, 2)
                )
                # rotate
                orient = MQuaternion()
                track.ik_joint.getOrientation(orient)
                axe = track.ik_joint.rotateOrientation(MSpace.kTransform)
                rotate = MQuaternion()
                track.ik_joint.getRotation(rotate, MSpace.kTransform)
                rotate = axe * rotate * orient
                pose.rotate = pyRitoFile.structs.Quaternion(
                    rotate.x, rotate.y, rotate.z, rotate.w)
                track.poses[frame] = pose