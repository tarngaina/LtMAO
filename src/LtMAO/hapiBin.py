from LtMAO.pyRitoFile import bin_hash, read_bin, write_bin


LOG = print


def copy_linked_list(src, dst):
    src_bin = read_bin(src)
    dst_bin = read_bin(dst)
    dst_bin.links = src_bin.links
    write_bin(dst, dst_bin)
    LOG(f'hapiBin: Done: Copy linked list from {src} to {dst}.')


def copy_vfx_colors(src, dst):
    PRE_BIN_HASH = {
        'VfxSystemDefinitionData': bin_hash('VfxSystemDefinitionData'),
        'particlePath': bin_hash('particlePath'),
        'complexEmitterDefinitionData': bin_hash('complexEmitterDefinitionData'),
        'VfxEmitterDefinitionData': bin_hash('VfxEmitterDefinitionData'),
        'emitterName': bin_hash('emitterName'),
        'color': bin_hash('color'),
        'birthColor': bin_hash('birthColor'),
        'reflectionDefinition': bin_hash('reflectionDefinition'),
        'lingerColor': bin_hash('lingerColor')
    }
    src_bin = read_bin(src)
    dst_bin = read_bin(dst)

    for dst_vfxdef in dst_bin.entries:
        # matching vfx entry
        if dst_vfxdef.type != PRE_BIN_HASH['VfxSystemDefinitionData']:
            continue
        src_vfxdef = next((entry for entry in src_bin.entries if entry.hash ==
                          dst_vfxdef.hash and entry.type == PRE_BIN_HASH['VfxSystemDefinitionData']), None)
        if src_vfxdef == None:
            continue
        entry_name = next((field.data for field in dst_vfxdef.data if field.hash ==
                          PRE_BIN_HASH['particlePath']), dst_vfxdef.hash)
        # matching list of emiiters block
        dst_bigemitter = next((field for field in dst_vfxdef.data if field.hash ==
                              PRE_BIN_HASH['complexEmitterDefinitionData']), None)
        if dst_bigemitter == None:
            continue
        src_bigemitter = next((field for field in src_vfxdef.data if field.hash ==
                              PRE_BIN_HASH['complexEmitterDefinitionData']), None)
        if src_bigemitter == None:
            continue
        for dst_emitter in dst_bigemitter.data:
            # matching emitter
            emitter_name = None
            for field in dst_emitter.data:
                if field.hash == PRE_BIN_HASH['emitterName']:
                    emitter_name = field.data
            if emitter_name == None:
                continue
            src_emitter = next((emitter for emitter in src_bigemitter.data for field in emitter.data if field.hash ==
                                PRE_BIN_HASH['emitterName'] and field.data == emitter_name), None)
            if src_emitter == None:
                continue
            # start copy colors from src_emitter to dst_emitter:
            field_need_to_copy = [
                'color',
                'birthColor',
                'reflectionDefinition',
                'lingerColor'
            ]
            for dst_field in dst_emitter.data:
                for field_hash in field_need_to_copy:
                    if dst_field.hash == PRE_BIN_HASH[field_hash]:
                        src_field = next(
                            (field for field in src_emitter.data if field.hash == PRE_BIN_HASH[field_hash]))
                        if src_field != None:
                            dst_field.data = src_field.data
                        LOG(f'hapiBin: Done: Copy {entry_name}.{emitter_name}.{field_hash}')

    write_bin(dst, dst_bin)
    LOG(f'hapiBin: Done: Copy vfx colors from {src} to {dst}.')


def prepare(_LOG):
    global LOG
    LOG = _LOG
