from io import BytesIO
from ..pyRitoFile.io import BinStream
from enum import Enum

class BNKHelper:
    @staticmethod
    def skip_init_params(bs):
        bs.pad(bs.read_u8()[0] * 5)
        bs.pad(bs.read_u8()[0] * 9)

    @staticmethod
    def skip_pos_params(bs, bkhd_version):
        pos_bits, = bs.read_u8()
        has_pos = pos_bits & 1
        has_3d = False
        has_automation = False
        if has_pos:
            if bkhd_version <= 89:
                has_2d, has_3d = bs.read_b(2)
                if has_2d: bs.pad(1)
            else:
                has_3d = pos_bits & 2
        if has_pos and has_3d:
            if bkhd_version <= 89:
                has_automation = (bs.read_u8()[0] & 3) != 1
                bs.pad(8)
            else:
                has_automation = (pos_bits >> 5) & 3
                bs.pad(1)
        if has_automation:
            bs.pad(9 if bkhd_version <= 89 else 5)
            bs.pad(16 * bs.read_u32()[0])
            bs.pad((16 if bkhd_version <= 89 else 20) * bs.read_u32()[0])
        elif bkhd_version <= 59:
            bs.pad(1)

    
    @staticmethod 
    def skip_aux(bs):
        has_aux = (bs.read_u8()[0] >> 3) & 1
        if has_aux: bs.pad(16)
        bs.pad(6)
        bs.pad(3 * bs.read_u8()[0])
        for i in range(bs.read_u8()[0]):
            bs.pad(5)
            bs.pad(8 * bs.read_u8()[0])
            
    @staticmethod
    def skip_rtpc(bs, bkhd_version):
        rtpc_count, = bs.read_u16()
        for i in range(rtpc_count):
            bs.pad(13 if bkhd_version <= 89 else 12)
            bs.pad(12 * bs.read_u16()[0])


    @staticmethod
    def skip_base_params(bs, bkhd_version):
        bs.pad(1)
        fx_count, = bs.read_u8()
        bs.pad(5 + int(fx_count != 0) - int(bkhd_version <= 89) + (fx_count * 7))

        parent_id, = bs.read_u32()
    
        bs.pad(2 if bkhd_version <= 89 else 1)
        BNKHelper.skip_init_params(bs)
        BNKHelper.skip_pos_params(bs, bkhd_version)
        BNKHelper.skip_aux(bs)
        BNKHelper.skip_rtpc(bs, bkhd_version)

        return parent_id
    
    @staticmethod
    def skip_clip_automation(bs):
        for i in range(bs.read_u32()[0]):
            bs.pad(8)
            bs.pad(12 * bs.read_u32()[0])
    

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
    __slots__ = ('bkhd', 'didx', 'data', 'hirc', 'unknown_sections')

    def __init__(self):
        self.bkhd = None
        self.didx = None
        self.data = None
        self.hirc = None
        self.unknown_sections = []

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
                    self.bkhd = bkhd = section.data
                    bkhd.version, bkhd.id = bs.read_u32(2)
                    bkhd.unk = bs.read(section.size - 8)
                elif section.signature == 'DIDX':
                    # data index: contains list of wems(id, offset, size)
                    self.didx = didx = section.data
                    wem_count = section.size // 12
                    didx.wems = []
                    for i in range(wem_count):
                        wem = BNKWem()
                        wem.id, wem.offset, wem.size = bs.read_u32(3)
                        didx.wems.append(wem)
                elif section.signature == 'DATA':
                    # data: all wems data, should just save start offset
                    self.data = data = section.data
                    data.start_offset = bs.tell()
                    bs.pad(section.size)
                elif section.signature == 'HIRC':
                    # hierarchy: contains list of wwise objects
                    self.hirc = hirc = section.data
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
                            bs.pad(4)
                            if self.bkhd.version == 88:
                                sound.stream_type, = bs.read_u32()
                            else:
                                sound.stream_type, = bs.read_u8()
                            sound.wem_id, sound.source_id, = bs.read_u32(
                                2)
                            if self.bkhd.version == 88:
                                bs.pad(7)
                            else:
                                bs.pad(8)
                            sound.object_id, = bs.read_u32()
                        elif obj.type == BNKObjectType.Action:
                            action = obj.data
                            action.scope, = bs.read_u8()
                            action.type, = bs.read_u8()
                            if action.type == 25:
                                bs.pad(5)
                                BNKHelper.skip_init_params(bs)
                                action.switch_group_id, action.switch_id = bs.read_u32(2)
                            else:
                                action.object_id, = bs.read_u32()       
                        elif obj.type == BNKObjectType.Event:
                            event = obj.data
                            if self.bkhd.version == 58:
                                action_id_count, = bs.read_u32()
                            else:
                                action_id_count, = bs.read_u8()
                            event.action_ids = bs.read_u32(action_id_count)
                        elif obj.type == BNKObjectType.RandomOrSequenceContainer:
                            container = obj.data
                            container.switch_container_id = BNKHelper.skip_base_params(bs, self.bkhd.version)
                            bs.pad(24)
                            container.sound_ids = bs.read_u32(bs.read_u32()[0])
                        elif obj.type in (BNKObjectType.MusicSegment, BNKObjectType.MusicPlaylistContainer):
                            segment = obj.data
                            bs.pad(4)
                            segment.music_switch_id, segment.sound_id = bs.read_u32(2)
                            bs.pad(1)
                            BNKHelper.skip_init_params(bs)
                            BNKHelper.skip_pos_params(bs, self.bkhd.version)
                            BNKHelper.skip_aux(bs)
                            BNKHelper.skip_rtpc()
                            segment.music_track_ids = bs.read_u32(bs.read_u32()[0])
                        elif obj.type == BNKObjectType.MusicTrack:
                            track = obj.data 
                            bs.pad(1)
                            bs.pad(14 * bs.read_u32()[0])
                            playlist_count, = bs.read_u32()
                            bs.pad(playlist_count * 44)
                            track.track_count, = bs.read_u32()
                            bs.pad(0 - 4 - playlist_count * 44)
                            
                            track.wem_ids = [0 for i in range(track.track_count)]
                            for i in range(playlist_count):
                                track_index, wem_id, event_id = bs.read_u32(3)
                                play_at, begin_strim_offset, end_trim_offset, source_duration = bs.read_f64(4)
                                track.wem_ids[track_index] = wem_id
                            bs.pad(4)
                            BNKHelper.skip_clip_automation(bs)
                            track.parent_id = BNKHelper.skip_base_params(bs, self.bkhd.version)
                            if bs.read_u8()[0] == 3:
                                track.has_switch_ids = True
                                bs.pad(1)
                                track.switch_group_id, = bs.read_u32()
                                bs.pad(4+4)
                                track.switch_ids = bs.read_u32(track.track_count)

                                
                        obj_size = bs.tell() - obj_offset + 4
                        if obj_size < obj.size:
                            bs.pad(obj.size-obj_size)
                        hirc.objects.append(obj)
                else:
                    # unknown sections to read
                    section.data = bs.read(section.size)
                    self.unknown_sections.append(section)
