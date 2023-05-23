from io import BytesIO
from LtMAO.pyRitoFile.io import BinStream
from enum import Enum
from json import JSONEncoder


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
    def __init__(self):
        pass

    def __json__(self):
        return vars(self)


class BNKWem:
    # didx
    def __init__(self):
        self.id = None
        self.offset = None
        self.size = None

    def __json__(self):
        return vars(self)


class BNKSectionData:
    def __init__(self):
        pass

    def __json__(self):
        return vars(self)


class BNKSection:
    def __init__(self):
        self.signature = None
        self.size = None
        self.data = None

    def __json__(self):
        return vars(self)


class BNK:
    def __init__(self):
        self.sections = []

    def __json__(self):
        # {key: getattr(self, key) for key in self.__slots__}
        return vars(self)

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
                    bkhd.unknown = bs.read(section.size - 8)
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
                        if obj.type == BNKObjectType.Sound:
                            sound = obj.data
                            sound.unknown1 = bs.read(4)
                            sound.stream_type, = bs.read_u8()
                            sound.audio_id, sound.source_id, = bs.read_u32(
                                2)
                            sound.unknown2 = bs.read(8)
                            sound.object_id, = bs.read_u32()
                            sound.unknown3 = bs.read(obj.size-4-25)
                        elif obj.type == BNKObjectType.Event:
                            event = obj.data
                            event.event_actions = bs.read_u32(bs.read_u8()[0])
                        elif obj.type == BNKObjectType.Action:
                            action = obj.data
                            action.scope, = bs.read_u8()
                            action.type, = bs.read_u8()
                            action.object_id, = bs.read_u32()

                            action.unknown1 = bs.read(1)
                            param_count, = bs.read_u8()
                            if param_count > 0:
                                action.param_types = [
                                    bs.read_u8()[0] for i in range(param_count)]
                                action.params = [bs.read_u8()[0]
                                                 for i in range(param_count)]
                            action.unknown2 = bs.read(1)
                            if action.type == 18:
                                action.state_group_id, action.state_id = bs.read_u32(
                                    2)
                            elif action.type == 25:
                                action.switch_group_id, action.swith_id = bs.read_u32(
                                    2)
                            else:
                                action.unknown = bs.read(
                                    obj.size-4-9-(param_count)*2)
                        else:
                            obj.data.unknown = bs.read(obj.size-4)
                        hirc.objects.append(obj)
                else:
                    # unknown sections to read
                    section.data = bs.read(section.size)
                self.sections.append(section)
