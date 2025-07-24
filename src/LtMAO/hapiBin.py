import os.path, shutil
from . import lepath, pyRitoFile, hash_helper

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
                map_bin_src_dst[src] = (dst, pyRitoFile.bin.BIN().read(src), pyRitoFile.bin.BIN().read(dst))
            else:
                map_bin_src_dst[src] = (None, pyRitoFile.bin.BIN().read(src), None)
        elif src_type == 'folder':
            # scan src folder
            src_bin_paths = []
            src_wad_paths = []
            for root, dirs, files in os.walk(src):
                for file in files:
                    if file.endswith('.bin'):
                        src_bin_paths.append(lepath.join(root, file))
                    elif file.endswith('.wad.client'):
                        src_wad_paths.append(lepath.join(root, file))
            # match bin in subfolders
            for src_bin_path in src_bin_paths:
                if require_dst:
                    dst_bin_path = lepath.join(dst, lepath.rel(src_bin_path, src))
                    if os.path.exists(dst_bin_path):
                        map_bin_src_dst[src_bin_path] = (dst_bin_path, pyRitoFile.bin.BIN().read(src_bin_path), pyRitoFile.bin.BIN().read(dst_bin_path))
                else:
                    map_bin_src_dst[src_bin_path] = (None, pyRitoFile.bin.BIN().read(src_bin_path), None)
            # match bin in wads
            for src_wad_path in src_wad_paths:
                src_wad = pyRitoFile.wad.WAD().read(src_wad_path)
                if require_dst:
                    dst_wad_path = lepath.join(dst, lepath.rel(src_wad_path, src))
                    dst_wad = pyRitoFile.wad.WAD().read(dst_wad_path)
                    map_wad_src_dst[src_wad_path] = (dst_wad_path, [])
                    dst_bins = {}
                    with pyRitoFile.stream.BytesStream.reader(dst_wad_path) as bs:
                        for dst_chunk in dst_wad.chunks:
                            dst_chunk.read_data(bs)
                            if dst_chunk.extension == 'bin':
                                dst_bins[dst_chunk.hash] = pyRitoFile.bin.BIN().read(dst_chunk.data, raw=True)
                            dst_chunk.free_data()
                else:
                     map_wad_src_dst[src_wad_path] = (None, [])
                with pyRitoFile.stream.BytesStream.reader(src_wad_path) as bs:
                    for src_chunk in src_wad.chunks:
                        src_chunk.read_data(bs)
                        if src_chunk.extension == 'bin': 
                            if require_dst:
                                if src_chunk.hash in dst_bins:
                                    map_wad_src_dst[src_wad_path][1].append((
                                        src_chunk.hash,
                                        pyRitoFile.bin.BIN().read(src_chunk.data, raw=True), 
                                        dst_bins[src_chunk.hash]
                                    ))
                            else:
                                map_wad_src_dst[src_wad_path][1].append((
                                    src_chunk.hash,
                                    pyRitoFile.bin.BIN().read(src_chunk.data, raw=True), 
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
                dst_bin.write(dst_bin_path)
            else:
                src_bin.write(src_bin_path)
        # write bin inside wads
        for src_wad_path in map_wad_src_dst:
            dst_wad_path, wad_datas = map_wad_src_dst[src_wad_path]
            map_wad_datas = {}
            for chunk_hash, src_bin, dst_bin in wad_datas:
                map_wad_datas[chunk_hash] = dst_bin if require_dst else src_bin

            wad_path = dst_wad_path if require_dst else src_wad_path
            wad = pyRitoFile.wad.WAD().read(wad_path)
            with pyRitoFile.stream.BytesStream.updater(wad_path) as bs:
                for chunk in wad.chunks:
                    if chunk.hash in map_wad_datas:
                        chunk.write_data(bs, chunk.id, chunk.hash, map_wad_datas[chunk.hash].write('', raw=True))
                        chunk.free_data()
        print(f'hapiBin: Finish: Write source & target.')

    @staticmethod
    def backup(path):
        backup_path = lepath.join(
            os.path.dirname(path),
            'hp_backup_' + os.path.basename(path)
        )
        print(f'hapiBin: Start:  Backup target {path} -> {backup_path}.')
        if os.path.isdir(path):
            shutil.copytree(path, backup_path, dirs_exist_ok=True)
        else:
            shutil.copy(path, backup_path)
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
        if dst_entry.type == hash_helper.Storage.bin_hashes['VfxSystemDefinitionData']:
            # matching VfxSystemDefinitionData
            dst_VfxSystemDefinitionData = dst_entry
            src_VfxSystemDefinitionDatas = src_bin.get_items(
                lambda entry: entry.hash == dst_VfxSystemDefinitionData.hash and entry.type == hash_helper.Storage.bin_hashes['VfxSystemDefinitionData']
            )
            if len(src_VfxSystemDefinitionDatas) > 0:
                src_VfxSystemDefinitionData = src_VfxSystemDefinitionDatas[0]
                matching_emitter = [] 
                # finding complexEmitterDefinitionData block
                dst_complexEmitterDefinitionDatas = dst_VfxSystemDefinitionData.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['complexEmitterDefinitionData']
                )
                src_complexEmitterDefinitionDatas = src_VfxSystemDefinitionData.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['complexEmitterDefinitionData']
                )
                if len(dst_complexEmitterDefinitionDatas) > 0 and len(src_complexEmitterDefinitionDatas) > 0:
                    matching_emitter.append((dst_complexEmitterDefinitionDatas[0], src_complexEmitterDefinitionDatas[0]))
                # finding simpleEmitterDefinitionData block
                dst_simpleEmitterDefinitionDatas = dst_VfxSystemDefinitionData.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['simpleEmitterDefinitionData']
                )
                src_simpleEmitterDefinitionDatas = src_VfxSystemDefinitionData.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['simpleEmitterDefinitionData']
                )
                if len(dst_simpleEmitterDefinitionDatas) > 0 and len(src_simpleEmitterDefinitionDatas) > 0:
                    matching_emitter.append((dst_simpleEmitterDefinitionDatas[0], src_simpleEmitterDefinitionDatas[0]))
                for dst_emitter, src_emitter in matching_emitter:
                    matching_vfxdatas = []
                    for dst_VfxEmitterDefinitionData in dst_emitter.data:
                        # find dst emitterName
                        dst_emitterNames = dst_VfxEmitterDefinitionData.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['emitterName']
                        )
                        if len(dst_emitterNames) > 0:
                            dst_emitterName = dst_emitterNames[0]
                            for src_VfxEmitterDefinitionData in src_emitter.data:
                                src_emitterNames = src_VfxEmitterDefinitionData.get_items(
                                    lambda field: field.hash == hash_helper.Storage.bin_hashes['emitterName']
                                )
                                if len(src_emitterNames) > 0:
                                    src_emitterName = src_emitterNames[0]
                                    if src_emitterName.data == dst_emitterName.data:
                                        matching_vfxdatas.append((dst_VfxEmitterDefinitionData, src_VfxEmitterDefinitionData))
                    for dst_VfxEmitterDefinitionData, src_VfxEmitterDefinitionData in matching_vfxdatas:
                        # copy colors from src_VfxEmitterDefinitionData to dst_VfxEmitterDefinitionData:
                        for dst_field in dst_VfxEmitterDefinitionData.data:
                            for field_name in (
                                'color',
                                'birthColor',
                                'reflectionDefinition',
                                'lingerColor'
                            ):
                                if dst_field.hash == hash_helper.Storage.bin_hashes[field_name]:
                                    src_fields = src_VfxEmitterDefinitionData.get_items(
                                        lambda field: field.hash == hash_helper.Storage.bin_hashes[field_name]
                                    )
                                    if len(src_fields) > 0:
                                        src_field = src_fields[0]
                                        dst_field.data = src_field.data
                                        copied_field_count += 1
                                                
        elif dst_entry.type == hash_helper.Storage.bin_hashes['StaticMaterialDef']:
            # matching StaticMaterialDef
            dst_StaticMaterialDef = dst_entry
            src_StaticMaterialDefs = src_bin.get_items(
                lambda entry: entry.hash == dst_StaticMaterialDef.hash and entry.type == hash_helper.Storage.bin_hashes['StaticMaterialDef']
            )
            if len(src_StaticMaterialDefs) > 0:
                src_StaticMaterialDef = src_StaticMaterialDefs[0]
                # finding paramValues
                dst_paramValuess = dst_StaticMaterialDef.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['paramValues']
                )
                src_paramValuess = src_StaticMaterialDef.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['paramValues']
                )
                if len(dst_paramValuess) > 0 and len(src_paramValuess) > 0:
                    dst_paramValues = dst_paramValuess[0]
                    src_paramValues = src_paramValuess[0]

                    matching_paramdefs = []
                    for dst_StaticMaterialShaderParamDef in dst_paramValues.data:
                        # find name
                        dst_names = dst_StaticMaterialShaderParamDef.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['name']
                        )
                        if len(dst_names) > 0:
                            dst_name = dst_names[0]
                            for src_StaticMaterialShaderParamDef in src_paramValues.data:
                                src_names = src_StaticMaterialShaderParamDef.get_items(
                                    lambda field: field.hash == hash_helper.Storage.bin_hashes['name']
                                )
                                if len(src_names) > 0:
                                    src_name = src_names[0]
                                    if src_name.data == dst_name.data:
                                        if src_name in ('Color', 'Fresnel_Color'):
                                            matching_paramdefs.append((dst_StaticMaterialShaderParamDef, src_StaticMaterialShaderParamDef))
                    for dst_StaticMaterialShaderParamDef, src_StaticMaterialShaderParamDef in matching_paramdefs:
                        dst_values = dst_StaticMaterialDef.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['value']
                        )
                        src_values = src_StaticMaterialDef.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['value']
                        )
                        if len(dst_values) > 0 and len(src_values) > 0:
                            dst_values[0].data = src_values[0].data
                            copied_field_count += 1
                # finding dynamicMaterial
                dst_dynamicMaterials = dst_StaticMaterialDef.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['dynamicMaterial']
                )
                src_dynamicMaterials = src_StaticMaterialDef.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes['dynamicMaterial']
                )
                if len(dst_dynamicMaterials) > 0 and len(src_dynamicMaterials) > 0:
                    dst_dynamicMaterial = dst_dynamicMaterials[0]
                    src_dynamicMaterial = src_dynamicMaterials[0]
                    dst_parameters = dst_dynamicMaterial.get_items(
                        lambda field: field.hash == hash_helper.Storage.bin_hashes['parameters']
                    )
                    src_parameters = src_dynamicMaterial.get_items(
                        lambda field: field.hash == hash_helper.Storage.bin_hashes['parameters']
                    )
                    if len(dst_parameters) == 0 or len(src_parameters) == 0:
                        continue
                    # matching DynamicMaterialParameterDef.Fresnel_Color
                    dst_Fresnel_Color = None
                    for dst_DynamicMaterialParameterDef in dst_parameters[0].data:
                        dst_Fresnel_Colors = dst_DynamicMaterialParameterDef.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['name'] and field.data == 'Fresnel_Color'
                        )
                        if len(dst_Fresnel_Colors) > 0:
                            dst_Fresnel_Color = dst_Fresnel_Colors[0]
                    src_Fresnel_Color = None
                    for src_DynamicMaterialParameterDef in src_parameters[0].data:
                        src_Fresnel_Colors = src_DynamicMaterialParameterDef.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['name'] and field.data == 'Fresnel_Color'
                        )
                        if len(src_Fresnel_Colors) > 0:
                            src_Fresnel_Color = src_Fresnel_Colors[0]
                    if dst_Fresnel_Color == None or src_Fresnel_Color == None:
                        continue
                    # matching driver
                    dst_drivers = dst_Fresnel_Color.get_items(
                        lambda field: field.hash == hash_helper.Storage.bin_hashes['driver']
                    )
                    src_drivers = src_Fresnel_Color.get_items(
                        lambda field: field.hash == hash_helper.Storage.bin_hashes['driver']
                    )
                    if len(dst_drivers) == 0 or len(src_drivers) == 0:
                        continue
                    # matching mElements
                    dst_mElementss = dst_drivers[0].get_items(
                        lambda field: field.hash == hash_helper.Storage.bin_hashes['mElements']
                    )
                    src_mElementss = src_drivers[0].get_items(
                        lambda field: field.hash == hash_helper.Storage.bin_hashes['mElements']
                    )
                    if len(dst_mElementss) == 0 or len(src_mElementss) == 0:
                        continue
                    dst_mElements = dst_mElementss[0]
                    src_mElements = src_mElementss[0]
                    # matching SwitchMaterialDriverElement by order
                    src_mElements_length = len(src_mElements.data)
                    for id, dst_SwitchMaterialDriverElement in enumerate(dst_mElements.data):
                        if id >= src_mElements_length:
                            continue
                        src_SwitchMaterialDriverElement = src_mElements.data[id]
                        # matching mValue
                        dst_mValues = dst_SwitchMaterialDriverElement.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['mValue']
                        )
                        src_mValues = src_SwitchMaterialDriverElement.get_items(
                            lambda field: field.hash == hash_helper.Storage.bin_hashes['mValue']
                        )
                        if len(dst_mValues) == 0 or len(src_mValues) == 0:
                            continue
                        dst_mValue = dst_mValues[0]
                        src_mValue = src_mValues[0]
                        # copy colors from src_mValue to dst_mValue
                        for dst_field in dst_mValue.data:
                            for field_name in (
                                'colors',
                                'mColorOn',
                                'mColorOff',
                            ):
                                if dst_field.hash == hash_helper.Storage.bin_hashes[field_name]:
                                    src_fields = src_mValue.get_items(
                                        lambda field: field.hash == hash_helper.Storage.bin_hashes[field_name]
                                    )
                                    if len(src_fields) > 0:
                                        dst_field.data = src_fields[0].data
                                        copied_field_count += 1
    print(f'hapiBin: Finish: Copy {copied_field_count} color fields.')                          


