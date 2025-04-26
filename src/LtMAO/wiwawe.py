import os, os.path, shutil, json
from subprocess import Popen, CREATE_NO_WINDOW, PIPE
from . import tools, pyRitoFile

# wwise convert stuffs
wwise_console_file = './res/wiwawe/WwiseApp/Authoring/x64/Release/bin/WwiseConsole.exe'
wwise_wproj_file = './res/wiwawe/WwiseLeagueProjects/WWiseLeagueProjects.wproj'

wiwawe_dir = './pref/wiwawe'
wsources_file = f'{wiwawe_dir}/wiwawe.wsources'
input_dir = f'{wiwawe_dir}/input'
ouput_dir = f'{wiwawe_dir}/output'

def copy_wav_to_input(wav_files):
    map_sounds = {}
    for wav_file in wav_files:
        basename = os.path.basename(wav_file).replace('.wav', '')
        if basename not in map_sounds:
            map_sounds[basename] = []
            input_file = os.path.join(input_dir, f'{basename}.wav')
            shutil.copy2(wav_file, input_file)
        map_sounds[basename].append(wav_file)
    return map_sounds

def generate_wsources(map_sounds):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    lines.append(f'<ExternalSourcesList SchemaVersion="1" Root="{os.path.abspath(input_dir)}">\n')
    for basename in map_sounds:
        lines.append(f'\t<Source Path="{basename}.wav" Conversion="Vorbis Quality High" />\n')
    lines.append('</ExternalSourcesList>')
    with open(wsources_file, 'w+') as f:
        f.writelines(lines)

def convert_inputs():
    cmds = [
        wwise_console_file,
        'convert-external-source',
        os.path.abspath(wwise_wproj_file),
        '--source-file',
        os.path.abspath(wsources_file),
        '--output',
        os.path.abspath(ouput_dir)
    ]
    p = Popen(
        cmds, creationflags=CREATE_NO_WINDOW,
        stdout=PIPE, stderr=PIPE
    )
    tools.block_and_stream_process_output(p, 'WwiseConsole: ')

def copy_output_to_wem(map_sounds):
    map_wems = {}
    for root, dirs, files in os.walk(ouput_dir):
        for file in files:
            if file.endswith('.wem'):
                basename = file.replace('.wem', '')
                map_wems[basename] = os.path.join(root, file)

    for basename in map_sounds:
        if basename in map_wems:
            for wav_file in map_sounds[basename]:
                wem_file = wav_file.replace('.wav', '.wem')
                shutil.copy2(map_wems[basename], wem_file)

