from math import sqrt
from io import BytesIO
from ..pyRitoFile.io import BinStream
from ..pyRitoFile.structs import Quaternion, Vector
from ..pyRitoFile.hash import Elf


def decompress_quat(bytes):
    first = bytes[0] | (bytes[1] << 8)
    second = bytes[2] | (bytes[3] << 8)
    third = bytes[4] | (bytes[5] << 8)
    bits = first | second << 16 | third << 32
    max_index = (bits >> 45) & 3
    one_div_sqrt2 = 0.70710678118
    sqrt2_div_32767 = 0.00004315969
    a = ((bits >> 30) & 32767) * sqrt2_div_32767 - one_div_sqrt2
    b = ((bits >> 15) & 32767) * sqrt2_div_32767 - one_div_sqrt2
    c = (bits & 32767) * sqrt2_div_32767 - one_div_sqrt2
    d = sqrt(max(0.0, 1.0 - (a * a + b * b + c * c)))
    if max_index == 0:
        return Quaternion(d, a, b, c)
    elif max_index == 1:
        return Quaternion(a, d, b, c)
    elif max_index == 2:
        return Quaternion(a, b, d, c)
    else:
        return Quaternion(a, b, c, d)


def decompress_vec3(min, max, bytes):
    return Vector(
        (max.x - min.x) / 65535.0 * (bytes[0] | bytes[1] << 8) + min.x,
        (max.y - min.y) / 65535.0 * (bytes[2] | bytes[3] << 8) + min.y,
        (max.z - min.z) / 65535.0 * (bytes[4] | bytes[5] << 8) + min.z
    )


