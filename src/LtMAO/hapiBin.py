import os.path
from shutil import copy, copytree
from .pyRitoFile import read_bin, write_bin, read_wad, write_wad, BINHelper
from .pyRitoFile import BINField, BINType
from .pyRitoFile.structs import Vector
from .hash_manager import cached_bin_hashes

tk_widgets_data = []
LOG = print


class HPHelper:
    @staticmethod
    def create_tk_button(label, description, icon, require_dst):
        def wrapper(hp_command):
            tk_widgets_data.append((label, description, icon, hp_command, require_dst))
        return wrapper

    @staticmethod
    def main(src, dst, hp_command, require_dst, backup):
        matching_src_dst_bins, src_type = HPHelper.read_src_dst(src, dst, require_dst)

        # backup dst if require dst else src
        HPHelper.backup(dst if backup and require_dst else src)

        for src_bin_path, dst_bin_path, src_bin, dst_bin in matching_src_dst_bins:
            if require_dst:
                LOG(f'hapiBin: Running: {hp_command.__name__}: {src_bin_path} -> {dst_bin_path}.')
            else:
                LOG(f'hapiBin: Running: {hp_command.__name__}: {src_bin_path}.')
            hp_command(src_bin, dst_bin)
        
        HPHelper.write_src_dst(src, dst, matching_src_dst_bins, src_type, require_dst)

    @staticmethod
    def check_type(path):
        if os.path.isdir(path):
            return 'folder'
        else:
            if path.endswith('.wad.client'):
                return 'wad'
            elif path.endswith('.bin'):
                return 'bin'
        raise Exception('hapiBin: Failed: {path} is not a BIN/WAD or FOLDER.')

    @staticmethod
    def read_src_dst(src, dst, require_dst):
        LOG(f'hapiBin: Running: Read source & target.')
        # parsing src first
        if src == '':
            raise Exception('hapiBin: Failed: Source entry is empty.')
        src_type = HPHelper.check_type(src)
        # parsing dst next if require
        if require_dst:
            if dst == '':
                raise Exception('hapiBin: Failed: Target entry is empty.')
            dst_type = HPHelper.check_type(dst)
            if src_type != dst_type:
                raise Exception('hapiBin: Failed: Source entry\'s type is different from target entry type.')

        # list of matching src_dst_bins 
        # (src_path, dst_path, src_bin, dst_bin)
        matching_src_dst_bins = []
        if src_type == 'bin':
            matching_src_dst_bins.append((
                src, 
                dst if require_dst else None, 
                read_bin(src), 
                read_bin(dst) if require_dst else None
            ))
        elif src_type == 'folder':
            for root, dirs, files in os.walk(src):
                for file in files:
                    if file.endswith('.bin'):
                        src_bin_path = os.path.join(root, file).replace('\\','/')
                        if require_dst:
                            dst_bin_path = os.path.join(dst, os.path.relpath(src_bin_path, src)).replace('\\','/')
                            if os.path.exists(dst_bin_path):
                                matching_src_dst_bins.append((
                                    src_bin_path,
                                    dst_bin_path, 
                                    read_bin(src_bin_path),
                                    read_bin(dst_bin_path)
                                ))
                        else:
                            matching_src_dst_bins.append((
                                src_bin_path,
                                None,
                                read_bin(src_bin_path),
                                None
                            ))
        else:
            src_wad = read_wad(src)
            if require_dst:
                prepared_dst_chunks = {}
                dst_wad = read_wad(dst)
                with dst_wad.stream(dst, 'rb') as bs:
                    for chunk in dst_wad.chunks:
                        chunk.read_data(bs)
                        if chunk.extension == 'bin':
                            prepared_dst_chunks[chunk.hash] = read_bin('', raw=chunk.data)
                        chunk.free_data()
            with src_wad.stream(src, 'rb') as bs:
                for chunk in src_wad.chunks:
                    chunk.read_data(bs)
                    if chunk.extension == 'bin': 
                        if require_dst:
                            if chunk.hash in prepared_dst_chunks:
                                matching_src_dst_bins.append((
                                    os.path.join(src, chunk.hash).replace('\\','/'),
                                    os.path.join(dst, chunk.hash).replace('\\','/'),
                                    read_bin('', raw=chunk.data),
                                    prepared_dst_chunks[chunk.hash]
                                ))
                        else:
                            matching_src_dst_bins.append((
                                chunk.hash,
                                None,
                                read_bin('', raw=chunk.data),
                                None
                            ))
                    chunk.free_data()
        return matching_src_dst_bins, src_type

    @staticmethod
    def write_src_dst(src, dst, matching_src_dst_bins, src_type, require_dst):
        if src_type == 'bin':
            for src_bin_path, dst_bin_path, src_bin, dst_bin in matching_src_dst_bins:
                if require_dst:
                    write_bin(dst_bin_path, dst_bin)
                else:
                    write_bin(src_bin_path, src_bin)               
        elif src_type == 'folder':
            for src_bin_path, dst_bin_path, src_bin, dst_bin in matching_src_dst_bins:
                if require_dst:
                    write_bin(dst_bin_path, dst_bin)
                else:
                    write_bin(src_bin_path, src_bin)     
        else:
            if require_dst:
                wad_path = dst
                wad = read_wad(wad_path)
                chunks = [(os.path.basename(dst_bin_path), dst_bin) for src_bin_path, dst_bin_path, src_bin, dst_bin in matching_src_dst_bins]
            else:
                wad_path = src
                wad = read_wad(wad_path)
                chunks = [(os.path.basename(src_bin_path), src_bin) for src_bin_path, dst_bin_path, src_bin, dst_bin in matching_src_dst_bins]
            with wad.stream(wad_path, 'rb+') as bs:
                for chunk in wad.chunks:
                    matching_chunk_hash, matching_chunk_bin_data = next(
                        ((chunk_hash, chunk_bin_data) for chunk_hash, chunk_bin_data in chunks if chunk_hash == chunk.hash),
                        (None, None)
                    )
                    if matching_chunk_hash == None:
                        continue
                    chunk.write_data(bs, chunk.id, chunk.hash, matching_chunk_bin_data.write('', raw=True))
                    chunk.free_data()
        LOG(f'hapiBin: Done: Write source & target.')

    @staticmethod
    def backup(path):
        backup_path = os.path.join(
            os.path.dirname(path),
            'hapiBin_backup_' + os.path.basename(path)
        ).replace('\\','/')
        LOG(f'hapiBin: Running: Backup target {path} -> {backup_path}.')
        if os.path.isdir(path):
            copytree(path, backup_path)
        else:
            copy(path, backup_path)
        LOG(f'hapiBin: Done: Backup target {path} -> {backup_path}.')


