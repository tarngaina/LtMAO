from maya.OpenMaya import *
from .....pyRitoFile.structs import Vector, Quaternion

def ensure_path_extension(path, ext):
    if not path.endswith(ext):
        path += f'.{ext}'
    return path

def mirrorX(skn=None, skl=None, anm=None, so=None, mapgeo=None):
    if skn != None:
        for vertex in skn.vertices:
            vertex.position.x = -vertex.position.x
            if vertex.normal != None:
                vertex.normal.y = -vertex.normal.y
                vertex.normal.z = -vertex.normal.z
    if skl != None:
        for joint in skl.joints:
            joint.local_translate.x = -joint.local_translate.x
            joint.local_rotate.y = -joint.local_rotate.y
            joint.local_rotate.z = -joint.local_rotate.z
            joint.ibind_translate.x = -joint.ibind_translate.x
            joint.ibind_rotate.y = -joint.ibind_rotate.y
            joint.ibind_rotate.z = -joint.ibind_rotate.z
    if anm != None:
        for track in anm.tracks:
            for time in track.poses:
                pose = track.poses[time]
                if pose.translation != None:
                    pose.translation.x = -pose.translation.x
                if pose.rotation != None:
                    pose.rotation.y = -pose.rotation.y
                    pose.rotation.z = -pose.rotation.z
    if so != None:
        for vertex in so.vertices:
            vertex.x = -vertex.x
        so.central.x = -so.central.x
        if so.pivot != None:
            so.pivot.x = -so.pivot.x



class MayaTransform:

    @staticmethod
    def decompose(transform, space):
        # get translation, scale and rotation (quaternion) out of transformation matrix
        translate = transform.getTranslation(space)

        rotate = transform.rotation()

        util = MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        transform.getScale(ptr, space)

        return (
            Vector(
                translate.x, translate.y, translate.z
            ),
            Quaternion(
                rotate.x,
                rotate.y,
                rotate.z,
                rotate.w
            ),
            Vector(
                util.getDoubleArrayItem(ptr, 0),
                util.getDoubleArrayItem(ptr, 1),
                util.getDoubleArrayItem(ptr, 2)
            )
        )

    @staticmethod
    def compose(translate, rotate, scale, space):
        # set translation, scale and rotation (quaternion) into a transformation matrix
        transform = MTransformationMatrix()

        # translation
        transform.setTranslation(
            MVector(translate.x, translate.y, translate.z), space)
        
        # easy rotation (quaternion)
        transform.setRotationQuaternion(
            rotate.x, rotate.y, rotate.z, rotate.w, space)

        # cursed scale
        util = MScriptUtil()
        util.createFromDouble(scale.x, scale.y, scale.z)
        ptr = util.asDoublePtr()
        transform.setScale(ptr, space)

        return transform