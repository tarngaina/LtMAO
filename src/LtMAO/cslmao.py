import os
import os.path
import json
from LtMAO.ext_tools import CSLOL, block_and_stream_process_output
from LtMAO import setting
from PIL import Image
from threading import Thread
from shutil import rmtree, copy

LOG = print


class MOD:
    __slots__ = (
        'path', 'enable', 'profile'
    )

    def __init__(self, path=None, enable=False, profile='0'):
        self.path = path
        self.enable = enable
        self.profile = profile


class CSLMAO:
    local_dir = './prefs/cslmao'

    raw_dir = f'{local_dir}/raw'
    mod_file = f'{local_dir}/mods.json'
    MODS = []

    profile_dir = f'{local_dir}/profiles'
    config_file = f'{local_dir}/config.txt'
    blank_image = Image.new('RGB', (144, 81))

    def create_mod(mod_path, enable, profile):
        existed_mod = next(
            (mod for mod in CSLMAO.MODS if mod.path == mod_path), None)
        if existed_mod != None:
            raise Exception(
                f'cslmao: Failed: Create mod: A mod with path: {mod_path} already existed in profile {existed_mod.profile}.')
        m = MOD(mod_path, enable, profile)
        CSLMAO.MODS.append(m)
        return m

    def create_mod_folder(mod):
        mod_folder = os.path.join(CSLMAO.raw_dir, mod.path)
        meta_folder = os.path.join(mod_folder, 'META')
        wad_folder = os.path.join(mod_folder, 'WAD')
        os.makedirs(mod_folder, exist_ok=True)
        os.makedirs(meta_folder, exist_ok=True)
        os.makedirs(wad_folder, exist_ok=True)

    def delete_mod(mod):
        rmtree(os.path.join(CSLMAO.raw_dir, mod.path))

    def get_info(mod):
        info_file = os.path.join(CSLMAO.raw_dir, mod.path, 'META', 'info.json')
        with open(info_file, 'r') as f:
            info = json.load(f)
        image = None
        image_file = os.path.join(
            CSLMAO.raw_dir, mod.path, 'META', 'image.png')
        if os.path.exists(image_file):
            image = Image.open(os.path.abspath(image_file))
        return info, image

    def set_info(mod, info=None, image_path=None):
        if info != None:
            info_file = os.path.join(
                CSLMAO.raw_dir, mod.path, 'META', 'info.json')
            with open(info_file, 'w+') as f:
                json.dump(info, f, indent=4)
        if image_path != None:
            image_file = os.path.join(
                CSLMAO.raw_dir, mod.path, 'META', 'image.png')
            copy(image_path, image_file)

    def add_mod_to_profile(path, profile_id):
        if not path in CSLMAO.PROFILES[profile_id]:
            CSLMAO.PROFILES[profile_id].append(path)

    def load_mods():
        l = []
        with open(CSLMAO.mod_file, 'r') as f:
            l = json.load(f)
        CSLMAO.MODS = [MOD(path, enable, profile)
                       for path, enable, profile in l]

    def save_mods():
        with open(CSLMAO.mod_file, 'w+') as f:
            json.dump([(mod.path, mod.enable, mod.profile)
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
            paths = [mod.path for mod in CSLMAO.MODS if mod.enable]
        else:
            paths = [
                mod.path for mod in CSLMAO.MODS if mod.enable and mod.profile == profile]
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
            info, image = get_info(mod)
            mgs.append(tk_add_mod(image=image, name=info['Name'], author=info['Author'],
                       version=info['Version'], description=info['Description'], enable=mod.enable, profile=mod.profile))
        # grid all mod frame at one
        for mg in mgs:
            mg()
        tk_refresh_profile(setting.get('Cslmao.profile', 'all'))
        preparing = False
        LOG(f'cslmao: Status: Finished loading mods.')
    Thread(target=prepare_cmd, daemon=True).start()
