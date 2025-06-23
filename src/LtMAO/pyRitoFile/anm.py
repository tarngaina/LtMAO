from math import sqrt
from .stream import BytesStream
from ..pyRitoFile.structs import Quaternion, Vector
from .helper import Elf

class ANMHepler:
    @staticmethod
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
        
    @staticmethod
    def compress_quat(quat):
        sqrt_2 = 1.41421356237
        max_index = 3
        abs_x, abs_y, abs_z, abs_w = abs(quat.x), abs(quat.y), abs(quat.z), abs(quat.w)
        if abs_x >= abs_w and abs_x >= abs_y and abs_x >= abs_z:
            max_index = 0
            if quat.x < 0:
                quat *= -1
        elif abs_y >= abs_w and abs_y >= abs_x and abs_y >= abs_z:
            max_index = 1
            if quat.y < 0:
                quat *= -1
        elif abs_z >= abs_w and abs_z >= abs_x and abs_z >= abs_y:
            max_index = 2
            if quat.z < 0:
                quat *= -1
        elif quat.w < 0:
            quat *= -1
        bits = max_index << 45
        quatvalues = (quat.x, quat.y, quat.z, quat.w)
        compressed_index = 0
        for i in range(4):
            if i == max_index:
                continue
            temp = round(16383.5 * (sqrt_2 * quatvalues[i] + 1.0))
            bits |= (temp & 32767) << (30 - 15 * compressed_index)
            compressed_index += 1
        compressed = [(bits >> (8 * i)) & 255 for i in range(6)]
        return bytes(compressed)

    @staticmethod
    def decompress_vec3(min, max, bytes):
        return Vector(
            (max.x - min.x) / 65535.0 * (bytes[0] | bytes[1] << 8) + min.x,
            (max.y - min.y) / 65535.0 * (bytes[2] | bytes[3] << 8) + min.y,
            (max.z - min.z) / 65535.0 * (bytes[4] | bytes[5] << 8) + min.z
        )
        
    @staticmethod
    def interpolate_integer_frames(anm):
        def interpolate(frame, curve, func):
            times = curve.keys()
            # loop from right, get left 
            left = None
            for time in reversed(times):
                if time <= frame and curve[time] != None:
                    left = frame
                    break
            # loop from left, get right
            right = None
            for time in times:
                if time >= frame and curve[time] != None:
                    right = frame
                    break
            # set if frame outside range
            if left == None:
                return curve[right]
            if right == None:
                return curve[left]
            # interpolate if frame inside range
            return func(
                curve[left], 
                curve[right],
                (frame - left) / (right - left)
            )
            
        for track in anm.tracks:
            # sort time and init curve
            track.poses = dict(sorted(track.poses.items()))
            translate_curve = {time: track.poses[time].translate for time in track.poses}
            scale_curve = {time: track.poses[time].scale for time in track.poses}
            rotate_curve = {time: track.poses[time].rotate for time in track.poses}
            # integer frame
            for frame in range(anm.duration):
                if frame not in track.poses:
                    track.poses[frame] = pose = ANMPose()
                else:
                    pose = track.poses[frame]
                # only interpolate if need
                if pose.translate == None:
                    pose.translate = interpolate(frame, translate_curve, Vector.lerp)
                if pose.scale == None:
                    pose.scale = interpolate(frame, scale_curve, Vector.lerp)
                if pose.rotate == None:
                    pose.rotate = interpolate(frame, rotate_curve, Quaternion.slerp)

    @staticmethod
    def build_frames(anm):
        track_count = len(anm.tracks)
        vec_index = 0
        quat_index = 0
        vec_bank = {}
        quat_bank = {}
        frames = [None] * anm.duration * track_count
        for t, track in enumerate(anm.tracks):
            for f in range(anm.duration):
                translate, rotate, scale = track.poses[f].translate, track.poses[f].rotate, track.poses[f].scale
                # translate
                translate_key = f'{translate.x:.4g} {translate.y:.4g} {translate.z:.4g}'
                if translate_key not in vec_bank:
                    vec_bank[translate_key] = vec_index
                    translate_index = vec_index
                    vec_index += 1
                else:
                    translate_index = vec_bank[translate_key]
                # scale
                scale_key = f'{scale.x:.4g} {scale.y:.4g} {scale.z:.4g}'
                if scale_key not in vec_bank:
                    vec_bank[scale_key] = vec_index
                    scale_index = vec_index
                    vec_index += 1
                else:
                    scale_index = vec_bank[scale_key]
                # rotate
                rotate_key = f'{rotate.x:.7g} {rotate.y:.7g} {rotate.z:.7g} {rotate.w:.7g}'
                if rotate_key not in quat_bank:
                    quat_bank[rotate_key] = quat_index
                    rotate_index = quat_index
                    quat_index += 1
                else:
                    rotate_index = quat_bank[rotate_key]
                # add to frame
                frames[f * track_count + t] = (translate_index, scale_index, rotate_index)
        vec_bank = [Vector(*[float(value) for value in vec_key.split()]) for vec_key in list(vec_bank.keys())]
        quat_bank = [Quaternion(*[float(value) for value in quat_key.split()]) for quat_key in list(quat_bank.keys())]
        return vec_bank, quat_bank, frames

