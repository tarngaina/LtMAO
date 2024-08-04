
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
            sub_commands='LtMAO.RawToWad;LtMAO.ZipFantome;LtMAO.hashextract;LtMAO.PT;'
        )
        # .wad (.client) contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.client\\shell',
            sub_commands='LtMAO.WadToRaw;LtMAO.hashextract;LtMAO.PT;LtMAO.LFI;'
        )
        # .bin contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.bin\\shell',
            sub_commands='LtMAO.RitobinToPy;LtMAO.hashextract;LtMAO.LFI;'
        )
        # .py contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.py\\shell',
            sub_commands='LtMAO.RitobinToBin;'
        )
        # .skl contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.skl\\shell',
            sub_commands='LtMAO.hashextract;LtMAO.LFI;'
        )
        # .skn contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.skn\\shell',
            sub_commands='LtMAO.UVEE;LtMAO.hashextract;LtMAO.LFI;'
        )
        # .sco contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.sco\\shell',
            sub_commands='LtMAO.UVEE;LtMAO.LFI;'
        )
        # .scb contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.scb\\shell',
            sub_commands='LtMAO.UVEE;LtMAO.LFI;'
        )
        # .anm contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.anm\\shell',
            sub_commands='LtMAO.LFI;'
        )
        # .mapgeo contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.mapgeo\\shell',
            sub_commands='LtMAO.LFI;'
        )
        # .tex contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.tex\\shell',
            sub_commands='LtMAO.tex2dds;LtMAO.LFI;'
        )
        # .dds contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.dds\\shell',
            sub_commands='LtMAO.dds2tex;LtMAO.dds2png;LtMAO.dds2x4x'
        )
        # .png contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.png\\shell',
            sub_commands='LtMAO.png2dds;'
        )
        # .bnk contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.bnk\\shell',
            sub_commands='LtMAO.LFI;'
        )
        # .wpk contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.wpk\\shell',
            sub_commands='LtMAO.LFI;'
        )
        # .wem contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.wem\\shell',
            sub_commands='LtMAO.wem2ogg;'
        )
        # .fantome contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.fantome\\shell',
            sub_commands='LtMAO.UnzipFantome;'
        )

        # create commands
        with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CommandStore\\shell') as key:
            # RawToWad
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RawToWad',
                cmd_desc='wad_tool: Pack to WAD',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadpack" -src="%V"'
            )
            # WadToRaw
            Context.create_command(
                root=key,
                cmd_name='LtMAO.WadToRaw',
                cmd_desc='wad_tool: Unpack to Folder',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadunpack" -src="%V"'
            )
            # RitobinToPy
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RitobinToPy',
                cmd_desc='ritobin: Convert To PY',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobin" -src="%V"'
            )
            # RitobinToBin
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RitobinToBin',
                cmd_desc='ritobin: Convert To BIN',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobin" -src="%V"'
            )
            # LFI
            Context.create_command(
                root=key,
                cmd_name='LtMAO.LFI',
                cmd_desc='leaguefile_inspector: Print infos as JSON',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="lfi" -src="%V"'
            )
            # UVEE
            Context.create_command(
                root=key,
                cmd_name='LtMAO.UVEE',
                cmd_desc='uvee: Extract UVs out as PNGs',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="uvee" -src="%V"'
            )
            # hashextract
            Context.create_command(
                root=key,
                cmd_name='LtMAO.hashextract',
                cmd_desc='hash_manager: Extract hashes',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="hashextract" -src="%V"'
            )
            # PT
            Context.create_command(
                root=key,
                cmd_name='LtMAO.PT',
                cmd_desc='pyntex: Check mentioned, missing files of BINs',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="pyntex" -src="%V"'
            )
            # tex2dds
            Context.create_command(
                root=key,
                cmd_name='LtMAO.tex2dds',
                cmd_desc='Ritoddstex: Convert To DDS',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="tex2dds" -src="%V"'
            )
            # dds2tex
            Context.create_command(
                root=key,
                cmd_name='LtMAO.dds2tex',
                cmd_desc='Ritoddstex: Convert To TEX',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2tex" -src="%V"'
            )
            # dds2png
            Context.create_command(
                root=key,
                cmd_name='LtMAO.dds2png',
                cmd_desc='ImageMagick: Convert To PNG',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2png" -src="%V"'
            )
            # png2dds
            Context.create_command(
                root=key,
                cmd_name='LtMAO.png2dds',
                cmd_desc='ImageMagick: Convert To DDS (No Mipmap)',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="png2dds" -src="%V"'
            )
            # dds2x4x
            Context.create_command(
                root=key,
                cmd_name='LtMAO.dds2x4x',
                cmd_desc='ImageMagick: Make 2x_, 4x_ DDS',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2x4x" -src="%V"'
            )
            # wem2ogg
            Context.create_command(
                root=key,
                cmd_name='LtMAO.wem2ogg',
                cmd_desc='ww2ogg, ReVorb: Convert To Ogg',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wem2ogg" -src="%V"'
            )
            # ZipFantome
            Context.create_command(
                root=key,
                cmd_name='LtMAO.ZipFantome',
                cmd_desc='cslmao: Zip Fantome',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="zipfantome" -src="%V"'
            )
            # UnzipFantome
            Context.create_command(
                root=key,
                cmd_name='LtMAO.UnzipFantome',
                cmd_desc='cslmao: Unzip Fantome',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="unzipfantome" -src="%V"'
            )
        LOG('winLT: Done: Create Explorer Contexts')

    @staticmethod
    def remove_submenu(shell):
        with winreg.OpenKeyEx(winreg.HKEY_CLASSES_ROOT, shell) as key:
            try:
                winreg.DeleteKeyEx(key, 'LtMAO')
            except Exception as e:
                raise e

    @staticmethod
    def remove_contexts():
        # folder contexts
        Context.remove_submenu('Directory\\shell')
        # .wad (.client) contexts
        Context.remove_submenu('SystemFileAssociations\\.client\\shell')
        # .bin contexts
        Context.remove_submenu('SystemFileAssociations\\.bin\\shell')
        # .py contexts
        Context.remove_submenu('SystemFileAssociations\\.py\\shell')
        # .skl contexts
        Context.remove_submenu('SystemFileAssociations\\.skl\\shell')
        # .skn contexts
        Context.remove_submenu('SystemFileAssociations\\.skn\\shell')
        # .sco contexts
        Context.remove_submenu('SystemFileAssociations\\.sco\\shell')
        # .scb contexts
        Context.remove_submenu('SystemFileAssociations\\.scb\\shell')
        # .anm contexts
        Context.remove_submenu('SystemFileAssociations\\.anm\\shell')
        # .mapgeo contexts
        Context.remove_submenu('SystemFileAssociations\\.mapgeo\\shell')
        # .tex contexts
        Context.remove_submenu('SystemFileAssociations\\.tex\\shell')
        # .dds contexts
        Context.remove_submenu('SystemFileAssociations\\.dds\\shell')
        # .png contexts
        Context.remove_submenu('SystemFileAssociations\\.png\\shell')
        LOG('winLT: Done: Remove Explorer Contexts')