class ANMErrorMetric:
    __slots__ = (
        'margin', 'discontinuity_threshold'
    )

    def __init__(self):
        self.margin = None
        self.discontinuity_threshold = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class ANMPose:
    __slots__ = (
        'time', 'translate', 'scale', 'rotate'
    )

    def __init__(self):
        self.time = None
        self.translate = None
        self.scale = None
        self.rotate = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class ANMTrack:
    __slots__ = (
        'joint_hash', 'poses'
    )

    def __init__(self):
        self.joint_hash = None
        self.poses = []

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class ANM:
    __slots__ = (
        'signature', 'version', 'file_size', 'format_token', 'flags1', 'flags2',
        'duration', 'fps', 'error_metrics', 'tracks'
    )

    def __init__(self):
        self.signature = None
        self.version = None
        self.file_size = None
        self.format_token = None
        self.flags1 = None
        self.flags2 = None
        self.duration = None
        self.fps = None
        self.error_metrics = None
        self.tracks = []

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
            self.signature, = bs.read_a(8)
            self.version, = bs.read_u32()

            if self.signature == 'r3d2canm':
                # compressed
                # read header
                self.file_size, self.format_token, self.flags1 = bs.read_u32(3)
                joint_count, frame_count = bs.read_u32(2)
                bs.pad(4)  # jump cache count
                max_time, self.fps = bs.read_f32(2)
                self.duration = (max_time + 1) * self.fps
                # read error metrics
                self.error_metrics = {'rotate': ANMErrorMetric(
                ), 'translate': ANMErrorMetric(), 'scale': ANMErrorMetric()}
                self.error_metrics['rotate'].margin, self.error_metrics['rotate'].discontinuity_threshold = bs.read_f32(
                    2)
                self.error_metrics['translate'].margin, self.error_metrics['translate'].discontinuity_threshold = bs.read_f32(
                    2)
                self.error_metrics['scale'].margin, self.error_metrics['scale'].discontinuity_threshold = bs.read_f32(
                    2)
                translate_min, translate_max, scale_min, scale_max = bs.read_vec3(
                    4)
                # read offsets
                frames_offset,  _, joint_hashes_offset = bs.read_i32(3)
                if frames_offset <= 0:
                    raise Exception(
                        f'pyRitoFile: Failed: Read ANM: File does not contain frames.'
                    )
                if joint_hashes_offset <= 0:
                    raise Exception(
                        f'pyRitoFile: Failed: Read ANM: File does not contain joint hashes.'
                    )
                # read joint hashes
                bs.seek(joint_hashes_offset + 12)
                joint_hashes = bs.read_u32(joint_count)
                # create tracks
                self.tracks = [ANMTrack() for i in range(joint_count)]
                for track_id, track in enumerate(self.tracks):
                    track.joint_hash = joint_hashes[track_id]
                # read frames
                bs.seek(frames_offset + 12)
                for i in range(frame_count):
                    compressed_time, bits = bs.read_u16(2)
                    compressed_transform = bs.read(6)
                    # parse track
                    joint_hash = joint_hashes[bits & 16383]
                    match_track = None
                    for track in self.tracks:
                        if track.joint_hash == joint_hash:
                            match_track = track
                            break
                    if match_track == None:
                        # this frame has wrong joint hash?
                        continue
                    # parse pose
                    time = (compressed_time / 65535.0 *
                            max_time) * self.fps
                    match_pose = None
                    for pose in match_track.poses:
                        if pose.time == time:
                            match_pose = pose
                            break
                    if match_pose == None:
                        pose = ANMPose()
                        pose.time = time
                        track.poses.append(pose)
                    else:
                        pose = match_pose
                    # decompress pose data
                    transform_type = bits >> 14
                    if transform_type == 0:
                        pose.rotate = decompress_quat(
                            compressed_transform)
                    elif transform_type == 1:
                        pose.translate = decompress_vec3(
                            translate_min, translate_max, compressed_transform)
                    elif transform_type == 2:
                        pose.scale = decompress_vec3(
                            scale_min, scale_max, compressed_transform)
                    else:
                        raise Exception(
                            f'pyRitoFile: Failed: Read ANM: Unknown compressed transform type: {transform_type}.'
                        )
            elif self.signature == 'r3d2anmd':
                if self.version == 5:
                    # v5
                    # read headers
                    self.file_size, self.format_token, self.flags1, self.flags2 = bs.read_u32(
                        4)
                    track_count, frame_count = bs.read_u32(2)
                    self.fps = 1 / bs.read_f32()[0]  # frame duration
                    self.duration = frame_count
                    # read offsets and calculate stuffs
                    joint_hashes_offset, _, _, vecs_offset, quats_offset, frames_offset = bs.read_i32(
                        6)
                    if joint_hashes_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Failed: Read ANM: File does not contain joint hashes data.'
                        )
                    if vecs_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Failed: Read ANM: File does not contain unique vectors data.'
                        )
                    if quats_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Failed: Read ANM: File does not contain unique quaternions data.'
                        )
                    if frames_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Failed: Read ANM: File does not contain frames data.'
                        )
                    joint_hash_count = (
                        frames_offset - joint_hashes_offset) // 4
                    vec_count = (quats_offset - vecs_offset) // 12
                    quat_count = (joint_hashes_offset - quats_offset) // 6
                    # read joint hashes
                    bs.seek(joint_hashes_offset + 12)
                    joint_hashes = bs.read_u32(joint_hash_count)
                    # read vecs
                    bs.seek(vecs_offset + 12)
                    uni_vecs = bs.read_vec3(vec_count)
                    # read quats
                    bs.seek(quats_offset + 12)
                    uni_quats = [decompress_quat(
                        bs.read(6)) for i in range(quat_count)]
                    # parse tracks
                    self.tracks = [ANMTrack() for i in range(joint_count)]
                    for track_id, track in enumerate(self.tracks):
                        track.joint_hash = joint_hashes[track_id]
                    # read frames
                    bs.seek(frames_offset + 12)
                    for track in self.tracks:
                        for f in range(frame_count):
                            translate_index, scale_index, rotate_index = bs.read_u16(
                                3)
                            # parse pose
                            pose = ANMPose()
                            pose.time = f
                            translate = uni_vecs[translate_index]
                            pose.translate = Vector(
                                translate.x, translate.y, translate.z)
                            scale = uni_vecs[scale_index]
                            pose.scale = Vector(scale.x, scale.y, scale.z)
                            rotate = uni_quats[rotate_index]
                            pose.rotate = Quaternion(
                                rotate.x, rotate.y, rotate.z, rotate.w)
                            track.poses.append(pose)
                elif self.version == 4:
                    # v4
                    # read headers
                    self.file_size, self.format_token, self.flags1, self.flags2 = bs.read_u32(
                        4)
                    track_count, frame_count = bs.read_u32(2)
                    self.fps = 1 / bs.read_f32()[0]  # frame duration
                    self.duration = frame_count
                    # read offsets & calculate stuffs
                    _, _, _, vecs_offset, quats_offset, frames_offset = bs.read_i32(
                        6)
                    if vecs_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Failed: File does not contain unique vectors data.'
                        )
                    if quats_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Failed: File does not contain unique quaternions data.'
                        )
                    if frames_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Failed: File does not contain frames data.'
                        )
                    vec_count = (quats_offset - vecs_offset) // 12
                    quat_count = (frames_offset - quats_offset) // 16
                    # read uni vecs
                    bs.seek(vecs_offset + 12)
                    uni_vecs = bs.read_vec3(vec_count)
                    # read uni quats
                    bs.seek(quats_offset + 12)
                    uni_quats = bs.read_quat(quat_count)
                    # read frames
                    bs.seek(frames_offset + 12)
                    for i in range(frame_count * track_count):
                        # parse track
                        joint_hash = bs.read_u32()
                        match_track = None
                        for track in self.tracks:
                            if track.joint_hash == joint_hash:
                                match_track = track
                                break
                        if match_track == None:
                            track = ANMTrack()
                            track.joint_hash = joint_hash
                            self.tracks.append(track)
                        else:
                            track = match_track
                        translate_index, scale_index, rotate_index = bs.read_u16(
                            3)
                        bs.pad(2)
                        # parse pose
                        pose = ANMPose()
                        pose.time = len(track.poses)
                        translate = uni_vecs[translate_index]
                        pose.translate = Vector(
                            translate.x, translate.y, translate.z)
                        scale = uni_vecs[scale_index]
                        pose.scale = Vector(scale.x, scale.y, scale.z)
                        rotate = uni_quats[rotate_index]
                        pose.rotate = Quaternion(
                            rotate.x, rotate.y, rotate.z, rotate.w)
                        track.poses.append(pose)
                elif self.version == 3:
                    # legacy
                    # read headers
                    bs.pad(4)  # skl id
                    track_count, frame_count = bs.read_u32(2)
                    self.fps, = bs.read_u32()
                    self.duration = frame_count
                    # parse tracks
                    self.tracks = [ANMTrack() for i in range(track_count)]
                    for track in self.tracks:
                        track.joint_hash = Elf(bs.read_a_padded(32)[0])
                        bs.pad(4)  # flags
                        # parse pose
                        for f in range(frame_count):
                            pose = ANMPose()
                            pose.time = f
                            pose.rotate = bs.read_quat()
                            pose.translate = bs.read_vec3()
                            # legacy not support scaling
                            pose.scale = Vector(1.0, 1.0, 1.0)
                            track.poses.append(pose)
                else:
                    raise Exception(
                        f'pyRitoFile: Failed: Read ANM: Unsupported file version: {self.version}')
            else:
                raise Exception(
                    f'pyRitoFile: Failed: Read ANM: Wrong signature file: {hex(self.signature)}')
            # sort pose by time
            if len(self.tracks) > 0:
                for track in self.tracks:
                    if len(track.poses) > 0:
                        track.poses.sort(key=lambda pose: pose.time)
