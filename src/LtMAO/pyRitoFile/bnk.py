from io import BytesIO
from ..pyRitoFile.io import BinStream
from enum import Enum


class BNKObjectType(Enum):
    Settings = 1
    Sound = 2
    Action = 3
    Event = 4
    RandomOrSequenceContainer = 5
    SwitchContainer = 6
    ActorMixer = 7
    AudioBus = 8
    BlendContainer = 9
    MusicSegment = 10
    MusicTrack = 11
    MusicSwitchContainer = 12
    MusicPlaylistContainer = 13
    Attenuation = 14
    DialogueEvent = 15
    MotionBus = 16
    MotionFX = 17
    Effect = 18
    AuxiliaryBus = 19

    def __json__(self):
        return self.name


class BNKObjectData:
    def __init__(self):
        pass

    def __json__(self):
        return vars(self)


class BNKObject:
    # hirc
    __slots__ = (
        'id', 'type', 'size', 'data'
    )

    def __init__(self):
        self.id = None
        self.type = None
        self.size = None
        self.data = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class BNKWem:
    # didx
    __slots__ = (
        'id', 'offset', 'size'
    )

    def __init__(self):
        self.id = None
        self.offset = None
        self.size = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class BNKSectionData:
    def __init__(self):
        pass

    def __json__(self):
        return vars(self)


class BNKSection:
    __slots__ = (
        'signature', 'size', 'data'
    )

    def __init__(self):
        self.signature = None
        self.size = None
        self.data = None

    def __json__(self):
        return {key: getattr(self, key) for key in self.__slots__}


class BNK:
    __slots__ = ('sections')

    def __init__(self):
        self.sections = []

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
            while bs.tell() < bs.end():
                section = BNKSection()
                section.signature, = bs.read_a(4)
                section.size, = bs.read_u32()
                section.data = BNKSectionData()
                if section.signature == 'BKHD':
                    # bank header: data is depend of version
                    bkhd = section.data
                    bkhd.version, bkhd.id = bs.read_u32(2)
                    bkhd.unk = bs.read(section.size - 8)
                elif section.signature == 'DIDX':
                    # data index: contains list of wems(id, offset, size)
                    didx = section.data
                    wem_count = section.size // 12
                    didx.wems = []
                    for i in range(wem_count):
                        wem = BNKWem()
                        wem.id, wem.offset, wem.size = bs.read_u32(3)
                        didx.wems.append(wem)
                elif section.signature == 'DATA':
                    # data: all wems data, should just save start offset
                    data = section.data
                    data.start_offset = bs.tell()
                    bs.pad(section.size)
                elif section.signature == 'HIRC':
                    # hierarchy: contains list of wwise objects
                    hirc = section.data
                    object_count, = bs.read_u32()
                    hirc.objects = []
                    for i in range(object_count):
                        obj = BNKObject()
                        obj.type = BNKObjectType(bs.read_u8()[0])
                        obj.size, obj.id = bs.read_u32(2)
                        obj.data = BNKObjectData()
                        obj_offset = bs.tell()
                        if obj.type == BNKObjectType.Sound:
                            sound = obj.data
                            sound.unk1 = bs.read(4)
                            sound.stream_type, = bs.read_u8()
                            sound.wem_id, sound.source_id, = bs.read_u32(
                                2)
                            sound.unk2 = bs.read(8)
                            sound.object_id, = bs.read_u32()
                        elif obj.type == BNKObjectType.Event:
                            event = obj.data
                            event.action_ids = bs.read_u32(bs.read_u8()[0])
                        elif obj.type == BNKObjectType.Action:
                            action = obj.data
                            action.scope, = bs.read_u8()
                            action.type, = bs.read_u8()
                            action.object_id, = bs.read_u32()

                            action.unk1 = bs.read(1)
                            param_count, = bs.read_u8()
                            if param_count > 0:
                                action.param_types = [
                                    bs.read_u8()[0] for i in range(param_count)]
                                action.param_values = [bs.read(4)
                                                       for i in range(param_count)]
                            action.unk2 = bs.read(1)
                            if action.type == 18:
                                action.state_group_id, action.state_id = bs.read_u32(
                                    2)
                            elif action.type == 25:
                                action.switch_group_id, action.swith_id = bs.read_u32(
                                    2)
                        elif obj.type == BNKObjectType.RandomOrSequenceContainer:
                            container = obj.data
                            container.unk1 = bs.read(1)
                            effect_count, = bs.read_u8()
                            container.unk2 = bs.read(5)
                            if effect_count > 0:
                                container.bypass_effect = bs.read(1)
                                for i in range(effect_count):
                                    container.effect_id, = bs.read_u8()
                                    container.object_id, = bs.read_u32()
                                    container.effect_unk = bs.read(2)
                            container.switch_container_id, = bs.read_u32()
                            container.unk3 = bs.read(1)
                            prop_count, = bs.read_u8()
                            if prop_count > 0:
                                container.prop_ids = [
                                    bs.read_u8()[0] for i in range(prop_count)]
                                container.prop_values = [
                                    bs.read(4) for i in range(prop_count)]
                            ranged_prob_count, = bs.read_u8()
                            if ranged_prob_count > 0:
                                container.ranged_prob_ids = [bs.read(1)
                                                             for i in range(ranged_prob_count)]
                                container.ranged_prob_ranges = [(bs.read(4), bs.read(4))
                                                                for i in range(ranged_prob_count)]
                            positioning, = bs.read_u8()
                            container.has_pos = (positioning & 1) == 1
                            container.has_3d,  container.has_automation = False, False
                            if container.has_pos:
                                container.has_3d = (positioning & 2) == 2
                            if container.has_3d and container.has_pos:
                                container.has_automation = (
                                    (positioning >> 5) & 3) == 3
                                container.unk4 = bs.read(1)
                            if container.has_automation:
                                container.path_mode, = bs.read_u8()
                                container.transition_time, = bs.read_i32()
                                vertex_count, = bs.read_u32()
                                if vertex_count > 0:
                                    container.vertices = []
                                    for i in range(vertex_count):
                                        vertex_x, vertex_y, vertex_z = bs.read_f32(
                                            3)
                                        duration, = bs.read_i32()
                                        container.vertices.append(
                                            (vertex_x, vertex_y, vertex_z, duration))
                                playlist_item_count, = bs.read_u32()
                                if playlist_item_count > 0:
                                    container.playlist_items = []
                                    for i in range(playlist_item_count):
                                        vertex_offset, vertex_count = bs.read_u32(
                                            2)
                                        x_range, y_range, z_range = bs.read_f32(
                                            3)
                                        container.playlist_items.append(
                                            (vertex_offset, vertex_count, x_range, y_range, z_range))
                            container.unk5 = bs.read(9)
                            rtpc_count, = bs.read_u16()
                            if rtpc_count > 0:
                                container.rtpcs = []
                                for i in range(rtpc_count):
                                    unk = bs.read(12)
                                    point_count, = bs.read_u16()
                                    container.rtpcs.append(
                                        unk,
                                        [bs.read(12)
                                         for i in range(point_count)]
                                    )
                            container.unk6 = bs.read(24)
                            sound_id_count, = bs.read_u32()
                            container.sound_ids = [
                                bs.read_u32()[0] for i in range(sound_id_count)]

                        obj_size = bs.tell() - obj_offset + 4
                        if obj_size < obj.size:
                            obj.data.end_unknown = bs.read(
                                obj.size-obj_size)
                        hirc.objects.append(obj)
                else:
                    # unknown sections to read
                    section.data = bs.read(section.size)
                self.sections.append(section)
