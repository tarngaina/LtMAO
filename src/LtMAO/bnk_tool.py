from LtMAO import pyRitoFile
import os
import os.path

LOG = print
bin_hash = pyRitoFile.bin_hash
PRE_BIN_HASH = {
    'SkinCharacterDataProperties': bin_hash('SkinCharacterDataProperties'),
    'skinAudioProperties': bin_hash('skinAudioProperties'),
    'bankUnits': bin_hash('bankUnits'),
    'events': bin_hash('events'),
}


def parse_audio_bnk(audio_bnk):
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
    return didx, data


def parse_events_bnk(events_bnk):
    hirc = None
    for section in events_bnk.sections:
        if section.signature == 'HIRC':
            hirc = section.data
    if hirc == None:
        raise Exception(
            'bnk_tool: Failed: Extract BNK: No HIRC section found in events BNK.')
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
        compare_func=lambda entry: entry.type == PRE_BIN_HASH['SkinCharacterDataProperties']
    )
    if SkinCharacterDataProperties != None:
        skinAudioProperties = pyRitoFile.BINHelper.find_item(
            items=SkinCharacterDataProperties.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH['skinAudioProperties']
        )
        if skinAudioProperties != None:
            bankUnits = pyRitoFile.BINHelper.find_item(
                items=skinAudioProperties.data,
                compare_func=lambda field: field.hash == PRE_BIN_HASH['bankUnits']
            )
            if bankUnits != None and len(bankUnits.data) > 0:
                for BankUnit in bankUnits.data:
                    events = pyRitoFile.BINHelper.find_item(
                        items=BankUnit.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH['events']
                    )
                    if events == None:
                        continue
                    for event in events.data:
                        event_names_by_id[pyRitoFile.hash.FNV1(event)] = event
    return event_names_by_id


def extract(audio_path, events_path, output_dir, bin_path=''):
    # parse audio.bnk
    audio_bnk = pyRitoFile.read_bnk(audio_path)
    didx, data = parse_audio_bnk(audio_bnk)
    # parse events.bnk
    events_bnk = pyRitoFile.read_bnk(events_path)
    sounds_by_id, events_by_id, actions_by_id, ranseq_containers_by_id = parse_events_bnk(
        events_bnk)
    # parse bin
    event_names_by_id = {}
    if bin_path != '':
        bin = pyRitoFile.read_bin(bin_path)
        event_names_by_id = parse_bin(bin)
    # parse wem ids per event
    wem_ids_by_event_id = {}
    for event_id, event in events_by_id.items():
        wem_ids_by_event_id[event_id] = []
        for action_id in event.action_ids:
            action = actions_by_id[action_id]
            # if action link to ranseq container object
            if action.object_id in ranseq_containers_by_id:
                container = ranseq_containers_by_id[action.object_id]
                # ranseq container a list of sound objects
                for sound_id in container.sound_ids:
                    wem_id = sounds_by_id[sound_id].wem_id
                    if wem_id not in wem_ids_by_event_id[event_id]:
                        wem_ids_by_event_id[event_id].append(wem_id)
            # if action link to sound object
            elif action.object_id in sounds_by_id:
                wem_id = sounds_by_id[action.object_id].wem_id
                if wem_id not in wem_ids_by_event_id[event_id]:
                    wem_ids_by_event_id[event_id].append(wem_id)
    # extract bnk
    # prepare output
    os.makedirs(output_dir, exist_ok=True)
    with audio_bnk.stream(audio_path, 'rb') as bs:
        for wem in didx.wems:
            bs.seek(data.start_offset+wem.offset)
            wem_data = bs.read(wem.size)
            for event_id in wem_ids_by_event_id:
                if wem.id in wem_ids_by_event_id[event_id]:
                    event_name = str(event_id)
                    if event_id in event_names_by_id:
                        event_name = event_names_by_id[event_id]
                    event_dir = os.path.join(
                        output_dir, event_name)
                    os.makedirs(event_dir, exist_ok=True)
                    audio_file = os.path.join(
                        event_dir, f'{wem.id}.wem')
                    with open(audio_file, 'wb') as f:
                        f.write(wem_data)
                    LOG(
                        f'bnk_tool: Done: Extracted [{wem.size}] {wem.id} of {event_id}-{event_name}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
