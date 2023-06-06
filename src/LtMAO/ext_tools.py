import os
import os.path
from subprocess import Popen, CREATE_NO_WINDOW, PIPE, STDOUT
from threading import Thread

LOG = print


def block_and_stream_process_output(process, log_message_header=''):
    for line in process.stdout:
        LOG(log_message_header + line.decode()[:-1])
    process.wait()


class CSLOL:
    local_file = './resources/ext_tools/mod-tools.exe'

    def import_fantome(src, dst, game=None, noTFT=True):
        local_file = os.path.abspath(CSLOL.local_file)
        cmds = [local_file, 'import', src, dst]
        if game:
            cmds.append('--game:' + game)
        if noTFT:
            cmds.append('--noTFT')
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        return p

    def export_fantome(src, dst, game=None, noTFT=True):
        local_file = os.path.abspath(CSLOL.local_file)
        cmds = [local_file, 'export', src, dst]
        if game:
            cmds.append('--game:' + game)
        if noTFT:
            cmds.append('--noTFT')
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        return p

    def make_overlay(src, overlay, game=None, mods=None, noTFT=True, ignore_conflict=True):
        local_file = os.path.abspath(CSLOL.local_file)
        cmds = [local_file, 'mkoverlay', src, overlay]
        if game:
            cmds.append('--game:' + game)
        if mods:
            cmds.append('--mods:' + '/'.join(mods))
        if noTFT:
            cmds.append('--noTFT')
        if ignore_conflict:
            cmds.append('--ignoreConflict')
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        return p

    def run_overlay(overlay, config, game=None):
        local_file = os.path.abspath(CSLOL.local_file)
        cmds = [local_file, 'runoverlay', overlay, config]
        if game:
            cmds.append(game)
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdin=PIPE, stdout=PIPE, stderr=STDOUT
        )
        return p


class RITOBIN:
    local_file = './resources/ext_tools/ritobin_cli.exe'

    def run(src, dst=None, *, dir_hashes=None):
        cmds = [os.path.abspath(RITOBIN.local_file), src]
        if dst:
            cmds.append(dst)
        if dir_hashes:
            cmds.extend(('--dir-hashes', dir_hashes))
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        block_and_stream_process_output(p, 'ritobin: ')
        return p


class ImageMagick:
    local_file = './resources/ext_tools/magick.exe'

    def to_png(src, png):
        cmds = [
            os.path.abspath(ImageMagick.local_file),
            src,
            png
        ]
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        block_and_stream_process_output(p, 'ImageMagick: ')
        return p

    def to_dds(src, dds, format='dxt5', mipmap=False):
        if format not in ('dxt1', 'dxt5'):
            format = 'dxt5'
        cmds = [
            os.path.abspath(ImageMagick.local_file),
            src,
            '-define',
            f'dds:compression={format}',
            '-define',
            f'dds:mipmaps={8 if mipmap else 0}',
            dds
        ]
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        block_and_stream_process_output(p, 'ImageMagick: ')
        return p

    def resize_dds(src, dst, width, height):
        cmds = [
            os.path.abspath(ImageMagick.local_file),
            src,
            '-resize',
            f'{width}x{height}',
            dst
        ]
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        block_and_stream_process_output(p, 'ImageMagick: ')
        return p


class WW2OGG:
    local_file = './resources/ext_tools/ww2ogg.exe'
    pcb_file = './resources/ext_tools/packed_codebooks.bin'

    def run(src):
        cmds = [
            os.path.abspath(WW2OGG.local_file),
            src,
            '--pcb',
            os.path.abspath(WW2OGG.pcb_file)
        ]
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        block_and_stream_process_output(p, 'ww2ogg: ')
        return p


class REVORB:
    local_file = './resources/ext_tools/ReVorb.exe'

    def run(src):
        cmds = [os.path.abspath(REVORB.local_file), src]
        p = Popen(
            cmds, creationflags=CREATE_NO_WINDOW,
            stdout=PIPE, stderr=STDOUT
        )
        block_and_stream_process_output(p, 'ReVorb: ')
        return p


def prepare(_LOG):
    global LOG
    LOG = _LOG