class Shortcut:
    @staticmethod
    def create_desktop():
        # need to fix desktop dir
        desktop_dir = os.path.expanduser("~/Desktop").replace('\\', '/')
        desktop_file = f'{desktop_dir}/LtMAO.lnk'
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(desktop_file)
        shortcut.Targetpath = os.path.abspath(pythonw_file)
        shortcut.WorkingDirectory = os.path.abspath('.')
        shortcut.Arguments = f'"{os.path.abspath(gui_file)}"'
        shortcut.IconLocation = os.path.abspath(icon_file)
        shortcut.Description = 'Run LtMAO'
        shortcut.save()
        LOG(f'winLT: Done: Create Desktop Shortcut: {desktop_file}')

    @staticmethod
    def create_launch():
        launch_file = os.path.abspath('./LtMAO.lnk')
        if not os.path.exists(launch_file):
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(launch_file)
            shortcut.Targetpath = os.path.abspath(pythonw_file)
            shortcut.WorkingDirectory = os.path.abspath('.')
            shortcut.Arguments = f'"{os.path.abspath(gui_file)}"'
            shortcut.IconLocation = os.path.abspath(icon_file)
            shortcut.Description = 'Run LtMAO'
            shortcut.save()
            LOG(f'winLT: Done: Create Launch Shortcut: {launch_file}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
    Shortcut.create_launch()
