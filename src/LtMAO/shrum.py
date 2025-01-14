from .pyRitoFile.stream import BinStream
from .pyRitoFile.hash import Elf
import os
import os.path
import traceback
from shutil import copytree, copy

LOG = print


def rename(path, olds, news, backup=True):
    if os.path.isdir(path):
        if backup:
            backup_dir = os.path.join(os.path.dirname(
                path), 'shrum_backup_' + os.path.basename(path))
            copytree(path, backup_dir, dirs_exist_ok=True)
        rename_anm_dir(path, olds, news)
    else:
        if path.endswith('.anm'):
            if backup:
                backup_file = os.path.join(os.path.dirname(
                    path), 'shrum_backup_' + os.path.basename(path))
                copy(path, backup_file)
            try:
                rename_anm(path, olds, news)
                LOG('shrum: Done: Rename: {path}')
            except Exception as e:
                LOG(f'shrum: Failed: Rename: {path}: {e}')
                LOG(traceback.format_exc())


def rename_anm_dir(path, olds, news):
    for file in os.listdir(path):
        if file.endswith('.anm'):
            try:
                rename_anm(os.path.join(path, file), olds, news)
                LOG('shrum: Done: Rename: {path}')
            except Exception as e:
                LOG(f'shrum: Failed: Rename: {path}: {e}')
                LOG(traceback.format_exc())


def rename_anm(path, olds, news):
    path = path.replace('\\', '/')
    olds_hashes = [Elf(old) for old in olds]
    news_hashes = [Elf(new) for new in news]
    count = 0
    with BinStream(open(path, 'rb+')) as bs:
        magic, = bs.read_s(8)
        version, = bs.read_u32()
        if magic == 'r3d2canm':
            bs.pad(12)
            joint_count, = bs.read_u32()
            bs.pad(96)
            joint_hashes_offset, = bs.read_i32()
            if joint_hashes_offset <= 0:
                raise Exception(
                    f'File does not contain joint hashes.'
                )
            bs.seek(joint_hashes_offset + 12)
            for i in range(joint_count):
                offset = bs.tell()
                joint_hash, = bs.read_u32()
                joint_id = None
                for id, old_hash in enumerate(olds_hashes):
                    if old_hash == joint_hash:
                        joint_id = id
                        break
                if joint_id != None:
                    bs.seek(offset)
                    bs.write_u32(news_hashes[joint_id])
                    count += 1
        elif magic == 'r3d2anmd':
            if version == 5:
                bs.pad(28)
                joint_hashes_offset, = bs.read_i32()
                bs.pad(16)
                frames_offset, = bs.read_i32()
                if joint_hashes_offset <= 0:
                    raise Exception(
                        f'File does not contain joint hashes.'
                    )
                if frames_offset <= 0:
                    raise Exception(
                        f'File does not contain frames data.'
                    )
                joint_count = (
                    frames_offset - joint_hashes_offset) // 4
                bs.seek(joint_hashes_offset + 12)
                for i in range(joint_count):
                    offset = bs.tell()
                    joint_hash, = bs.read_u32()
                    joint_id = None
                    for id, old_hash in enumerate(olds_hashes):
                        if old_hash == joint_hash:
                            joint_id = id
                            break
                    if joint_id != None:
                        bs.seek(offset)
                        bs.write_u32(news_hashes[joint_id])
                        count += 1
            elif version == 4:
                bs.pad(16)
                track_count, frame_count = bs.read_u32(2)
                bs.pad(24)
                frames_offset, = bs.read_i32()
                if frames_offset <= 0:
                    raise Exception(
                        f'File does not contain frames data.'
                    )
                bs.seek(frames_offset + 12)
                for i in range(frame_count * track_count):
                    offset = bs.tell()
                    joint_hash, = bs.read_u32()
                    joint_id = None
                    for id, old_hash in enumerate(olds_hashes):
                        if old_hash == joint_hash:
                            joint_id = id
                            break
                    if joint_id != None:
                        bs.seek(offset)
                        bs.write_u32(news_hashes[joint_id])
                        count += 1
                    bs.pad(8)
            else:
                bs.pad(4)
                track_count, frame_count = bs.read_u32(2)
                bs.pad(4)
                for i in range(track_count):
                    offset = bs.tell()
                    joint_name, = bs.read_s_padded(32)
                    joint_id = None
                    for id, old in enumerate(olds):
                        if old == joint_name:
                            joint_id = id
                            break
                    if joint_id != None:
                        bs.seek(offset)
                        bs.write_s_padded(news[joint_id], 32)
                        count += 1
                    bs.pad(4+frame_count*28)
        else:
            raise Exception(
                f'Wrong signature file: {magic}')


def prepare(_LOG):
    global LOG
    LOG = _LOG
