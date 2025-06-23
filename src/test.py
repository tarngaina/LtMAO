from LtMAO import ritobin, pyRitoFile, file_inspector, hash_helper, tools


def db(func):
    import cProfile, pstats
    with cProfile.Profile() as profiler:
        func()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(15)

def test2():
    ritobin.text_to_bin('D:/test/a.py', 'D:/test/a.bin')

def test():
    ss = ritobin.Reader.stream_from("""
    "Characters/Aatrox/Skins/Skin0/Particles/Aatrox_Base_E_Active_buff" = VfxSystemDefinitionData {
        complexEmitterDefinitionData: list[pointer] = {
            VfxEmitterDefinitionData {
                rate: embed = ValueFloat {
                    constantValue: f32 = 1
                }
                particleLifetime: embed = ValueFloat {
                    constantValue: f32 = 1.5
                }
                particleLinger: option[f32] = {
                    1
                }
                lifetime: option[f32] = {
                    1
                }
                isSingleParticle: flag = true
                emitterName: string = "Avatar"
                bindWeight: embed = ValueFloat {
                    constantValue: f32 = 1
                }
                primitive: pointer = VfxPrimitiveAttachedMesh {
                    mMesh: embed = VfxMeshDefinitionData {
                        mSubmeshesToDraw: list[hash] = {
                            "BODY"
                            "Shoulder"
                        }
                    }
                }
                blendMode: u8 = 1
                color: embed = ValueColor {
                    dynamics: pointer = VfxAnimatedColorVariableData {
                        times: list[f32] = {
                            0
                            0.100000001
                            0.899999976
                            1
                        }
                        values: list[vec4] = {
                            { 1, 1, 1, 0 }
                            { 1, 1, 1, 1 }
                            { 1, 1, 1, 1 }
                            { 1, 1, 1, 0 }
                        }
                    }
                }
                depthBiasFactors: vec2 = { -1, -1 }
                disableBackfaceCull: bool = true
                particleIsLocalOrientation: flag = true
                isUniformScale: flag = true
                isRandomStartFrame: flag = true
                birthScale0: embed = ValueVector3 {
                    constantValue: vec3 = { 1.00100005, 1.00100005, 1.00100005 }
                }
                texture: string = "ASSETS/Characters/Aatrox/Skins/Base/Particles/Aatrox_Base_E_buff_avatar.tex"
                uvMode: u8 = 2
            }
            VfxEmitterDefinitionData {
                rate: embed = ValueFloat {
                    constantValue: f32 = 1
                }
                particleLifetime: embed = ValueFloat {
                    constantValue: f32 = 0.25
                }
                particleLinger: option[f32] = {
                    1
                }
                lifetime: option[f32] = {
                    1
                }
                isSingleParticle: flag = true
                emitterName: string = "Avatar_activate"
                bindWeight: embed = ValueFloat {
                    constantValue: f32 = 1
                }
                primitive: pointer = VfxPrimitiveAttachedMesh {
                    mMesh: embed = VfxMeshDefinitionData {
                        mSubmeshesToDraw: list[hash] = {
                            "BODY"
                            "Shoulder"
                        }
                    }
                }
                blendMode: u8 = 4
                color: embed = ValueColor {
                    constantValue: vec4 = { 1, 1, 1, 0.650003791 }
                    dynamics: pointer = VfxAnimatedColorVariableData {
                        times: list[f32] = {
                            0
                            0.100000001
                            0.800000012
                            1
                        }
                        values: list[vec4] = {
                            { 1, 1, 1, 0 }
                            { 1, 1, 1, 0.650003791 }
                            { 1, 1, 1, 0.650003791 }
                            { 1, 1, 1, 0 }
                        }
                    }
                }
                pass: i16 = 1
                disableBackfaceCull: bool = true
                particleIsLocalOrientation: flag = true
                isUniformScale: flag = true
                isRandomStartFrame: flag = true
                uvScrollClamp: flag = true
                birthScale0: embed = ValueVector3 {
                    constantValue: vec3 = { 1.00999999, 1.00999999, 1.00999999 }
                }
                texture: string = "ASSETS/Characters/Aatrox/Skins/Base/Particles/Aatrox_Base_E_buff_avatar_sheen.tex"
                uvMode: u8 = 2
                birthUvScrollRate: embed = ValueVector2 {
                    constantValue: vec2 = { 0, 2 }
                }
                texAddressModeBase: u8 = 2
            }
        }
        particleName: string = "Aatrox_Base_E_Active_buff"
        particlePath: string = "Characters/Aatrox/Skins/Skin0/Particles/Aatrox_Base_E_Active_buff"
    }
    """)

    entry = ritobin.Reader.read_entry(ss)

    import json
    print(json.dumps(entry, indent=4, ensure_ascii=False, cls=file_inspector.FIEncoder))

db(test2)