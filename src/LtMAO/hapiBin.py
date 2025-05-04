import os.path
from shutil import copy, copytree
from .pyRitoFile import read_bin, write_bin, read_wad, write_wad, BINHelper
from .pyRitoFile import BINField, BINType
from .pyRitoFile.structs import Vector
from .hash_helper import cached_bin_hashes

class Helper:
    qt_datas = [] 

    @staticmethod
    def create_qt_data(name, description, require_dst):
        def wrapper(hp_command):
            Helper.qt_datas.append((name, description, hp_command, require_dst))
        return wrapper

    @staticmethod
    def run_command(src, dst, hp_command, require_dst, backup):
        map_bin_src_dst, map_wad_src_dst = Helper.read_src_dst(src, dst, require_dst)

        # backup dst if require dst else src
        Helper.backup(dst if backup and require_dst else src)

        for src_bin_path in map_bin_src_dst:
            dst_bin_path, src_bin, dst_bin = map_bin_src_dst[src_bin_path]
            if require_dst:
                print(f'hapiBin: Start:  {hp_command.__name__}: {src_bin_path} -> {dst_bin_path}.')
            else:
                print(f'hapiBin: Start:  {hp_command.__name__}: {src_bin_path}.')
            hp_command(src_bin, dst_bin)
        for src_wad_path in map_wad_src_dst:
            dst_wad_path, wad_datas = map_wad_src_dst[src_wad_path]
            for chunk_hash, src_bin, dst_bin in wad_datas:
                if require_dst:
                    print(f'hapiBin: Start:  {hp_command.__name__}: {src_wad_path}/{chunk_hash} -> {dst_wad_path}/{chunk_hash}.')
                else:
                    print(f'hapiBin: Start:  {hp_command.__name__}: {src_wad_path}/{chunk_hash}.')
                hp_command(src_bin, dst_bin)
        
        Helper.write_src_dst(require_dst, map_bin_src_dst, map_wad_src_dst)

    @staticmethod
    def check_type(path):
        if os.path.isdir(path):
            return 'folder'
        else: 
            if path.endswith('.bin'):
                return 'bin'
        raise Exception('hapiBin: Error: {path} is not a BIN/Folder.')

    @staticmethod
    def read_src_dst(src, dst, require_dst):
        print(f'hapiBin: Start:  Read source & target.')
        # parsing src first
        if src == '':
            raise Exception('hapiBin: Error: Source entry is empty.')
        src_type = Helper.check_type(src)
        # parsing dst next if require
        if require_dst:
            if dst == '':
                raise Exception('hapiBin: Error: Target entry is empty.')
            dst_type = Helper.check_type(dst)
            if src_type != dst_type:
                raise Exception('hapiBin: Error: Source entry\'s type is different from target entry type.')

        # map_bin_src_dst[src_bin_path] = (dst_bin_path, src_bin, dst_bin)
        map_bin_src_dst = {}
        # map_wad_src_dst[src_wad_path] = (dst_wad_path, list[tuple(chunk_hash, src_bin, dst_bin)])
        map_wad_src_dst = {}
        if src_type == 'bin':
            if require_dst:
                map_bin_src_dst[src] = (dst, read_bin(src), read_bin(dst))
            else:
                map_bin_src_dst[src] = (None, read_bin(src), None)
        elif src_type == 'folder':
            # scan src folder
            src_bin_paths = []
            src_wad_paths = []
            for root, dirs, files in os.walk(src):
                for file in files:
                    if file.endswith('.bin'):
                        src_bin_paths.append(os.path.join(root, file).replace('\\','/'))
                    elif file.endswith('.wad.client'):
                        src_wad_paths.append(os.path.join(root, file).replace('\\','/'))
            # match bin in subfolders
            for src_bin_path in src_bin_paths:
                if require_dst:
                    dst_bin_path = os.path.join(dst, os.path.relpath(src_bin_path, src)).replace('\\','/')
                    if os.path.exists(dst_bin_path):
                        map_bin_src_dst[src_bin_path] = (dst_bin_path, read_bin(src_bin_path), read_bin(dst_bin_path))
                else:
                    map_bin_src_dst[src_bin_path] = (None, read_bin(src_bin_path), None)
            # match bin in wads
            for src_wad_path in src_wad_paths:
                src_wad = read_wad(src_wad_path)
                if require_dst:
                    dst_wad_path = os.path.join(dst, os.path.relpath(src_wad_path, src)).replace('\\','/')
                    dst_wad = read_wad(dst_wad_path)
                    map_wad_src_dst[src_wad_path] = (dst_wad_path, [])
                    dst_bins = {}
                    with dst_wad.stream(dst_wad_path, 'rb') as bs:
                        for dst_chunk in dst_wad.chunks:
                            dst_chunk.read_data(bs)
                            if dst_chunk.extension == 'bin':
                                dst_bins[dst_chunk.hash] = read_bin('', raw=dst_chunk.data)
                            dst_chunk.free_data()
                else:
                     map_wad_src_dst[src_wad_path] = (None, [])
                with src_wad.stream(src_wad_path, 'rb') as bs:
                    for src_chunk in src_wad.chunks:
                        src_chunk.read_data(bs)
                        if src_chunk.extension == 'bin': 
                            if require_dst:
                                if src_chunk.hash in dst_bins:
                                    map_wad_src_dst[src_wad_path][1].append((
                                        src_chunk.hash,
                                        read_bin('', raw=src_chunk.data), 
                                        dst_bins[src_chunk.hash]
                                    ))
                            else:
                                map_wad_src_dst[src_wad_path][1].append((
                                    src_chunk.hash,
                                    read_bin('', raw=src_chunk.data), 
                                    None,
                                ))
                        src_chunk.free_data()
        return map_bin_src_dst, map_wad_src_dst

    @staticmethod
    def write_src_dst(require_dst, map_bin_src_dst, map_wad_src_dst):
        # write bin
        for src_bin_path in map_bin_src_dst:
            dst_bin_path, src_bin, dst_bin = map_bin_src_dst[src_bin_path]
            if require_dst:
                write_bin(dst_bin_path, dst_bin)
            else:
                write_bin(src_bin_path, src_bin)
        # write bin inside wads
        for src_wad_path in map_wad_src_dst:
            dst_wad_path, wad_datas = map_wad_src_dst[src_wad_path]
            map_wad_datas = {}
            for chunk_hash, src_bin, dst_bin in wad_datas:
                map_wad_datas[chunk_hash] = dst_bin if require_dst else src_bin

            wad_path = dst_wad_path if require_dst else src_wad_path
            wad = read_wad(wad_path)
            with wad.stream(wad_path, 'rb+') as bs:
                for chunk in wad.chunks:
                    if chunk.hash in map_wad_datas:
                        chunk.write_data(bs, chunk.id, chunk.hash, map_wad_datas[chunk.hash].write('', raw=True))
                        chunk.free_data()
        print(f'hapiBin: Finish: Write source & target.')

    @staticmethod
    def backup(path):
        backup_path = os.path.join(
            os.path.dirname(path),
            'hp_backup_' + os.path.basename(path)
        )
        print(f'hapiBin: Start:  Backup target {path} -> {backup_path}.')
        if os.path.isdir(path):
            copytree(path, backup_path, dirs_exist_ok=True)
        else:
            copy(path, backup_path)
        print(f'hapiBin: Finish: Backup target {path} -> {backup_path}.')


