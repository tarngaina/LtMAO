import os
import os.path
import json
import datetime
from .tools import CSLOL, block_and_stream_process_output, RITOBIN
from . import setting, Ritoddstex
from shutil import rmtree, copy


class MOD:
    __slots__ = (
        'id', 'path', 'enable', 'profile'
    )

    def __init__(self, id=None, path=None, enable=False, profile='0'):
        self.id = id
        self.path = path
        self.enable = enable
        self.profile = profile

    def get_path(self):
        return self.path + f' {self.id}'

    mods = []
    @staticmethod
    def generate_id():
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')


local_dir = './pref/cslmao'
raw_dir = f'{local_dir}/raw'
mod_file = f'{local_dir}/mods.json'
profile_dir = f'{local_dir}/profiles'
config_file = f'{local_dir}/config.txt'

profiles = []

def create_mod(path, enable, profile):
    m = MOD(MOD.generate_id(), path, enable, profile)
    check_path = m.get_path()
    for mod in MOD.mods:
        if mod.get_path() == check_path:
            raise Exception(
                f'cslmao: Error: Create mod: A mod with path: {check_path} already existed in profile {mod.profile}.')
    MOD.mods.append(m)
    return m

def create_mod_folder(mod):
    mod_folder = os.path.join(raw_dir, mod.get_path())
    meta_folder = os.path.join(mod_folder, 'META')
    wad_folder = os.path.join(mod_folder, 'WAD')
    os.makedirs(mod_folder, exist_ok=True)
    os.makedirs(meta_folder, exist_ok=True)
    os.makedirs(wad_folder, exist_ok=True)

def delete_mod(mod):
    if mod in MOD.mods:
       MOD.mods.remove(mod)
    rmtree(os.path.join(raw_dir, mod.get_path()), ignore_errors=True)

def get_info(mod):
    info_file = os.path.join(raw_dir, mod.get_path(), 'META', 'info.json')
    with open(info_file, 'r') as f:
        info = json.load(f)
    image_path = None
    image_file = os.path.join(raw_dir, mod.get_path(), 'META', 'image.png')
    if os.path.exists(image_file):
        image_path = image_file
    return info, image_path

def set_info(mod, info=None, image_path=None):
    old_path = mod.get_path()
    mod.path = f'{info["Name"]}'
    mod.id = MOD.generate_id()
    os.rename(
        os.path.abspath(os.path.join(raw_dir, old_path)),
        os.path.abspath(os.path.join(raw_dir, mod.get_path()))
    )
    if info != None:
        info_file = os.path.join(raw_dir, mod.get_path(), 'META', 'info.json')
        with open(info_file, 'w+') as f:
            json.dump(info, f, indent=4)
    if image_path != None:
        image_file = os.path.join(raw_dir, mod.get_path(), 'META', 'image.png')
        copy(image_path, image_file)

def delete_info_image(mod):
    image_file = os.path.join(raw_dir, mod.get_path(), 'META', 'image.png')
    if os.path.exists(image_file):
        os.remove(image_file)
        
def load_mods():
    # load through mod file
    try:
        l = []
        with open(mod_file, 'r') as f:
            l = json.load(f)
        MOD.mods = [MOD(id, path, enable, profile) for id, path, enable, profile in l]
    except Exception as e:
        print(f'cslmao: Error: Can not load {mod_file}: {e}')
        import traceback
        print(traceback.format_exc())
        MOD.mods = []
        with open(mod_file, 'w+') as f:
            json.dump({}, f, indent=4)
        print(f'cslmao: Finish: Reset {mod_file}')
    # load outside mod file
    existed_mod_path = [mod.get_path() for mod in MOD.mods]
    for dirname in os.listdir(raw_dir):
        info_file = os.path.join(raw_dir, dirname, 'META', 'info.json')
        if not os.path.exists(info_file):
            continue
        if dirname in existed_mod_path:
            continue
        try: 
            mod_id = MOD.generate_id()
            mod_path = dirname
            mod = MOD(id=mod_id, path=mod_path, enable=False, profile='0')
            os.rename(
                os.path.join(raw_dir, mod_path),
                os.path.join(raw_dir, mod.get_path())
            )
            MOD.mods.append(mod)
        except Exception as e:
            print(f'cslmao: Error: Can not load {dirname}: {e}')
            import traceback
            print(traceback.format_exc())
            

def save_mods():
    with open(mod_file, 'w+') as f:
        json.dump([(mod.id, mod.path, mod.enable, mod.profile) for mod in MOD.mods], f, indent=4)

def import_fantome(fantome_path, mod_path):
    p = CSLOL.import_fantome(
        src=fantome_path,
        dst=os.path.abspath(os.path.join(raw_dir, mod_path)),
        game=setting.get('game_folder', '')
    )
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
        paths = [mod.get_path() for mod in MOD.mods if mod.enable]
    else:
        paths = [
            mod.get_path() for mod in MOD.mods if mod.enable and mod.profile == profile]
    overlay = f'{profile_dir}/{profile}'
    os.makedirs(overlay, exist_ok=True)
    return CSLOL.make_overlay(
        src=os.path.abspath(raw_dir),
        overlay=os.path.abspath(overlay),
        game=setting.get('game_folder', ''),
        mods=paths,
        noTFT=not setting.get('cslmao.tft', False)
    )

def run_overlay(profile):
    overlay = f'{profile_dir}/{profile}'
    return CSLOL.run_overlay(
        overlay=overlay,
        config=config_file,
        game=setting.get('game_folder', '')
    )

def diagnose():
    return CSLOL.diagnose()

def convert_raw_files_before_run():
    # scan enabled mod paths
    py2bin_files = []
    dds2tex_files = []
    for mod in MOD.mods:
        if mod.enable:
            for root, dirs, files in os.walk(os.path.join(raw_dir, mod.get_path())):
                for file in files:
                    if file.endswith('.py'):
                        py_file = os.path.join(root, file)
                        bin_file = py_file.replace('.py', '.bin')
                        py2bin_files.append((py_file, bin_file))
                    elif file.endswith('.dds'):
                        dds_file = os.path.join(root, file)
                        tex_file = dds_file.replace('.dds', '.tex')
                        dds2tex_files.append((dds_file, tex_file))
    # converts
    if setting.get('cslmao.auto_py2bin', False):
        for py_file, bin_file in py2bin_files:
            RITOBIN.run(py_file, bin_file)
        print(f'cslmao: Finish: Convert {len(py2bin_files)} files from PY to BIN.')
    if setting.get('cslmao.auto_dds2tex', False):
        for dds_file, tex_file in dds2tex_files:
            try:
                Ritoddstex.dds2tex(dds_file, tex_file)
            except Exception as e:
                print(f'Ritoddstex: Error: {str(e)} on {dds_file}')
        print(f'cslmao: Finish: Convert {len(dds2tex_files)} files from DDS to TEX.')



tk_add_mod = None
tk_refresh_profile = None
preparing = False


def init():
    # ensure folders and files
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(profile_dir, exist_ok=True)
    if not os.path.exists(config_file):
        open(config_file, 'w+').close()
    if not os.path.exists(mod_file):
        with open(mod_file, 'w+') as f:
            f.write('{}')
    load_mods()
    save_mods()
