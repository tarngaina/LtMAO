from LtMAO.utils.bin_io import BinIO
from LtMAO.utils import Hash


class SKLJoint:
    __slots__ = (
        'name', 'parent'
    )

    def __init__(self):
        self.name = None
        self.parent = None


class SKL:
    def __init__(self):
        self.joints = []
        self.influences = []

    def read(self, path):
        with open(path, 'rb') as f:
            bs = BinaryStream(f)

            bs.pad(4)  # resource size
            magic = bs.read_uint32()
            if magic == 0x22FD4FC3:
                # new skl data
                version = bs.read_uint32()
                if version != 0:
                    raise Exception(
                        f'[SKL.read()]: Unsupported file version: {version}')

                bs.pad(2)  # flags
                joint_count = bs.read_uint16()
                influence_count = bs.read_uint32()
                joints_offset = bs.read_int32()
                bs.pad(4)  # joint indices offset
                influences_offset = bs.read_int32()
                # name offset, asset name offset, joint names offset, 5 reserved offset
                bs.pad(32)

                # read joints
                if joints_offset > 0 and joint_count > 0:
                    bs.seek(joints_offset)
                    self.joints = [SKLJoint() for i in range(joint_count)]
                    for i in range(joint_count):
                        joint = self.joints[i]

                        bs.pad(4)  # flags and id
                        joint.parent = bs.read_int16()  # cant be uint
                        bs.pad(2)  # flags
                        joint_hash = bs.read_uint32()
                        bs.pad(4)  # radius

                        # local & iglobal translation, scale, rotation (quat)
                        bs.pad(80)

                        # name
                        joint_name_offset = bs.read_int32()
                        return_offset = bs.tell()
                        bs.seek(return_offset - 4 + joint_name_offset)
                        joint.name = bs.read_char_until_zero()

                        # skl convert 0.1 fix before return
                        # (2 empty bytes asset name override on first joint)
                        if i == 0 and joint.name == '':
                            # pad 1 more
                            bs.pad(1)
                            # read the rest
                            joint.name = bs.read_char_until_zero()

                            # brute force unhash 2 letters

                            table = '_abcdefighjklmnopqrstuvwxyz'
                            names = [
                                a+b+joint.name for a in table for b in table]
                            founds = [name.capitalize() for name in names if Hash.elf(
                                name) == joint_hash]
                            if len(founds) == 1:
                                joint.name = founds[0]
                            else:
                                msg = ' Sugest name: ' + \
                                    ', '.join(founds) if len(
                                        founds) > 1 else ''
                                print(
                                    f'[SKL.load()]: {joint.name} is a bad joint name, please rename it.{msg}')

                        bs.seek(return_offset)

                # read influences
                if influences_offset > 0 and influence_count > 0:
                    bs.seek(influences_offset)
                    self.influences = bs.read_uint16(influence_count, True)

                # i think that is all we need, reading joint_indices_offset, name and asset name doesnt help anything
            else:
                # legacy
                # because signature in old skl is first 8bytes
                # need to go back pos 0 to read 8bytes again
                bs.seek(0)

                magic = bs.read_ascii(8)
                if magic != 'r3d2sklt':
                    raise Exception(
                        f'[SKL.read()]: Wrong file signature: {magic}')

                version = bs.read_uint32()
                if version not in (1, 2):
                    raise Exception(
                        f'[SKL.read()]: Unsupported file version: {version}')

                bs.pad(4)  # designer id or skl id

                joint_count = bs.read_uint32()
                self.joints = [SKLJoint() for i in range(joint_count)]
                for i in range(joint_count):
                    joint = self.joints[i]

                    joint.name = bs.read_padded_ascii(32)
                    joint.parent = bs.read_int32()  # -1, cant be uint
                    bs.pad(4)  # radius/scale - pad
                    bs.pad(48)  # 12 float matrix

                # read influences
                if version == 1:
                    self.influences = list(range(joint_count))

                if version == 2:
                    influence_count = bs.read_uint32()
                    self.influences = bs.read_uint32(influence_count, True)