@Helper.create_qt_data(
    name='🔗 Copy Linked List: source -> target',
    description='Copy linked list.',
    require_dst=True
)
def copy_linked_list(src_bin, dst_bin):
    dst_bin.links = src_bin.links 
    print(f'hapiBin: Finish: Copy {len(dst_bin.links)} links.')

@Helper.create_qt_data(
    name='🎨 Copy VFX colors: source -> target',
    description='Copy color, birthColor, reflectionDefinition, lingerColor of VfxEmitterDefinitionData.\nCopy colors, Color, mColorOn, mColorOff of StaticMaterialShaderParamDef/DynamicMaterialParameterDef.',
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
    print(f'hapiBin: Finish: Copy {copied_field_count} color fields.')                          


@Helper.create_qt_data(
    name='🖼️ Copy Loadscreen and HUD Icon path: source -> target',
    description='Copy loadscreen, iconCircle, iconSquare.',
    require_dst=True
)
def copy_loadscreen_icon(src_bin, dst_bin):
    dst_SkinCharacterDataProperties =  BINHelper.find_item(
        items=dst_bin.entries,
        compare_func=lambda entry: entry.type == cached_bin_hashes['SkinCharacterDataProperties']
    )
    src_SkinCharacterDataProperties = BINHelper.find_item(
        items=src_bin.entries,
        compare_func=lambda entry: entry.type == cached_bin_hashes['SkinCharacterDataProperties']
    )
    fields_to_copy = (
        cached_bin_hashes('loadscreen'), 
        cached_bin_hashes('iconCircle'), 
        cached_bin_hashes('iconSquare')
    )
    if dst_SkinCharacterDataProperties != None and src_SkinCharacterDataProperties != None:    
        for dst_field in dst_SkinCharacterDataProperties.fields:
            if dst_field.hash in fields_to_copy:
                src_field = BINHelper.find_item(
                    items=src_SkinCharacterDataProperties.fields,
                    compare_func=lambda field: field.hash == dst_field.hash
                )
                if src_field != None:
                    dst_field.data = src_field.data
    print(f'hapiBin: Finish: Copy loadscreen and icons.')  



@Helper.create_qt_data(
    name='✨ Add VFX emitters: source -> target ',
    description='Add all emitters inside complexEmitterDefinitionData of VfxSystemDefinitionData.',
    require_dst=True
)
def add_vfx_emitters(src_bin, dst_bin):
    emitters_copied = 0
    for dst_entry in dst_bin.entries:
        if dst_entry.type == cached_bin_hashes['VfxSystemDefinitionData']:
            # find VfxSystemDefinitionData entry
            dst_VfxSystemDefinitionData = dst_entry
            src_VfxSystemDefinitionData = BINHelper.find_item(
                items=src_bin.entries,
                compare_func=lambda entry: entry.hash == dst_VfxSystemDefinitionData.hash and entry.type == cached_bin_hashes[
                    'VfxSystemDefinitionData']
            )
            if src_VfxSystemDefinitionData != None:
                # find complexEmitterDefinitionData block
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
                if src_complexEmitterDefinitionData != None and dst_complexEmitterDefinitionData != None:
                    # merge 2 list 
                    emitters_copied += len(src_complexEmitterDefinitionData.data)
                    dst_complexEmitterDefinitionData.data += src_complexEmitterDefinitionData.data
    print(f'hapiBin: Finish: Copy {emitters_copied} emitters.')   


@Helper.create_qt_data(
    name='💠 Fix VFX Shape Property + BirthTranslation: on source',
    description='Fix bin shape owo?! (patch 14.1)',
    require_dst=False
)
def fix_vfx_shape(src_bin, dst_bin):
    # These ones we dont know the name so hard keep it as a hash instead of trying to generate one u know
    cached_bin_hashes["NewBirthTranslation"] = "563d4a22"
    cached_bin_hashes["NewShapeHash"] = "3bf0b4ed"
    possible_emitters_containers = (cached_bin_hashes["ComplexEmitterDefinitionData"],
                                    cached_bin_hashes["SimpleEmitterDefinitionData"])
    for entry in src_bin.entries:
        if entry.type == cached_bin_hashes['VfxSystemDefinitionData']:
            for data in entry.data:
                if data.hash in possible_emitters_containers:
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
                                            if inside_of_shape.data[i].hash == cached_bin_hashes["ConstantValue"] and inside_of_shape.data[i].type == BINType.VEC3:
                                                birth_translation = BINField()
                                                birth_translation.data = [inside_of_shape.data[i]]
                                                birth_translation.hash = cached_bin_hashes["NewBirthTranslation"]
                                                birth_translation.type = BINType.EMBED
                                                birth_translation.hash_type = '68dc32b6'
                                                emitter.data.append(birth_translation)
                                                inside_of_shape.data = []
                                                break
                                                #shape.data.remove(inside_of_shape)  Cancer line
                                        inside_of_shape.data = []
                                    
                                    if inside_of_shape.hash == cached_bin_hashes["EmitOffset"]:
                                        for inside_of_emitoffset in inside_of_shape.data:
                                            if inside_of_emitoffset.hash == cached_bin_hashes["ConstantValue"] and inside_of_emitoffset.type == BINType.VEC3:
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
                                    shape.type = BINType.POINTER
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
                                            emitoffset.type = BINType.VEC3
                                            emitoffset.hash = cached_bin_hashes["EmitOffset"]
                                            emitoffset.data = constant_value.data
                                            shape.data = [emitoffset]
                                            continue
                                        else:
                                            # Clueless, default 0x4f4e2ed7
                                            shape.hash_type = '4f4e2ed7'
                                            continue
    print(f'hapiBin: Finish: FixVfxShape and BirthTranslation.')
