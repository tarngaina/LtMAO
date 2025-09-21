from . import lepath, tools, pyRitoFile, hash_helper

import os, os.path, time, io, json
from natsort import os_sorted
from shutil import rmtree
import pyaudio, wave, audioop


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
                'bnk_tool: Error: Parse BNK: No DIDX section found in audio BNK.')
        if audio_bnk.data == None:
            raise Exception(
                'bnk_tool: Error: Parse BNK: No DATA section found in audio BNK.')
        return audio_bnk.didx, audio_bnk.data

    @staticmethod
    def parse_events_bnk(events_bnk):
        if events_bnk.hirc == None:
            raise Exception(
                'bnk_tool: Error: Parse BNK: No HIRC section found in events BNK.')
        hirc = events_bnk.hirc
        map_bnk_objects = {}
        # yes only map wat we want to easy debug, its hell
        bnk_obj_types_need_to_be_mapped = [
            pyRitoFile.bnk.BNKObjectType.Sound,
            pyRitoFile.bnk.BNKObjectType.Event,
            pyRitoFile.bnk.BNKObjectType.Action,
            pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer,
            pyRitoFile.bnk.BNKObjectType.SwitchContainer,
            pyRitoFile.bnk.BNKObjectType.MusicSegment,
            pyRitoFile.bnk.BNKObjectType.MusicTrack,
            pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer,
            pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer
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
        SkinCharacterDataPropertiess = bin.get_items(lambda entry: entry.type == hash_helper.Storage.bin_hashes['SkinCharacterDataProperties'])
        for SkinCharacterDataProperties in SkinCharacterDataPropertiess:
            skinAudioPropertiess = SkinCharacterDataProperties.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['skinAudioProperties'])
            for skinAudioProperties in skinAudioPropertiess:
                bankUnitss = skinAudioProperties.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['bankUnits'])
                for bankUnits in bankUnitss:
                    for BankUnit in bankUnits.data:
                        eventss = BankUnit.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['events'])
                        for events in eventss:
                            for event_name in events.data:
                                map_event_namnes[pyRitoFile.helper.FNV1(event_name)] = event_name
        # parse feature bin
        FeatureAudioDataPropertiess =  bin.get_items(lambda entry: entry.type == hash_helper.Storage.bin_hashes['FeatureAudioDataProperties'])
        for FeatureAudioDataProperties in FeatureAudioDataPropertiess:
            bankUnitss = FeatureAudioDataProperties.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['bankUnits'])
            for bankUnits in bankUnitss:
                for BankUnit in bankUnits.data:
                    eventss = BankUnit.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['events'])
                    for events in eventss:
                        for event_name in events.data:
                            map_event_namnes[pyRitoFile.helper.FNV1(event_name)] = event_name
        # parse map bin
        MapAudioDataPropertiess =  bin.get_items(lambda entry: entry.type == hash_helper.Storage.bin_hashes['MapAudioDataProperties'])
        for MapAudioDataProperties in MapAudioDataPropertiess:
            bankUnitss = MapAudioDataProperties.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['bankUnits'])
            for bankUnits in bankUnitss:
                for BankUnit in bankUnits.data:
                    eventss = BankUnit.get_items(lambda field: field.hash == hash_helper.Storage.bin_hashes['events'])
                    for events in eventss:
                        for event_name in events.data:
                            map_event_namnes[pyRitoFile.helper.FNV1(event_name)] = event_name
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
        wem_founds = {wem_id: False for wem_id in existed_wems}
        for event_id, event in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Event].items():
            bank_tree.events[event_id] = bank_event = BankEvent(event_id)
            for action_id in event.action_ids:
                action = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Action][action_id]
                if hasattr(action, 'object_id'):
                    if action.type != 4: # play 
                        continue

                    # ranseq container sound ids could point to another ranseq container 
                    # if sound id point to sound then list wem, otherwise keep dfs
                    def list_ranseq_container_wems(ranseq_container_id):          
                        if ranseq_container_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer]:
                            ranseq_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer][ranseq_container_id]
                            for sound_id in ranseq_container.sound_ids:
                                # sound id point to another ranseq container, dfs
                                if sound_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer]:
                                    list_ranseq_container_wems(sound_id)
                                # sound id point to a switch container instead
                                elif sound_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer]:
                                    switch_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer][sound_id]
                                    for child_id in switch_container.child_ids:
                                        list_ranseq_container_wems(child_id)
                                # list wem if point to sound object
                                elif sound_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound]:
                                    wem_id = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound][sound_id].wem_id
                                    if wem_id not in existed_wems:
                                        continue
                                    wem_founds[wem_id] = True
                                    # create container if need
                                    if ranseq_container_id not in bank_event.containers:
                                        bank_event.containers[ranseq_container_id] = BankContainer(ranseq_container_id)
                                    # add wem to container
                                    bank_container = bank_event.containers[ranseq_container_id]
                                    if wem_id not in bank_container.wems:
                                        bank_container.wems[wem_id] = BankWem(wem_id)
                                    # remove wem if they in non containers 
                                    if wem_id in bank_event.wems:
                                        bank_event.wems.pop(wem_id)
                        
                    # if action link to ranseq container object
                    if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer]:
                        list_ranseq_container_wems(action.object_id)
                                
                    # if action link to sound object
                    if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound]:
                        wem_id = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound][action.object_id].wem_id
                        if wem_id not in existed_wems:
                            continue
                        wem_founds[wem_id] = True
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
                    if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer]:
                        switch_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer][action.object_id]
                        for child_id in switch_container.child_ids:
                            list_ranseq_container_wems(child_id)

                    # if action link to a music playlist container
                    # music tracks of music playlist container could point to music segment 
                    # list wem inside those segments 
                    if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer]:
                        for music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer][action.object_id].music_track_ids:
                            if music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment]:
                                music_segment_id = music_track_id
                                for real_music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                    for wem_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                        if wem_id not in existed_wems:
                                            continue
                                        wem_founds[wem_id] = True
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
                    if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer]:
                        def find_music_playlist_container_child(switch_container_id):
                            switch_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer][switch_container_id]
                            for child_id in switch_container.child_ids:
                                # child id point to another music switch container, keep dfs
                                if child_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer]:
                                    find_music_playlist_container_child(child_id)
                                # point to music playlist container, list wems
                                elif child_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer]:
                                    music_playlist_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer][child_id]
                                    for music_track_id in music_playlist_container.music_track_ids:
                                        if music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment]:
                                            music_segment_id = music_track_id
                                            for real_music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                                for wem_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                                    if wem_id not in existed_wems:
                                                        continue
                                                    wem_founds[wem_id] = True
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

        # list wem that not found
        for wem_id, wem_found in wem_founds.items():
            if not wem_found and wem_id not in bank_tree.wems:
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

    def __init__(self, audio_path, events_path='', bin_path='', volume=0.5):
        self.volume = volume
        self.port = pyaudio.PyAudio()
        self.streams = []
        self.audio_path = audio_path
        # parse audio.bnk or audio.wpk
        self.is_bnk = True if audio_path.endswith('.bnk') else False
        if self.is_bnk:
            self.audio = pyRitoFile.bnk.BNK().read(audio_path)
            self.didx, self.data = BankHelper.parse_audio_bnk(self.audio)
            self.wems = self.didx.wems
        else:
            self.audio = pyRitoFile.wpk.WPK().read(audio_path)
            self.wems = self.audio.wems
        # parse events.bnk
        map_bnk_objects = None
        if events_path != '':
            events_bnk = pyRitoFile.bnk.BNK().read(events_path)
            map_bnk_objects = BankHelper.parse_events_bnk(events_bnk)
        # parse bin
        map_event_namnes = {}
        if bin_path != '':
            bin = pyRitoFile.bin.BIN().read(bin_path)
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
                wav_file = lepath.ext(cache_wem_file, '.wem', '.wav')
                if os.path.exists(wav_file):
                    os.remove(wav_file)

    def extract(self, output_dir, convert_wavs=True):
        map_wem_paths = {}
        for wem in self.wems:
            map_wem_paths[wem.id] = []
        # read tree -> create dirs first -> map wem path to extract
        bank_tree = self.bank_tree
        tree_dir = output_dir
        os.makedirs(tree_dir, exist_ok=True)
        for event_id in bank_tree.events:
            bank_event = bank_tree.events[event_id]
            event_dir = lepath.join(output_dir, str(event_id))
            os.makedirs(event_dir, exist_ok=True)
            for container_id in bank_event.containers:
                bank_container = bank_event.containers[container_id]
                container_dir = lepath.join(event_dir, str(container_id))
                os.makedirs(container_dir, exist_ok=True)
                # map wems inside container
                for wem_id in bank_container.wems:
                    wem_file = lepath.join(container_dir, f'{wem_id}.wem')
                    map_wem_paths[wem_id].append(wem_file)
            # map wems inside event
            for wem_id in bank_event.wems:
                wem_file = lepath.join(event_dir, f'{wem_id}.wem')
                map_wem_paths[wem_id].append(wem_file)
        # map wems inside tree
        for wem_id in bank_tree.wems:
            wem_file = lepath.join(tree_dir, f'{wem_id}.wem')
            map_wem_paths[wem_id].append(wem_file)
        # extract wems with map
        with pyRitoFile.stream.BytesStream.reader(self.audio_path) as bs:
            for wem in self.wems:
                bs.seek(self.get_wem_offset(wem))
                wem_data = bs.read(wem.size)
                for wem_file in map_wem_paths[wem.id]:
                    with open(wem_file, 'wb') as f:
                        f.write(wem_data)
                    if convert_wavs:
                        tools.VGMStream.to_wav(wem_file)
                print(f'bnk_tool: Finish: Extracted [{BankHelper.to_human(wem.size)}] {wem.id}.wem')
                    
    def unpack(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        with pyRitoFile.stream.BytesStream.reader(self.audio_path) as bs:
            for wem in self.wems:
                bs.seek(self.get_wem_offset(wem))
                wem_data = bs.read(wem.size)
                wem_file = lepath.join(output_dir, str(wem.id) + '.wem')
                with open(wem_file, 'wb') as f:
                    f.write(wem_data)

    def unpack_wem(self, output_dir, wem_id):
        os.makedirs(output_dir, exist_ok=True)
        with pyRitoFile.stream.BytesStream.reader(self.audio_path) as bs:
            for wem in self.wems:
                if wem.id == wem_id:
                    bs.seek(self.get_wem_offset(wem))
                    wem_data = bs.read(wem.size)
                    wem_file = lepath.join(output_dir, str(wem.id) + '.wem')
                    with open(wem_file, 'wb') as f:
                        f.write(wem_data)
                    break

    def pack(self, output_file):
        wem_datas = []
        for wem in self.wems:
            wem_file = self.get_cache_wem_file(wem.id)
            with open(wem_file, 'rb') as f:
                wem_datas.append(f.read())
        self.audio.write(output_file, wem_datas)

    def get_cache_dir(self):
        return lepath.join(
            Inspector.cache_dir, 
            lepath.ext(os.path.basename(self.audio_path), '.bnk', '') 
            if self.is_bnk 
            else lepath.ext(os.path.basename(self.audio_path), '.wpk', '')
    )

    def get_cache_wem_file(self, wem_id):
        return lepath.join(self.get_cache_dir(), f'{wem_id}.wem')

    # need to play in thread
    def play(self, wem_id, stop_previous=True):
        wem_file = self.get_cache_wem_file(wem_id)
        if not os.path.exists(wem_file):
            self.unpack_wem(self.get_cache_dir(), wem_id)
        wav_file = lepath.ext(wem_file, '.wem', '.wav')
        if not os.path.exists(wav_file):
            tools.VGMStream.to_wav(wem_file)
        if stop_previous:
            self.stop()
        with open(wav_file, 'rb') as f:
            wav_data = f.read()
        with wave.open(io.BytesIO(wav_data), 'rb') as wav:
            sampwidth = wav.getsampwidth()
            def play_callback(in_data, frame_count, time_info, status):
                return (audioop.mul(wav.readframes(frame_count), sampwidth, self.volume), pyaudio.paContinue)
            stream = self.port.open(
                format=self.port.get_format_from_width(sampwidth),
                channels=wav.getnchannels(),
                rate=wav.getframerate(),
                output=True,
                stream_callback=play_callback
            )
            self.streams.append(stream)
            while stream.is_active():
                time.sleep(0.1) 
            stream.close()

    def stop(self):
        for stream in self.streams:
            stream.stop_stream()

def bnk2dir(input_file, output_dir, events_file = '', bin_file = ''):
    inspector = Inspector(input_file, events_file, bin_file) 
    inspector.extract(output_dir, convert_wavs=False)
    print(f'wad_tool: Finish: Unpack: {output_dir}')

def dir2bnk(input_dir, output_file, is_bnk):
    wem_files = {os.path.basename(wem): wem for wem in lepath.walk(input_dir, lambda f: f.endswith('.wem'))}.values()
    if is_bnk:
        audio = pyRitoFile.bnk.BNK()
        audio.didx = pyRitoFile.bnk.BNKSectionData()
        audio.didx.wems = []
        wem_datas = []
        for wem_file in wem_files:
            wem_id = lepath.ext(os.path.basename(wem_file), '.wem', '')
            if wem_id.isnumeric():
                wem_id = int(wem_id)
                wem = pyRitoFile.bnk.BNKWem()
                wem.id = wem_id
                with open(wem_file, 'rb') as f:
                    wem_datas.append(f.read())
                audio.didx.wems.append(wem)
        audio.write(output_file, wem_datas) 
    else:
        audio = pyRitoFile.wpk.WPK()
        audio.wems = []
        wem_datas = []
        for wem_file in wem_files:
            wem_id = lepath.ext(os.path.basename(wem_file), '.wem', '')
            if wem_id.isnumeric():
                wem_id = int(wem_id)
                wem = pyRitoFile.wpk.WPKWem()
                wem.id = wem_id
                with open(wem_file, 'rb') as f:
                    wem_datas.append(f.read())
                audio.wems.append(wem)
        audio.write(output_file, wem_datas)
    print(f'wad_tool: Finish: Pack: {output_file}')
    
# event bnk stuffs
def list_wem_inside_bank(bank_file, is_bnk):
    if is_bnk:
        bank = pyRitoFile.bnk.BNK().read(bank_file)
        if bank.hirc != None:
            # maps
            hirc = bank.hirc
            map_bnk_objects = {}
            bnk_obj_types_need_to_be_mapped = [
                pyRitoFile.bnk.BNKObjectType.Sound,
                pyRitoFile.bnk.BNKObjectType.Event,
                pyRitoFile.bnk.BNKObjectType.Action,
                pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer,
                pyRitoFile.bnk.BNKObjectType.SwitchContainer,
                pyRitoFile.bnk.BNKObjectType.MusicSegment,
                pyRitoFile.bnk.BNKObjectType.MusicTrack,
                pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer,
                pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer
            ]
            for object_type in bnk_obj_types_need_to_be_mapped:
                map_bnk_objects[object_type] = {}
            for obj in hirc.objects:
                if obj.type in bnk_obj_types_need_to_be_mapped:
                    map_bnk_objects[obj.type][obj.id] = obj.data
            # list wem - copied bnk tool codes
            listed_wems = []
            for event_id, event in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Event].items():
                for action_id in event.action_ids:
                    action = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Action][action_id]
                    if hasattr(action, 'object_id'):
                        if action.type != 4: # play 
                            continue
                        # ranseq container sound ids could point to another ranseq container 
                        # if sound id point to sound then list wem, otherwise keep dfs
                        def list_ranseq_container_wems(ranseq_container_id):          
                            if ranseq_container_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer]:
                                ranseq_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer][ranseq_container_id]
                                for sound_id in ranseq_container.sound_ids:
                                    # sound id point to another ranseq container, dfs
                                    if sound_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer]:
                                        list_ranseq_container_wems(sound_id)
                                    # sound id point to a switch container instead
                                    elif sound_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer]:
                                        switch_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer][sound_id]
                                        for child_id in switch_container.child_ids:
                                            list_ranseq_container_wems(child_id)
                                    # list wem if point to sound object
                                    elif sound_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound]:
                                        wem_id = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound][sound_id].wem_id
                                        if wem_id not in listed_wems:
                                            listed_wems.append(wem_id)
                        # if action link to ranseq container object
                        if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.RandomOrSequenceContainer]:
                            list_ranseq_container_wems(action.object_id)
                        # if action link to sound object
                        if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound]:
                            wem_id = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.Sound][action.object_id].wem_id
                            if wem_id not in listed_wems:
                                listed_wems.append(wem_id)
                        # if action link to a switch container 
                        # switch container child point to ranseq container
                        if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer]:
                            switch_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.SwitchContainer][action.object_id]
                            for child_id in switch_container.child_ids:
                                list_ranseq_container_wems(child_id)
                        # if action link to a music playlist container
                        # music tracks of music playlist container could point to music segment 
                        # list wem inside those segments 
                        if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer]:
                            for music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer][action.object_id].music_track_ids:
                                if music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment]:
                                    music_segment_id = music_track_id
                                    for real_music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                        for wem_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                            if wem_id not in listed_wems:
                                                listed_wems.append(wem_id)
                        # if action link to a music switch container  
                        # music switch container can have another music switch container as child
                        # keep dfs the child until the child appear as music playlist container
                        # list all wems inside music play list container same method as above
                        if action.object_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer]:
                            def find_music_playlist_container_child(switch_container_id):
                                switch_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer][switch_container_id]
                                for child_id in switch_container.child_ids:
                                    # child id point to another music switch container, keep dfs
                                    if child_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSwitchContainer]:
                                        find_music_playlist_container_child(child_id)
                                    # point to music playlist container, list wems
                                    elif child_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer]:
                                        music_playlist_container = map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicPlaylistContainer][child_id]
                                        for music_track_id in music_playlist_container.music_track_ids:
                                            if music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment]:
                                                music_segment_id = music_track_id
                                                for real_music_track_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                                    for wem_id in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                                        if wem_id not in listed_wems:
                                                            listed_wems.append(wem_id)
                            find_music_playlist_container_child(action.object_id)
                for music_track_id, music_track in map_bnk_objects[pyRitoFile.bnk.BNKObjectType.MusicTrack].items():
                    for wem_id in music_track.wem_ids:
                        if wem_id not in listed_wems:
                            listed_wems.append(wem_id)  
            return sorted(listed_wems)
        if bank.didx != None:
            return sorted(wem.id for wem in bank.didx.wems)
    else:
        bank = pyRitoFile.wpk.WPK().read(bank_file)
        return sorted(wem.id for wem in bank.wems)

