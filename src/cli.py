import sys
from argparse import ArgumentParser

def parse_arguments():
    # arg parse
    parser = ArgumentParser(
        prog='LtMAO command line interface',
        description='LtMAO stuffs here.')
    parser.add_argument('-t', '--tool', type=str,
                        help='Which tool to use: wadpack, wadunpack')
    parser.add_argument('-src', '--source', type=str, help='Input file')
    parser.add_argument('-dst', '--destination',
                        type=str, help='Output file')
    if len(sys.argv) == 1:
        parser.print_help()
        input()
        sys.exit(-1)
    return parser.parse_args()


def ensure_curdir():
    import os
    import os.path
    os.chdir(os.path.dirname(os.path.dirname(sys.argv[0])))


class CLI:
    @staticmethod
    def wadpack(src, dst):
        from LtMAO import wad_tool
        if dst == None:
            dst = src
            if dst.endswith('.wad'):
                dst += '.client'
            else:
                if not dst.endswith('.wad.client'):
                    dst += '.wad.client'
        wad_tool.pack(src, dst)

    @staticmethod
    def wadunpack(src, dst):
        from LtMAO import wad_tool, hash_helper
        if dst == None:
            dst = src.replace('.wad.client', '.wad')
        hash_helper.Storage.read_wad_hashes()
        wad_tool.unpack(src, dst, hash_helper.Storage.hashtables)
        hash_helper.Storage.free_wad_hashes()

    @staticmethod
    def wadunpack_all(src, dst):
        from LtMAO import wad_tool, hash_helper
        import os, os.path
        hash_helper.Storage.read_wad_hashes()
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.endswith('.wad.client'):
                    wad = os.path.join(root, file)
                    dir = wad.replace('.wad.client', '.wad')
                    wad_tool.unpack(wad, dir, hash_helper.Storage.hashtables)
        hash_helper.Storage.free_wad_hashes()

    @staticmethod
    def ritobin(src, dst):
        from LtMAO import hash_helper, ritobin, pyRitoFile
        if src.endswith('.py'):
            dst = src.replace('.py', '.bin')
            ritobin.text_to_bin(src, dst)
        else:
            is_bin = False
            if src.endswith('.bin'):
                is_bin = True
            if not is_bin:
                with pyRitoFile.stream.BytesStream.reader(src) as bs:
                    is_bin = pyRitoFile.wad.WADExtensioner.guess_extension(bs.read(20)) == 'bin'
            if is_bin:
                hash_helper.Storage.read_all_hashes()
                dst = src.replace('.bin', '.py') if '.bin' in src else src + '.py'
                ritobin.bin_to_text(src, dst, hashtables=hash_helper.Storage.hashtables)
                hash_helper.Storage.free_all_hashes()

    @staticmethod
    def ritobinnoext(src, dst):
        from LtMAO import ritobin
        dst = src.replace('.py', '')
        ritobin.text_to_bin(src, dst)

    @staticmethod
    def ritobindir(src, dst, bin2py=True):
        from LtMAO import hash_helper, ritobin, pyRitoFile
        import os, os.path
        if bin2py:
            hash_helper.Storage.read_all_hashes()
            for root, dirs, files in os.walk(src):
                for file in files:
                    bin_file = os.path.join(root, file).replace('\\', '/')
                    py_file = bin_file.replace('.bin', '.py') if '.bin' in bin_file else bin_file + '.py'
                    is_bin = False
                    if file.endswith('.bin'):
                        is_bin = True
                    if not is_bin:
                        with pyRitoFile.stream.BytesStream.reader(bin_file) as bs:
                            is_bin = pyRitoFile.wad.WADExtensioner.guess_extension(bs.read(20)) == 'bin'
                    if is_bin:
                        ritobin.bin_to_text(bin_file, py_file,  hashtables=hash_helper.Storage.hashtables)
            hash_helper.Storage.free_all_hashes()
        else:
            for root, dirs, files in os.walk(src):
                for file in files:
                    if file.endswith('.py'):
                        py_file = os.path.join(root, file).replace('\\', '/')
                        bin_file = py_file.replace('.py', '.bin')
                        ritobin.text_to_bin(py_file, bin_file)
        
    @staticmethod
    def ritobindirnoext(src, dst):
        from LtMAO import ritobin
        import os, os.path
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.endswith('.py'):
                    py_file = os.path.join(root, file).replace('\\', '/')
                    bin_file = py_file.replace('.py', '')
                    ritobin.text_to_bin(py_file, bin_file)

    @staticmethod
    def lfi(src):
        from LtMAO import hash_helper, file_inspector
        hash_helper.Storage.read_all_hashes()
        file_inspector.inspect(src, hash_helper.Storage.hashtables)
        hash_helper.Storage.free_all_hashes()
        
    @staticmethod
    def uvee(src):
        from LtMAO import uvee
        uvee.uvee_file(src)

    @staticmethod
    def hashextract(src):
        from LtMAO import hash_helper
        import os
        import os.path
        if os.path.isdir(src):
            file_paths = []
            for root, dirs, files in os.walk(src):
                for file in files:
                    file_paths.append(os.path.join(root, file))
            hash_helper.ExtractedHashes.extract(*file_paths)
        else:
            hash_helper.ExtractedHashes.extract(src)

    @staticmethod
    def pyntex(src, delete_junk_files=False):
        from LtMAO import pyntex
        pyntex.parse(src, delete_junk_files)

    @staticmethod
    def tex2dds(src):
        from LtMAO import Ritoddstex
        Ritoddstex.tex2dds(src)

    @staticmethod
    def dds2tex(src):
        from LtMAO import Ritoddstex
        Ritoddstex.dds2tex(src)
    
    @staticmethod
    def tex2ddsdir(src):
        import os, os.path
        from LtMAO import Ritoddstex
        for root, dirs, files in os.walk(src):
            for file in files:  
                if file.endswith('.tex'):
                    tex_file = os.path.join(root, file).replace('\\', '/')
                    Ritoddstex.tex2dds(tex_file)

    @staticmethod
    def dds2texdir(src):
        import os, os.path
        from LtMAO import Ritoddstex
        for root, dirs, files in os.walk(src):
            for file in files:  
                if file.endswith('.dds'):
                    dds_file = os.path.join(root, file).replace('\\', '/')
                    Ritoddstex.dds2tex(dds_file)

    @staticmethod
    def png2dds(src, dst):
        from LtMAO import tools
        if dst == None:
            dst = src.replace('.png', '.dds')
        tools.ImageMagick.to_dds(
            src=src,
            dds=dst,
            format='dxt5',
            mipmap=False
        )

    @staticmethod
    def png2ddsmm(src, dst):
        from LtMAO import tools
        if dst == None:
            dst = src.replace('.png', '.dds')
        tools.ImageMagick.to_dds(
            src=src,
            dds=dst,
            format='dxt5',
            mipmap=True
        )


    @staticmethod
    def dds2png(src, dst):
        from LtMAO import tools
        if dst == None:
            dst = src.replace('.dds', '.png')
        tools.ImageMagick.to_png(
            src=src,
            png=dst,
        )

    @staticmethod
    def dds2x4x(src):
        import os
        import os.path
        from PIL import Image
        from LtMAO import tools
        with Image.open(src) as img:
            basename = os.path.basename(src)
            dirname = os.path.dirname(src)
            width_2x = img.width // 2
            height_2x = img.height // 2
            file_2x = os.path.join(dirname, '2x_'+basename).replace('\\', '/')
            width_4x = img.width // 4
            height_4x = img.height // 4
            file_4x = os.path.join(dirname, '4x_'+basename).replace('\\', '/')
        print(f'dds2x4x: Running: Create: {file_2x}')
        tools.ImageMagick.resize_dds(
            src=src,
            dst=file_2x, width=width_2x, height=height_2x
        )
        print(f'dds2x4x: Running: Create: {file_4x}')
        tools.ImageMagick.resize_dds(
            src=src,
            dst=file_4x, width=width_4x, height=height_4x
        )

    def wem2wav(src):
        from LtMAO import wiwawe
        wiwawe.wem2wav([src])

    def wav2wem(src):
        from LtMAO import wiwawe
        wiwawe.wav2wem([src])
    
    def ogg2wem(src):
        from LtMAO import wiwawe
        wiwawe.ogg2wem([src])

    def wem2wavdir(src):
        import os, os.path
        wem_files = []
        for root, dirs, files in os.walk(src):
            for file in files:  
                if file.endswith('.wem'):
                    wem_files.append(os.path.join(root, file).replace('\\', '/')) 
        from LtMAO import wiwawe
        wiwawe.wem2wav(wem_files)

    def wav2wemdir(src):
        import os, os.path
        wav_files = []
        for root, dirs, files in os.walk(src):
            for file in files:  
                if file.endswith('.wav'):
                    wav_files.append(os.path.join(root, file).replace('\\', '/')) 
        from LtMAO import wiwawe
        wiwawe.wav2wem(wav_files)
    
    def ogg2wemdir(src):
        import os, os.path
        ogg_files = []
        for root, dirs, files in os.walk(src):
            for file in files:  
                if file.endswith('.ogg'):
                    ogg_files.append(os.path.join(root, file).replace('\\', '/')) 
        from LtMAO import wiwawe
        wiwawe.ogg2wem(ogg_files)

    def bnk2dir(src):
        from LtMAO import bnk_tool
        bnk_tool.bnk2dir(src)
    
    def wpk2dir(src):
        from LtMAO import bnk_tool
        bnk_tool.bnk2dir(src)

    def dir2bnk(src):
        from LtMAO import bnk_tool
        bnk_tool.dir2bnk(src, True)
    
    def dir2wpk(src):
        from LtMAO import bnk_tool
        bnk_tool.dir2bnk(src, False)

    def zipfantome(src):
        import os.path, json, zipfile
        info_file = src + '/META/info.json'
        if not os.path.exists(info_file):
            raise Exception(f'zipfantome: Error:  No META/info.json found inside {src}.')

        info = {}
        with open(info_file, 'r', encoding='utf-8') as f:
            info = json.load(f)

        dst = os.path.dirname(src) + f'/{info["Name"]} V{info["Version"]} by {info["Author"]}.fantome'
        print(f'zipfantome: Running: Zip: {src} to {dst}')
        with zipfile.ZipFile(dst, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip:
            for root, dirs, files in os.walk(src):
                for file in files:
                    filename = os.path.join(root, file)
                    arcname = os.path.relpath(filename, src)
                    zip.write(filename, arcname)

    def unzipfantome(src):
        import zipfile

        dst = src.replace('.fantome', '')
        print(f'unzipfantome: Running: Unzip: {src} to {dst}')
        with zipfile.ZipFile(src, 'r') as zip:
            zip.extractall(dst)

    def geb(src):
        from LtMAO import bnk_tool
        bnk_tool.guess_events_bnk(src)
        input('Press enter to exit')
        

def main():
    funcs = {
        'wadpack':          lambda src, dst: CLI.wadpack(src, dst),
        'wadunpack':        lambda src, dst: CLI.wadunpack(src, dst),
        'wadunpack_all':    lambda src, dst: CLI.wadunpack_all(src, dst),

        'ritobin':          lambda src, dst: CLI.ritobin(src, dst),
        'ritobinnoext':     lambda src, dst: CLI.ritobinnoext(src, dst),
        'ritobindir2py':    lambda src, dst: CLI.ritobindir(src, dst, True),
        'ritobindir2bin':   lambda src, dst: CLI.ritobindir(src, dst, False),
        'ritobindirnoext':  lambda src, dst: CLI.ritobindirnoext(src, dst),

        'lfi':              lambda src, dst: CLI.lfi(src),

        'uvee':             lambda src, dst: CLI.uvee(src),

        'hashextract':      lambda src, dst: CLI.hashextract(src),

        'pyntex':           lambda src, dst: CLI.pyntex(src),
        'pyntexdeljunk':    lambda src, dst: CLI.pyntex(src, True),

        'tex2dds':          lambda src, dst: CLI.tex2dds(src),
        'dds2tex':          lambda src, dst: CLI.dds2tex(src),
        'tex2ddsdir':       lambda src, dst: CLI.tex2ddsdir(src),
        'dds2texdir':       lambda src, dst: CLI.dds2texdir(src),

        'dds2png':          lambda src, dst: CLI.dds2png(src, dst),
        'png2dds':          lambda src, dst: CLI.png2dds(src, dst),
        'png2ddsmm':        lambda src, dst: CLI.png2ddsmm(src, dst),

        'dds2x4x':          lambda src, dst: CLI.dds2x4x(src),

        'wem2wav':          lambda src, dst: CLI.wem2wav(src),
        'wav2wem':          lambda src, dst: CLI.wav2wem(src),
        'ogg2wem':          lambda src, dst: CLI.ogg2wem(src),
        'wem2wavdir':       lambda src, dst: CLI.wem2wavdir(src),
        'wav2wemdir':       lambda src, dst: CLI.wav2wemdir(src),
        'ogg2wemdir':       lambda src, dst: CLI.ogg2wemdir(src),

        'dir2bnk':          lambda src, dst: CLI.dir2bnk(src),
        'dir2wpk':          lambda src, dst: CLI.dir2wpk(src),
        'bnk2dir':          lambda src, dst: CLI.bnk2dir(src),
        'wpk2dir':          lambda src, dst: CLI.wpk2dir(src),

        'geb':              lambda src, dst: CLI.geb(src),

        'zipfantome':       lambda src, dst: CLI.zipfantome(src),
        'unzipfantome':     lambda src, dst: CLI.unzipfantome(src),
    }

    args = parse_arguments()
    ensure_curdir()
    funcs[args.tool](args.source, args.destination)

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)
        input()
        sys.exit(-1)
