from LtMAO.pyRitoFile.io import BinStream
from LtMAO.pyRitoFile.structs import Matrix4
from LtMAO.pyRitoFile.hash import Elf
from json import JSONEncoder


class SKLEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        else:
            return JSONEncoder.default(self, obj)


class SKLJoint:
    def __init__(self):
        self.id = None
        self.name = None
        self.bin_hash = None
        self.parent = None
        self.hash = None
        self.radius = None
        self.flags = None
        self.local_translate = None
        self.local_rotate = None
        self.local_scale = None
        self.ibind_translate = None
        self.ibind_rotate = None
        self.ibind_scale = None

    def __json__(self):
        return vars(self)


class SKL:
    def __init__(self):
        self.file_size = None
        self.signature = None
        self.version = None
        self.flags = None
        self.name = None
        self.asset = None
        self.joints = []
        self.influences = []

    def __json__(self):
        return vars(self)

    def read(self, path):
        with open(path, 'rb') as f:
            bs = BinStream(f)

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
                        f'Failed: Read {path}: Unsupported file version: {self.version}')
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
                    for i in range(joint_count):
                        joint = self.joints[i]

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
                self.signature, = bs.read_a(8)
                if self.signature != 'r3d2sklt':
                    raise Exception(
                        f'Failed: Read {path}: Wrong file signature: {self.signature}')

                self.version, = bs.read_u32()
                if self.version not in (1, 2):
                    raise Exception(
                        f'Failed: Read {path}: Unsupported file version: {self.version}')

                # skeleton id
                self.id, = bs.read_u32()

                joint_count, = bs.read_u32()
                self.joints = [SKLJoint() for i in range(joint_count)]
                old_matrices = [None] * joint_count
                for i in range(joint_count):
                    joint = self.joints[i]

                    joint.name, = bs.read_a_padded(32)
                    joint.id = i
                    joint.hash = Elf(joint.name)
                    joint.parent, = bs.read_i32()
                    joint.radius, = bs.read_f32()
                    floats = [0.0]*16
                    for c in range(3):
                        for r in range(4):
                            floats[r*4+c], = bs.read_f32()
                    floats[15] = 1.0
                    old_matrices[i] = Matrix4(*floats)

                # old matrix to local translation, ibind rotation
                for i in range(joint_count):
                    joint = self.joints[i]
                    ibind = old_matrices[i].inverse()
                    local = old_matrices[i] if joint.parent == - \
                        1 else old_matrices[i] * ibind
                    joint.local_translate, joint.local_rotate, joint.local_scale = local.decompose()
                    joint.ibind_translate, joint.ibind_rotate, joint.ibind_scale = ibind.decompose()

                # read influences
                if self.version == 1:
                    self.influences = list(range(joint_count))

                if self.version == 2:
                    influence_count, = bs.read_u32()
                    self.influences = bs.read_u32(influence_count)

    def write(self, path):
        with open(path, 'wb') as f:
            bs = BinStream(f)

            # file size, magic, version
            bs.write_u32(0, 0x22FD4FC3, 0)

            joint_count = len(self.joints)
            influence_count = len(self.influences)
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
                bs.write_a(self.joints[i].name)
                bs.write_b(0)

            bs.seek(joints_offset)
            for i in range(joint_count):
                joint = self.joints[i]

                bs.write_u16(0, i)  # flags + id
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

                bs.write_u32(joint_offset[i] - bs.tell())

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
