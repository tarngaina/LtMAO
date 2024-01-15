import os.path
from shutil import copy
from .pyRitoFile import bin_hash, read_bin, write_bin, BINHelper
from .hash_manager import PRE_BIN_HASH
LOG = print

# These ones we dont know the name so hard keep it as a hash instead of trying to generate one u know
PRE_BIN_HASH["NewBirthTranslation"] = "563d4a22"
PRE_BIN_HASH["NewShapeHash"] = "3bf0b4ed"

def copy_linked_list(src, dst, backup=True):
    src_bin = read_bin(src)
    dst_bin = read_bin(dst)
    dst_bin.links = src_bin.links
    if backup:
        print('called')
        LOG(f'hapiBin: Running: Backup target BIN.')
        backup_dst = os.path.join(
            os.path.dirname(dst),
            'hapiBin_backup_' + os.path.basename(dst)
        )
        copy(dst, backup_dst)
        LOG(f'hapiBin: Done: Backup target BIN.')
    write_bin(dst, dst_bin)
    LOG(f'hapiBin: Done: Copy linked list from {src} to {dst}.')


def copy_vfx_colors(src, dst, backup=True):
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
    
    if backup:
        print('called')
        LOG(f'hapiBin: Running: Backup target BIN.')
        backup_dst = os.path.join(
            os.path.dirname(dst),
            'hapiBin_backup_' + os.path.basename(dst)
        )
        copy(dst, backup_dst)
        LOG(f'hapiBin: Done: Backup target BIN.')
    write_bin(dst, dst_bin)
    LOG(f'hapiBin: Done: Copy vfx colors from {src} to {dst}.')

