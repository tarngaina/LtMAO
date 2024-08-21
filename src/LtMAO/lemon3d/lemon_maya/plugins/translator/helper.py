from maya.OpenMaya import *
from maya import cmds

from random import choice
from ..... import pyRitoFile
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

# compose and decompose transformation matrix
class MayaTransformMatrix:
    
    @staticmethod
    def decompose(matrix, space):
        # get translation, scale and rotation (quaternion) out of transformation matrix
        translate = matrix.getTranslation(space)

        rotate = matrix.rotation()

        util = MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        matrix.getScale(ptr, space)

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
        matrix = MTransformationMatrix()

        # translation
        matrix.setTranslation(
            MVector(translate.x, translate.y, translate.z), space)
        
        # easy rotation (quaternion)
        matrix.setRotationQuaternion(
            rotate.x, rotate.y, rotate.z, rotate.w, space)

        # cursed scale
        util = MScriptUtil()
        util.createFromDouble(scale.x, scale.y, scale.z)
        ptr = util.asDoublePtr()
        matrix.setScale(ptr, space)

        return matrix

# get all joints, meshes of a selected group node
class MIterator:
    cached_result = []

    @staticmethod
    def reset():
        MIterator.cached_result = []

    @staticmethod
    def iter_node(node, type):
        for i in range(node.childCount()):
            child = node.child(i)
            if child.apiType() == type:
                MIterator.cached_result.append(child)
                child_dagpath = MDagPath()
                MDagPath.getAPathTo(child, child_dagpath)
                MIterator.iter_node(child_dagpath, type)

    @staticmethod
    def list_all_joints(group):
        MIterator.reset()
        MIterator.iter_node(group, MFn.kJoint)
        return MIterator.cached_result
    
    @staticmethod
    def list_all_meshes(group):
        result = []
        for i in range(group.childCount()):
            child = group.child(i)
            if child.apiType() == MFn.kTransform:
                transform = MFnTransform(child)
                if transform.childCount() > 0:
                    grandchild = transform.child(0)
                    if grandchild.apiType() == MFn.kMesh:
                        result.append(grandchild)
        return result

# error dialog
class FunnyError(Exception):

    def __init__(self, text):
        self.show(text)

    def show(self, text):
        temp = text.split(':')
        title = temp[0]
        message = ':'.join(temp[1:])
        button = choice([
            'UwU', '<(\")', 'ok boomer', 'funny man', 'jesus', 'bruh', 'bro', 'please', 'man',
            'stop', 'get some help', 'haha', 'lmao', 'ay yo', 'SUS', 'sOcIEtY.', 'yeah', 'whatever',
            'gurl', 'fck', 'im ded', '(~`u`)~', 't(^u^t)', '(>w<)', 'xdd', 'cluegi', 'kappachungusdeluxe'
        ])
        cmds.confirmDialog(
            title=title,
            message=message,
            button=button,
            icon='critical',
            defaultButton=button
        )

# inheritance pyRitoFile classes to set custom attribute
class LemonSKLJoint(pyRitoFile.SKLJoint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dagpath = None

class LemonSKNVertex(pyRitoFile.SKNVertex):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uv_index = None
        self.new_index = None

class LemonSKNSubmesh(pyRitoFile.SKNSubmesh):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indices = []
        self.vertices = []