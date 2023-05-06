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
    def __init__(self, path=None, enable=None):
        self.path = path
        self.enable = enable


class CSLMAO:
    local_dir = './prefs/cslmao'

    raw_dir = f'{local_dir}/raw'
    mod_file = f'{local_dir}/mods.json'
    MODS = []

    profile_file = f'{local_dir}/profiles.json'
    profile_dir_all = f'{local_dir}/profiles/profile_ALL'
    profile_dirs = [f'./prefs/cslmao/profiles/profile{i}' for i in range(10)]
    PROFILES = []

    config_file = f'{local_dir}/config.txt'

    blank_image = Image.new('RGB', (144, 81))

    def create_mod(mod_path, enable):
        existed_path = next(
            (mod for mod in CSLMAO.MODS if mod.path == mod_path), None) != None
        if existed_path:
            raise Exception(
                f'Failed: CSLMAO: Create mod: A mod with path: {mod_path} already existed.')
        m = MOD(mod_path, enable)
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
        CSLMAO.MODS = [MOD(path, enable) for path, enable in l]

    def save_mods():
        with open(CSLMAO.mod_file, 'w+') as f:
            json.dump([(mod.path, mod.enable)
                      for mod in CSLMAO.MODS], f, indent=4)

    def load_profiles():
        with open(CSLMAO.profile_file, 'r') as f:
            CSLMAO.PROFILES = json.load(f)

    def save_profiles():
        with open(CSLMAO.profile_file, 'w+') as f:
            json.dump(CSLMAO.PROFILES, f, indent=4)

    def import_fantome(fantome_path, mod_path):
        return CSLOL.import_fantome(
            src=fantome_path,
            dst=os.path.abspath(os.path.join(CSLMAO.raw_dir, mod_path)),
            game=setting.get('game_folder', ''))

    def export_fantome(mod_path, fantome_path):
        return CSLOL.export_fantome(
            src=mod_path,
            dst=fantome_path,
            game=setting.get('game_folder', '')
        )

    def make_overlay(profile_id):
        paths = [mod.path for mod in CSLMAO.MODS if mod.enable] if profile_id == 'all' else [
            path for path in CSLMAO.PROFILES[profile_id] if next((mod.enable for mod in CSLMAO.MODS if mod.path == path), False)]
        overlay = CSLMAO.profile_dir_all if profile_id == 'all' else CSLMAO.profile_dirs[
            profile_id]
        return CSLOL.make_overlay(
            src=os.path.abspath(CSLMAO.raw_dir),
            overlay=os.path.abspath(overlay),
            game=setting.get('game_folder', ''),
            mods=paths
        )

    def run_overlay(profile_id):
        overlay = CSLMAO.profile_dir_all if profile_id == 'all' else CSLMAO.profile_dirs[
            profile_id]
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
load_profiles = CSLMAO.load_profiles
save_profiles = CSLMAO.save_profiles
tk_add_mod = None
preparing = False


def prepare(_LOG):
    global LOG
    LOG = _LOG
    # ensure folders and files
    os.makedirs(CSLMAO.raw_dir, exist_ok=True)
    for profile_id in range(10):
        os.makedirs(CSLMAO.profile_dirs[profile_id], exist_ok=True)
    os.makedirs(CSLMAO.profile_dir_all, exist_ok=True)
    if not os.path.exists(CSLMAO.config_file):
        open(CSLMAO.config_file, 'w+').close()
    if not os.path.exists(CSLMAO.mod_file):
        with open(CSLMAO.mod_file, 'w+') as f:
            f.write('{}')
    if not os.path.exists(CSLMAO.profile_file):
        with open(CSLMAO.profile_file, 'w+') as f:
            f.write('{}')
    CSLMAO.load_mods()
    CSLMAO.save_mods()
    CSLMAO.load_profiles()
    CSLMAO.save_profiles()

    def prepare_cmd():
        global preparing
        preparing = True
        LOG(f'CSLMAO: Status: Loading mods.')
        mgs = []
        for mod in CSLMAO.MODS:
            info, image = get_info(mod)
            mgs.append(tk_add_mod(image=image, name=info['Name'], author=info['Author'],
                       version=info['Version'], description=info['Description'], enable=mod.enable))
        # grid all mod frame at one
        for mg in mgs:
            mg()
        preparing = False
        LOG(f'CSLMAO: Status: Finished loading mods.')
    Thread(target=prepare_cmd, daemon=True).start()
