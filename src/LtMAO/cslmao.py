import os
import os.path
import json
import datetime
from .ext_tools import CSLOL, block_and_stream_process_output
from . import setting
from PIL import Image
from threading import Thread
from shutil import rmtree, copy

LOG = print


class MOD:
    __slots__ = (
        'id', 'path', 'enable', 'profile'
    )

    def __init__(self, id=None, path=None, enable=False, profile='0'):
        self.id = id
        self.path = path
        self.enable = enable
        self.profile = profile

    def generate_id():
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

    def get_path(self):
        return self.path + f' {self.id}'


class CSLMAO:
    local_dir = './prefs/cslmao'

    raw_dir = f'{local_dir}/raw'
    mod_file = f'{local_dir}/mods.json'
    MODS = []

    profile_dir = f'{local_dir}/profiles'
    config_file = f'{local_dir}/config.txt'
    blank_image = Image.new('RGB', (144, 81))

    def create_mod(path, enable, profile):
        m = MOD(MOD.generate_id(), path, enable, profile)
        check_path = m.get_path()
        for mod in CSLMAO.MODS:
            if mod.get_path() == check_path:
                raise Exception(
                    f'cslmao: Failed: Create mod: A mod with path: {check_path} already existed in profile {mod.profile}.')
        CSLMAO.MODS.append(m)
        return m

    def create_mod_folder(mod):
        mod_folder = os.path.join(CSLMAO.raw_dir, mod.get_path())
        meta_folder = os.path.join(mod_folder, 'META')
        wad_folder = os.path.join(mod_folder, 'WAD')
        os.makedirs(mod_folder, exist_ok=True)
        os.makedirs(meta_folder, exist_ok=True)
        os.makedirs(wad_folder, exist_ok=True)

    def delete_mod(mod):
        if mod in CSLMAO.MODS:
            CSLMAO.MODS.remove(mod)
        rmtree(os.path.join(CSLMAO.raw_dir, mod.get_path()), ignore_errors=True)

    def get_info(mod):
        info_file = os.path.join(
            CSLMAO.raw_dir, mod.get_path(), 'META', 'info.json')
        with open(info_file, 'r') as f:
            info = json.load(f)
        image = None
        image_file = os.path.join(
            CSLMAO.raw_dir, mod.get_path(), 'META', 'image.png')
        if os.path.exists(image_file):
            image = Image.open(os.path.abspath(image_file))
        return info, image

    def set_info(mod, info=None, image_path=None):
        old_path = mod.get_path()
        mod.path = f'{info["Name"]}'
        mod.id = MOD.generate_id()
        os.rename(
            os.path.abspath(os.path.join(CSLMAO.raw_dir, old_path)),
            os.path.abspath(os.path.join(CSLMAO.raw_dir, mod.get_path()))
        )
        if info != None:
            info_file = os.path.join(
                CSLMAO.raw_dir, mod.get_path(), 'META', 'info.json')
            with open(info_file, 'w+') as f:
                json.dump(info, f, indent=4)
        if image_path != None:
            image_file = os.path.join(
                CSLMAO.raw_dir, mod.get_path(), 'META', 'image.png')
            copy(image_path, image_file)

    def add_mod_to_profile(path, profile_id):
        if not path in CSLMAO.PROFILES[profile_id]:
            CSLMAO.PROFILES[profile_id].append(path)

    def load_mods():
        # load through mod file
        try:
            l = []
            with open(CSLMAO.mod_file, 'r') as f:
                l = json.load(f)
            CSLMAO.MODS = [MOD(id, path, enable, profile)
                           for id, path, enable, profile in l]
        except Exception as e:
            LOG(f'cslmao: Failed to load: {CSLMAO.mod_file}: {e}')
            CSLMAO.MODS = []
            with open(CSLMAO.mod_file, 'w+') as f:
                json.dump({}, f, indent=4)
            LOG(f'cslmao: Done: Reset {CSLMAO.mod_file}')
        # load outside mod file
        for dirname in os.listdir(CSLMAO.raw_dir):
            info_file = os.path.join(
                CSLMAO.raw_dir, dirname, 'META', 'info.json')
            if not os.path.exists(info_file):
                continue
            existed_mod = False
            for mod in CSLMAO.MODS:
                if dirname == mod.get_path():
                    existed_mod = True
                    break
            if existed_mod:
                continue

            with open(info_file, 'r') as f:
                info = json.load(f)
            mod_path = f'{info["Name"]}'
            mod = MOD(id=MOD.generate_id(), path=mod_path,
                      enable=False, profile='0')
            CSLMAO.MODS.append(mod)
            os.rename(
                os.path.abspath(os.path.join(CSLMAO.raw_dir, dirname)),
                os.path.abspath(os.path.join(CSLMAO.raw_dir, mod.get_path()))
            )
            CSLMAO.save_mods()

    def save_mods():
        with open(CSLMAO.mod_file, 'w+') as f:
            json.dump([(mod.id, mod.path, mod.enable, mod.profile)
                      for mod in CSLMAO.MODS], f, indent=4)

    def import_fantome(fantome_path, mod_path):
        p = CSLOL.import_fantome(
            src=fantome_path,
            dst=os.path.abspath(os.path.join(CSLMAO.raw_dir, mod_path)),
            game=setting.get('game_folder', ''))
        block_and_stream_process_output(p, 'cslmao: ')
        return p

    def export_fantome(mod_path, fantome_path):
        p = CSLOL.export_fantome(
            src=mod_path,
            dst=fantome_path,
            game=setting.get('game_folder', '')
        )
        block_and_stream_process_output(p, 'cslmao: ')
        return p

    def make_overlay(profile):
        if profile == 'all':
            paths = [mod.get_path() for mod in CSLMAO.MODS if mod.enable]
        else:
            paths = [
                mod.get_path() for mod in CSLMAO.MODS if mod.enable and mod.profile == profile]
        overlay = f'{CSLMAO.profile_dir}/{profile}'
        os.makedirs(overlay, exist_ok=True)
        return CSLOL.make_overlay(
            src=os.path.abspath(CSLMAO.raw_dir),
            overlay=os.path.abspath(overlay),
            game=setting.get('game_folder', ''),
            mods=paths,
            noTFT=setting.get('Cslmao.extra_game_modes', 0) == 0
        )

    def run_overlay(profile):
        overlay = f'{CSLMAO.profile_dir}/{profile}'
        return CSLOL.run_overlay(
            overlay=overlay,
            config=CSLMAO.config_file,
            game=setting.get('game_folder', '')
        )