@Helper.create_qt_data(
    name='🖼️ Copy Loadscreen and HUD Icon path: source -> target',
    description='Copy loadscreen, iconCircle, iconSquare.',
    require_dst=True
)
def copy_loadscreen_icon(src_bin, dst_bin):
    fields_to_copy = (
        hash_helper.Storage.bin_hashes['loadscreen'], 
        hash_helper.Storage.bin_hashes['iconCircle'], 
        hash_helper.Storage.bin_hashes['iconSquare']
    )
    dst_SkinCharacterDataPropertiess =  dst_bin.get_items(
        lambda entry: entry.type == hash_helper.Storage.bin_hashes['SkinCharacterDataProperties']
    )
    src_SkinCharacterDataPropertiess = src_bin.get_items(
        lambda entry: entry.type == hash_helper.Storage.bin_hashes['SkinCharacterDataProperties']
    )
    if len(dst_SkinCharacterDataPropertiess) > 0 and len(src_SkinCharacterDataPropertiess) > 0:
        dst_SkinCharacterDataProperties = dst_SkinCharacterDataPropertiess[0]
        src_SkinCharacterDataProperties = src_SkinCharacterDataPropertiess[0]
        for dst_field in dst_SkinCharacterDataProperties.data:
            if dst_field.hash in fields_to_copy:
                src_fields = src_SkinCharacterDataProperties.get_items(
                    lambda field: field.hash == dst_field.hash
                )
                if len(src_fields) > 0:
                    dst_field.data = src_fields[0].data
    print(f'hapiBin: Finish: Copy loadscreen and icons.')  



