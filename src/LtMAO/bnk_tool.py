from .pyRitoFile import BNKObjectType, BINHelper, read_bnk, read_wpk, read_bin
from .pyRitoFile.hash import FNV1
from .hash_manager import cached_bin_hashes
import os
import os.path
from natsort import os_sorted


LOG = print
INF = float('inf')

def parse_audio_bnk(audio_bnk):
    if audio_bnk.didx == None:
        raise Exception(
            'bnk_tool: Failed: Extract BNK: No DIDX section found in audio BNK.')
    if audio_bnk.data == None:
        raise Exception(
            'bnk_tool: Failed: Extract BNK: No DATA section found in audio BNK.')
    return audio_bnk.didx, audio_bnk.data


def parse_events_bnk(events_bnk):
    if events_bnk.hirc == None:
        raise Exception(
            'bnk_tool: Failed: Extract BNK: No HIRC section found in events BNK.')
    hirc = events_bnk.hirc
    map_bnk_objects = {}
    bnk_obj_types_need_to_be_mapped = [
        BNKObjectType.Sound,
        BNKObjectType.Event,
        BNKObjectType.Action,
        BNKObjectType.RandomOrSequenceContainer,
        BNKObjectType.MusicSegment,
        BNKObjectType.MusicTrack,
        BNKObjectType.MusicPlaylistContainer,
        BNKObjectType.MusicSwitchContainer
    ]
    for object_type in bnk_obj_types_need_to_be_mapped:
        map_bnk_objects[object_type] = {}
    for obj in hirc.objects:
        if obj.type in bnk_obj_types_need_to_be_mapped:
            map_bnk_objects[obj.type][obj.id] = obj.data
        
    return map_bnk_objects


def parse_bin(bin):
    event_names_by_id = {}
    # parse skin bin
    SkinCharacterDataProperties = BINHelper.find_item(
        items=bin.entries,
        compare_func=lambda entry: entry.type == cached_bin_hashes['SkinCharacterDataProperties']
    )
    if SkinCharacterDataProperties != None:
        skinAudioProperties = BINHelper.find_item(
            items=SkinCharacterDataProperties.data,
            compare_func=lambda field: field.hash == cached_bin_hashes['skinAudioProperties']
        )
        if skinAudioProperties != None:
            bankUnits = BINHelper.find_item(
                items=skinAudioProperties.data,
                compare_func=lambda field: field.hash == cached_bin_hashes['bankUnits']
            )
            if bankUnits != None and len(bankUnits.data) > 0:
                for BankUnit in bankUnits.data:
                    events = BINHelper.find_item(
                        items=BankUnit.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['events']
                    )
                    if events == None:
                        continue
                    for event in events.data:
                        event_names_by_id[FNV1(event)] = event
    # parse map bin
    MapAudioDataProperties = BINHelper.find_item(
        items=bin.entries,
        compare_func=lambda entry: entry.type == cached_bin_hashes['MapAudioDataProperties']
    )
    if MapAudioDataProperties != None:
        bankUnits = BINHelper.find_item(
            items=MapAudioDataProperties.data,
            compare_func=lambda field: field.hash == cached_bin_hashes['bankUnits']
        )
        if bankUnits != None and len(bankUnits.data) > 0:
            for BankUnit in bankUnits.data:
                events = BINHelper.find_item(
                    items=BankUnit.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes['events']
                )
                if events == None:
                    continue
                for event in events.data:
                    event_names_by_id[FNV1(event)] = event
    event_names_by_id[INF] = INF
    return event_names_by_id


