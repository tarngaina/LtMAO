from LtMAO import setting
import os, winreg

pythonw_file = './cpy/pythonw.exe'
python_file = './cpy/python.exe'
gui_file = './src/gui.py'
cli_file = './src/cli.py'


class Context:
    submenus = {
        'Directory': {
            'RawToWad': True,
            'AllWadToRaw': True,
            'hashextract': True,
            'PT': True,
            'PTdeljunk': True,
            'ZipFantome': True,
            'RitobinDirToPy': True,
            'RitobinDirToBin': True,
            'tex2ddsdir': True,
            'dds2texdir': True,
            'dir2bnk': True,
            'dir2wpk': True,
            'wem2wavdir': True,
            'wav2wemdir': True,
            'ogg2wemdir': True
        }, 
        'No Extension': {
            'RitobinToPy': True,
        },
        'wad': {
            'WadToRaw': True,
            'hashextract': True,
            'PT': True,
            'PTdeljunk': True,
            'LFI': True,
        },
        'bin': {
            'RitobinToPy': True,
            'hashextract': True,
            'LFI': True,
        },
        'py': {
            'RitobinToBin': True,
        },
        'skl': {
            'hashextract': True,
            'LFI': True,
        },
        'skn': {
            'UVEE': True,
            'hashextract': True,
            'infinityQT': True,
            'LFI': True,
        },
        'sco': {
            'UVEE': True,
            'LFI': True,
        },
        'scb': {
            'UVEE': True,
            'LFI': True,
        },
        'anm': {
            'LFI': True,
        },
        'mapgeo': {
            'LFI': True,
        },
        'tex': {
            'tex2dds': True,
            'infinityQT': True,
            'LFI': True,
        },
        'dds': {
            'dds2tex': True,
            'dds2png': True,
            'dds2x4x': True,
        },
        'png': {
            'png2ddsmm': True,
            'png2dds': True,
        },
        'bnk': {
            'bnk2dir': True,
            'geb': True,
            'LFI': True,
        },
        'wpk': {
            'wpk2dir': True,
            'geb': True,
            'LFI': True,
        },
        'wem': {
            'wem2wav': True,
            'infinityQT': True,
        },
        'wav': {
            'wav2wem': True,
        },
        'ogg': {
            'ogg2wem': True,
        },
        'fantome': {
            'UnzipFantome': True,
        },
    }

    commands = {
        'RawToWad': {
            'desc': 'wad_tool: Pack To WAD',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadpack" -src="%V"'
        },
        'WadToRaw': {
            'desc': 'wad_tool: Unpack To Folder',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadunpack" -src="%V"'
        },
        'AllWadToRaw': {
            'desc': 'wad_tool: Unpack All WAD',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadunpack_all" -src="%V"'
        },
        'RitobinToPy': {
            'desc': 'ritobin: Convert To PY',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobin" -src="%V"'
        },
        'RitobinToBin': {
            'desc': 'ritobin: Convert To BIN',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobin" -src="%V"'
        },
        'RitobinDirToPy': {
            'desc': 'ritobin: Convert All BIN To PY',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobindir2py" -src="%V"'
        },
        'RitobinDirToBin': {
            'desc': 'ritobin: Convert All PY To BIN',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobindir2bin" -src="%V"'
        },
        'LFI': {
            'desc': 'file_inspector: Print infos as JSON',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="lfi" -src="%V"'
        },
        'UVEE': {
            'desc': 'uvee: Extract UVs out as PNGs',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="uvee" -src="%V"'
        },
        'hashextract': {
            'desc': 'hash_helper: Extract hashes',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="hashextract" -src="%V"'
        },
        'PT': {
            'desc': 'pyntex: Check mentioned, missing, junk files of BINs',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="pyntex" -src="%V"'
        },
        'PTdeljunk': {
            'desc': 'pyntex: Remove junk files',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="pyntexdeljunk" -src="%V"'
        },
        'tex2dds': {
            'desc': 'Ritoddstex: Convert To DDS',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="tex2dds" -src="%V"'
        },
        'dds2tex': {
            'desc': 'Ritoddstex: Convert To TEX',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2tex" -src="%V"'
        },
        'tex2ddsdir': {
            'desc': 'Ritoddstex: Convert All TEX To DDS',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="tex2ddsdir" -src="%V"'
        },
        'dds2texdir': {
            'desc': 'Ritoddstex: Convert All DDS To TEX',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2texdir" -src="%V"'
        },
        'dds2png': {
            'desc': 'ImageMagick: Convert To PNG',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2png" -src="%V"'
        },
        'png2dds': {
            'desc': 'ImageMagick: Convert To DDS (No Mipmap)',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="png2dds" -src="%V"'
        },
        'png2ddsmm': {
            'desc': 'ImageMagick: Convert To DDS',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="png2ddsmm" -src="%V"'
        },
        'dds2x4x': {
            'desc': 'ImageMagick: Make 2x_, 4x_ DDS',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2x4x" -src="%V"'
        },
        'wem2wav': {
            'desc': 'wiwawe: Convert To WAV',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wem2wav" -src="%V"'
        },
        'wav2wem': {
            'desc': 'wiwawe: Convert To WEM',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wav2wem" -src="%V"'
        },
        'ogg2wem': {
            'desc': 'wiwawe: Convert To WEM',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ogg2wem" -src="%V"'
        },
        'wem2wavdir': {
            'desc': 'wiwawe: Convert All WEM To WAV',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wem2wavdir" -src="%V"'
        },
        'wav2wemdir': {
            'desc': 'wiwawe: Convert All WAV To WEM',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wav2wemdir" -src="%V"'
        },
        'ogg2wemdir': {
            'desc': 'wiwawe: Convert All OGG To WEM',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ogg2wemdir" -src="%V"'
        },
        'ZipFantome': {
            'desc': 'cslmao: Zip Fantome',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="zipfantome" -src="%V"'
        },
        'UnzipFantome': {
            'desc': 'cslmao: Unzip Fantome',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="unzipfantome" -src="%V"'
        },
        'dir2bnk': {
            'desc': 'bnk_tool: Pack To BNK',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dir2bnk" -src="%V"'
        },
        'dir2wpk': {
            'desc': 'bnk_tool: Pack To WPK',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dir2wpk" -src="%V"'
        },
        'bnk2dir': {
            'desc': 'bnk_tool: Unpack To Folder',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="bnk2dir" -src="%V"'
        },
        'wpk2dir': {
            'desc': 'bnk_tool: Unpack To Folder',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wpk2dir" -src="%V"'
        },
        'geb': {
            'desc': 'bnk_tool: Guess name of Voice Events BNK',
            'value': f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="geb" -src="%V"'
        },
        'infinityQT': {
            'desc': 'infinityQT: Preview this file',
            'value': f'"{os.path.abspath(pythonw_file)}" "{os.path.abspath(cli_file)}" -t="infinityQT" -src="%V"'
        },
    }

    @staticmethod
    def get_shell(shell_id):
        if shell_id == 'Directory':
            return 'Directory\\shell'
        elif shell_id == 'No Extension':
            return 'SystemFileAssociations\\.\\shell'
        elif shell_id == 'wad':
            return 'SystemFileAssociations\\.client\\shell'
        else:
            return f'SystemFileAssociations\\.{shell_id}\\shell'

    @staticmethod
    def create_submenu(shell, sub_commands, icon_file):
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
    def create_command(root, cmd_name, cmd_desc, cmd_value, icon_file):
        subkey = winreg.CreateKeyEx(root, cmd_name)
        winreg.SetValue(subkey, None, winreg.REG_SZ, cmd_name)
        winreg.SetValueEx(subkey, 'MUIVerb', 0,
                          winreg.REG_SZ, cmd_desc)
        winreg.SetValueEx(subkey, 'Icon', 0, winreg.REG_SZ,
                          os.path.abspath(icon_file))
        command = winreg.CreateKeyEx(subkey, 'command')
        winreg.SetValue(command, None, winreg.REG_SZ, cmd_value)

    @staticmethod
    def create_contexts(icon_file):
        # create submenus
        for shell_id in Context.submenus:
            commands = [f'LtMAO.{command_id}' for command_id in Context.submenus[shell_id] if Context.submenus[shell_id][command_id]]
            if len(commands) > 0:
                Context.create_submenu(
                    shell=Context.get_shell(shell_id),
                    sub_commands=';'.join(commands),
                    icon_file=icon_file
                )
            else:
                Context.remove_submenu(Context.get_shell(shell_id))

        # create commands
        with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CommandStore\\shell') as key:
            for command_id in Context.commands:
                Context.create_command(
                    root=key,
                    cmd_name=f'LtMAO.{command_id}',
                    cmd_desc=Context.commands[command_id]['desc'],
                    cmd_value=Context.commands[command_id]['value'],
                    icon_file=icon_file
                )
        print('winLT: Finish: Set Explorer Contexts')

    @staticmethod
    def remove_submenu(shell):
        try:
            with winreg.OpenKeyEx(winreg.HKEY_CLASSES_ROOT, shell) as key:
                winreg.DeleteKeyEx(key, 'LtMAO')
        except FileNotFoundError:
            pass
        except Exception as e:
            raise e

    @staticmethod
    def remove_contexts():
        for shell_id in Context.submenus:
            Context.remove_submenu(Context.get_shell(shell_id))
        print('winLT: Finish: Remove Explorer Contexts')


