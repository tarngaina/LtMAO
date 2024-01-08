from .pyRitoFile import bin_hash, read_bin, write_bin, BINHelper


LOG = print

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
    'lingerColor': bin_hash('lingerColor'),
    'StaticMaterialDef': bin_hash('StaticMaterialDef'),
    'paramValues': bin_hash('paramValues'),
    'name': bin_hash('name'),
    'dynamicMaterial': bin_hash('dynamicMaterial'),
    'parameters': bin_hash('parameters'),
    'driver': bin_hash('driver'),
    'mElements': bin_hash('mElements'),
    'mValue': bin_hash('mValue'),
    'colors': bin_hash('colors'),
    'mColorOn': bin_hash('mColorOn'),
    'mColorOff': bin_hash('mColorOff')
}


def copy_linked_list(src, dst):
    src_bin = read_bin(src)
    dst_bin = read_bin(dst)
    dst_bin.links = src_bin.links
    write_bin(dst, dst_bin)
    LOG(f'hapiBin: Done: Copy linked list from {src} to {dst}.')


def copy_vfx_colors(src, dst):
    src_bin = read_bin(src)
    dst_bin = read_bin(dst)

    for dst_entry in dst_bin.entries:
        # VfxSystemDefinitionData entry
        if dst_entry.type == PRE_BIN_HASH['VfxSystemDefinitionData']:
            # matching VfxSystemDefinitionData
            dst_VfxSystemDefinitionData = dst_entry
            src_VfxSystemDefinitionData = BINHelper.find_item(
                items=src_bin.entries,
                compare_func=lambda entry: entry.hash == dst_VfxSystemDefinitionData.hash and entry.type == PRE_BIN_HASH[
                    'VfxSystemDefinitionData']
            )
            if src_VfxSystemDefinitionData != None:
                # finding particlePath
                dst_particlePath = BINHelper.find_item(
                    items=dst_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH['particlePath'],
                    return_func=lambda field: field.data
                )
                if dst_particlePath == None:
                    dst_particlePath == dst_VfxSystemDefinitionData.hash
                # finding complexEmitterDefinitionData block
                dst_complexEmitterDefinitionData = BINHelper.find_item(
                    items=dst_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH[
                        'complexEmitterDefinitionData']
                )
                src_complexEmitterDefinitionData = BINHelper.find_item(
                    items=src_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH[
                        'complexEmitterDefinitionData']
                )
                # finding simpleEmitterDefinitionData block
                dst_simpleEmitterDefinitionData = BINHelper.find_item(
                    items=dst_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH[
                        'simpleEmitterDefinitionData']
                )
                src_simpleEmitterDefinitionData = BINHelper.find_item(
                    items=src_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH[
                        'simpleEmitterDefinitionData']
                )
                for dst_emitters, src_emitters in [
                    (dst_complexEmitterDefinitionData,
                     src_complexEmitterDefinitionData),
                    (dst_simpleEmitterDefinitionData,
                     src_simpleEmitterDefinitionData)
                ]:
                    if dst_emitters == None or src_emitters == None:
                        continue
                    for dst_VfxEmitterDefinitionData in dst_emitters.data:
                        # find dst emitterName
                        dst_emitterName = BINHelper.find_item(
                            items=dst_VfxEmitterDefinitionData.data,
                            compare_func=lambda field: field.hash == PRE_BIN_HASH['emitterName'],
                            return_func=lambda field: field.data
                        )
                        if dst_emitterName != None:
                            # matching VfxEmitterDefinitionData with emitterName
                            src_VfxEmitterDefinitionData = BINHelper.find_item(
                                items=src_emitters.data,
                                compare_func=lambda emitter: BINHelper.find_item(
                                    items=emitter.data,
                                    compare_func=lambda field: field.hash == PRE_BIN_HASH[
                                        'emitterName'] and field.data == dst_emitterName
                                ) != None
                            )
                            if src_VfxEmitterDefinitionData != None:
                                # copy colors from src_VfxEmitterDefinitionData to dst_VfxEmitterDefinitionData:
                                for dst_field in dst_VfxEmitterDefinitionData.data:
                                    for field_name in (
                                        'color',
                                        'birthColor',
                                        'reflectionDefinition',
                                        'lingerColor'
                                    ):
                                        if dst_field.hash == PRE_BIN_HASH[field_name]:
                                            src_field = BINHelper.find_item(
                                                items=src_VfxEmitterDefinitionData.data,
                                                compare_func=lambda field: field.hash == PRE_BIN_HASH[
                                                    field_name]
                                            )
                                            if src_field != None:
                                                dst_field.data = src_field.data
                                                LOG(
                                                    f'hapiBin: Done: Copy {dst_particlePath}.{dst_emitterName}.{field_name}')
        elif dst_entry.type == PRE_BIN_HASH['StaticMaterialDef']:
            # matching StaticMaterialDef
            dst_StaticMaterialDef = dst_entry
            src_StaticMaterialDef = BINHelper.find_item(
                items=src_bin.entries,
                compare_func=lambda entry: entry.hash == dst_StaticMaterialDef.hash and entry.type == PRE_BIN_HASH[
                    'StaticMaterialDef']
            )
            if src_StaticMaterialDef != None:
                # finding name
                dst_name = BINHelper.find_item(
                    items=dst_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH['name'],
                    return_func=lambda field: field.data
                )
                if dst_name == None:
                    dst_name == dst_StaticMaterialDef.hash
                # finding paramValues
                dst_paramValues = BINHelper.find_item(
                    items=dst_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH['paramValues']
                )
                src_paramValues = BINHelper.find_item(
                    items=src_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH['paramValues']
                )
                if dst_paramValues != None and src_paramValues != None:
                    # matching StaticMaterialShaderParamDef.Fresnel_Color
                    dst_StaticMaterialShaderParamDef_Fresnel_Color = BINHelper.find_item(
                        items=dst_paramValues.data,
                        compare_func=lambda param: BINHelper.find_item(
                            items=param.data,
                            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                                'name'] and field.data == 'Fresnel_Color'
                        ) != None
                    )
                    src_StaticMaterialShaderParamDef_Fresnel_Color = BINHelper.find_item(
                        items=src_paramValues.data,
                        compare_func=lambda param: BINHelper.find_item(
                            items=param.data,
                            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                                'name'] and field.data == 'Fresnel_Color'
                        ) != None
                    )
                    # copy StaticMaterialShaderParamDef.Fresnel_Color
                    if dst_StaticMaterialShaderParamDef_Fresnel_Color != None and src_StaticMaterialShaderParamDef_Fresnel_Color != None:
                        dst_StaticMaterialShaderParamDef_Fresnel_Color.data = src_StaticMaterialShaderParamDef_Fresnel_Color.data
                        LOG(
                            f'hapiBin: Done: Copy {dst_name}.StaticMaterialShaderParamDef.Fresnel_Color')
                # finding dynamicMaterial
                dst_dynamicMaterial = BINHelper.find_item(
                    items=dst_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH['dynamicMaterial']
                )
                src_dynamicMaterial = BINHelper.find_item(
                    items=src_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == PRE_BIN_HASH['dynamicMaterial']
                )
                if dst_dynamicMaterial != None and src_dynamicMaterial != None:
                    dst_parameters = BINHelper.find_item(
                        items=dst_dynamicMaterial.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH['parameters']
                    )
                    if dst_parameters == None:
                        continue
                    src_parameters = BINHelper.find_item(
                        items=src_dynamicMaterial.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH['parameters']
                    )
                    if src_parameters == None:
                        continue
                    # matching DynamicMaterialParameterDef.Fresnel_Color
                    dst_DynamicMaterialParameterDef_Fresnel_Color = BINHelper.find_item(
                        items=dst_parameters.data,
                        compare_func=lambda param: BINHelper.find_item(
                            items=param.data,
                            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                                'name'] and field.data == 'Fresnel_Color'
                        ) != None
                    )
                    if dst_DynamicMaterialParameterDef_Fresnel_Color == None:
                        continue
                    src_DynamicMaterialParameterDef_Fresnel_Color = BINHelper.find_item(
                        items=src_parameters.data,
                        compare_func=lambda param: BINHelper.find_item(
                            items=param.data,
                            compare_func=lambda field: field.hash == PRE_BIN_HASH[
                                'name'] and field.data == 'Fresnel_Color'
                        ) != None
                    )
                    if src_DynamicMaterialParameterDef_Fresnel_Color == None:
                        continue
                    # matching driver
                    dst_driver = BINHelper.find_item(
                        items=dst_DynamicMaterialParameterDef_Fresnel_Color.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH['driver']
                    )
                    if dst_driver == None:
                        continue
                    src_driver = BINHelper.find_item(
                        items=src_DynamicMaterialParameterDef_Fresnel_Color.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH['driver']
                    )
                    if src_driver == None:
                        continue
                    # matching mElements
                    dst_mElements = BINHelper.find_item(
                        items=dst_driver.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH['mElements']
                    )
                    if dst_mElements == None:
                        continue
                    src_mElements = BINHelper.find_item(
                        items=src_driver.data,
                        compare_func=lambda field: field.hash == PRE_BIN_HASH['mElements']
                    )
                    if src_mElements == None:
                        continue
                    # matching SwitchMaterialDriverElement by order
                    src_mElements_length = len(src_mElements.data)
                    for id, dst_SwitchMaterialDriverElement in enumerate(dst_mElements.data):
                        if id >= src_mElements_length:
                            continue
                        src_SwitchMaterialDriverElement = src_mElements.data[id]
                        # matching mValue
                        dst_mValue = BINHelper.find_item(
                            items=dst_SwitchMaterialDriverElement.data,
                            compare_func=lambda field: field.hash == PRE_BIN_HASH['mValue']
                        )
                        if dst_mValue == None:
                            continue
                        src_mValue = BINHelper.find_item(
                            items=src_SwitchMaterialDriverElement.data,
                            compare_func=lambda field: field.hash == PRE_BIN_HASH['mValue']
                        )
                        if src_mValue == None:
                            continue
                        # copy colors from src_mValue to dst_mValue
                        for dst_field in dst_mValue.data:
                            for field_name in (
                                'colors',
                                'mColorOn',
                                'mColorOff',
                            ):
                                if dst_field.hash == PRE_BIN_HASH[field_name]:
                                    src_field = BINHelper.find_item(
                                        items=src_mValue.data,
                                        compare_func=lambda field: field.hash == PRE_BIN_HASH[
                                            field_name]
                                    )
                                    if src_field != None:
                                        dst_field.data = src_field.data
                                        LOG(
                                            f'hapiBin: Done: Copy {dst_name}.DynamicMaterialParameterDef.Fresnel_Color.{id}.{field_name}')
    write_bin(dst, dst_bin)
    LOG(f'hapiBin: Done: Copy vfx colors from {src} to {dst}.')


def prepare(_LOG):
    global LOG
    LOG = _LOG
