import subprocess, math
from LtMAO import lepath
from PIL import Image

def block_and_stream_process_output(process, log_message_header=''):
    for line in process.stdout:
        msg = line.decode().strip().replace('\\', '/')
        if msg != '':
            print(log_message_header + msg)
    process.wait()

def block_and_stream_nothing(process):
    process.wait()


class CSLOL:
    local_file = './res/tools/mod-tools.exe'
    diag_file = './res/tools/cslol-diag.exe'

    @staticmethod
    def import_fantome(src, dst, game=None, noTFT=True):
        local_file = lepath.abs(CSLOL.local_file)
        cmds = [local_file, 'import', src, dst]
        if game:
            cmds.append('--game:' + game)
        if noTFT:
            cmds.append('--noTFT')
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return p

    @staticmethod
    def export_fantome(src, dst, game=None, noTFT=True):
        local_file = lepath.abs(CSLOL.local_file)
        cmds = [local_file, 'export', src, dst]
        if game:
            cmds.append('--game:' + game)
        if noTFT:
            cmds.append('--noTFT')
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return p

    @staticmethod
    def make_overlay(src, overlay, game=None, mods=None, noTFT=True, ignore_conflict=True):
        local_file = lepath.abs(CSLOL.local_file)
        cmds = [local_file, 'mkoverlay', src, overlay]
        if game:
            cmds.append('--game:' + game)
        if mods:
            cmds.append('--mods:' + '/'.join(mods))
        if noTFT:
            cmds.append('--noTFT')
        if ignore_conflict:
            cmds.append('--ignoreConflict')
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return p

    @staticmethod
    def run_overlay(overlay, config, game=None):
        local_file = lepath.abs(CSLOL.local_file)
        cmds = [local_file, 'runoverlay', overlay, config]
        if game:
            cmds.append(game)
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return p
    
    
    @staticmethod
    def diagnose():
        diag_file = lepath.abs(CSLOL.diag_file)
        cmds = [diag_file]
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        block_and_stream_process_output(p, 'cslol-diag: ')
        return p


class ImageMagick:
    local_file = './res/tools/magick.exe'

    @staticmethod
    def to_png(src, png):
        cmds = [
            lepath.abs(ImageMagick.local_file),
            src,
            png
        ]
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        block_and_stream_process_output(p, 'ImageMagick: ')
        return p

    @staticmethod
    def to_dds(src, dds, format='dxt5', mipmap=False):
        if format not in ('dxt1', 'dxt5'):
            format = 'dxt5'
        if mipmap:
            with Image.open(src) as img:
                mipmap_count = math.floor(math.log2(max(img.width, img.height))) + 1
        cmds = [
            lepath.abs(ImageMagick.local_file),
            src,
            '-define',
            f'dds:compression={format}',
            '-define',
            f'dds:mipmaps={mipmap_count if mipmap else 0}',
            dds
        ]
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        block_and_stream_process_output(p, 'ImageMagick: ')
        return p

    @staticmethod
    def resize_dds(src, dst, width, height):
        cmds = [
            lepath.abs(ImageMagick.local_file),
            src,
            '-resize',
            f'{width}x{height}',
            dst
        ]
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        block_and_stream_process_output(p, 'ImageMagick: ')
        return p


class VGMStream:
    local_file = './res/tools/vgmstream/vgmstream-cli.exe'

    @staticmethod
    def to_wav(src, dst=None):
        if dst == None:
            dst = '.'.join(src.split('.')[:-1] + ['wav']) 
        cmds = [
            lepath.abs(VGMStream.local_file),
            '-o',
            dst,
            src,
        ]
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        block_and_stream_nothing(p)
        return p
    

class WWiseConsole:
    local_file = './res/wiwawe/WwiseApp/Authoring/x64/Release/bin/WwiseConsole.exe'
    wproj_file = './res/wiwawe/WwiseLeagueProjects/WWiseLeagueProjects.wproj'

    @staticmethod
    def to_wem(wsources_file, output_dir):
        cmds = [
            WWiseConsole.local_file,
            'convert-external-source',
            lepath.abs(WWiseConsole.wproj_file),
            '--source-file',
            lepath.abs(wsources_file),
            '--output',
            lepath.abs(output_dir)
        ]
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        block_and_stream_process_output(p, 'WwiseConsole: ')
        return p