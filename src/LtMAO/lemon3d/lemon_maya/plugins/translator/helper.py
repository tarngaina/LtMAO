from maya.OpenMaya import *
from maya import cmds

import os.path, traceback, random
from ..... import lepath, pyRitoFile

def try_cmd(cmd):
    try:
        cmd()
        return True
    except Exception as e:
        print(traceback.format_exc())
        raise e

def get_option_key_name(key):
    return 'lemon3d_'+key

def get_name_from_path(path):
    name = os.path.basename(path).split('.')[0]
    if name[0] in '0123456789': # does not allow name start with number
        name = 'lemon_' + name
    return name

def get_riot_path(path):
    # check riot path
    ext = os.path.basename(path).split('.')[-1]
    riot_path = lepath.join(
        os.path.dirname(path), 
        f'riot_{os.path.basename(path)}'
    )
    if not os.path.exists(riot_path):
        riot_path = lepath.join(
            os.path.dirname(path),
            f'riot.{ext}'
        )
        if not os.path.exists(riot_path):
            riot_path = ''
    return riot_path

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
                if pose.translate != None:
                    pose.translate.x = -pose.translate.x
                if pose.rotate != None:
                    pose.rotate.y = -pose.rotate.y
                    pose.rotate.z = -pose.rotate.z
    if so != None:
        for position in so.positions:
            position.x = -position.x
        so.central.x = -so.central.x
        if so.pivot != None:
            so.pivot.x = -so.pivot.x
    if mapgeo != None:
        for model in mapgeo.models:
            # flip matrix 
            matrix = MMatrix()
            MScriptUtil.createMatrixFromList([value for value in model.matrix], matrix)
            translate, rotate, scale = MayaTransformMatrix.decompose(MTransformationMatrix(matrix), MSpace.kWorld)
            translate.x = -translate.x
            rotate.y = -rotate.y
            rotate.z = -rotate.z
            matrix = MayaTransformMatrix.compose(translate, rotate, scale, MSpace.kWorld).asMatrix()
            model.matrix = pyRitoFile.structs.Matrix4(*[matrix(i, j) for i in range(4) for j in range(4)]) 
            # flip vertex
            for vertex in model.vertices:
                if pyRitoFile.mapgeo.MAPGEOVertexElementName.Position in vertex.value:
                    position = vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Position]
                    position.x = -position.x
                if pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord5 in vertex.value:
                    bush_vertex_animation = vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Texcoord5]
                    bush_vertex_animation.x = -bush_vertex_animation.x
                if pyRitoFile.mapgeo.MAPGEOVertexElementName.Normal in vertex.value:
                    normal = vertex.value[pyRitoFile.mapgeo.MAPGEOVertexElementName.Normal]
                    normal.y = -normal.y
                    normal.z = -normal.z

# compose and decompose transformation matrix
class MayaTransformMatrix:
    
    @staticmethod
    def decompose(matrix, space):
        # get translate, scale and rotate (quaternion) out of transformation matrix
        translate = matrix.getTranslation(space)

        rotate = matrix.rotation()

        util = MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        matrix.getScale(ptr, space)

        return (
            pyRitoFile.structs.Vector(
                translate.x, translate.y, translate.z
            ),
            pyRitoFile.structs.Quaternion(
                rotate.x,
                rotate.y,
                rotate.z,
                rotate.w
            ),
            pyRitoFile.structs.Vector(
                util.getDoubleArrayItem(ptr, 0),
                util.getDoubleArrayItem(ptr, 1),
                util.getDoubleArrayItem(ptr, 2)
            )
        )

    @staticmethod
    def compose(translate, rotate, scale, space):
        # set translate, scale and rotate (quaternion) into a transformation matrix
        matrix = MTransformationMatrix()

        # translate
        matrix.setTranslation(
            MVector(translate.x, translate.y, translate.z), space)
        
        # easy rotate (quaternion)
        matrix.setRotationQuaternion(
            rotate.x, rotate.y, rotate.z, rotate.w, space)

        # cursed scale
        util = MScriptUtil()
        util.createFromDouble(scale.x, scale.y, scale.z)
        ptr = util.asDoublePtr()
        matrix.setScale(ptr, space)

        return matrix

# error dialog
class FunnyError(Exception):

    def __init__(self, text):
        self.show(text)

    def show(self, text):
        temp = text.split(':')
        title = temp[0]
        message = ':'.join(temp[1:])
        button = random.choice([
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

# pyRitoFile -> Lemon
def convert_pyRitoFile_objects_to_Lemon(pyritofile_objects, lemon_class):
    return [lemon_class(**{key: getattr(pyritofile_object, key) for key in pyritofile_object.__slots__}) for pyritofile_object in pyritofile_objects]

class LemonSKLJoint(pyRitoFile.skl.SKLJoint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dagpath = None

class LemonSKNVertex(pyRitoFile.skn.SKNVertex):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uv_index = None
        self.new_index = None

class LemonSKNSubmesh(pyRitoFile.skn.SKNSubmesh):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indices = []
        self.vertices = []

class LemonANMTrack(pyRitoFile.anm.ANMTrack):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.joint_name = None
        self.ik_joint = None
        self.curve_times = {}
        self.curve_values = {}

class LemonMAPGEOVertex(pyRitoFile.mapgeo.MAPGEOVertex):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uv_index = None