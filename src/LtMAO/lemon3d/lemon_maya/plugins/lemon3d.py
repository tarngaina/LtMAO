# pythonpath can be overrided by windows environment variable
# in that case maya.env's pythonpath will be completely ignored
# so this part manually add ltmao to python paths 
import inspect
import sys
lemon3d_file = inspect.getfile(inspect.currentframe()).replace('\\', '/')
ltmao_dir = lemon3d_file.replace('/src/LtMAO/lemon3d/lemon_maya/plugins/lemon3d.py', '')
pythonpaths = [f'{ltmao_dir}/src', f'{ltmao_dir}/epython/Lib/site-packages']
for pythonpath in pythonpaths:
    if pythonpath not in sys.path:
        sys.path.append(pythonpath)


from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from LtMAO.lemon3d.lemon_maya.plugins.translator.skin import SKNTranslator, SKLTranslator, SkinTranslator
from LtMAO.lemon3d.lemon_maya.plugins.translator.anm import ANMTranslator
from LtMAO.lemon3d.lemon_maya.plugins.translator.so import SCOTranslator, SCBTranslator

AUTHOR = 'tarngaina'
VERSION = '5.0.0'


def register_file_translator(plugin, translator_name, translator_creator):
    plugin.registerFileTranslator(
        translator_name,
        None,
        translator_creator,
        None,
        None,
        True
    )

def deregister_file_translator(plugin, translator_name):
    plugin.deregisterFileTranslator(
        translator_name
    )

def initializePlugin(obj):
    plugin = MFnPlugin(obj, AUTHOR, VERSION)
    register_file_translator(plugin, SKNTranslator.name, SKNTranslator.creator)
    register_file_translator(plugin, SKLTranslator.name, SKLTranslator.creator)
    register_file_translator(plugin, SkinTranslator.name, SkinTranslator.creator)
    register_file_translator(plugin, ANMTranslator.name, ANMTranslator.creator)
    register_file_translator(plugin, SCOTranslator.name, SCOTranslator.creator)
    register_file_translator(plugin, SCBTranslator.name, SCBTranslator.creator)
    
def uninitializePlugin(obj):
    plugin = MFnPlugin(obj)
    plugin.deregisterFileTranslator(SKNTranslator.name)
    plugin.deregisterFileTranslator(SKLTranslator.name)
    plugin.deregisterFileTranslator(SkinTranslator.name)
    plugin.deregisterFileTranslator(ANMTranslator.name)
    plugin.deregisterFileTranslator(SCOTranslator.name)
    plugin.deregisterFileTranslator(SCBTranslator.name)