def fix_vfx_shape(bin1):
    from .pyRitoFile import BINField, BINType, BIN
    from .pyRitoFile.structs import Vector


    bin_file = BIN()
    bin_file.read(bin1)
    for entry in bin_file.entries:
        if entry.type == PRE_BIN_HASH['VfxSystemDefinitionData']:
            for data in entry.data:
                if data.hash == PRE_BIN_HASH["ComplexEmitterDefinitionData"]:
                    for emitter in data.data:
                        for attribute in emitter.data:
                            if attribute.hash == PRE_BIN_HASH["Shape"]:
                                shape = attribute
                                if not len(shape.data): continue
                                shit_dict = {}
                                shit_dict["EmitRotationAnglesKeyValues"] = False
                                shit_dict["EmitRotationAxesShit"] = False
                                shit_dict["Flags"] = False
                                shit_dict["KeepItAs0x4f4e2ed7"] = False
                                
                                for inside_of_shape in shape.data:
                                    # Handle birtTranslatation outside
                                    if inside_of_shape.hash == PRE_BIN_HASH["BirthTranslation"]:
                                        # To get the constant
                                        for i in range(len(inside_of_shape.data)):
                                            if inside_of_shape.data[i].hash == PRE_BIN_HASH["ConstantValue"] and inside_of_shape.data[i].type == BINType.Vec3:
                                                birth_translation = BINField()
                                                birth_translation.data = [inside_of_shape.data[i]]
                                                birth_translation.hash = PRE_BIN_HASH["NewBirthTranslation"]
                                                birth_translation.type = BINType.Embed
                                                birth_translation.hash_type = '68dc32b6'
                                                emitter.data.append(birth_translation)
                                                inside_of_shape.data = []
                                                break
                                                #shape.data.remove(inside_of_shape)  Cancer line
                                        inside_of_shape.data = []
                                    
                                    if inside_of_shape.hash == PRE_BIN_HASH["EmitOffset"]:
                                        for inside_of_emitoffset in inside_of_shape.data:
                                            if inside_of_emitoffset.hash == PRE_BIN_HASH["ConstantValue"] and inside_of_emitoffset.type == BINType.Vec3:
                                                shit_dict["Radius"] = inside_of_emitoffset.data.x
                                                shit_dict["Height"] = inside_of_emitoffset.data.y # lmao?
                                            if inside_of_emitoffset.hash == PRE_BIN_HASH["Dynamics"]:
                                                for table_data in inside_of_emitoffset.data:
                                                    if table_data.hash == PRE_BIN_HASH["ProbabilityTables"]:
                                                        for shit in table_data.data:
                                                            for smoll_shit in shit.data:
                                                                if smoll_shit.hash == PRE_BIN_HASH["KeyValues"]:
                                                                    if smoll_shit.data[0] == 0 and smoll_shit.data[1] >= 1:
                                                                        shit_dict["Flags"] = True
                                                                    elif smoll_shit.data[0] == -1 and smoll_shit.data[1] == 1:
                                                                        shit_dict["KeepItAs0x4f4e2ed7"] = True

                                    if inside_of_shape.hash == PRE_BIN_HASH["EmitRotationAngles"]:
                                        for value_float in inside_of_shape.data:
                                            for stuff in value_float.data:
                                                if stuff.hash == PRE_BIN_HASH["Dynamics"]:
                                                    for table_data in stuff.data:
                                                        if table_data.hash == PRE_BIN_HASH["ProbabilityTables"]:
                                                            for shit in table_data.data:
                                                                for smoll_shit in shit.data:
                                                                    if smoll_shit.hash == PRE_BIN_HASH["KeyValues"]:
                                                                        if smoll_shit.data[0] == 0 and smoll_shit.data[1] > 1:
                                                                            shit_dict["EmitRotationAnglesKeyValues"] = True
                                                
                                    if inside_of_shape.hash == PRE_BIN_HASH["EmitRotationAxes"]:
                                        if len(inside_of_shape.data) == 2:
                                            # This is just a theory that if EmitRotationAxes: list[vec3] = { { 0, 1, 0 } { 0, 0, 1 } }
                                            # Will create a 3dbe415d
                                            if int(inside_of_shape.data[0].y) == 1 and int(inside_of_shape.data[1].z) == 1:
                                                shit_dict["EmitRotationAxesShit"] = True

                                    shape.hash = PRE_BIN_HASH["NewShapeHash"]
                                    shape.type = BINType.Pointer
                                    if not shit_dict.get("KeepItAs0x4f4e2ed7") and shit_dict["EmitRotationAnglesKeyValues"] and shit_dict["EmitRotationAxesShit"]:
                                        # wow 0x3dbe415d moment
                                        shape.hash_type = '3dbe415d'
                                        shape.data = []
                                        
                                        radius = BINField()
                                        radius.data = float(shit_dict.get("Radius", 0))
                                        radius.type = BINType.F32
                                        radius.hash = PRE_BIN_HASH["Radius"]
                                        shape.data.append(radius)

                                        if shit_dict.get("Height"):
                                            height = BINField()
                                            height.data = float(shit_dict.get("Height", 0))
                                            height.type = BINType.F32
                                            height.hash = PRE_BIN_HASH["Height"]
                                            shape.data.append(radius)
                                        if shit_dict["Flags"]:
                                            flags = BINField()
                                            flags.data = 1
                                            flags.type = BINType.U8
                                            flags.hash = PRE_BIN_HASH["Flags"]
                                            shape.data.append(flags)
                                        continue
                                    else:
                                        if len(shape.data) == 1 and shape.data[0].hash == PRE_BIN_HASH["EmitOffset"] and isinstance(shape.data[0].data[0].data, Vector):
                                            # 0xee39916f moment, transform emitoffset to a vec3
                                            shape.hash_type = 'ee39916f'
                                            constant_value = shape.data[0].data[0]
                                            emitoffset = BINField()
                                            emitoffset.type = BINType.Vec3
                                            emitoffset.hash = PRE_BIN_HASH["EmitOffset"]
                                            emitoffset.data = constant_value.data
                                            shape.data = [emitoffset]
                                            continue
                                        else:
                                            # Clueless, default 0x4f4e2ed7
                                            shape.hash_type = '4f4e2ed7'
                                            continue
    
    bin_file.write(bin1)
    LOG(f'hapiBin: Done: FixVfxShape and BirthTranslation')

def prepare(_LOG):
    global LOG
    LOG = _LOG
