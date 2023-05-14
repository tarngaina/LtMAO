from LtMAO.pyRitoFile import bin_hash, read_bin, write_bin, BINHelper


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
        'simpleEmitterDefinitionData': bin_hash('simpleEmitterDefinitionData'),
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
        # matching VfxSystemDefinitionData entry
        if dst_vfxdef.type != PRE_BIN_HASH['VfxSystemDefinitionData']:
            continue
        src_vfxdef = BINHelper.find_item(
            items=src_bin.entries,
            compare_func=lambda entry: entry.hash == dst_vfxdef.hash and entry.type == PRE_BIN_HASH[
                'VfxSystemDefinitionData']
        )
        if src_vfxdef == None:
            continue
        entry_name = BINHelper.find_item(
            items=dst_vfxdef.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH['particlePath'],
            return_func=lambda field: field.data
        )
        # finding complexEmitterDefinitionData block
        dst_complex = BINHelper.find_item(
            items=dst_vfxdef.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                'complexEmitterDefinitionData']
        )
        src_complex = BINHelper.find_item(
            items=src_vfxdef.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                'complexEmitterDefinitionData']
        )

        # finding SimpleEmitterDefinitionData block
        dst_simple = BINHelper.find_item(
            items=dst_vfxdef.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                'simpleEmitterDefinitionData']
        )
        src_simple = BINHelper.find_item(
            items=src_vfxdef.data,
            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                'simpleEmitterDefinitionData']
        )
        for dst_emitters, src_emitters in [(dst_complex, src_complex), (dst_simple, src_simple)]:
            if dst_emitters == None or src_emitters == None:
                continue
            for dst_emitter in dst_emitters.data:
                # matching emitter
                emitter_name = BINHelper.find_item(
                    items=dst_emitter.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH['emitterName'],
                    return_func=lambda field: field.data
                )
                if emitter_name == None:
                    continue
                src_emitter = BINHelper.find_item(
                    items=src_emitters.data,
                    compare_func=lambda emitter: BINHelper.find_item(
                        items=emitter.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH[
                            'emitterName'] and field.data == emitter_name
                    ) != None
                )
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
                            src_field = BINHelper.find_item(
                                items=src_emitter.data,
                                compare_func=lambda field: field.hash == PRE_BIN_HASH[field_hash]
                            )
                            if src_field == None:
                                continue
                            dst_field.data = src_field.data
                            LOG(
                                f'hapiBin: Done: Copy {entry_name}.{emitter_name}.{field_hash}')

    write_bin(dst, dst_bin)
    LOG(f'hapiBin: Done: Copy vfx colors from {src} to {dst}.')


def prepare(_LOG):
    global LOG
    LOG = _LOG
