
import os
import os.path
import winreg

LOG = print
icon_file = './resources/appicon.ico'
pythonw_file = './epython/pythonw.exe'
python_file = './epython/python.exe'
gui_file = './src/gui.py'
cli_file = './src/cli.py'


class Context:
    @staticmethod
    def create_submenu(shell, sub_commands):
        with winreg.CreateKeyEx(winreg.HKEY_CLASSES_ROOT, shell) as key:
            shell_key = winreg.CreateKeyEx(key, 'LtMAO')
            winreg.SetValueEx(shell_key, 'MUIVerb', 0, winreg.REG_SZ, 'LtMAO')
            winreg.SetValueEx(shell_key, 'Icon', 0, winreg.REG_SZ,
                              os.path.abspath(icon_file))
            winreg.SetValueEx(shell_key, 'Position', 0, winreg.REG_SZ, 'mid')
            winreg.SetValueEx(
                shell_key,
                'SubCommands',
                0,
                winreg.REG_SZ,
                sub_commands
            )

    @staticmethod
    def create_command(root, cmd_name, cmd_desc, cmd_value):
        subkey = winreg.CreateKeyEx(root, cmd_name)
        winreg.SetValue(subkey, None, winreg.REG_SZ, cmd_name)
        winreg.SetValueEx(subkey, 'MUIVerb', 0,
                          winreg.REG_SZ, cmd_desc)
        winreg.SetValueEx(subkey, 'Icon', 0, winreg.REG_SZ,
                          os.path.abspath(icon_file))
        command = winreg.CreateKeyEx(subkey, 'command')
        winreg.SetValue(command, None, winreg.REG_SZ, cmd_value)

    @staticmethod
    def create_contexts():
        # folder contexts
        Context.create_submenu(
            shell='Directory\\shell',
            sub_commands='LtMAO.RawToWad'
        )
        # .wad (.client) contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.client\\shell',
            sub_commands='LtMAO.WadToRaw;LtMAO.LFI;LtMAO.hashextract'
        )
        # .bin contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.bin\\shell',
            sub_commands='LtMAO.RitobinToPy;LtMAO.LFI;LtMAO.hashextract'
        )
        # .py contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.py\\shell',
            sub_commands='LtMAO.RitobinToBin'
        )
        # .skl contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.skl\\shell',
            sub_commands='LtMAO.LFI;LtMAO.hashextract'
        )
        # .skn contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.skn\\shell',
            sub_commands='LtMAO.LFI;LtMAO.UVEE;LtMAO.hashextract'
        )
        # .sco contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.sco\\shell',
            sub_commands='LtMAO.LFI;LtMAO.UVEE'
        )
        # .scb contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.scb\\shell',
            sub_commands='LtMAO.LFI;LtMAO.UVEE'
        )

        # create commands
        with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CommandStore\\shell') as key:
            # RawToWad
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RawToWad',
                cmd_desc='wad_tool: Pack to WAD',
                cmd_value=f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=wadpack -src="%V"'
            )
            # WadToRaw
            Context.create_command(
                root=key,
                cmd_name='LtMAO.WadToRaw',
                cmd_desc='wad_tool: Unpack to Folder',
                cmd_value=f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=wadunpack -src="%V"'
            )
            # RitobinToPy
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RitobinToPy',
                cmd_desc='ritobin: Convert To PY',
                cmd_value=f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=ritobin -src="%V"'
            )
            # RitobinToBin
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RitobinToBin',
                cmd_desc='ritobin: Convert To BIN',
                cmd_value=f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=ritobin -src="%V"'
            )
            # LFI
            Context.create_command(
                root=key,
                cmd_name='LtMAO.LFI',
                cmd_desc='leaguefile_inspector: Print infos as JSON',
                cmd_value=f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=lfi -src="%V"'
            )
            # UVEE
            Context.create_command(
                root=key,
                cmd_name='LtMAO.UVEE',
                cmd_desc='uvee: Extract UVs out as PNGs',
                cmd_value=f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=uvee -src="%V"'
            )
            # hashextract
            Context.create_command(
                root=key,
                cmd_name='LtMAO.hashextract',
                cmd_desc='hash_manager: Extract hashes',
                cmd_value=f'{os.path.abspath(python_file)} {os.path.abspath(cli_file)} -t=hashextract -src="%V"'
            )
        LOG('Done: Create Explorer Contexts')

    @staticmethod
    def remove_context(shell):
        with winreg.OpenKeyEx(winreg.HKEY_CLASSES_ROOT, shell) as key:
            try:
                winreg.DeleteKeyEx(key, 'LtMAO')
            except:
                pass

    @staticmethod
    def remove_contexts():
        # folder contexts
        Context.remove_context('Directory\\shell')
        # .wad (.client) contexts
        Context.remove_context('SystemFileAssociations\\.client\\shell')
        # .bin contexts
        Context.remove_context('SystemFileAssociations\\.bin\\shell')
        # .py contexts
        Context.remove_context('SystemFileAssociations\\.py\\shell')
        # .skl contexts
        Context.remove_context('SystemFileAssociations\\.skl\\shell')
        # .skn contexts
        Context.remove_context('SystemFileAssociations\\.skn\\shell')
        # .sco contexts
        Context.remove_context('SystemFileAssociations\\.sco\\shell')
        # .scb contexts
        Context.remove_context('SystemFileAssociations\\.scb\\shell')
        LOG('Done: Remove Explorer Contexts')


class Shortcut:
    @staticmethod
    def create_desktop():
        desktop_dir = os.path.expanduser("~/Desktop").replace('\\', '/')
        desktop_file = f'{desktop_dir}/LtMAO.lnk'
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(desktop_file)
        shortcut.Targetpath = os.path.abspath(pythonw_file)
        shortcut.WorkingDirectory = os.path.abspath('.')
        shortcut.IconLocation = os.path.abspath(icon_file)
        shortcut.Description = 'Launch LtMAO.'
        shortcut.Arguments = os.path.abspath(gui_file)
        shortcut.save()
        LOG('Done: Create Desktop Shortcut')

    @staticmethod
    def create_launch():
        launch_file = os.path.abspath('./LtMAO.lnk')
        if not os.path.exists(launch_file):
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(launch_file)
            shortcut.Targetpath = os.path.abspath(pythonw_file)
            shortcut.WorkingDirectory = os.path.abspath('.')
            shortcut.IconLocation = os.path.abspath(icon_file)
            shortcut.Description = 'Launch LtMAO.'
            shortcut.Arguments = os.path.abspath(gui_file)
            shortcut.save()
            LOG('Done: Create Launch Shortcut')


def prepare(_LOG):
    global LOG
    LOG = _LOG
    Shortcut.create_launch()
