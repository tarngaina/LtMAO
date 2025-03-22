from maya.OpenMaya import *
from maya.OpenMayaMPx import *
from maya.OpenMayaAnim import *
from maya import cmds

import os.path
from . import helper
from ..... import pyRitoFile
from .....pyRitoFile.helper import Elf
from .....pyRitoFile.structs import Vector, Quaternion


class MAPGEOTranslator(MPxFileTranslator):
    name = 'League of Legends: MAPGEO'
    extension = 'mapgeo'

    def __init__(self):
        MPxFileTranslator.__init__(self)

    def haveReadMethod(self):
        return True
    
    def haveWriteMethod(self):
        return True

    def defaultExtension(self):
        return self.extension

    def filter(self):
        return f'*.{self.extension}'
    
    def identifyFile(self, file, buffer, size):
        if file.fullName().endswith(f'.{self.extension}'):
            return MPxFileTranslator.kIsMyFileType
        return MPxFileTranslator.kNotMyFileType

    @classmethod
    def creator(cls):
        return asMPxPtr(cls())

    def reader(self, file, option, access):
        mapgeo_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
        # read mapgeo
        mapgeo = pyRitoFile.read_mapgeo(mapgeo_path)
        # load mapgeo
        helper.mirrorX(mapgeo=mapgeo)
        MAPGEO.scene_load(mapgeo)
        return True

    def writer(self, file, option, access):
        # export options
        mapgeo_path = helper.ensure_path_extension(file.expandedFullName(), self.extension)
        dismiss, mapgeo_export_options = MAPGEO.create_ui_mapgeo_export_options(mapgeo_path)
        if dismiss != 'Export':
            return False
        mapgeo = pyRitoFile.MAPGEO()
        dump_options = {
            'version': mapgeo_export_options['version'],
            'riot_mapgeo_path': mapgeo_export_options['riot_mapgeo_path'],
        }
        MAPGEO.scene_dump(mapgeo, dump_options)
        helper.mirrorX(mapgeo=mapgeo)
        pyRitoFile.write_mapgeo(mapgeo_path, mapgeo)
        return True

class MAPGEO:
    @staticmethod
    def create_ui_mapgeo_export_options(mapgeo_path):
        # check riot mapgeo path
        riot_mapgeo_path = os.path.join(
            os.path.dirname(mapgeo_path), 
            f'riot_{os.path.basename(mapgeo_path)}'
        ).replace('\\', '/')
        if not os.path.exists(riot_mapgeo_path):
            riot_mapgeo_path = os.path.join(
                os.path.dirname(mapgeo_path),
                'riot.mapgeo'
            ).replace('\\', '/')
        if not os.path.exists(riot_mapgeo_path):
            riot_mapgeo_path = ''

        mapgeo_export_options = {
            'version': 17,
            'riot_mapgeo_path': riot_mapgeo_path
        } 
        def set_value_cmd(key, value):
            mapgeo_export_options[key] = value

        def ui_cmd():
            cmds.columnLayout()

            cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
            cmds.text(label='MAPGEO Path:')
            cmds.text(label=mapgeo_path, align='left', width=600)
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=1, adjustableColumn=1)
            cmds.optionMenu(label='Version: ')
            cmds.menuItem(label = '17')
            cmds.menuItem(label = '15')
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=3, adjustableColumn=3)
            cmds.text(label='Riot MAPGEO Path:')
            mapgeo_text = cmds.text(label=riot_mapgeo_path, align='left', width=600)
            def mapgeobrowse_cmd(text):
                mapgeo_path = cmds.fileDialog2(
                    dialogStyle=2, 
                    fileMode=1,
                    fileFilter='MAPGEO(*.mapgeo)',
                    caption='Select Riot MAPGEO file',
                    okCaption='Select'
                )
                if mapgeo_path:
                    mapgeo_path = mapgeo_path[0].replace('\\', '/')
                    cmds.text(text, edit=True, label=mapgeo_path)
                    mapgeo_export_options['riot_mapgeo_path'] = mapgeo_path
            cmds.button(label='Browse Riot MAPGEO', command=lambda e: mapgeobrowse_cmd(mapgeo_text))
            cmds.setParent('..')

            cmds.rowLayout(numberOfColumns=2)
            cmds.text(label='', w=700)
            def dismiss(result):
                cmds.layoutDialog(dismiss=result)
            cmds.button(label='Export', width=100, command=lambda e: dismiss('Export'))
        
        return cmds.layoutDialog(title='ANM Export Options', ui=ui_cmd), mapgeo_export_options

    @staticmethod
    def scene_load(mapgeo):
        pass

    @staticmethod
    def scene_dump(mapgeo, dump_options):
        pass