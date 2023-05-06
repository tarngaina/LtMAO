
import os
import os.path
import winreg

LOG = print
icon_file = './resources/appicon.ico'
pythonw_file = './epython/pythonw.exe'
python_file = './epython/python.exe'
main_file = './src/main.py'
cli_file = './src/cli.py'


class Context:
    @staticmethod
    def create_contexts():
        # folder contexts
        with winreg.OpenKeyEx(winreg.HKEY_CLASSES_ROOT, 'Directory\\shell') as key:
            subkey = winreg.CreateKeyEx(key, 'LtMAO')
            winreg.SetValueEx(subkey, 'MUIVerb', 0, winreg.REG_SZ, 'LtMAO')
            winreg.SetValueEx(subkey, 'Icon', 0, winreg.REG_SZ,
                              os.path.abspath(icon_file))
            winreg.SetValueEx(subkey, 'Position', 0, winreg.REG_SZ, 'mid')
            winreg.SetValueEx(
                subkey,
                'SubCommands',
                0,
                winreg.REG_SZ,
                'LtMAO.RawToWad'
            )
        # .wad contexts
        with winreg.CreateKeyEx(winreg.HKEY_CLASSES_ROOT, 'SystemFileAssociations\\.client\\shell') as key:
            subkey = winreg.CreateKeyEx(key, 'LtMAO')
            winreg.SetValueEx(subkey, 'MUIVerb', 0, winreg.REG_SZ, 'LtMAO')
            winreg.SetValueEx(subkey, 'Icon', 0, winreg.REG_SZ,
                              os.path.abspath(icon_file))
            winreg.SetValueEx(subkey, 'Position', 0, winreg.REG_SZ, 'mid')
            winreg.SetValueEx(
                subkey,
                'SubCommands',
                0,
                winreg.REG_SZ,
                'LtMAO.WadToRaw'
            )

        # create commands
        with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CommandStore\\shell') as key:
            # RawToWad
            subkey = winreg.CreateKeyEx(key, 'LtMAO.RawToWad')
            winreg.SetValue(subkey, None, winreg.REG_SZ, 'LtMAO.RawToWad')
            winreg.SetValueEx(subkey, 'MUIVerb', 0,
                              winreg.REG_SZ, 'Pack RAW to WAD')
            winreg.SetValueEx(subkey, 'Icon', 0, winreg.REG_SZ,
                              os.path.abspath(icon_file))
            command = winreg.CreateKeyEx(subkey, 'command')
            cmd = f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=wadpack -src="%V"'
            winreg.SetValue(command, None, winreg.REG_SZ, cmd)
            # WadToRaw
            subkey = winreg.CreateKeyEx(key, 'LtMAO.WadToRaw')
            winreg.SetValue(subkey, None, winreg.REG_SZ, 'LtMAO.WadToRaw')
            winreg.SetValueEx(subkey, 'MUIVerb', 0,
                              winreg.REG_SZ, 'Unpack WAD to RAW')
            winreg.SetValueEx(subkey, 'Icon', 0, winreg.REG_SZ,
                              os.path.abspath(icon_file))
            command = winreg.CreateKeyEx(subkey, 'command')
            cmd = f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=wadunpack -src="%V"'
            winreg.SetValue(command, None, winreg.REG_SZ, cmd)

    @staticmethod
    def remove_contexts():
        # folder contexts
        with winreg.OpenKeyEx(winreg.HKEY_CLASSES_ROOT, 'Directory\\shell') as key:
            try:
                winreg.DeleteKeyEx(key, 'LtMAO')
            except:
                pass


class Desktop:
    desktop_dir = os.path.expanduser("~/Desktop").replace('\\', '/')
    lnk_file = f'{desktop_dir}/LtMAO.lnk'

    @staticmethod
    def create_shorcut():
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(Desktop.lnk_file)
        shortcut.Targetpath = os.path.abspath(pythonw_file)
        shortcut.WorkingDirectory = os.path.abspath('.')
        shortcut.IconLocation = os.path.abspath(icon_file)
        shortcut.Description = 'Launch LtMAO.'
        shortcut.Arguments = os.path.abspath(main_file)
        shortcut.save()
        LOG('Done: Create Desktop Shortcut')

    @staticmethod
    def create_launch_shortcut():
        launch_file = os.path.abspath('./LtMAO.lnk')
        if not os.path.exists(launch_file):
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(launch_file)
            shortcut.Targetpath = os.path.abspath(pythonw_file)
            shortcut.WorkingDirectory = os.path.abspath('.')
            shortcut.IconLocation = os.path.abspath(icon_file)
            shortcut.Description = 'Launch LtMAO.'
            shortcut.Arguments = os.path.abspath(main_file)
            shortcut.save()
            LOG('Done: Create Desktop Shortcut')


def prepare(_LOG):
    global LOG
    LOG = _LOG
    Desktop.create_launch_shortcut()
