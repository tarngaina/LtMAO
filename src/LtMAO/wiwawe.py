import os, os.path, shutil, math
import pyaudio, wave
from subprocess import Popen, CREATE_NO_WINDOW, PIPE
from . import tools, pyRitoFile, bnk_tool


wiwawe_dir = './pref/wiwawe'
wsources_file = f'{wiwawe_dir}/wiwawe.wsources'
input_dir = f'{wiwawe_dir}/input'
ouput_dir = f'{wiwawe_dir}/output'

def copy_wav_to_input(wav_files):
    map_sounds = {}
    for wav_file in wav_files:
        basename = os.path.basename(wav_file).replace('.wav', '')
        if basename not in map_sounds:
            map_sounds[basename] = []
            input_file = os.path.join(input_dir, f'{basename}.wav')
            shutil.copy2(wav_file, input_file)
        map_sounds[basename].append(wav_file)
    return map_sounds

def generate_wsources(map_sounds):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    lines.append(f'<ExternalSourcesList SchemaVersion="1" Root="{os.path.abspath(input_dir)}">\n')
    for basename in map_sounds:
        lines.append(f'\t<Source Path="{basename}.wav" Conversion="Vorbis Quality High" />\n')
    lines.append('</ExternalSourcesList>')
    with open(wsources_file, 'w+') as f:
        f.writelines(lines)

def convert_inputs(wwise_path, wproj_path):
    wwise_console_file = os.path.join(wwise_path, 'Authoring/x64/Release/bin/WwiseConsole.exe')
    cmds = [
        wwise_console_file,
        'convert-external-source',
        wproj_path,
        '--source-file',
        os.path.abspath(wsources_file),
        '--output',
        os.path.abspath(ouput_dir)
    ]
    p = Popen(
        cmds, creationflags=CREATE_NO_WINDOW,
        stdout=PIPE, stderr=PIPE
    )
    tools.block_and_stream_process_output(p, 'WwiseConsole: ')

def copy_output_to_wem(map_sounds):
    map_wems = {}
    for root, dirs, files in os.walk(ouput_dir):
        for file in files:
            if file.endswith('.wem'):
                basename = file.replace('.wem', '')
                map_wems[basename] = os.path.join(root, file)

    for basename in map_sounds:
        if basename in map_wems:
            for wav_file in map_sounds[basename]:
                wem_file = wav_file.replace('.wav', '.wem')
                shutil.copy2(map_wems[basename], wem_file)

def reset_cache():
    shutil.rmtree(input_dir, ignore_errors=True)
    shutil.rmtree(ouput_dir, ignore_errors=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(ouput_dir, exist_ok=True)
    if os.path.exists(wsources_file):
        os.remove(wsources_file)

def wav2wem(wav_files, wwise_path, wproj_path):
    if wwise_path == None:
        raise Exception('wiwawe: Error: No Wwise folder selected.')
    if wproj_path == None:
        raise Exception('wiwawe: Error: No .wproj file selected.')
    map_sounds = copy_wav_to_input(wav_files)
    generate_wsources(map_sounds)
    convert_inputs(wwise_path, wproj_path)
    copy_output_to_wem(map_sounds)
    reset_cache()

def wem2wav(wem_files):
    for wem_file in wem_files:
        tools.VGMStream.to_wav(wem_file)
        
def init():
    os.makedirs(wiwawe_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(ouput_dir, exist_ok=True)