class Shortcut:
    @staticmethod
    def create_shortcut(path, icon_file):
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = os.path.abspath(pythonw_file)
        shortcut.WorkingDirectory = os.path.abspath('.')
        shortcut.Arguments = f'"{os.path.abspath(gui_file)}"'
        shortcut.IconLocation = os.path.abspath(icon_file)
        shortcut.Description = 'Run LtMAO'
        shortcut.save()

    @staticmethod
    def create_desktop(icon_file):
        import userpaths
        desktop_file = f'{userpaths.get_desktop()}/LtMAO.lnk'.replace('\\', '/')
        Shortcut.create_shortcut(desktop_file, icon_file)
        print(f'winLT: Finish: Create Desktop Shortcut: {desktop_file}')

    @staticmethod
    def create_launch(icon_file):
        launch_file = os.path.abspath('./LtMAO.lnk')
        if not os.path.exists(launch_file):
            Shortcut.create_shortcut(launch_file, icon_file)
            print(f'winLT: Finish: Create Launch Shortcut: {launch_file}')

    @staticmethod
    def update_shortcuts(icon_file):
        import userpaths
        desktop_file = f'{userpaths.get_desktop()}/LtMAO.lnk'.replace('\\', '/')
        if os.path.exists(desktop_file):
            Shortcut.create_shortcut(desktop_file, icon_file)
        launch_file = os.path.abspath('./LtMAO.lnk')
        if os.path.exists(launch_file):
            Shortcut.create_shortcut(launch_file, icon_file)