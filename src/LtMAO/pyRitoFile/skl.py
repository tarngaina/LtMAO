from io import BytesIO
from .stream import BinStream
from ..pyRitoFile.structs import Matrix4
from .ermmm import Elf, FNV1a


def bin_hash(name):
    return f'{FNV1a(name):08x}'


class SKLJoint:
    __slots__ = (
        'id', 'name', 'bin_hash', 'parent', 'hash', 'radius', 'flags',
        'local_translate', 'local_rotate', 'local_scale',
        'ibind_translate', 'ibind_rotate', 'ibind_scale'
    )

    def __init__(self, id=None, name=None, bin_hash=None, parent=None, hash=None, radius=None, flags=None, local_translate=None, local_rotate=None, local_scale=None, ibind_translate=None, ibind_rotate=None, ibind_scale=None):
        self.id = id
        self.name = name
        self.bin_hash = bin_hash
        self.parent = parent
        self.hash = hash
        self.radius = radius
        self.flags = flags
        self.local_translate = local_translate
        self.local_rotate = local_rotate
        self.local_scale = local_scale
        self.ibind_translate = ibind_translate
        self.ibind_rotate = ibind_rotate
        self.ibind_scale = ibind_scale

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class SKL:
    __slots__ = (
        'file_size', 'signature', 'version', 'flags',
        'name', 'asset', 'joints', 'influences'
    )

    def __init__(self, file_size=None, signature=None, version=None, flags=None, name=None, asset=None, joints=None, influences=None):
        self.file_size = file_size
        self.signature = signature
        self.version = version
        self.flags = flags
        self.name = name
        self.asset = asset
        self.joints = joints
        self.influences = influences

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def stream(self, path, mode, raw=None):
        if raw != None:
            if raw == True:  # the bool True value
                return BinStream(BytesIO())
            else:
                return BinStream(BytesIO(raw))
        return BinStream(open(path, mode))

    def read(self, path, raw=None):
        with self.stream(path, 'rb', raw) as bs:
            # read signature first to check legacy or not
            bs.pad(4)
            signature, = bs.read_u32()
            bs.seek(0)

            if signature == 0x22FD4FC3:
                # new skl data
                self.file_size, self.signature, self.version, = bs.read_u32(
                    3)
                if self.version != 0:
                    raise Exception(
                        f'pyRitoFile: Failed: Read SKL {path}: Unsupported file version: {self.version}')
                self.signature = hex(self.signature)
                # unknown
                self.flags, = bs.read_u16()
                # counts
                joint_count, = bs.read_u16()
                influence_count, = bs.read_u32()
                # offsets
                joints_offset, _, influences_offset, name_offset, asset_offset, _, = bs.read_i32(
                    6)
                # pad empty
                bs.pad(20)

                # read joints
                if joints_offset > 0 and joint_count > 0:
                    bs.seek(joints_offset)
                    self.joints = [SKLJoint() for i in range(joint_count)]
                    for joint in self.joints:
                        joint.flags, = bs.read_u16()
                        joint.id, joint.parent, = bs.read_i16(2)
                        bs.pad(2)  # pad
                        joint.hash, = bs.read_u32()
                        joint.radius, = bs.read_f32()
                        joint.local_translate, = bs.read_vec3()
                        joint.local_scale, = bs.read_vec3()
                        joint.local_rotate, = bs.read_quat()

                        joint.ibind_translate, = bs.read_vec3()
                        joint.ibind_scale, = bs.read_vec3()
                        joint.ibind_rotate, = bs.read_quat()
                        # name
                        joint_name_offset, = bs.read_i32()
                        return_offset = bs.tell()
                        bs.seek(return_offset-4 + joint_name_offset)
                        joint.name, = bs.read_c_until0()
                        joint.bin_hash = bin_hash(joint.name)
                        bs.seek(return_offset)

                # read influences
                if influences_offset > 0 and influence_count > 0:
                    bs.seek(influences_offset)
                    self.influences = bs.read_u16(influence_count)
                # name and asset string
                if name_offset > 0:
                    self.name, = bs.read_c_until0()
                if asset_offset > 0:
                    self.asset, = bs.read_c_until0()
            else:
                self.signature, = bs.read_s(8)
                if self.signature != 'r3d2sklt':
                    raise Exception(
                        f'pyRitoFile: Failed: Read SKL {path}: Wrong file signature: {self.signature}')

                self.version, = bs.read_u32()
                if self.version not in (1, 2):
                    raise Exception(
                        f'pyRitoFile: Failed: Read SKL {path}: Unsupported file version: {self.version}')

                # skeleton id
                skeleton_id, = bs.read_u32()

                joint_count, = bs.read_u32()
                self.joints = [SKLJoint() for i in range(joint_count)]
                old_matrices = [None] * joint_count
                for joint_id, joint in enumerate(self.joints):
                    joint.name, = bs.read_s_padded(32)
                    joint.bin_hash = bin_hash(joint.name)
                    joint.id = joint_id
                    joint.hash = Elf(joint.name)
                    joint.parent, = bs.read_i32()
                    joint.radius, = bs.read_f32()
                    floats = [0.0]*16
                    for c in range(3):
                        for r in range(4):
                            floats[r*4+c], = bs.read_f32()
                    floats[15] = 1.0
                    old_matrices[joint_id] = Matrix4(*floats)

                # old matrix to local translation, ibind rotation
                for joint_id, joint in enumerate(self.joints):
                    local = old_matrices[joint_id] if joint.parent == - \
                        1 else old_matrices[joint_id] * old_matrices[joint.parent].inverse()
                    joint.local_translate, joint.local_rotate, joint.local_scale = local.decompose()
                    ibind = old_matrices[joint_id].inverse()
                    joint.ibind_translate, joint.ibind_rotate, joint.ibind_scale = ibind.decompose()

                # read influences
                if self.version == 1:
                    self.influences = list(range(joint_count))

                if self.version == 2:
                    influence_count, = bs.read_u32()
                    self.influences = bs.read_u32(influence_count)

    def write(self, path, raw=None):
        with self.stream(path, 'wb', raw) as bs:
            # file size, magic, version
            bs.write_u32(0, 0x22FD4FC3, 0)

            joint_count = len(self.joints)
            bs.write_u16(0)  # flags
            bs.write_u16(joint_count)
            bs.write_u32(joint_count)

            joints_offset = 64
            joint_indices_offset = joints_offset + joint_count * 100
            influences_offset = joint_indices_offset + joint_count * 8
            joint_names_offset = influences_offset + joint_count * 2

            bs.write_i32(
                joints_offset,
                joint_indices_offset,
                influences_offset,
                0,  # name offset
                0,  # asset offset
                joint_names_offset
            )

            bs.write_u32(0xFFFFFFFF, 0xFFFFFFFF,
                         0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF)

            joint_offset = [None] * joint_count
            bs.seek(joint_names_offset)
            for i in range(joint_count):
                joint_offset[i] = bs.tell()
                bs.write_s(self.joints[i].name)
                bs.write_b(0)

            bs.seek(joints_offset)
            for joint_id, joint in enumerate(self.joints):
                bs.write_u16(0, joint_id)  # flags + id
                bs.write_i16(joint.parent)  # -1, cant be uint
                bs.write_u16(0)  # pad
                bs.write_u32(joint.hash)
                bs.write_f32(joint.radius)

                # local
                bs.write_vec3(joint.local_translate)
                bs.write_vec3(joint.local_scale)
                bs.write_quat(joint.local_rotate)

                # inversed bind
                bs.write_vec3(joint.ibind_translate)
                bs.write_vec3(joint.ibind_scale)
                bs.write_quat(joint.ibind_rotate)

                bs.write_u32(joint_offset[joint_id] - bs.tell())

            # influences
            bs.seek(influences_offset)
            bs.write_u16(*[i for i in range(joint_count)])

            # joint indices
            bs.seek(joint_indices_offset)
            for i in range(joint_count):
                bs.write_u16(i)
                bs.write_u16(0)  # pad
                bs.write_u32(joint.hash)

            # file size
            bs.seek(0)
            bs.write_u32(bs.end())
            return bs.raw() if raw else None
