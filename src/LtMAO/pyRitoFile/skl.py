from LtMAO.prettyUI.helper import Log
from LtMAO.pyRitoFile.io import BinStream


class SKLJoint:
    def __init__(self):
        self.flags = None
        self.id = None
        self.parent = None
        self.hash = None
        self.radius = None
        self.local_translate = None
        self.local_rotate = None
        self.local_scale = None
        self.ibind_translate = None
        self.ibind_rotate = None
        self.ibind_scale = None
        self.name = None


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

    def read(self, path):
        Log.add(f'Running: Read {path}')

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
                # unknown
                self.flags, = bs.read_u16()
                # counts
                joint_count, = bs.read_u16()
                influence_count, = bs.read_u32()
                # offsets
                joints_offset, joint_ids_offset, influences_offset, name_offset, asset_offset, bones_names_offset, = bs.read_i32(
                    6)
                # reserved offset
                bs.pad(32)

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
                        joint.radius, bs.read_f()
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
                if name_offset:
                    self.name, = bs.read_c_until0()
                if asset_offset:
                    self.asset, = bs.read_c_until0()
            else:
                self.signature, = bs.read_a(8)
                if self.signature != 'r3d2sklt':
                    raise Exception(
                        f'Failed: Read {path}: Wrong file signature: {self.signature}')

                self.version, = bs.read_uint32()
                if self.version not in (1, 2):
                    raise Exception(
                        f'Failed: Read {path}: Unsupported file version: {self.version}')

                # skeleton id
                self.id, = bs.read_u32()

                joint_count, = bs.read_u32()
                self.joints = [SKLJoint() for i in range(joint_count)]
                for i in range(joint_count):
                    joint = self.joints[i]

                    joint.name, = bs.read_a_padded(32)
                    joint.parent, = bs.read_i32()
                    joint.radius, = bs.read_f()
                    joint.global_matrix = [0.0]*16
                    for c in range(3):
                        for r in range(4):
                            joint.global_matrix[r*4+c], = bs.read_f()
                    joint.global_matrix[15] = 1.0

                # read influences
                if self.version == 1:
                    self.influences = list(range(joint_count))

                if self.version == 2:
                    influence_count, = bs.read_u32()
                    self.influences = bs.read_u32(influence_count)

        Log.add(f'Done: Read {path}')