class ANMErrorMetric:
    __slots__ = (
        'margin', 'discontinuity_threshold'
    )

    def __init__(self, margin=None, discontinuity_threshold=None):
        self.margin = margin
        self.discontinuity_threshold = discontinuity_threshold

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class ANMPose:
    __slots__ = (
        'translate', 'rotate', 'scale'
    )

    def __init__(self, translate=None, rotate=None, scale=None):
        self.translate = translate
        self.rotate = rotate
        self.scale = scale

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class ANMTrack:
    __slots__ = (
        'joint_hash', 'poses'
    )

    def __init__(self, joint_hash=None, poses=None):
        self.joint_hash = joint_hash
        self.poses = poses # poses[time] = pose at time

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class ANM:
    __slots__ = (
        'signature', 'version', 'file_size', 'format_token', 'flags1', 'flags2',
        'duration', 'fps', 'error_metrics', 'tracks'
    )

    def __init__(self, signature=None, version=None, file_size=None, format_token=None, flags1=None, flags2=None, duration=None, fps=None, error_metrics=None, tracks=None):
        self.signature = signature
        self.version = version
        self.file_size = file_size
        self.format_token = format_token
        self.flags1 = flags1
        self.flags2 = flags2
        self.duration = duration
        self.fps = fps
        self.error_metrics = error_metrics
        self.tracks = tracks

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def read(self, path, raw=False):
        with BytesStream.reader(path, raw) as bs:
            self.signature, = bs.read_s(8)
            self.version, = bs.read_u32()

            if self.signature == 'r3d2canm':
                # compressed
                # read header
                self.file_size, self.format_token, self.flags1 = bs.read_u32(3)
                track_count, frame_count = bs.read_u32(2)
                bs.pad(4)  # jump cache count
                max_time, self.fps = bs.read_f32(2)
                self.duration = max_time * self.fps + 1
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
                        f'pyRitoFile: Error: Read ANM: File does not contain frames.'
                    )
                if joint_hashes_offset <= 0:
                    raise Exception(
                        f'pyRitoFile: Error: Read ANM: File does not contain joint hashes.'
                    )
                # read joint hashes
                bs.seek(joint_hashes_offset + 12)
                joint_hashes = bs.read_u32(track_count)
                # create tracks
                self.tracks = [ANMTrack() for i in range(track_count)]
                for track_id, track in enumerate(self.tracks):
                    track.joint_hash = joint_hashes[track_id]
                    track.poses = {}
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
                    time = (compressed_time / 65535.0 * max_time) * self.fps
                    if time in match_track.poses:
                        pose = match_track.poses[time]
                    else:
                        pose = ANMPose()
                        match_track.poses[time] = pose
                    # decompress pose data
                    transform_type = bits >> 14
                    if transform_type == 0:
                        pose.rotate = ANMHepler.decompress_quat(
                            compressed_transform)
                    elif transform_type == 1:
                        pose.translate = ANMHepler.decompress_vec3(
                            translate_min, translate_max, compressed_transform)
                    elif transform_type == 2:
                        pose.scale = ANMHepler.decompress_vec3(
                            scale_min, scale_max, compressed_transform)
                    else:
                        raise Exception(
                            f'pyRitoFile: Error: Read ANM: Unknown compressed transform type: {transform_type}.'
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
                            f'pyRitoFile: Error: Read ANM: File does not contain joint hashes data.'
                        )
                    if vecs_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Error: Read ANM: File does not contain unique vectors data.'
                        )
                    if quats_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Error: Read ANM: File does not contain unique quaternions data.'
                        )
                    if frames_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Error: Read ANM: File does not contain frames data.'
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
                    vec_bank = bs.read_vec3(vec_count)
                    # read quats
                    bs.seek(quats_offset + 12)
                    quat_bank = [ANMHepler.decompress_quat(
                        bs.read(6)) for i in range(quat_count)]
                    # prepare tracks
                    self.tracks = [ANMTrack() for i in range(track_count)]
                    for track_id, track in enumerate(self.tracks):
                        track.joint_hash = joint_hashes[track_id]
                        track.poses = {}
                    # read frames
                    bs.seek(frames_offset + 12)
                    for f in range(frame_count):
                        for track in self.tracks:
                            translate_index, scale_index, rotate_index = bs.read_u16(3)
                            # parse pose
                            pose = ANMPose()
                            translate = vec_bank[translate_index]
                            pose.translate = Vector(
                                translate.x, translate.y, translate.z)
                            scale = vec_bank[scale_index]
                            pose.scale = Vector(scale.x, scale.y, scale.z)
                            rotate = quat_bank[rotate_index]
                            pose.rotate = Quaternion(
                                rotate.x, rotate.y, rotate.z, rotate.w)
                            track.poses[f] = pose
                    
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
                            f'pyRitoFile: Error: File does not contain unique vectors data.'
                        )
                    if quats_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Error: File does not contain unique quaternions data.'
                        )
                    if frames_offset <= 0:
                        raise Exception(
                            f'pyRitoFile: Error: File does not contain frames data.'
                        )
                    vec_count = (quats_offset - vecs_offset) // 12
                    quat_count = (frames_offset - quats_offset) // 16
                    # read uni vecs
                    bs.seek(vecs_offset + 12)
                    vec_bank = bs.read_vec3(vec_count)
                    # read uni quats
                    bs.seek(quats_offset + 12)
                    quat_bank = bs.read_quat(quat_count)
                    # prepare tracks
                    self.tracks = [ANMTrack() for i in range(track_count)]
                    for track in self.tracks:
                        track.poses = {}
                    # read frames
                    bs.seek(frames_offset + 12)
                    for f in range(frame_count):
                        for t in range(track_count):
                            joint_hash, = bs.read_u32()
                            translate_index, scale_index, rotate_index = bs.read_u16(3)
                            bs.pad(2)
                            track = self.tracks[t]
                            if track.joint_hash == None:
                                # if track t is new
                                track.joint_hash = joint_hash
                            else:
                                # if track t is not new
                                if track.joint_hash != joint_hash:
                                    # track t is wrong for this joint hash, find another track
                                    match_track = None
                                    for track in self.tracks:
                                        if track.joint_hash == joint_hash:
                                            match_track = track
                                            break
                                    if match_track == None:
                                        # no track found???
                                        continue
                            # parse pose
                            pose = ANMPose()
                            translate = vec_bank[translate_index]
                            pose.translate = Vector(
                                translate.x, translate.y, translate.z)
                            scale = vec_bank[scale_index]
                            pose.scale = Vector(scale.x, scale.y, scale.z)
                            rotate = quat_bank[rotate_index]
                            pose.rotate = Quaternion(
                                rotate.x, rotate.y, rotate.z, rotate.w)
                            track.poses[len(track.poses)] = pose
                elif self.version == 3:
                    # legacy
                    # read headers
                    bs.pad(4)  # skl id
                    track_count, frame_count = bs.read_u32(2)
                    self.fps, = bs.read_u32()
                    self.duration = frame_count
                    # prepare tracks
                    self.tracks = [ANMTrack() for i in range(track_count)]
                    for track in self.tracks:
                        track.joint_hash = Elf(bs.read_s_padded(32)[0])
                        bs.pad(4)  # flags
                        # read pose
                        track.poses = {}
                        for f in range(frame_count):
                            pose = ANMPose()
                            pose.rotate, = bs.read_quat()
                            pose.translate, = bs.read_vec3()
                            # legacy not support scaling
                            pose.scale = Vector(1.0, 1.0, 1.0)
                            track.poses[f] = pose
                else:
                    raise Exception(
                        f'pyRitoFile: Error: Read ANM: Unsupported file version: {self.version}')
            else:
                raise Exception(
                    f'pyRitoFile: Error: Read ANM: Wrong signature file: {hex(self.signature)}') 
            
            return self
        
    def write(self, path, raw=False):
        with BytesStream.writer(path, raw) as bs:
            self.duration = int(self.duration)
            ANMHepler.interpolate_integer_frames(self)
            vec_bank, quat_bank, frames = ANMHepler.build_frames(self)
            vec_count = len(vec_bank)
            if vec_count > 65535:
                raise Exception(
                    f'pyRitoFile: Error: Write ANM: Animation size is too big, vector bank size: {vec_count} exceed 65535.'
                )
            quat_count = len(quat_bank)
            if quat_count > 65535:
                raise Exception(
                    f'pyRitoFile: Error: Write ANM: Animation size is too big, quaternion bank size: {quat_count} exceed 65535.'
                )
            # start write anm
            bs.write_s('r3d2anmd') # signature
            bs.write_u32(
                5, # version
                0, # file_size
                0, # format token
                0, # flags1
                0, # flags2
            )
            bs.write_u32(
                len(self.tracks), # track_count
                self.duration # frame_count
            )
            bs.write_f32(1 / self.fps) # fps
            bs.write_u32(
                0, # joint_hashes_offset
                0,
                0,
                0, # vecs_offset
                0, # quats_offset
                0 # frames_offset
            )
            bs.write_u32(0, 0, 0) # pad 12 bytes
            # write data 
            # must in order: vecs -> quats -> joint_hashses -> frames
            # vec
            vecs_offset = bs.tell()
            bs.write_vec3(*vec_bank)
            # quat
            quat_offsets = bs.tell()
            bs.write(b''.join(ANMHepler.compress_quat(quat) for quat in quat_bank))
            # joint_hash
            joint_hashes_offset = bs.tell()
            bs.write_u32(*[track.joint_hash for track in self.tracks])
            # frame
            frames_offset = bs.tell()
            for translate_index, rotate_index, scale_index in frames:
                bs.write_u16(translate_index, rotate_index, scale_index)
            # write offsets
            bs.seek(12) 
            bs.write_u32(bs.end()) # file_size
            bs.seek(40)
            bs.write_u32(joint_hashes_offset-12)
            bs.seek(52)
            bs.write_u32(vecs_offset-12, quat_offsets-12, frames_offset-12)
            return bs.raw() if raw else None