@Helper.create_qt_data(
    name='✨ Add VFX emitters: source -> target ',
    description='Add all emitters inside complexEmitterDefinitionData of VfxSystemDefinitionData.',
    require_dst=True
)
def add_vfx_emitters(src_bin, dst_bin):
    emitters_copied = 0
    for dst_entry in dst_bin.entries:
        if dst_entry.type == hash_helper.Storage.bin_hashes['VfxSystemDefinitionData']:
            # find VfxSystemDefinitionData entry
            dst_VfxSystemDefinitionData = dst_entry
            src_VfxSystemDefinitionDatas = src_bin.get_items(
                lambda entry: entry.hash == dst_VfxSystemDefinitionData.hash and entry.type == hash_helper.Storage.bin_hashes[
                    'VfxSystemDefinitionData']
            )
            if len(src_VfxSystemDefinitionDatas) > 0:
                src_VfxSystemDefinitionData = src_VfxSystemDefinitionDatas[0]
                # find complexEmitterDefinitionData block
                dst_complexEmitterDefinitionDatas = dst_VfxSystemDefinitionData.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes[
                        'complexEmitterDefinitionData']
                )
                src_complexEmitterDefinitionDatas = src_VfxSystemDefinitionData.get_items(
                    lambda field: field.hash == hash_helper.Storage.bin_hashes[
                        'complexEmitterDefinitionData']
                )
                if len(src_complexEmitterDefinitionDatas) > 0 and len(dst_complexEmitterDefinitionDatas) > 0:
                    # merge 2 list 
                    dst_complexEmitterDefinitionDatas[0].data += src_complexEmitterDefinitionDatas[0].data
                    emitters_copied += len(src_complexEmitterDefinitionDatas[0].data)
    print(f'hapiBin: Finish: Copy {emitters_copied} emitters.')   


