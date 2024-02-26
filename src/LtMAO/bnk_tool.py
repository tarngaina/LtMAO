from . import pyRitoFile
from .hash_manager import cached_bin_hashes
import os
import os.path

LOG = print

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
    sounds_by_id = {}
    events_by_id = {}
    actions_by_id = {}
    ranseq_containers_by_id = {}
    for obj in hirc.objects:
        if obj.type == pyRitoFile.BNKObjectType.Sound:
            sounds_by_id[obj.id] = obj.data
        elif obj.type == pyRitoFile.BNKObjectType.Event:
            events_by_id[obj.id] = obj.data
        elif obj.type == pyRitoFile.BNKObjectType.Action:
            actions_by_id[obj.id] = obj.data
        elif obj.type == pyRitoFile.BNKObjectType.RandomOrSequenceContainer:
            ranseq_containers_by_id[obj.id] = obj.data
    return sounds_by_id, events_by_id, actions_by_id, ranseq_containers_by_id


def parse_bin(bin):
    event_names_by_id = {}
    SkinCharacterDataProperties = pyRitoFile.BINHelper.find_item(
        items=bin.entries,
        compare_func=lambda entry: entry.type == cached_bin_hashes['SkinCharacterDataProperties']
    )
    if SkinCharacterDataProperties != None:
        skinAudioProperties = pyRitoFile.BINHelper.find_item(
            items=SkinCharacterDataProperties.data,
            compare_func=lambda field: field.hash == cached_bin_hashes['skinAudioProperties']
        )
        if skinAudioProperties != None:
            bankUnits = pyRitoFile.BINHelper.find_item(
                items=skinAudioProperties.data,
                compare_func=lambda field: field.hash == cached_bin_hashes['bankUnits']
            )
            if bankUnits != None and len(bankUnits.data) > 0:
                for BankUnit in bankUnits.data:
                    events = pyRitoFile.BINHelper.find_item(
                        items=BankUnit.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['events']
                    )
                    if events == None:
                        continue
                    for event in events.data:
                        event_names_by_id[pyRitoFile.hash.FNV1(event)] = event
    return event_names_by_id


def extract(audio_path, events_path, output_dir, bin_path=''):
    # parse audio.bnk or audio.wpk
    bnk_audio_parsing = True if audio_path.endswith('.bnk') else False
    if bnk_audio_parsing:
        audio = pyRitoFile.read_bnk(audio_path)
        didx, data = parse_audio_bnk(audio)
    else:
        audio = pyRitoFile.read_wpk(audio_path)
    # parse events.bnk
    events_bnk = pyRitoFile.read_bnk(events_path)
    sounds_by_id, events_by_id, actions_by_id, ranseq_containers_by_id = parse_events_bnk(
        events_bnk)
    # parse bin
    event_names_by_id = {}
    if bin_path != '':
        bin = pyRitoFile.read_bin(bin_path)
        event_names_by_id = parse_bin(bin)
    for id, name in event_names_by_id.items():
        print(id, name)
    # parse wem ids per event
    wem_ids_by_event_id = {}
    for event_id, event in events_by_id.items():
        wem_ids_by_event_id[event_id] = []
        for action_id in event.action_ids:
            action = actions_by_id[action_id]
            if hasattr(action, 'object_id'):
                if action.type != 4: # play 
                    continue
                # if action link to ranseq container object
                if action.object_id in ranseq_containers_by_id:
                    container = ranseq_containers_by_id[action.object_id]
                    # ranseq container a list of sound objects
                    for sound_id in container.sound_ids:
                        wem_id = sounds_by_id[sound_id].wem_id
                        new_wem = True
                        for existed_wem_id, existed_container_id in wem_ids_by_event_id[event_id]:
                            if wem_id == existed_wem_id:
                                new_wem = False
                                break
                        if new_wem:
                            wem_ids_by_event_id[event_id].append([wem_id, None])
                # if action link to sound object
                elif action.object_id in sounds_by_id:
                    wem_id = sounds_by_id[action.object_id].wem_id
                    new_wem = True
                    for existed_wem_id, existed_container_id in wem_ids_by_event_id[event_id]:
                        if wem_id == existed_wem_id:
                            new_wem = False
                            break
                    if new_wem:
                        wem_ids_by_event_id[event_id].append([wem_id, None])
                # if action link to a ranseq container object switch container
                else:
                    for container_id, container in ranseq_containers_by_id.items():
                        if container.switch_container_id == action.object_id:
                            for sound_id in container.sound_ids:
                                wem_id = sounds_by_id[sound_id].wem_id
                                new_wem = True
                                for stuffs in wem_ids_by_event_id[event_id]:
                                    existed_wem_id, existed_container_id = stuffs
                                    if wem_id == existed_wem_id:
                                        if existed_container_id == None:
                                            stuffs[1] = container_id
                                        new_wem = False
                                        break
                                if new_wem:
                                    wem_ids_by_event_id[event_id].append([wem_id, container_id])

    # extract bnk
    # prepare output
    os.makedirs(output_dir, exist_ok=True)
    with audio.stream(audio_path, 'rb') as bs:
        wems = didx.wems if bnk_audio_parsing else audio.wems
        for wem in wems:
            bs.seek(data.start_offset+wem.offset if bnk_audio_parsing else wem.offset)
            wem_data = bs.read(wem.size)
            for event_id in wem_ids_by_event_id:
                for wem_id, container_id in wem_ids_by_event_id[event_id]:
                    if wem.id == wem_id:
                        event_name = str(event_id)
                        if event_id in event_names_by_id:
                            event_name = event_names_by_id[event_id]
                        event_dir = os.path.join(
                            output_dir, event_name)
                        os.makedirs(event_dir, exist_ok=True)
                        wem_dir = event_dir
                        if container_id != None:
                            container_dir = os.path.join(event_dir, str(container_id))
                            os.makedirs(container_dir, exist_ok=True)
                            wem_dir = container_dir
                        wem_file = os.path.join(
                            wem_dir, f'{wem.id}.wem')
                        with open(wem_file, 'wb') as f:
                            f.write(wem_data)
                        LOG(
                            f'bnk_tool: Done: Extracted [{wem.size}bytes] {wem.id} of {event_id}-{event_name}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
