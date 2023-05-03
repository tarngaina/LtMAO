import os
import os.path
from LtMAO.ext_tools import CSLOL
from PIL import Image

LOG = print


class CSLMAO:
    local_dir = './prefs/cslmao'
    raw_dir = f'{local_dir}/raw'
    overlay_dir = f'{local_dir}/overlay'
    config_file = f'{local_dir}/config.txt'
    blank_image = Image.new('RGB', (144, 81))
    running_process = None


import_fantome = CSLOL.import_fantome
export_fantome = CSLOL.export_fantome
make_overlay = CSLOL.make_overlay
run_overlay = CSLOL.run_overlay


def prepare(_LOG):
    global LOG
    LOG = _LOG
    # ensure folders and files
    os.makedirs(CSLMAO.raw_dir, exist_ok=True)
    os.makedirs(CSLMAO.overlay_dir, exist_ok=True)
    open(CSLMAO.config_file, 'w+').close()
