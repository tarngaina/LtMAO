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
version_file = ltmao_dir+'/version'

from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from LtMAO.lemon3d.lemon_maya.plugins.translator.skin import SKNImporter, SKLImporter, SkinExporter, SKLExporter
from LtMAO.lemon3d.lemon_maya.plugins.translator.anm import ANMImporter, ANMExporter
from LtMAO.lemon3d.lemon_maya.plugins.translator.so import SCOImporter, SCOExporter, SCBImporter, SCBExporter
from LtMAO.lemon3d.lemon_maya.plugins.translator.mapgeo import MAPGEOImporter, MAPGEOExporter

AUTHOR = 'tarngaina'
try: 
    with open(version_file, 'r') as f:
        VERSION = f.read()
except:
    VERSION = 'Unknown'

def register_file_translator(plugin, translator_name, translator_creator, options_script, default_options_string):
    try: 
        plugin.registerFileTranslator(
            translator_name,
            '',
            translator_creator,
            options_script,
            default_options_string,
            True
        )
    except Exception as e:
        MGlobal.displayWarning(f'register_file_translator({translator_name}): Error: {e}: {e.message}')

def deregister_file_translator(plugin, translator_name):
    try: 
        plugin.deregisterFileTranslator(
            translator_name
        )
    except Exception as e:
        MGlobal.displayWarning(f'deregister_file_translator({translator_name}): Error: {e}: {e.message}')

def initializePlugin(obj):
    plugin = MFnPlugin(obj, AUTHOR, VERSION)
    # skin
    register_file_translator(plugin, SKNImporter.name, SKNImporter.creator, '', '')
    register_file_translator(plugin, SkinExporter.name, SkinExporter.creator, '', '')
    register_file_translator(plugin, SKLImporter.name, SKLImporter.creator, '', '')
    register_file_translator(plugin, SKLExporter.name, SKLExporter.creator, '', '')
    # anm
    register_file_translator(plugin, ANMImporter.name, ANMImporter.creator, 'ANMImporterOptions', 'reset_channel=1')
    register_file_translator(plugin, ANMExporter.name, ANMExporter.creator, '', '')
    # so
    register_file_translator(plugin, SCOImporter.name, SCOImporter.creator, '', '')
    register_file_translator(plugin, SCOExporter.name, SCOExporter.creator, '', '')
    register_file_translator(plugin, SCBImporter.name, SCBImporter.creator, '', '')
    register_file_translator(plugin, SCBExporter.name, SCBExporter.creator, 'SCBExporterOptions', 'scb_flags=HasLocalOriginLocatorAndPivot;')
    # mapgeo
    register_file_translator(plugin, MAPGEOImporter.name, MAPGEOImporter.creator, '', '')
    register_file_translator(plugin, MAPGEOExporter.name, MAPGEOExporter.creator, 'MAPGEOExporterOptions', 'version=17;float16=0')
    
def uninitializePlugin(obj):
    plugin = MFnPlugin(obj)
    #skin
    deregister_file_translator(plugin, SKNImporter.name)
    deregister_file_translator(plugin, SkinExporter.name)
    deregister_file_translator(plugin, SKLImporter.name)
    deregister_file_translator(plugin, SKLExporter.name)
    # anm
    deregister_file_translator(plugin, ANMImporter.name)
    deregister_file_translator(plugin, ANMExporter.name)
    # so
    deregister_file_translator(plugin, SCOImporter.name)
    deregister_file_translator(plugin, SCOExporter.name)
    deregister_file_translator(plugin, SCBImporter.name)
    deregister_file_translator(plugin, SCBExporter.name)
    # mapgeo
    deregister_file_translator(plugin, MAPGEOImporter.name)
    deregister_file_translator(plugin, MAPGEOExporter.name)