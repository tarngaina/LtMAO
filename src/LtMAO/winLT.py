
import os
import os.path
import winreg

icon_file = './res/appicon.ico'
pythonw_file = './cpy/pythonw.exe'
python_file = './cpy/python.exe'
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
            sub_commands='LtMAO.RawToWad;LtMAO.AllWadToRaw;LtMAO.hashextract;LtMAO.ZipFantome;LtMAO.dir2bnk;LtMAO.dir2wpk;LtMAO.PT;LtMAO.RitobinDirToPy;LtMAO.RitobinDirToBin;LtMAO.tex2ddsdir;LtMAO.dds2texdir;'
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
            sub_commands='LtMAO.dds2tex;LtMAO.dds2png;LtMAO.dds2x4x;'
        )
        # .png contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.png\\shell',
            sub_commands='LtMAO.png2dds;LtMAO.png2ddsmm;'
        )
        # .bnk contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.bnk\\shell',
            sub_commands='LtMAO.bnk2dir;LtMAO.geb;LtMAO.LFI;'
        )
        # .wpk contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.wpk\\shell',
            sub_commands='LtMAO.wpk2dir;LtMAO.geb;LtMAO.LFI;'
        )
        # .wem contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.wem\\shell',
            sub_commands='LtMAO.wem2wav;'
        )
        # .wav contexts
        Context.create_submenu(
            shell='SystemFileAssociations\\.wav\\shell',
            sub_commands='LtMAO.wav2wem;'
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
                cmd_desc='wad_tool: Pack To WAD',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadpack" -src="%V"'
            )
            # WadToRaw
            Context.create_command(
                root=key,
                cmd_name='LtMAO.WadToRaw',
                cmd_desc='wad_tool: Unpack To Folder',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadunpack" -src="%V"'
            )
            # AllWadToRaw
            Context.create_command(
                root=key,
                cmd_name='LtMAO.AllWadToRaw',
                cmd_desc='wad_tool: Unpack All WAD',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wadunpack_all" -src="%V"'
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
            # RitobinDirToPy
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RitobinDirToPy',
                cmd_desc='ritobin: Convert All BIN To PY',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobindir2py" -src="%V"'
            )
            # RitobinDirToBin
            Context.create_command(
                root=key,
                cmd_name='LtMAO.RitobinDirToBin',
                cmd_desc='ritobin: Convert All PY To BIN',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="ritobindir2bin" -src="%V"'
            )
            # LFI
            Context.create_command(
                root=key,
                cmd_name='LtMAO.LFI',
                cmd_desc='file_inspector: Print infos as JSON',
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
                cmd_desc='hash_helper: Extract hashes',
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
            # tex2ddsdir
            Context.create_command(
                root=key,
                cmd_name='LtMAO.tex2ddsdir',
                cmd_desc='Ritoddstex: Convert All TEX To DDS',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="tex2ddsdir" -src="%V"'
            )
            # dds2texdir
            Context.create_command(
                root=key,
                cmd_name='LtMAO.dds2texdir',
                cmd_desc='Ritoddstex: Convert All DDS To TEX',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2texdir" -src="%V"'
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
            # png2ddsmm
            Context.create_command(
                root=key,
                cmd_name='LtMAO.png2ddsmm',
                cmd_desc='ImageMagick: Convert To DDS (With Mipmap 10)',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="png2ddsmm" -src="%V"'
            )
            # dds2x4x
            Context.create_command(
                root=key,
                cmd_name='LtMAO.dds2x4x',
                cmd_desc='ImageMagick: Make 2x_, 4x_ DDS',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dds2x4x" -src="%V"'
            )
            # wem2wav
            Context.create_command(
                root=key,
                cmd_name='LtMAO.wem2wav',
                cmd_desc='wiwawe: Convert To WAV',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wem2wav" -src="%V"'
            )
            # wav2wem
            Context.create_command(
                root=key,
                cmd_name='LtMAO.wav2wem',
                cmd_desc='wiwawe: Convert To WEM',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wav2wem" -src="%V"'
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
            # dir2bnk
            Context.create_command(
                root=key,
                cmd_name='LtMAO.dir2bnk',
                cmd_desc='bnk_tool: Pack To BNK',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dir2bnk" -src="%V"'
            )
            # dir2wpk
            Context.create_command(
                root=key,
                cmd_name='LtMAO.dir2wpk',
                cmd_desc='bnk_tool: Pack To WPK',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="dir2wpk" -src="%V"'
            )
            # bnk2dir
            Context.create_command(
                root=key,
                cmd_name='LtMAO.bnk2dir',
                cmd_desc='bnk_tool: Unpack To Folder',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="bnk2dir" -src="%V"'
            )
            # wpk2dir
            Context.create_command(
                root=key,
                cmd_name='LtMAO.wpk2dir',
                cmd_desc='bnk_tool: Unpack To Folder',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="wpk2dir" -src="%V"'
            )
            # geb
            Context.create_command(
                root=key,
                cmd_name='LtMAO.geb',
                cmd_desc='bnk_tool: Guess name of Voice Events BNK',
                cmd_value=f'"{os.path.abspath(python_file)}" "{os.path.abspath(cli_file)}" -t="geb" -src="%V"'
            )
        print('winLT: Finish: Create Explorer Contexts')

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
        print('winLT: Finish: Remove Explorer Contexts')


class Shortcut:
    @staticmethod
    def create_desktop():
        import userpaths
        desktop_file = f'{userpaths.get_desktop()}/LtMAO.lnk'.replace('\\','/')
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(desktop_file)
        shortcut.Targetpath = os.path.abspath(pythonw_file)
        shortcut.WorkingDirectory = os.path.abspath('.')
        shortcut.Arguments = f'"{os.path.abspath(gui_file)}"'
        shortcut.IconLocation = os.path.abspath(icon_file)
        shortcut.Description = 'Run LtMAO'
        shortcut.save()
        print(f'winLT: Finish: Create Desktop Shortcut: {desktop_file}')

    @staticmethod
    def create_launch():
        launch_file = os.path.abspath('./LtMAO.lnk').replace('\\','/')
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
            print(f'winLT: Finish: Create Launch Shortcut: {launch_file}')


def init():
    Shortcut.create_launch()