def parse_audio_tree(map_bnk_objects):
    audio_tree = {}
    audio_tree[INF] = {}
    audio_tree[INF][INF] = []
    for event_id, event in map_bnk_objects[BNKObjectType.Event].items():
        audio_tree[event_id] = {}
        audio_tree[event_id][INF] = []
        for action_id in event.action_ids:
            action = map_bnk_objects[BNKObjectType.Action][action_id]
            if hasattr(action, 'object_id'):
                if action.type != 4: # play 
                    continue
                # if action link to ranseq container object
                if action.object_id in map_bnk_objects[BNKObjectType.RandomOrSequenceContainer]:
                    container = map_bnk_objects[BNKObjectType.RandomOrSequenceContainer][action.object_id]
                    for sound_id in container.sound_ids:
                        wem_id = map_bnk_objects[BNKObjectType.Sound][sound_id].wem_id
                        new_wem = True
                        for container_name, container_wems in audio_tree[event_id].items():
                            if wem_id in container_wems:
                                new_wem = False
                                break
                        if new_wem:
                            audio_tree[event_id][INF].append(wem_id)
                # if action link to sound object
                if action.object_id in map_bnk_objects[BNKObjectType.Sound]:
                    wem_id = map_bnk_objects[BNKObjectType.Sound][action.object_id].wem_id
                    new_wem = True
                    for container_name, container_wems in audio_tree[event_id].items():
                        if wem_id in container_wems:
                            new_wem = False
                            break
                    if new_wem:
                        audio_tree[event_id][INF].append(wem_id)
                # if action link to a ranseq container object switch container 
                for container_id, container in map_bnk_objects[BNKObjectType.RandomOrSequenceContainer].items():
                    if container.switch_container_id == action.object_id:
                        for sound_id in container.sound_ids:
                            wem_id = map_bnk_objects[BNKObjectType.Sound][sound_id].wem_id
                            if container_id not in audio_tree[event_id]:
                                audio_tree[event_id][container_id] = []
                            if wem_id not in audio_tree[event_id][container_id]:
                                audio_tree[event_id][container_id].append(wem_id)
                            if wem_id in audio_tree[event_id][INF]:
                                audio_tree[event_id][INF].remove(wem_id)
                # if action link to a music segment sound id   
                if action.object_id in map_bnk_objects[BNKObjectType.MusicPlaylistContainer]:
                    for music_track_id in map_bnk_objects[BNKObjectType.MusicPlaylistContainer][action.object_id].music_track_ids:
                        if music_track_id in map_bnk_objects[BNKObjectType.MusicSegment]:
                            music_segment_id = music_track_id
                            for real_music_track_id in map_bnk_objects[BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                for wem_id in map_bnk_objects[BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                    if music_segment_id not in audio_tree[event_id]:
                                        audio_tree[event_id][music_segment_id] = []
                                    if wem_id not in audio_tree[event_id][music_segment_id]:
                                        audio_tree[event_id][music_segment_id].append(wem_id)
                                    if wem_id in audio_tree[event_id][INF]:
                                        audio_tree[event_id][INF].remove(wem_id)
                # if action link to a music switch container
                elif action.object_id in map_bnk_objects[BNKObjectType.MusicSwitchContainer]:
                    for music_playlist_container_id, music_playlist_container in map_bnk_objects[BNKObjectType.MusicPlaylistContainer].items():
                        if music_playlist_container.sound_id == action.object_id:
                            for music_track_id in music_playlist_container.music_track_ids:
                                if music_track_id in map_bnk_objects[BNKObjectType.MusicSegment]:
                                    music_segment_id = music_track_id
                                    for real_music_track_id in map_bnk_objects[BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                        for wem_id in map_bnk_objects[BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                            if music_segment_id not in audio_tree[event_id]:
                                                audio_tree[event_id][music_segment_id] = []
                                            if wem_id not in audio_tree[event_id][music_segment_id]:
                                                audio_tree[event_id][music_segment_id].append(wem_id)
                                            if wem_id in audio_tree[event_id][INF]:
                                                audio_tree[event_id][INF].remove(wem_id)                            
    for music_track_id, music_track in map_bnk_objects[BNKObjectType.MusicTrack].items():
        for wem_id in music_track.wem_ids:
            new_wem = True
            for event_id in audio_tree:
                for container_id in audio_tree[event_id]:
                    if wem_id in audio_tree[event_id][container_id]:
                        new_wem = False
            if new_wem and wem_id not in audio_tree[INF][INF]:
                audio_tree[INF][INF].append(wem_id)
    # clean up empty event                                   
    for event_id in list(audio_tree):
        if event_id != INF and len(audio_tree[event_id]) == 1 and len(audio_tree[event_id][INF]) == 0:
            audio_tree.pop(event_id)
    return audio_tree


def sort_audio_tree(audio_tree, event_names_by_id):
    for event_id in audio_tree:
        for container_id in audio_tree[event_id]:
            audio_tree[event_id][container_id] = os_sorted(audio_tree[event_id][container_id])
    for event_id in audio_tree:
        audio_tree[event_id] = dict(os_sorted(audio_tree[event_id].items()))
    event_names_by_id = dict(os_sorted(event_names_by_id.items(), key=lambda x:x[1]))
    for event_id in event_names_by_id:
        if event_id in audio_tree:
            audio_tree[event_names_by_id[event_id]] = audio_tree.pop(event_id)
    audio_tree = dict(os_sorted(audio_tree.items()))
    return audio_tree


class BNKParser:
    def __init__(self, audio_path, events_path, bin_path=''):
        self.audio_path = audio_path
        # parse audio.bnk or audio.wpk
        self.bnk_audio_parsing = True if audio_path.endswith('.bnk') else False
        if self.bnk_audio_parsing:
            self.audio = read_bnk(audio_path)
            self.didx, self.data = parse_audio_bnk(self.audio)
        else:
            self.audio = read_wpk(audio_path)
        # parse events.bnk
        events_bnk = read_bnk(events_path)
        map_bnk_objects = parse_events_bnk(events_bnk)
        # parse bin
        self.event_names_by_id = {}
        if bin_path != '':
            bin = read_bin(bin_path)
            self.event_names_by_id = parse_bin(bin)
        # parse audio tree
        self.audio_tree = sort_audio_tree(parse_audio_tree(map_bnk_objects), self.event_names_by_id)


    def extract(self, output_dir):
        # extract bnk
        os.makedirs(output_dir, exist_ok=True)
        with self.audio.stream(self.audio_path, 'rb') as bs:
            wems = self.didx.wems if self.bnk_audio_parsing else self.audio.wems
            for wem in wems:
                bs.seek(self.data.start_offset+wem.offset if self.bnk_audio_parsing else wem.offset)
                wem_data = bs.read(wem.size)
                for event_id in self.audio_tree:
                    if event_id != INF:
                        for container_id in self.audio_tree[event_id]:
                            if wem.id in self.audio_tree[event_id][container_id]:
                                event_dir = os.path.join(output_dir, event_id)
                                os.makedirs(event_dir, exist_ok=True)
                                if container_id != INF:
                                    container_dir = os.path.join(event_dir, str(container_id))
                                    os.makedirs(container_dir, exist_ok=True)
                                    wem_dir = container_dir
                                else:
                                    wem_dir = event_dir
                                wem_file = os.path.join(wem_dir, f'{wem.id}.wem')
                                with open(wem_file, 'wb') as f:
                                    f.write(wem_data)
                                LOG(
                                    f'bnk_tool: Done: Extracted [{wem.size}bytes] {wem.id} of {event_id}')
                    else:
                        if wem.id in self.audio_tree[event_id][INF]:
                            wem_file = os.path.join(output_dir, f'{wem.id}.wem')
                            with open(wem_file, 'wb') as f:
                                f.write(wem_data)
                            LOG(
                                f'bnk_tool: Done: Extracted [{wem.size}bytes] {wem.id}')


    

def prepare(_LOG):
    global LOG
    LOG = _LOG
