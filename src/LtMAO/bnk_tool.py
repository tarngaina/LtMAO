from LtMAO import pyRitoFile
import os
import os.path

LOG = print


def extract(audio_path, events_path, bin_path, output_dir):
    audio_bnk = pyRitoFile.read_bnk(audio_path)
    events_bnk = pyRitoFile.read_bnk(events_path)
    bin = pyRitoFile.read_bin(bin_path)
    # parse audio.bnk
    didx = None
    data = None
    for section in audio_bnk.sections:
        if section.signature == 'DIDX':
            didx = section.data
        if section.signature == 'DATA':
            data = section.data
    if didx == None:
        raise Exception(
            'bnk_tool: Failed: Extract BNK: No DIDX section found in audio BNK.')
    if data == None:
        raise Exception(
            'bnk_tool: Failed: Extract BNK: No DATA section found in audio BNK.')
    # parse events.bnk
    hirc = None
    for section in events_bnk.sections:
        if section.signature == 'HIRC':
            hirc = section.data
    if hirc == None:
        raise Exception(
            'bnk_tool: Failed: Extract BNK: No HIRC section found in events BNK.')
    map_sounds = {}
    map_events = {}
    map_actions = {}
    map_ranseq_containers = {}
    for obj in hirc.objects:
        if obj.type == pyRitoFile.BNKObjectType.Sound:
            map_sounds[obj.id] = obj.data
        elif obj.type == pyRitoFile.BNKObjectType.Event:
            map_events[obj.id] = obj.data
        elif obj.type == pyRitoFile.BNKObjectType.Action:
            map_actions[obj.id] = obj.data
        elif obj.type == pyRitoFile.BNKObjectType.RandomOrSequenceContainer:
            map_ranseq_containers[obj.id] = obj.data
    # parse bin
    bin_hash = pyRitoFile.bin_hash
    PRE_BIN_HASH = {
        'SkinCharacterDataProperties': bin_hash('SkinCharacterDataProperties'),
        'skinAudioProperties': bin_hash('skinAudioProperties'),
        'bankUnits': bin_hash('bankUnits'),
        'events': bin_hash('events'),
    }
    SkinCharacterDataProperties = pyRitoFile.BINHelper.find_item(
        items=bin.entries,
        compare_func=lambda entry: entry.type == PRE_BIN_HASH['SkinCharacterDataProperties']
    )
    if SkinCharacterDataProperties == None:
        raise Exception(
            f'bnk_tool: Failed: Extract BNK: Could not find SFX events: SkinCharacterDataProperties')
    skinAudioProperties = pyRitoFile.BINHelper.find_item(
        items=SkinCharacterDataProperties.data,
        compare_func=lambda field: field.hash == PRE_BIN_HASH['skinAudioProperties']
    )
    if skinAudioProperties == None:
        raise Exception(
            f'bnk_tool: Failed: Extract BNK: Could not find SFX events: skinAudioProperties')
    bankUnits = pyRitoFile.BINHelper.find_item(
        items=skinAudioProperties.data,
        compare_func=lambda field: field.hash == PRE_BIN_HASH['bankUnits']
    )
    if bankUnits == None or len(bankUnits.data) == 0:
        raise Exception(
            f'bnk_tool: Failed: Extract BNK: Could not find SFX events: bankUnits')
    unhashed_events = {}
    for BankUnit in bankUnits.data:
        events = pyRitoFile.BINHelper.find_item(
            items=BankUnit.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH['events']
        )
        if events == None:
            continue
        for event in events.data:
            unhashed_events[pyRitoFile.hash.FNV1(event)] = event
    # extract bnk
    # prepare output
    os.makedirs(output_dir, exist_ok=True)
    with audio_bnk.stream(audio_path, 'rb') as bs:
        for wem in didx.wems:
            bs.seek(data.start_offset+wem.offset)
            wem_data = bs.read(wem.size)
            for event_id, event in map_events.items():
                for action_id in event.action_ids:
                    action = map_actions[action_id]
                    if action.object_id in map_ranseq_containers:
                        container = map_ranseq_containers[action.object_id]
                        for sound_id in container.sound_ids:
                            sound = map_sounds[sound_id]
                            if wem.id == sound.wem_id:
                                event_name = event_id
                                if event_id in unhashed_events:
                                    event_name = unhashed_events[event_id]
                                event_dir = os.path.join(
                                    output_dir, event_name)
                                os.makedirs(event_dir, exist_ok=True)
                                audio_file = os.path.join(
                                    event_dir, f'{wem.id}.wem')
                                with open(audio_file, 'wb') as f:
                                    f.write(wem_data)
                                LOG(
                                    f'bnk_tool: Done: Extracted [{wem.size}] {wem.id} of {event_name}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