@HPHelper.create_tk_button(
    label='Copy Linked List from source to target',
    description='Copy linked list.',
    icon='🔗',
    require_dst=True
)
def copy_linked_list(src_bin, dst_bin):
    dst_bin.links = src_bin.links 
    LOG(f'hapiBin: Done: Copy {len(dst_bin.links)} links.')

@HPHelper.create_tk_button(
    label='Copy VFX colors from source to target',
    description='Copy color, birthColor, reflectionDefinition, lingerColor of VfxEmitterDefinitionData.\nCopy colors, Color, mColorOn, mColorOff of StaticMaterialShaderParamDef/DynamicMaterialParameterDef.',
    icon='🎨',
    require_dst=True
)
def copy_vfx_colors(src_bin, dst_bin):
    copied_field_count = 0
    for dst_entry in dst_bin.entries:
        # VfxSystemDefinitionData entry
        if dst_entry.type == cached_bin_hashes['VfxSystemDefinitionData']:
            # matching VfxSystemDefinitionData
            dst_VfxSystemDefinitionData = dst_entry
            src_VfxSystemDefinitionData = BINHelper.find_item(
                items=src_bin.entries,
                compare_func=lambda entry: entry.hash == dst_VfxSystemDefinitionData.hash and entry.type == cached_bin_hashes[
                    'VfxSystemDefinitionData']
            )
            if src_VfxSystemDefinitionData != None:
                # finding particlePath
                dst_particlePath = BINHelper.find_item(
                    items=dst_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes['particlePath'],
                    return_func=lambda field: field.data
                )
                if dst_particlePath == None:
                    dst_particlePath == dst_VfxSystemDefinitionData.hash
                # finding complexEmitterDefinitionData block
                dst_complexEmitterDefinitionData = BINHelper.find_item(
                    items=dst_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes[
                        'complexEmitterDefinitionData']
                )
                src_complexEmitterDefinitionData = BINHelper.find_item(
                    items=src_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes[
                        'complexEmitterDefinitionData']
                )
                # finding simpleEmitterDefinitionData block
                dst_simpleEmitterDefinitionData = BINHelper.find_item(
                    items=dst_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes[
                        'simpleEmitterDefinitionData']
                )
                src_simpleEmitterDefinitionData = BINHelper.find_item(
                    items=src_VfxSystemDefinitionData.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes[
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
                            compare_func=lambda field: field.hash == cached_bin_hashes['emitterName'],
                            return_func=lambda field: field.data
                        )
                        if dst_emitterName != None:
                            # matching VfxEmitterDefinitionData with emitterName
                            src_VfxEmitterDefinitionData = BINHelper.find_item(
                                items=src_emitters.data,
                                compare_func=lambda emitter: BINHelper.find_item(
                                    items=emitter.data,
                                    compare_func=lambda field: field.hash == cached_bin_hashes[
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
                                        if dst_field.hash == cached_bin_hashes[field_name]:
                                            src_field = BINHelper.find_item(
                                                items=src_VfxEmitterDefinitionData.data,
                                                compare_func=lambda field: field.hash == cached_bin_hashes[
                                                    field_name]
                                            )
                                            if src_field != None:
                                                dst_field.data = src_field.data
                                                copied_field_count += 1
                                                
        elif dst_entry.type == cached_bin_hashes['StaticMaterialDef']:
            # matching StaticMaterialDef
            dst_StaticMaterialDef = dst_entry
            src_StaticMaterialDef = BINHelper.find_item(
                items=src_bin.entries,
                compare_func=lambda entry: entry.hash == dst_StaticMaterialDef.hash and entry.type == cached_bin_hashes[
                    'StaticMaterialDef']
            )
            if src_StaticMaterialDef != None:
                # finding name
                dst_name = BINHelper.find_item(
                    items=dst_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes['name'],
                    return_func=lambda field: field.data
                )
                if dst_name == None:
                    dst_name == dst_StaticMaterialDef.hash
                # finding paramValues
                dst_paramValues = BINHelper.find_item(
                    items=dst_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes['paramValues']
                )
                src_paramValues = BINHelper.find_item(
                    items=src_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes['paramValues']
                )
                if dst_paramValues != None and src_paramValues != None:
                    for color_field_name in ['Color', 'Fresnel_Color']:
                        # matching StaticMaterialShaderParamDef.Fresnel_Color
                        dst_StaticMaterialShaderParamDef_color_field = BINHelper.find_item(
                            items=dst_paramValues.data,
                            compare_func=lambda param: BINHelper.find_item(
                                items=param.data,
                                compare_func=lambda field: field.hash == cached_bin_hashes[
                                    'name'] and field.data == color_field_name
                            ) != None
                        )
                        src_StaticMaterialShaderParamDef_color_field = BINHelper.find_item(
                            items=src_paramValues.data,
                            compare_func=lambda param: BINHelper.find_item(
                                items=param.data,
                                compare_func=lambda field: field.hash == cached_bin_hashes[
                                    'name'] and field.data == color_field_name
                            ) != None
                        )
                        # copy StaticMaterialShaderParamDef.Fresnel_Color
                        if dst_StaticMaterialShaderParamDef_color_field != None and src_StaticMaterialShaderParamDef_color_field != None:
                            dst_StaticMaterialShaderParamDef_color_field.data = src_StaticMaterialShaderParamDef_color_field.data
                            copied_field_count += 1
                # finding dynamicMaterial
                dst_dynamicMaterial = BINHelper.find_item(
                    items=dst_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes['dynamicMaterial']
                )
                src_dynamicMaterial = BINHelper.find_item(
                    items=src_StaticMaterialDef.data,
                    compare_func=lambda field: field.hash == cached_bin_hashes['dynamicMaterial']
                )
                if dst_dynamicMaterial != None and src_dynamicMaterial != None:
                    dst_parameters = BINHelper.find_item(
                        items=dst_dynamicMaterial.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['parameters']
                    )
                    if dst_parameters == None:
                        continue
                    src_parameters = BINHelper.find_item(
                        items=src_dynamicMaterial.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['parameters']
                    )
                    if src_parameters == None:
                        continue
                    # matching DynamicMaterialParameterDef.Fresnel_Color
                    dst_DynamicMaterialParameterDef_Fresnel_Color = BINHelper.find_item(
                        items=dst_parameters.data,
                        compare_func=lambda param: BINHelper.find_item(
                            items=param.data,
                            compare_func=lambda field: field.hash == cached_bin_hashes[
                                'name'] and field.data == 'Fresnel_Color'
                        ) != None
                    )
                    if dst_DynamicMaterialParameterDef_Fresnel_Color == None:
                        continue
                    src_DynamicMaterialParameterDef_Fresnel_Color = BINHelper.find_item(
                        items=src_parameters.data,
                        compare_func=lambda param: BINHelper.find_item(
                            items=param.data,
                            compare_func=lambda field: field.hash == cached_bin_hashes[
                                'name'] and field.data == 'Fresnel_Color'
                        ) != None
                    )
                    if src_DynamicMaterialParameterDef_Fresnel_Color == None:
                        continue
                    # matching driver
                    dst_driver = BINHelper.find_item(
                        items=dst_DynamicMaterialParameterDef_Fresnel_Color.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['driver']
                    )
                    if dst_driver == None:
                        continue
                    src_driver = BINHelper.find_item(
                        items=src_DynamicMaterialParameterDef_Fresnel_Color.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['driver']
                    )
                    if src_driver == None:
                        continue
                    # matching mElements
                    dst_mElements = BINHelper.find_item(
                        items=dst_driver.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['mElements']
                    )
                    if dst_mElements == None:
                        continue
                    src_mElements = BINHelper.find_item(
                        items=src_driver.data,
                        compare_func=lambda field: field.hash == cached_bin_hashes['mElements']
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
                            compare_func=lambda field: field.hash == cached_bin_hashes['mValue']
                        )
                        if dst_mValue == None:
                            continue
                        src_mValue = BINHelper.find_item(
                            items=src_SwitchMaterialDriverElement.data,
                            compare_func=lambda field: field.hash == cached_bin_hashes['mValue']
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
                                if dst_field.hash == cached_bin_hashes[field_name]:
                                    src_field = BINHelper.find_item(
                                        items=src_mValue.data,
                                        compare_func=lambda field: field.hash == cached_bin_hashes[
                                            field_name]
                                    )
                                    if src_field != None:
                                        dst_field.data = src_field.data
                                        copied_field_count += 1
    LOG(f'hapiBin: Done: Copy {copied_field_count} color fields.')                          

@HPHelper.create_tk_button(
    label='Fix VFX Shape Property + BirthTranslation on source',
    description='Fix bin shape owo?! (patch 14.1)',
    icon='💠',
    require_dst=False
)
def fix_vfx_shape(src_bin, dst_bin):
    # These ones we dont know the name so hard keep it as a hash instead of trying to generate one u know
    cached_bin_hashes["NewBirthTranslation"] = "563d4a22"
    cached_bin_hashes["NewShapeHash"] = "3bf0b4ed"
    for entry in src_bin.entries:
        if entry.type == cached_bin_hashes['VfxSystemDefinitionData']:
            for data in entry.data:
                if data.hash == cached_bin_hashes["ComplexEmitterDefinitionData"]:
                    for emitter in data.data:
                        for attribute in emitter.data:
                            if attribute.hash == cached_bin_hashes["Shape"]:
                                shape = attribute
                                if not len(shape.data): continue
                                shit_dict = {}
                                shit_dict["EmitRotationAnglesKeyValues"] = False
                                shit_dict["EmitRotationAxesShit"] = False
                                shit_dict["Flags"] = False
                                shit_dict["KeepItAs0x4f4e2ed7"] = False
                                
                                for inside_of_shape in shape.data:
                                    # Handle birtTranslatation outside
                                    if inside_of_shape.hash == cached_bin_hashes["BirthTranslation"]:
                                        # To get the constant
                                        for i in range(len(inside_of_shape.data)):
                                            if inside_of_shape.data[i].hash == cached_bin_hashes["ConstantValue"] and inside_of_shape.data[i].type == BINType.Vec3:
                                                birth_translation = BINField()
                                                birth_translation.data = [inside_of_shape.data[i]]
                                                birth_translation.hash = cached_bin_hashes["NewBirthTranslation"]
                                                birth_translation.type = BINType.Embed
                                                birth_translation.hash_type = '68dc32b6'
                                                emitter.data.append(birth_translation)
                                                inside_of_shape.data = []
                                                break
                                                #shape.data.remove(inside_of_shape)  Cancer line
                                        inside_of_shape.data = []
                                    
                                    if inside_of_shape.hash == cached_bin_hashes["EmitOffset"]:
                                        for inside_of_emitoffset in inside_of_shape.data:
                                            if inside_of_emitoffset.hash == cached_bin_hashes["ConstantValue"] and inside_of_emitoffset.type == BINType.Vec3:
                                                shit_dict["Radius"] = inside_of_emitoffset.data.x
                                                shit_dict["Height"] = inside_of_emitoffset.data.y # lmao?
                                            if inside_of_emitoffset.hash == cached_bin_hashes["Dynamics"]:
                                                for table_data in inside_of_emitoffset.data:
                                                    if table_data.hash == cached_bin_hashes["ProbabilityTables"]:
                                                        for shit in table_data.data:
                                                            for smoll_shit in shit.data:
                                                                if smoll_shit.hash == cached_bin_hashes["KeyValues"]:
                                                                    if smoll_shit.data[0] == 0 and smoll_shit.data[1] >= 1:
                                                                        shit_dict["Flags"] = True
                                                                    elif smoll_shit.data[0] == -1 and smoll_shit.data[1] == 1:
                                                                        shit_dict["KeepItAs0x4f4e2ed7"] = True

                                    if inside_of_shape.hash == cached_bin_hashes["EmitRotationAngles"]:
                                        for value_float in inside_of_shape.data:
                                            for stuff in value_float.data:
                                                if stuff.hash == cached_bin_hashes["Dynamics"]:
                                                    for table_data in stuff.data:
                                                        if table_data.hash == cached_bin_hashes["ProbabilityTables"]:
                                                            for shit in table_data.data:
                                                                for smoll_shit in shit.data:
                                                                    if smoll_shit.hash == cached_bin_hashes["KeyValues"]:
                                                                        if smoll_shit.data[0] == 0 and smoll_shit.data[1] > 1:
                                                                            shit_dict["EmitRotationAnglesKeyValues"] = True
                                                
                                    if inside_of_shape.hash == cached_bin_hashes["EmitRotationAxes"]:
                                        if len(inside_of_shape.data) == 2:
                                            # This is just a theory that if EmitRotationAxes: list[vec3] = { { 0, 1, 0 } { 0, 0, 1 } }
                                            # Will create a 3dbe415d
                                            if int(inside_of_shape.data[0].y) == 1 and int(inside_of_shape.data[1].z) == 1:
                                                shit_dict["EmitRotationAxesShit"] = True

                                    shape.hash = cached_bin_hashes["NewShapeHash"]
                                    shape.type = BINType.Pointer
                                    if not shit_dict.get("KeepItAs0x4f4e2ed7") and shit_dict["EmitRotationAnglesKeyValues"] and shit_dict["EmitRotationAxesShit"]:
                                        # wow 0x3dbe415d moment
                                        shape.hash_type = '3dbe415d'
                                        shape.data = []
                                        
                                        radius = BINField()
                                        radius.data = float(shit_dict.get("Radius", 0))
                                        radius.type = BINType.F32
                                        radius.hash = cached_bin_hashes["Radius"]
                                        shape.data.append(radius)

                                        if shit_dict.get("Height"):
                                            height = BINField()
                                            height.data = float(shit_dict.get("Height", 0))
                                            height.type = BINType.F32
                                            height.hash = cached_bin_hashes["Height"]
                                            shape.data.append(radius)
                                        if shit_dict["Flags"]:
                                            flags = BINField()
                                            flags.data = 1
                                            flags.type = BINType.U8
                                            flags.hash = cached_bin_hashes["Flags"]
                                            shape.data.append(flags)
                                        continue
                                    else:
                                        if len(shape.data) == 1 and shape.data[0].hash == cached_bin_hashes["EmitOffset"] and isinstance(shape.data[0].data[0].data, Vector):
                                            # 0xee39916f moment, transform emitoffset to a vec3
                                            shape.hash_type = 'ee39916f'
                                            constant_value = shape.data[0].data[0]
                                            emitoffset = BINField()
                                            emitoffset.type = BINType.Vec3
                                            emitoffset.hash = cached_bin_hashes["EmitOffset"]
                                            emitoffset.data = constant_value.data
                                            shape.data = [emitoffset]
                                            continue
                                        else:
                                            # Clueless, default 0x4f4e2ed7
                                            shape.hash_type = '4f4e2ed7'
                                            continue
    LOG(f'hapiBin: Done: FixVfxShape and BirthTranslation')

def prepare(_LOG):
    global LOG
    LOG = _LOG
