

LOG = print



def install_plugin(maya_pref_dir):
    import os, os.path

    
    # get maya.env path
    maya_env_file = f'{maya_pref_dir}/Maya.env'
    maya_env = {}
    # ensure maya.env
    if not os.path.exists(maya_env_file):
        open(maya_env_file, 'w+').close()
    # read existed maya.env 
    with open(maya_env_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            maya_env[key] = value
    lemon_maya_dir = os.path.abspath('./src/LtMAO/lemon3d/lemon_maya').replace('\\', '/')
    # add lemon3d to maya env  
    ltmao_dir = os.path.abspath('.').replace('\\','/')
    maya_paths = {
        'MAYA_PLUG_IN_PATH': f'{lemon_maya_dir}/plugins;',
        'MAYA_SHELF_PATH': f'{lemon_maya_dir}/prefs/shelves;',
        'XBMLANGPATH': f'{lemon_maya_dir}/prefs/icons;',
        'MAYA_SCRIPT_PATH': f'{lemon_maya_dir}/scripts;',
        'PYTHONPATH': f'{ltmao_dir}/src;{ltmao_dir}/epython/Lib/site-packages;'
    }
    for key, value in maya_paths.items():
        if key not in maya_env:
            maya_env[key] = ''
        if value not in maya_env[key]:
            maya_env[key] += value
    # save maya.env
    with open(maya_env_file, 'w+') as f:
        for key, value in maya_env.items():
            f.write(f'{key}={value}\n')
    LOG(f'lemon_maya: Done: Install plugin: {maya_pref_dir}')
    

def prepare(_LOG):
    global LOG
    LOG = _LOG