@Helper.create_qt_data(
    name='💠 Fix VFX Shape Property + BirthTranslation: on source',
    description='Fix bin shape owo?! (patch 14.1)',
    require_dst=False
)
def fix_vfx_shape(src_bin, dst_bin):
    # These ones we dont know the name so hard keep it as a hash instead of trying to generate one u know
    hash_helper.Storage.bin_hashes["NewBirthTranslation"] = "563d4a22"
    hash_helper.Storage.bin_hashes["NewShapeHash"] = "3bf0b4ed"
    possible_emitters_containers = (hash_helper.Storage.bin_hashes["ComplexEmitterDefinitionData"],
                                    hash_helper.Storage.bin_hashes["SimpleEmitterDefinitionData"])
    for entry in src_bin.entries:
        if entry.type == hash_helper.Storage.bin_hashes['VfxSystemDefinitionData']:
            for data in entry.data:
                if data.hash in possible_emitters_containers:
                    for emitter in data.data:
                        for attribute in emitter.data:
                            if attribute.hash == hash_helper.Storage.bin_hashes["Shape"]:
                                shape = attribute
                                if not len(shape.data): continue
                                shit_dict = {}
                                shit_dict["EmitRotationAnglesKeyValues"] = False
                                shit_dict["EmitRotationAxesShit"] = False
                                shit_dict["Flags"] = False
                                shit_dict["KeepItAs0x4f4e2ed7"] = False
                                
                                for inside_of_shape in shape.data:
                                    # Handle birtTranslatation outside
                                    if inside_of_shape.hash == hash_helper.Storage.bin_hashes["BirthTranslation"]:
                                        # To get the constant
                                        for i in range(len(inside_of_shape.data)):
                                            if inside_of_shape.data[i].hash == hash_helper.Storage.bin_hashes["ConstantValue"] and inside_of_shape.data[i].type == pyRitoFile.bin.BINType.VEC3:
                                                birth_translation = pyRitoFile.bin.BINField()
                                                birth_translation.data = [inside_of_shape.data[i]]
                                                birth_translation.hash = hash_helper.Storage.bin_hashes["NewBirthTranslation"]
                                                birth_translation.type = pyRitoFile.bin.BINType.EMBED
                                                birth_translation.hash_type = '68dc32b6'
                                                emitter.data.append(birth_translation)
                                                inside_of_shape.data = []
                                                break
                                                #shape.data.remove(inside_of_shape)  Cancer line
                                        inside_of_shape.data = []
                                    
                                    if inside_of_shape.hash == hash_helper.Storage.bin_hashes["EmitOffset"]:
                                        for inside_of_emitoffset in inside_of_shape.data:
                                            if inside_of_emitoffset.hash == hash_helper.Storage.bin_hashes["ConstantValue"] and inside_of_emitoffset.type == pyRitoFile.bin.BINType.VEC3:
                                                shit_dict["Radius"] = inside_of_emitoffset.data.x
                                                shit_dict["Height"] = inside_of_emitoffset.data.y # lmao?
                                            if inside_of_emitoffset.hash == hash_helper.Storage.bin_hashes["Dynamics"]:
                                                for table_data in inside_of_emitoffset.data:
                                                    if table_data.hash == hash_helper.Storage.bin_hashes["ProbabilityTables"]:
                                                        for shit in table_data.data:
                                                            for smoll_shit in shit.data:
                                                                if smoll_shit.hash == hash_helper.Storage.bin_hashes["KeyValues"]:
                                                                    if smoll_shit.data[0] == 0 and smoll_shit.data[1] >= 1:
                                                                        shit_dict["Flags"] = True
                                                                    elif smoll_shit.data[0] == -1 and smoll_shit.data[1] == 1:
                                                                        shit_dict["KeepItAs0x4f4e2ed7"] = True

                                    if inside_of_shape.hash == hash_helper.Storage.bin_hashes["EmitRotationAngles"]:
                                        for value_float in inside_of_shape.data:
                                            for stuff in value_float.data:
                                                if stuff.hash == hash_helper.Storage.bin_hashes["Dynamics"]:
                                                    for table_data in stuff.data:
                                                        if table_data.hash == hash_helper.Storage.bin_hashes["ProbabilityTables"]:
                                                            for shit in table_data.data:
                                                                for smoll_shit in shit.data:
                                                                    if smoll_shit.hash == hash_helper.Storage.bin_hashes["KeyValues"]:
                                                                        if smoll_shit.data[0] == 0 and smoll_shit.data[1] > 1:
                                                                            shit_dict["EmitRotationAnglesKeyValues"] = True
                                                
                                    if inside_of_shape.hash == hash_helper.Storage.bin_hashes["EmitRotationAxes"]:
                                        if len(inside_of_shape.data) == 2:
                                            # This is just a theory that if EmitRotationAxes: list[vec3] = { { 0, 1, 0 } { 0, 0, 1 } }
                                            # Will create a 3dbe415d
                                            if int(inside_of_shape.data[0].y) == 1 and int(inside_of_shape.data[1].z) == 1:
                                                shit_dict["EmitRotationAxesShit"] = True

                                    shape.hash = hash_helper.Storage.bin_hashes["NewShapeHash"]
                                    shape.type = pyRitoFile.bin.BINType.POINTER
                                    if not shit_dict.get("KeepItAs0x4f4e2ed7") and shit_dict["EmitRotationAnglesKeyValues"] and shit_dict["EmitRotationAxesShit"]:
                                        # wow 0x3dbe415d moment
                                        shape.hash_type = '3dbe415d'
                                        shape.data = []
                                        
                                        radius = pyRitoFile.bin.BINField()
                                        radius.data = float(shit_dict.get("Radius", 0))
                                        radius.type = pyRitoFile.bin.BINType.F32
                                        radius.hash = hash_helper.Storage.bin_hashes["Radius"]
                                        shape.data.append(radius)

                                        if shit_dict.get("Height"):
                                            height = pyRitoFile.bin.BINField()
                                            height.data = float(shit_dict.get("Height", 0))
                                            height.type = pyRitoFile.bin.BINType.F32
                                            height.hash = hash_helper.Storage.bin_hashes["Height"]
                                            shape.data.append(radius)
                                        if shit_dict["Flags"]:
                                            flags = pyRitoFile.bin.BINField()
                                            flags.data = 1
                                            flags.type = pyRitoFile.bin.BINType.U8
                                            flags.hash = hash_helper.Storage.bin_hashes["Flags"]
                                            shape.data.append(flags)
                                        continue
                                    else:
                                        if len(shape.data) == 1 and shape.data[0].hash == hash_helper.Storage.bin_hashes["EmitOffset"] and isinstance(shape.data[0].data[0].data, pyRitoFile.structs.Vector):
                                            # 0xee39916f moment, transform emitoffset to a vec3
                                            shape.hash_type = 'ee39916f'
                                            constant_value = shape.data[0].data[0]
                                            emitoffset = pyRitoFile.bin.BINField()
                                            emitoffset.type = pyRitoFile.bin.BINType.VEC3
                                            emitoffset.hash = hash_helper.Storage.bin_hashes["EmitOffset"]
                                            emitoffset.data = constant_value.data
                                            shape.data = [emitoffset]
                                            continue
                                        else:
                                            # Clueless, default 0x4f4e2ed7
                                            shape.hash_type = '4f4e2ed7'
                                            continue
    print(f'hapiBin: Finish: FixVfxShape and BirthTranslation.')
