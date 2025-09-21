from ... import lepath
import os.path, os, userpaths

def set_startup_py(blender_path, ltmao_path):
    # get info
    version = os.path.basename(blender_path)
    appdata = userpaths.get_appdata()
    # set up data
    startup_py_path = f'{appdata}/Roaming/Blender Foundation/Blender/{version}/scripts/startup/lemon3d_startup.py'
    startup_py_data = f"""
def register():
    import sys
    sys.path.append('{ltmao_path}\\cpy\\Lib\\site-packages')
    sys.path.append('{ltmao_path}\\src')

def unregister():
    pass

if __name__ == "__main__":
    register()
"""
    # write data
    os.makedirs(os.path.dirname(startup_py_path), exist_ok=True)
    with open(startup_py_path, 'w+') as f:
        f.write(startup_py_data)