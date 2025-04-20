from .pyRitoFile import BNKObjectType, BINHelper, read_bnk, read_wpk, read_bin, write_bnk, write_wpk, BNK, WPK
from .pyRitoFile.helper import FNV1
from .hash_helper import cached_bin_hashes
from . import tools, pyRitoFile

import os
import os.path
from natsort import os_sorted
from shutil import rmtree
from threading import Thread
import pyaudio, wave


class BankTree:
    __slots__ = ('events', 'wems')

    def __init__(self):
        self.events = {}
        self.wems = {}

class BankEvent:
    __slots__ = ('id', 'containers', 'wems')

    def __init__(self, id):
        self.id = id
        self.containers = {}
        self.wems = {}

class BankContainer:
    __slots__ = ('id', 'wems')

    def __init__(self, id):
        self.id = id
        self.wems = {}

class BankWem:
    __slots__ = ('id')

    def __init__(self, id):
        self.id = id

class BankHelper:
    @staticmethod
    def to_human(size): 
        return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) +  ["", " KB", " MB", " GB", " TB", " PB", " EB"][max(size.bit_length()-1, 0)//10]
    
    @staticmethod
    def parse_audio_bnk(audio_bnk):
        if audio_bnk.didx == None:
            raise Exception(
                'bnk_tool: Error: Extract BNK: No DIDX section found in audio BNK.')
        if audio_bnk.data == None:
            raise Exception(
                'bnk_tool: Error: Extract BNK: No DATA section found in audio BNK.')
        return audio_bnk.didx, audio_bnk.data

    @staticmethod
    def parse_events_bnk(events_bnk):
        if events_bnk.hirc == None:
            raise Exception(
                'bnk_tool: Error: Extract BNK: No HIRC section found in events BNK.')
        hirc = events_bnk.hirc
        map_bnk_objects = {}
        # yes only map wat we want to easy debug, its hell
        bnk_obj_types_need_to_be_mapped = [
            BNKObjectType.Sound,
            BNKObjectType.Event,
            BNKObjectType.Action,
            BNKObjectType.RandomOrSequenceContainer,
            BNKObjectType.SwitchContainer,
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

    @staticmethod
    def parse_bin(bin):
        map_event_namnes = {}
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
                            map_event_namnes[FNV1(event)] = event
        # parse feature bin
        FeatureAudioDataPropertiesCollection = BINHelper.find_items(
            items=bin.entries,
            compare_func=lambda entry: entry.type == cached_bin_hashes['FeatureAudioDataProperties']
        )
        if len(FeatureAudioDataPropertiesCollection) > 0:
            for FeatureAudioDataProperties in FeatureAudioDataPropertiesCollection:
                if FeatureAudioDataProperties != None:
                    bankUnitsCollection = BINHelper.find_items(
                        items=FeatureAudioDataProperties.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['bankUnits']
                    )
                    if len(bankUnitsCollection) > 0:
                        for bankUnits in bankUnitsCollection:
                            if bankUnits != None and len(bankUnits.data) > 0:
                                for BankUnit in bankUnits.data:
                                    events = BINHelper.find_item(
                                        items=BankUnit.data,
                                        compare_func=lambda field: field.hash == cached_bin_hashes['events']
                                    )
                                    if events == None:
                                        continue
                                    for event in events.data:
                                        map_event_namnes[FNV1(event)] = event
        # parse map bin
        MapAudioDataPropertiesCollection = BINHelper.find_items(
            items=bin.entries,
            compare_func=lambda entry: entry.type == cached_bin_hashes['MapAudioDataProperties']
        )
        if len(MapAudioDataPropertiesCollection) > 0:
            for MapAudioDataProperties in MapAudioDataPropertiesCollection:
                if MapAudioDataProperties != None:
                    bankUnitsCollection = BINHelper.find_items(
                        items=MapAudioDataProperties.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['bankUnits']
                    )
                    if len(bankUnitsCollection) > 0:
                        for bankUnits in bankUnitsCollection:
                            if bankUnits != None and len(bankUnits.data) > 0:
                                for BankUnit in bankUnits.data:
                                    events = BINHelper.find_item(
                                        items=BankUnit.data,
                                        compare_func=lambda field: field.hash == cached_bin_hashes['events']
                                    )
                                    if events == None:
                                        continue
                                    for event in events.data:
                                        map_event_namnes[FNV1(event)] = event
        return map_event_namnes

    @staticmethod
    def parse_bank_tree(map_bnk_objects, existed_wems):
        bank_tree = BankTree()
        # if no events file, just display all existed wems inside tree
        if map_bnk_objects == None:
            for wem_id in existed_wems:
                bank_tree.wems[wem_id] = BankWem(wem_id)
            return bank_tree
        # parse if events file
        for event_id, event in map_bnk_objects[BNKObjectType.Event].items():
            bank_tree.events[event_id] = bank_event = BankEvent(event_id)
            for action_id in event.action_ids:
                action = map_bnk_objects[BNKObjectType.Action][action_id]
                if hasattr(action, 'object_id'):
                    if action.type != 4: # play 
                        continue

                    # if action link to ranseq container object
                    if action.object_id in map_bnk_objects[BNKObjectType.RandomOrSequenceContainer]:
                        container = map_bnk_objects[BNKObjectType.RandomOrSequenceContainer][action.object_id]
                        for sound_id in container.sound_ids: 
                            # it not actually a sound object, can point to a blend container too
                            # thats why we check if its in sounds
                            if sound_id in map_bnk_objects[BNKObjectType.Sound]: 
                                wem_id = map_bnk_objects[BNKObjectType.Sound][sound_id].wem_id
                                if wem_id not in existed_wems:
                                    continue
                                # check if wem already in containers, if not add to non containers
                                new_wem = True                 
                                for bank_container_id, bank_container in bank_event.containers.items():
                                    if wem_id in bank_container.wems:
                                        new_wem = False
                                        break
                                if new_wem:
                                    bank_event.wems[wem_id] = BankWem(wem_id)
                                
                    # if action link to sound object
                    if action.object_id in map_bnk_objects[BNKObjectType.Sound]:
                        wem_id = map_bnk_objects[BNKObjectType.Sound][action.object_id].wem_id
                        if wem_id not in existed_wems:
                            continue
                        # check if wem already in containers, if not add to non containers
                        new_wem = True                 
                        for bank_container_id, bank_container in bank_event.containers.items():
                            if wem_id in bank_container.wems:
                                new_wem = False
                                break
                        if new_wem:
                            bank_event.wems[wem_id] = BankWem(wem_id)

                    # if action link to a switch container 
                    # switch container child point to ranseq container
                    # list wem inside ranseq container sounds
                    if action.object_id in map_bnk_objects[BNKObjectType.SwitchContainer]:
                        switch_container = map_bnk_objects[BNKObjectType.SwitchContainer][action.object_id]
                        for child_id in switch_container.child_ids:
                            if child_id in map_bnk_objects[BNKObjectType.RandomOrSequenceContainer]:
                                ranseq_container = map_bnk_objects[BNKObjectType.RandomOrSequenceContainer][child_id]
                                for sound_id in ranseq_container.sound_ids:
                                    wem_id = map_bnk_objects[BNKObjectType.Sound][sound_id].wem_id
                                    if wem_id not in existed_wems:
                                        continue
                                    # create container if need
                                    if child_id not in bank_event.containers:
                                        bank_event.containers[child_id] = BankContainer(child_id)
                                    # add wem to container
                                    bank_container = bank_event.containers[child_id]
                                    if wem_id not in bank_container.wems:
                                        bank_container.wems[wem_id] = BankWem(wem_id)
                                    # remove wem if they in non containers 
                                    if wem_id in bank_event.wems:
                                        bank_event.wems.pop(wem_id)

                    # if action link to a music playlist container
                    # music tracks of music playlist container could point to music segment 
                    # list wem inside those segments 
                    if action.object_id in map_bnk_objects[BNKObjectType.MusicPlaylistContainer]:
                        for music_track_id in map_bnk_objects[BNKObjectType.MusicPlaylistContainer][action.object_id].music_track_ids:
                            if music_track_id in map_bnk_objects[BNKObjectType.MusicSegment]:
                                music_segment_id = music_track_id
                                for real_music_track_id in map_bnk_objects[BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                    for wem_id in map_bnk_objects[BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                        if wem_id not in existed_wems:
                                            continue
                                        # create container if need
                                        if music_segment_id not in bank_event.containers:
                                            bank_event.containers[music_segment_id] = BankContainer(music_segment_id)
                                        # add wem to container
                                        bank_container = bank_event.containers[music_segment_id]
                                        if wem_id not in bank_container.wems:
                                            bank_container.wems[wem_id] = BankWem(wem_id)
                                        # remove wem if they in non containers 
                                        if wem_id in bank_event.wems:
                                            bank_event.wems.pop(wem_id)

                    # if action link to a music switch container  
                    # music switch container can have another music switch container as child
                    # keep dfs the child until the child appear as music playlist container
                    # list all wems inside music play list container same method as above
                    if action.object_id in map_bnk_objects[BNKObjectType.MusicSwitchContainer]:
                        def find_music_playlist_container_child(switch_container_id):
                            switch_container = map_bnk_objects[BNKObjectType.MusicSwitchContainer][switch_container_id]
                            for child_id in switch_container.child_ids:
                                if child_id in map_bnk_objects[BNKObjectType.MusicSwitchContainer]:
                                    find_music_playlist_container_child(child_id)
                                elif child_id in map_bnk_objects[BNKObjectType.MusicPlaylistContainer]:
                                    music_playlist_container = map_bnk_objects[BNKObjectType.MusicPlaylistContainer][child_id]
                                    for music_track_id in music_playlist_container.music_track_ids:
                                        if music_track_id in map_bnk_objects[BNKObjectType.MusicSegment]:
                                            music_segment_id = music_track_id
                                            for real_music_track_id in map_bnk_objects[BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                                for wem_id in map_bnk_objects[BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                                    if wem_id not in existed_wems:
                                                        continue
                                                    # create container if need
                                                    if child_id not in bank_event.containers:
                                                        bank_event.containers[child_id] = BankContainer(child_id)
                                                    # add wem to container
                                                    bank_container = bank_event.containers[child_id]
                                                    if wem_id not in bank_container.wems:
                                                        bank_container.wems[wem_id] = BankWem(wem_id)
                                                    # remove wem if they in non containers 
                                                    if wem_id in bank_event.wems:
                                                        bank_event.wems.pop(wem_id)    

                        find_music_playlist_container_child(action.object_id)

        # list music track wems that dont link to anything????
        for music_track_id, music_track in map_bnk_objects[BNKObjectType.MusicTrack].items():
            for wem_id in music_track.wem_ids:
                if wem_id not in existed_wems:
                    continue
                new_wem = True
                for event_id in bank_tree.events:
                    bank_event = bank_tree.events[event_id]
                    for container_id in bank_event.containers:
                        bank_container = bank_event.containers[container_id]
                        if wem_id in bank_container.wems:
                            new_wem = False
                if new_wem and wem_id not in bank_tree.wems:
                    bank_tree.wems[wem_id] = BankWem(wem_id)
        # clean up empty event           
        empty_event_ids = []                 
        for event_id in bank_tree.events:
            if len(bank_tree.events[event_id].containers) == 0 and len(bank_tree.events[event_id].wems) == 0:
                empty_event_ids.append(event_id)
        for event_id in empty_event_ids:
            bank_tree.events.pop(event_id)
        return bank_tree

    @staticmethod
    def unhash_bank_tree(bank_tree, event_names_by_id):
        for event_id, event_name in event_names_by_id.items():
            if event_id in bank_tree.events:
                bank_tree.events[event_name] = bank_tree.events.pop(event_id)

    @staticmethod
    def sort_bank_tree(bank_tree):
        for event_id in bank_tree.events:
            bank_event = bank_tree.events[event_id]
            for container_id in bank_event.containers:
                bank_container = bank_event.containers[container_id]
                # sort wems inside container
                bank_container.wems = dict(os_sorted(bank_container.wems.items()))
            # sort containers inside event
            bank_event.containers = dict(os_sorted(bank_event.containers.items()))
            # sort wems inside event
            bank_event.wems = dict(os_sorted(bank_event.wems.items()))
        # sort events inside tree
        bank_tree.events = dict(os_sorted(bank_tree.events.items()))
        # sort wems inside tree
        bank_tree.wems = dict(os_sorted(bank_tree.wems.items()))

class Inspector:
    cache_dir = './pref/bnk_tool'
    
    @staticmethod
    def reset_cache():
        rmtree(Inspector.cache_dir, ignore_errors=True)
        os.makedirs(Inspector.cache_dir, exist_ok=True)

    def __init__(self, audio_path, events_path='', bin_path=''):
        self.streams = []
        self.audio_path = audio_path
        # parse audio.bnk or audio.wpk
        self.is_bnk = True if audio_path.endswith('.bnk') else False
        if self.is_bnk:
            self.audio = read_bnk(audio_path)
            self.didx, self.data = BankHelper.parse_audio_bnk(self.audio)
            self.wems = self.didx.wems
        else:
            self.audio = read_wpk(audio_path)
            self.wems = self.audio.wems
        # parse events.bnk
        map_bnk_objects = None
        if events_path != '':
            events_bnk = read_bnk(events_path)
            map_bnk_objects = BankHelper.parse_events_bnk(events_bnk)
        # parse bin
        map_event_namnes = {}
        if bin_path != '':
            bin = read_bin(bin_path)
            map_event_namnes = BankHelper.parse_bin(bin)
        # parse bank tree
        self.bank_tree = BankHelper.parse_bank_tree(map_bnk_objects, [wem.id for wem in self.wems])
        BankHelper.unhash_bank_tree(self.bank_tree, map_event_namnes)
        BankHelper.sort_bank_tree(self.bank_tree)

    def get_wem_offset(self, wem):
        return self.data.start_offset+wem.offset if self.is_bnk else wem.offset

    def replace_wem(self, wem_id, wem_file):
        for wem in self.wems:
            if wem.id == wem_id:
                with open(wem_file, 'rb') as f:
                    wem_data = f.read()
                wem.size = len(wem_data)
                cache_wem_file = self.get_cache_wem_file(wem_id)
                with open(cache_wem_file, 'wb+') as f:
                    f.write(wem_data)
                wav_file = cache_wem_file.replace('.wem', '.wav')
                if os.path.exists(wav_file):
                    os.remove(wav_file)

    def extract(self, output_dir):
        map_wem_paths = {}
        for wem in self.wems:
            map_wem_paths[wem.id] = []
        # read tree -> create dirs first -> map wem path to extract
        bank_tree = self.bank_tree
        tree_dir = output_dir
        os.makedirs(tree_dir, exist_ok=True)
        for event_id in bank_tree.events:
            bank_event = bank_tree.events[event_id]
            event_dir = os.path.join(output_dir, str(event_id))
            os.makedirs(event_dir, exist_ok=True)
            for container_id in bank_event.containers:
                bank_container = bank_event.containers[container_id]
                container_dir = os.path.join(event_dir, str(container_id))
                os.makedirs(container_dir, exist_ok=True)
                # map wems inside container
                for wem_id in bank_container.wems:
                    wem_file = os.path.join(container_dir, f'{wem_id}.wem')
                    map_wem_paths[wem_id].append(wem_file)
            # map wems inside event
            for wem_id in bank_event.wems:
                wem_file = os.path.join(event_dir, f'{wem_id}.wem')
                map_wem_paths[wem_id].append(wem_file)
        # map wems inside tree
        for wem_id in bank_tree.wems:
            wem_file = os.path.join(tree_dir, f'{wem_id}.wem')
            map_wem_paths[wem_id].append(wem_file)
        # extract wems with map
        with self.audio.stream(self.audio_path, 'rb') as bs:
            for wem in self.wems:
                bs.seek(self.get_wem_offset(wem))
                wem_data = bs.read(wem.size)
                for wem_file in map_wem_paths[wem.id]:
                    with open(wem_file, 'wb') as f:
                        f.write(wem_data)
                    tools.VGMStream.to_wav(wem_file)
                print(f'bnk_tool: Finish: Extracted [{BankHelper.to_human(wem.size)}] {wem.id}.wem')
                    
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
        if self.is_bnk:
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
        return os.path.join(Inspector.cache_dir, os.path.basename(self.audio_path).replace('.bnk', '') if self.is_bnk else os.path.basename(self.audio_path).replace('.wpk', ''))

    def get_cache_wem_file(self, wem_id):
        return os.path.join(self.get_cache_dir(), f'{wem_id}.wem')

    def play(self, wem_id):
        def play_thrd():
            wem_file = self.get_cache_wem_file(wem_id)
            if not os.path.exists(wem_file):
                self.unpack_wem(self.get_cache_dir(), wem_id)
            wav_file = wem_file.replace('.wem', '.wav')
            tools.VGMStream.to_wav(wem_file)
            with wave.open(wav_file, 'rb') as wav:
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=p.get_format_from_width(wav.getsampwidth()),
                    channels=wav.getnchannels(),
                    rate=wav.getframerate(),
                    output=True
                )
                self.streams.append(stream)
                while len(data := wav.readframes(1024)):
                    if stream.is_active(): 
                        stream.write(data)
                stream.close()
                p.terminate()
        
        Thread(target=play_thrd, daemon=True).start()

    def stop(self):
        for stream in self.streams:
            stream.stop_stream()

def bnk2dir(audio_path):
    inspector = Inspector(audio_path)
    dir_path = audio_path.replace('.bnk', '').replace('.wpk', '')
    inspector.unpack(dir_path)
    print(f'wad_tool: Finish: Unpack: {dir_path}')

def dir2bnk(dir_path, is_bnk):
    wem_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.wem'):
                wem_file = os.path.join(root, file).replace('\\', '/')
                wem_files.append(wem_file)
    if is_bnk:
        audio_path = dir_path + '.bnk'
        audio = pyRitoFile.BNK()
        audio.didx = pyRitoFile.BNKSectionData()
        audio.didx.wems = []
        wem_datas = []
        for wem_file in wem_files:
            wem_id = os.path.basename(wem_file).replace('.wem', '')
            if wem_id.isnumeric():
                wem_id = int(wem_id)
                wem = pyRitoFile.BNKWem()
                wem.id = wem_id
                with open(wem_file, 'rb') as f:
                    wem_datas.append(f.read())
                audio.didx.wems.append(wem)
        write_bnk(audio_path, audio, wem_datas) 
    else:
        audio_path = dir_path + '.wpk'
        audio = pyRitoFile.WPK()
        audio.wems = []
        wem_datas = []
        for wem_file in wem_files:
            wem_id = os.path.basename(wem_file).replace('.wem', '')
            if wem_id.isnumeric():
                wem_id = int(wem_id)
                wem = pyRitoFile.WPKWem()
                wem.id = wem_id
                with open(wem_file, 'rb') as f:
                    wem_datas.append(f.read())
                audio.wems.append(wem)
        write_wpk(audio_path, audio, wem_datas)
    print(f'wad_tool: Finish: Pack: {audio_path}')
    

def init():
    os.makedirs(Inspector.cache_dir, exist_ok=True)
