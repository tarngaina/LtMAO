from LtMAO.pyRitoFile.io import BinStream

"""
enum class ObjectType : std::int8_t
{
    SoundEffectOrVoice = 2,
    EventAction = 3,
    Event = 4,
    RandomOrSequenceContainer = 5,
    SwitchContainer = 6,
    ActorMixer = 7,
    AudioBus = 8,
    BlendContainer = 9,
    MusicSegment = 10,
    MusicTrack = 11,
    MusicSwitchContainer = 12,
    MusicPlaylistContainer = 13,
    Attenuation = 14,
    DialogueEvent = 15,
    MotionBus = 16,
    MotionFx = 17,
    Effect = 18,
    Unknown = 19,
    AuxiliaryBus = 20
};"""


class BNKSoundEffectOrVoice:
    def __init__(self):
        pass


class BNKEventEntry:
    def __init__(self):
        self.ids = []


class BNKEventActionEntry:
    def __init__(self):
        self.scope = None
        self.type = None
        self.object_id = None
        self.params = None
        self.param_types = None


class BNKEntry:
    def __init__(self):
        self.type = None
        self.size = None
        self.id = None
        self.content = None
        self.unknown = None


class BNKIndex:
    def __init__(self):
        self.id = None
        self.offset = None
        self.size = None


class BNKSection:
    def __init__(self):
        self.name = None
        self.size = None
        self.embed = None
        self.entries = None


class BNK:
    def __init__(self):
        self.version = None
        self.id = None
        self.header_unknown = None
        self.sections = []

    def read(self, path):
        with open(path, 'rb') as f:
            bs = BinStream(f)

            end = bs.end()
            while True:
                if bs.tell() >= end:
                    break
                section = BNKSection()
                section.name, = bs.read_a(4)
                section.size, = bs.read_u32()
                if section.name == 'BKHD':
                    self.version, self.id = bs.read_u32(
                        2)
                    self.header_unknown = bs.read(section.size - 8)
                elif section.name == 'DIDX':
                    section.embed = [bs.read_u32(3)
                                     for i in range(section.size // 12)]
                elif section.name == 'HIRC':
                    entry_count, = bs.read_u32()
                    section.entries = [BNKEntry() for i in range(entry_count)]
                    for i in range(entry_count):
                        entry = section.entries[i]

                        entry.type, = bs.read_u8()
                        entry.size, entry.id, = bs.read_u32(2)
                        if entry.type == 2:
                            id, = bs.read_u32()
                            unk = bs.read(4)
                            stream_type, = bs.read_u32()
                            audio_id, = bs.read_u32()
                            src_id, = bs.read_u32()
                            print(id, unk, stream_type, audio_id, src_id)
                            entry.unknown = bs.read(entry.size - 4 - 20)
                        elif entry.type == 3:  # EventAction
                            content = BNKEventActionEntry()
                            content.scope, content.type = bs.read_u8(2)
                            content.object_id = bs.read_u32()
                            bs.pad(1)  # 0x00
                            param_count, = bs.read_u8()
                            content.param_types = bs.read_u8(param_count)
                            content.params = bs.read_u8(param_count)
                            entry.content = content
                            bs.pad(1)  # 0x00
                            print(content.scope, content.object_id,
                                  content.param_types, content.params)
                            entry.unknown = bs.read(
                                entry.size-13-param_count*2)
                        elif entry.type == 4:  # Event
                            content = BNKEventEntry()
                            id_count, = bs.read_i8() if self.version >= 134 else bs.read_u32()
                            content.ids = bs.read_u32(id_count)
                            entry.content = content
                            print(content.ids)
                        else:
                            entry.unknown = bs.read(entry.size - 4)
                elif section.name == 'DATA':
                    didx_section = next(
                        (section for section in self.sections if section.name == 'DIDX'), None)
                    if didx_section == None:
                        raise Exception(
                            f'Failed: Read {path}: Found DATA section before DIDX?'
                        )
                    base_offset = bs.tell()
                    for id, offset, size in didx_section.embed:
                        bs.seek(base_offset+offset)
                        data = bs.read(size)
                else:
                    raise Exception(
                        f'Failed: Read {path}: Unknown BNK Section found: {section.name}'
                    )
                self.sections.append(section)
