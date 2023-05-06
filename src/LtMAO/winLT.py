
import os
import os.path

LOG = print


class Context:
    pass


class Desktop:
    desktop_dir = os.path.expanduser("~/Desktop").replace('\\', '/')
    lnk_file = f'{desktop_dir}/LtMAO.lnk'

    @staticmethod
    def create_shorcut():
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(Desktop.lnk_file)
        shortcut.Targetpath = os.path.abspath('./epython/pythonw.exe')
        shortcut.WorkingDirectory = os.path.abspath('.')
        shortcut.IconLocation = os.path.abspath('./resources/appicon.ico')
        shortcut.Description = 'Launch LtMAO.'
        shortcut.Arguments = os.path.abspath('./src/main.py')
        shortcut.save()
        LOG('Done: Create Desktop Shortcut')
    
    @staticmethod
    def create_launch_shortcut():
        launch_file = os.path.abspath('./LtMAO.lnk')
        if not os.path.exists(launch_file):
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(launch_file)
            shortcut.Targetpath = os.path.abspath('./epython/pythonw.exe')
            shortcut.WorkingDirectory = os.path.abspath('.')
            shortcut.IconLocation = os.path.abspath('./resources/appicon.ico')
            shortcut.Description = 'Launch LtMAO.'
            shortcut.Arguments = os.path.abspath('./src/main.py')
            shortcut.save()
            LOG('Done: Create Desktop Shortcut')


def prepare(_LOG):
    global LOG
    LOG = _LOG
    Desktop.create_launch_shortcut()
