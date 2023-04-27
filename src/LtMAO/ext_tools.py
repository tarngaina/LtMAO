import os
import os.path
import subprocess

LOG = print


class RITOBIN:
    local_file = './resources/ext_tools/ritobin_cli.exe'

    def run(src, dst=None, *, dir_hashes=None):
        cmds = [os.path.abspath(RITOBIN.local_file), src]
        if dst:
            cmds.append(dst)
        if dir_hashes:
            cmds.extend(('--dir-hashes', dir_hashes))
        p = subprocess.Popen(
            cmds, creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        for line in p.stdout:
            LOG(line.decode()[:-1])
        p.wait()
        if p.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=p.returncode,
                cmd=p.args,
                stderr=p.stderr
            )


def prepare(_LOG):
    global LOG
    LOG = _LOG