import_fantome = CSLMAO.import_fantome
export_fantome = CSLMAO.export_fantome
make_overlay = CSLMAO.make_overlay
run_overlay = CSLMAO.run_overlay
create_mod = CSLMAO.create_mod
create_mod_folder = CSLMAO.create_mod_folder
delete_mod = CSLMAO.delete_mod
get_info = CSLMAO.get_info
set_info = CSLMAO.set_info
load_mods = CSLMAO.load_mods
save_mods = CSLMAO.save_mods
tk_add_mod = None
tk_refresh_profile = None
preparing = False


def prepare(_LOG):
    global LOG
    LOG = _LOG
    # ensure folders and files
    os.makedirs(CSLMAO.raw_dir, exist_ok=True)
    os.makedirs(CSLMAO.profile_dir, exist_ok=True)
    if not os.path.exists(CSLMAO.config_file):
        open(CSLMAO.config_file, 'w+').close()
    if not os.path.exists(CSLMAO.mod_file):
        with open(CSLMAO.mod_file, 'w+') as f:
            f.write('{}')
    CSLMAO.load_mods()
    CSLMAO.save_mods()

    def prepare_cmd():
        global preparing
        preparing = True
        LOG(f'cslmao: Status: Loading mods.')
        mgs = []
        for mod in CSLMAO.MODS:
            try:
                info, image = get_info(mod)
                mgs.append(tk_add_mod(image=image, name=info['Name'], author=info['Author'],
                                      version=info['Version'], description=info['Description'], enable=mod.enable, profile=mod.profile))
            except Exception as e:
                LOG(f'cslmao: Failed: Load {mod.get_path()}: {e}')
                CSLMAO.MODS.remove(mod)

        # grid all mod frame at one
        for mg in mgs:
            mg()
        tk_refresh_profile(setting.get('Cslmao.profile', 'all'))
        preparing = False
        LOG(f'cslmao: Status: Finished loading mods.')
    Thread(target=prepare_cmd, daemon=True).start()
