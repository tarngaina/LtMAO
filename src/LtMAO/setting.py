import os
import os.path
import json

LOG = print


class SETTINGS:
    __settings__ = {}
    local_dir = './prefs'
    local_file = f'{local_dir}/settings.json'

    @staticmethod
    def get(key, default):
        if key in SETTINGS.__settings__:
            return SETTINGS.__settings__[key]
        return default

    @staticmethod
    def set(key, value):
        SETTINGS.__settings__[key] = value

    @staticmethod
    def load():
        with open(SETTINGS.local_file, 'r', encoding='utf-8') as f:
            SETTINGS.__settings__ = json.load(f)
        LOG(f'Done: Loaded {SETTINGS.local_file}')

    @staticmethod
    def save():
        with open(SETTINGS.local_file, 'w+', encoding='utf-8') as f:
            json.dump(SETTINGS.__settings__, f, indent=4)
        LOG(f'Done: Saved {SETTINGS.local_file}')


def get(key, default): return SETTINGS.get(key, default)
def set(key, value): SETTINGS.set(key, value)


load = SETTINGS.load
save = SETTINGS.save


def prepare(_LOG):
    # function need to call first
    global LOG
    LOG = _LOG
    # ensure folder
    if not os.path.exists(SETTINGS.local_dir):
        os.makedirs(SETTINGS.local_dir)
    # ensure file
    if not os.path.exists(SETTINGS.local_file):
        with open(SETTINGS.local_file, 'w+') as f:
            f.write('{}')
    load()
    save()
