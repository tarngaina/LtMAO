from maya.OpenMaya import *
from maya.OpenMayaMPx import *

def try_cmd(cmd):
    try:
        cmd()
        return True
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise e

def ensure_pythonpaths():
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
    # extra: set some global values 
    global AUTHOR, VERSION
    AUTHOR = 'tarngaina'
    version_file = ltmao_dir+'/version'
    try: 
        with open(version_file, 'r', encoding='utf-8') as f:
            VERSION = f.read()
    except:
        VERSION = 'Unknown'

try_cmd(ensure_pythonpaths)

def initializePlugin(obj):
    def register_cmd(obj):
        plugin = MFnPlugin(obj, AUTHOR, VERSION)
        # skin
        from LtMAO.lemon3d.lemon_maya.plugins.translator.skin import SKNImporter, SKLImporter, SkinExporter, SKLExporter
        plugin.registerFileTranslator(SKNImporter.name, '', SKNImporter.creator, '', '', True)
        plugin.registerFileTranslator(SkinExporter.name, '', SkinExporter.creator, '', '', True)
        plugin.registerFileTranslator(SKLImporter.name, '', SKLImporter.creator, '', '', True)
        plugin.registerFileTranslator(SKLExporter.name, '', SKLExporter.creator, '', '', True)
        # anm
        from LtMAO.lemon3d.lemon_maya.plugins.translator.anm import ANMImporter, ANMExporter
        plugin.registerFileTranslator(ANMImporter.name, '', ANMImporter.creator, 'ANMImporterOptions', 'reset_channel=1', True)
        plugin.registerFileTranslator(ANMExporter.name, '', ANMExporter.creator, '', '', True)
        # so
        from LtMAO.lemon3d.lemon_maya.plugins.translator.so import SCOImporter, SCOExporter, SCBImporter, SCBExporter
        plugin.registerFileTranslator(SCOImporter.name, '', SCOImporter.creator, '', '', True)
        plugin.registerFileTranslator(SCOExporter.name, '', SCOExporter.creator, '', '', True)
        plugin.registerFileTranslator(SCBImporter.name, '', SCBImporter.creator, '', '', True)
        plugin.registerFileTranslator(SCBExporter.name, '', SCBExporter.creator, 'SCBExporterOptions', 'scb_flags=HasLocalOriginLocatorAndPivot', True)
        # mapgeo
        from LtMAO.lemon3d.lemon_maya.plugins.translator.mapgeo import MAPGEOImporter, MAPGEOExporter
        plugin.registerFileTranslator(MAPGEOImporter.name, '', MAPGEOImporter.creator, '', '', True)
        plugin.registerFileTranslator(MAPGEOExporter.name, '', MAPGEOExporter.creator, 'MAPGEOExporterOptions', 'version=17;float16=0', True)
    
    try_cmd(lambda: register_cmd(obj))
def uninitializePlugin(obj):
    def deregister(obj):
        plugin = MFnPlugin(obj)
        #skin
        from LtMAO.lemon3d.lemon_maya.plugins.translator.skin import SKNImporter, SKLImporter, SkinExporter, SKLExporter
        plugin.deregisterFileTranslator(SKNImporter.name)
        plugin.deregisterFileTranslator(SkinExporter.name)
        plugin.deregisterFileTranslator(SKLImporter.name)
        plugin.deregisterFileTranslator(SKLExporter.name)
        # anm
        from LtMAO.lemon3d.lemon_maya.plugins.translator.anm import ANMImporter, ANMExporter
        plugin.deregisterFileTranslator(ANMImporter.name)
        plugin.deregisterFileTranslator(ANMExporter.name)
        # so
        from LtMAO.lemon3d.lemon_maya.plugins.translator.so import SCOImporter, SCOExporter, SCBImporter, SCBExporter
        plugin.deregisterFileTranslator(SCOImporter.name)
        plugin.deregisterFileTranslator(SCOExporter.name)
        plugin.deregisterFileTranslator(SCBImporter.name)
        plugin.deregisterFileTranslator(SCBExporter.name)
        # mapgeo
        from LtMAO.lemon3d.lemon_maya.plugins.translator.mapgeo import MAPGEOImporter, MAPGEOExporter
        plugin.deregisterFileTranslator(MAPGEOImporter.name)
        plugin.deregisterFileTranslator(MAPGEOExporter.name)
    
    try_cmd(lambda: deregister(obj))