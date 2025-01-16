from .pyRitoFile import BNKObjectType, BINHelper, read_bnk, read_wpk, read_bin, write_bnk, write_wpk, BNK, WPK
from .pyRitoFile.ermmm import FNV1
from .hash_manager import cached_bin_hashes
from . import ext_tools

import os
import os.path
from natsort import os_sorted
from shutil import rmtree
from pydub import utils, AudioSegment
from pydub.playback import _play_with_simpleaudio
from threading import Thread

AudioSegment.converter = os.path.abspath('./resources/ext_tools/ffmpeg/ffmpeg.exe')             
utils.get_prober_name = lambda: os.path.abspath('./resources/ext_tools/ffmpeg/ffprobe.exe')


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
    for event_id in list(audio_tree):
        for container_id in list(audio_tree[event_id]):
            if container_id == INF:
                audio_tree[event_id]['No container'] = audio_tree[event_id].pop(container_id)
        if event_id == INF:
            audio_tree['No container'] = audio_tree.pop(event_id)
    return audio_tree


class BNKParser:
    cache_dir = './prefs/bnk_tool'
    cached_segments = {}
    
    @staticmethod
    def reset_cache():
        rmtree(BNKParser.cache_dir, ignore_errors=True)
        os.makedirs(BNKParser.cache_dir, exist_ok=True)
        BNKParser.cached_segments = {}

    def __init__(self, audio_path, events_path, bin_path=''):
        self.playbacks = []
        self.audio_path = audio_path
        # parse audio.bnk or audio.wpk
        self.bnk_audio_parsing = True if audio_path.endswith('.bnk') else False
        if self.bnk_audio_parsing:
            self.audio = read_bnk(audio_path)
            self.didx, self.data = parse_audio_bnk(self.audio)
            self.wems = self.didx.wems
        else:
            self.audio = read_wpk(audio_path)
            self.wems = self.audio.wems
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

    def get_wem_offset(self, wem):
        return self.data.start_offset+wem.offset if self.bnk_audio_parsing else wem.offset

    def replace_wem(self, wem_id, wem_file):
        for wem in self.wems:
            if wem.id == wem_id:
                with open(wem_file, 'rb') as f:
                    wem_data = f.read()
                wem.size = len(wem_data)
                cache_wem_file = self.get_cache_wem_file(wem_id)
                with open(cache_wem_file, 'wb+') as f:
                    f.write(wem_data)
                ogg_file = cache_wem_file.replace('.wem', '.ogg')
                if os.path.exists(ogg_file):
                    os.remove(ogg_file)
                if ogg_file in BNKParser.cached_segments:
                    BNKParser.cached_segments.pop(ogg_file)

    def extract(self, output_dir, convert_ogg=False):
        # extract audio
        os.makedirs(output_dir, exist_ok=True)
        with self.audio.stream(self.audio_path, 'rb') as bs:
            for wem in self.wems:
                bs.seek(self.get_wem_offset(wem))
                wem_data = bs.read(wem.size)
                for event_id in self.audio_tree:
                    if event_id not in (INF, 'No container'):
                        for container_id in self.audio_tree[event_id]:
                            if wem.id in self.audio_tree[event_id][container_id]:
                                event_dir = os.path.join(output_dir, str(event_id))
                                os.makedirs(event_dir, exist_ok=True)
                                if container_id not in (INF, 'No container'):
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
                                if convert_ogg:
                                    ogg_file = wem_file.replace('.wem', '.ogg')
                                    if ext_tools.WW2OGG.run(wem_file, silent=True).returncode == 0:
                                        ext_tools.REVORB.run(ogg_file,silent=True)
                    else:
                        for container_id in self.audio_tree[event_id]:
                            if container_id in (INF, 'No container'):
                                if wem.id in self.audio_tree[event_id][container_id]:
                                    wem_file = os.path.join(output_dir, f'{wem.id}.wem')
                                    with open(wem_file, 'wb') as f:
                                        f.write(wem_data)
                                    if convert_ogg:
                                            ogg_file = wem_file.replace('.wem', '.ogg')
                                            if ext_tools.WW2OGG.run(wem_file, silent=True).returncode == 0:
                                                ext_tools.REVORB.run(ogg_file,silent=True)
                                    LOG(
                                        f'bnk_tool: Done: Extracted [{wem.size}bytes] {wem.id}')

    def unpack(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        with self.audio.stream(self.audio_path, 'rb') as bs:
            for wem in self.wems:
                bs.seek(self.get_wem_offset(wem))
                wem_data = bs.read(wem.size)
                wem_file = os.path.join(output_dir, str(wem.id) + '.wem')
                with open(wem_file, 'wb') as f:
                    f.write(wem_data)

    def unpack_wem(self, output_dir, wem_id):
        os.makedirs(output_dir, exist_ok=True)
        with self.audio.stream(self.audio_path, 'rb') as bs:
            for wem in self.wems:
                if wem.id == wem_id:
                    bs.seek(self.get_wem_offset(wem))
                    wem_data = bs.read(wem.size)
                    wem_file = os.path.join(output_dir, str(wem.id) + '.wem')
                    with open(wem_file, 'wb') as f:
                        f.write(wem_data)
                    break

    def pack(self, output_file):
        if self.bnk_audio_parsing:
            wem_datas = []
            for wem in self.wems:
                wem_file = self.get_cache_wem_file(wem.id)
                with open(wem_file, 'rb') as f:
                    wem_datas.append(f.read())
            write_bnk(output_file, self.audio, wem_datas) 
        else:
            wem_datas = []
            for wem in self.wems:
                wem_file = self.get_cache_wem_file(wem.id)
                with open(wem_file, 'rb') as f:
                    wem_datas.append(f.read())
            write_wpk(output_file, self.audio, wem_datas)

    def get_cache_dir(self):
        return os.path.join(BNKParser.cache_dir, os.path.basename(self.audio_path).replace('.bnk', '') if self.bnk_audio_parsing else os.path.basename(self.audio_path).replace('.wpk', ''))

    def get_cache_wem_file(self, wem_id):
        return os.path.join(self.get_cache_dir(), f'{wem_id}.wem')

    def play(self, wem_id):
        def play_thrd():
            wem_file = self.get_cache_wem_file(wem_id)
            if not os.path.exists(wem_file):
                self.unpack_wem(self.get_cache_dir(), wem_id)
            ogg_file = wem_file.replace('.wem', '.ogg')
            if not os.path.exists(ogg_file):
                if ext_tools.WW2OGG.run(wem_file, silent=True).returncode == 0:
                    ext_tools.REVORB.run(ogg_file,silent=True)
            if ogg_file not in BNKParser.cached_segments:
                BNKParser.cached_segments[ogg_file] = AudioSegment.from_ogg(ogg_file)
            self.playbacks.append(_play_with_simpleaudio(BNKParser.cached_segments[ogg_file]))
        
        Thread(target=play_thrd,daemon=True).start()

    def stop(self):
        for playback in self.playbacks:
            playback.stop()
        

def prepare(_LOG):
    global LOG
    LOG = _LOG
    os.makedirs(BNKParser.cache_dir, exist_ok=True)
