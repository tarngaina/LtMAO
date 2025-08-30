import os, os.path, json

class SETTINGS:
    __settings__ = {}
    local_dir = './pref'
    local_file = f'{local_dir}/settings.json'

def get(key, default):
    if key in SETTINGS.__settings__:
        return SETTINGS.__settings__[key]
    return default

def set(key, value):
    SETTINGS.__settings__[key] = value

def load():
    with open(SETTINGS.local_file, 'r', encoding='utf-8') as f:
        SETTINGS.__settings__ = json.load(f)

def save():
    with open(SETTINGS.local_file, 'w+', encoding='utf-8') as f:
        json.dump(SETTINGS.__settings__, f, indent=4, ensure_ascii=False)

def init():
    # ensure folder
    os.makedirs(SETTINGS.local_dir, exist_ok=True)
    # ensure file
    if not os.path.exists(SETTINGS.local_file):
        with open(SETTINGS.local_file, 'w+', encoding='utf-8') as f:
            f.write('{}')
    load()