def generate_events_bnk_json(events_bnks_dir, events_bnks_file):
    events_bnks = {}
    for lang in os.listdir(events_bnks_dir):
        events_bnks[lang] = {}
        lang_path = lepath.join(events_bnks_dir, lang)
        for root, dirs, files in os.walk(lang_path):
            for file in files:
                if file.endswith('_events.bnk'):
                    bnk_path = lepath.join(root, file)
                    events_bnks[lang][file] = list_wem_inside_bank(pyRitoFile.bnk.BNK().read(bnk_path))
        print(f'Finish: {lang_path}')
    # save to file
    with open(events_bnks_file, 'w+') as f:
        json.dump(events_bnks, f)

events_bnk_file = './res/bnk_tool/events_bnks.json'
def guess_events_bnk(bank_file):
    # list bnk wems
    wems = list_wem_inside_bank(bank_file, is_bnk=bank_file.endswith('.bnk'))
    # open generated events bnks
    with open(events_bnk_file, 'r') as f:
        events_bnks = json.load(f)
    # find all result 
    res = {}
    for lang in events_bnks:
        for file in events_bnks[lang]:
            for wem in wems:
                if wem in events_bnks[lang][file]:
                    r = f'{lang}/{file}'
                    if r not in res:
                        res[r] = 0
                    res[r] += 1
    # output
    res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    wem_count = len(wems)
    if len(res) > 0:
        result_text = '\n'.join(f'{res[r]/wem_count*100:.2g}%: {r}: {res[r]}/{wem_count} wems' for r in res)
        print(f'Compared result: {bank_file}:\n{result_text}')
    else:
        print(f'Could not guess {bank_file} name. Nothing i can do.')
       

def init():
    os.makedirs(Inspector.cache_dir, exist_ok=True)
