import os, os.path, shutil
from . import lepath, tools

wiwawe_dir = './pref/wiwawe'
wsources_file = f'{wiwawe_dir}/wiwawe.wsources'
input_dir = f'{wiwawe_dir}/input'
ouput_dir = f'{wiwawe_dir}/output'

def copy_wav_to_input(wav_files):
    map_sounds = {}
    for wav_file in wav_files:
        basename = lepath.ext(os.path.basename(wav_file), '.wav', '')
        if basename not in map_sounds:
            map_sounds[basename] = []
            input_file = lepath.join(input_dir, f'{basename}.wav')
            shutil.copy2(wav_file, input_file)
        map_sounds[basename].append(wav_file)
    return map_sounds

def generate_wsources(map_sounds):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    lines.append(f'<ExternalSourcesList SchemaVersion="1" Root="{lepath.abs(input_dir)}">\n')
    for basename in map_sounds:
        lines.append(f'\t<Source Path="{basename}.wav" Conversion="Vorbis Quality High" />\n')
    lines.append('</ExternalSourcesList>')
    with open(wsources_file, 'w+', encoding='utf-8') as f:
        f.writelines(lines)

def convert_inputs():
    tools.WWiseConsole.to_wem(lepath.abs(wsources_file), lepath.abs(ouput_dir))

def copy_output_to_wem(map_sounds):
    map_wems = {}
    for root, dirs, files in os.walk(ouput_dir):
        for file in files:
            if file.endswith('.wem'):
                basename = lepath.ext(file, '.wem', '')
                map_wems[basename] = lepath.join(root, file)

    for basename in map_sounds:
        if basename in map_wems:
            for wav_file in map_sounds[basename]:
                wem_file = lepath.ext(wav_file, '.wav', '.wem')
                shutil.copy2(map_wems[basename], wem_file)

def reset_cache():
    shutil.rmtree(input_dir, ignore_errors=True)
    shutil.rmtree(ouput_dir, ignore_errors=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(ouput_dir, exist_ok=True)
    if os.path.exists(wsources_file):
        os.remove(wsources_file)

def wav2wem(wav_files):
    map_sounds = copy_wav_to_input(wav_files)
    generate_wsources(map_sounds)
    convert_inputs()
    copy_output_to_wem(map_sounds)
    reset_cache()

def wem2wav(wem_files):
    for wem_file in wem_files:
        tools.VGMStream.to_wav(wem_file)

def ogg2wem(ogg_files):
    for ogg_file in ogg_files:
        tools.VGMStream.to_wav(ogg_file)
    wav_files = [lepath.ext(ogg_file, '.ogg', '.wav') for ogg_file in ogg_files]
    wav2wem(wav_files)
    for wav_file in wav_files:
        os.remove(wav_file)
        

def init():
    os.makedirs(wiwawe_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(ouput_dir, exist_ok=True)