def reset_cache():
    shutil.rmtree(input_dir, ignore_errors=True)
    shutil.rmtree(ouput_dir, ignore_errors=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(ouput_dir, exist_ok=True)
    if os.path.exists(wsources_file):
        os.remove(wsources_file)

def wav2wem(wav_files):
    map_sounds = copy_wav_to_input(wav_files)
    generate_wsources(map_sounds)
    convert_inputs()
    copy_output_to_wem(map_sounds)
    reset_cache()

def wem2wav(wem_files):
    for wem_file in wem_files:
        tools.VGMStream.to_wav(wem_file)

# event bnk stuffs
def list_wem_inside_bank(bank_file, is_bnk):
    from LtMAO.pyRitoFile import BNKObjectType
    if is_bnk:
        bank = pyRitoFile.read_bnk(bank_file)
        if bank.hirc != None:
            # maps
            hirc = bank.hirc
            map_bnk_objects = {}
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
            # list wem - copied bnk tool codes
            listed_wems = []
            for event_id, event in map_bnk_objects[BNKObjectType.Event].items():
                for action_id in event.action_ids:
                    action = map_bnk_objects[BNKObjectType.Action][action_id]
                    if hasattr(action, 'object_id'):
                        if action.type != 4: # play 
                            continue
                        if action.object_id in map_bnk_objects[BNKObjectType.RandomOrSequenceContainer]:
                            container = map_bnk_objects[BNKObjectType.RandomOrSequenceContainer][action.object_id]
                            for sound_id in container.sound_ids: 
                                if sound_id in map_bnk_objects[BNKObjectType.Sound]: 
                                    wem_id = map_bnk_objects[BNKObjectType.Sound][sound_id].wem_id
                                    if wem_id not in listed_wems:
                                        listed_wems.append(wem_id)
                        if action.object_id in map_bnk_objects[BNKObjectType.Sound]:
                            wem_id = map_bnk_objects[BNKObjectType.Sound][action.object_id].wem_id
                            if wem_id not in listed_wems:
                                listed_wems.append(wem_id)
                        if action.object_id in map_bnk_objects[BNKObjectType.MusicPlaylistContainer]:
                            for music_track_id in map_bnk_objects[BNKObjectType.MusicPlaylistContainer][action.object_id].music_track_ids:
                                if music_track_id in map_bnk_objects[BNKObjectType.MusicSegment]:
                                    music_segment_id = music_track_id
                                    for real_music_track_id in map_bnk_objects[BNKObjectType.MusicSegment][music_segment_id].music_track_ids:
                                        for wem_id in map_bnk_objects[BNKObjectType.MusicTrack][real_music_track_id].wem_ids:
                                            if wem_id not in listed_wems:
                                                listed_wems.append(wem_id)
                        if action.object_id in map_bnk_objects[BNKObjectType.SwitchContainer]:
                            def list_ranseq_container_wems(ranseq_container_id):
                                if ranseq_container_id in map_bnk_objects[BNKObjectType.RandomOrSequenceContainer]:
                                    ranseq_container = map_bnk_objects[BNKObjectType.RandomOrSequenceContainer][ranseq_container_id]
                                    for sound_id in ranseq_container.sound_ids:
                                        if sound_id in map_bnk_objects[BNKObjectType.RandomOrSequenceContainer]:
                                            list_ranseq_container_wems(sound_id)
                                        elif sound_id in map_bnk_objects[BNKObjectType.Sound]:
                                            wem_id = map_bnk_objects[BNKObjectType.Sound][sound_id].wem_id
                                            if wem_id not in listed_wems:
                                                listed_wems.append(wem_id)
                            switch_container = map_bnk_objects[BNKObjectType.SwitchContainer][action.object_id]
                            for child_id in switch_container.child_ids:
                                list_ranseq_container_wems(child_id)
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
                                                        if wem_id not in listed_wems:
                                                            listed_wems.append(wem_id)  
                            find_music_playlist_container_child(action.object_id)
            for music_track_id, music_track in map_bnk_objects[BNKObjectType.MusicTrack].items():
                for wem_id in music_track.wem_ids:
                    if wem_id not in listed_wems:
                        listed_wems.append(wem_id)  
                
            return sorted(listed_wems)
        if bank.didx != None:
            return sorted(wem.id for wem in bank.didx.wems)
    else:
        bank = pyRitoFile.read_wpk(bank_file)
        return sorted(wem.id for wem in bank.wems)


def generate_events_bnk_json(events_bnks_dir, events_bnks_file):
    events_bnks = {}
    for lang in os.listdir(events_bnks_dir):
        events_bnks[lang] = {}
        lang_path = os.path.join(events_bnks_dir, lang).replace('\\', '/')
        for root, dirs, files in os.walk(lang_path):
            for file in files:
                if file.endswith('_events.bnk'):
                    bnk_path = os.path.join(root, file)
                    events_bnks[lang][file] = list_wems_insdie_events_bnk(pyRitoFile.read_bnk(bnk_path))
        print(f'Finish: {lang_path}')
    # save to file
    with open(events_bnks_file, 'w+') as f:
        json.dump(events_bnks, f)

events_bnk_file = './res/wiwawe/events_bnks.json'
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
        result_text = '\n'.join(f'{res[r]/wem_count*100:.2f}%: {r}: {res[r]}/{wem_count} wems' for r in res)
        print(f'Result: {bank_file}:\n{result_text}')
    else:
        print(f'Could not guess {bank_file} name. Nothing i can do.')
       

def init():
    os.makedirs(wiwawe_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(ouput_dir, exist_ok=True)
