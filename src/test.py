from LtMAO.lemon3d import lemon_fbx

lemon_fbx.skin_to_fbx(
    'D:/Test/base/aatrox.skl',
    'D:/Test/base/aatrox.skn',
    'D:/Test/base/animations',
    'D:/Test/base_fbx/aatrox.fbx'
)

lemon_fbx.fbx_to_skin(
    'D:/Test/base_fbx/aatrox.fbx',
    'D:/Test/base_skin/aatrox.skl',
    'D:/Test/base_skin/aatrox.skn',
    'D:/Test/base_skin/animations'
)