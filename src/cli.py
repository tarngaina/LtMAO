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
        from LtMAO import hash_helper, tools
        tools.RITOBIN.run(src, dst, dir_hashes=hash_helper.CustomHashes.local_dir)


    @staticmethod
    def ritobindir(src, dst, bin2py=True):
        from LtMAO import hash_helper, tools
        tools.RITOBIN.run(src, None, dir_hashes=hash_helper.CustomHashes.local_dir, recursive=True, recursive_bin2py=bin2py)

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
    args = parse_arguments()
    ensure_curdir()
    if args.tool == 'wadpack':
        CLI.wadpack(args.source, args.destination)
    elif args.tool == 'wadunpack':
        CLI.wadunpack(args.source, args.destination)
    elif args.tool == 'wadunpack_all':
        CLI.wadunpack_all(args.source, args.destination)
    elif args.tool == 'ritobin':
        CLI.ritobin(args.source, args.destination)
    elif args.tool == 'ritobindir2py':
        CLI.ritobindir(args.source, args.destination, True)
    elif args.tool == 'ritobindir2bin':
        CLI.ritobindir(args.source, args.destination, False)
    elif args.tool == 'lfi':
        CLI.lfi(args.source)
    elif args.tool == 'uvee':
        CLI.uvee(args.source)
    elif args.tool == 'hashextract':
        CLI.hashextract(args.source)
    elif args.tool == 'pyntex':
        CLI.pyntex(args.source)
    elif args.tool == 'pyntexdeljunk':
        CLI.pyntex(args.source, True)
    elif args.tool == 'tex2dds':
        CLI.tex2dds(args.source)
    elif args.tool == 'dds2tex':
        CLI.dds2tex(args.source)
    elif args.tool == 'tex2ddsdir':
        CLI.tex2ddsdir(args.source)
    elif args.tool == 'dds2texdir':
        CLI.dds2texdir(args.source)
    elif args.tool == 'dds2png':
        CLI.dds2png(args.source, args.destination)
    elif args.tool == 'png2dds':
        CLI.png2dds(args.source, args.destination)
    elif args.tool == 'png2ddsmm':
        CLI.png2ddsmm(args.source, args.destination)
    elif args.tool == 'dds2x4x':
        CLI.dds2x4x(args.source)
    elif args.tool == 'wem2wav':
        CLI.wem2wav(args.source)
    elif args.tool == 'wav2wem':
        CLI.wav2wem(args.source)
    elif args.tool == 'dir2bnk':
        CLI.dir2bnk(args.source)
    elif args.tool == 'dir2wpk':
        CLI.dir2wpk(args.source)
    elif args.tool == 'bnk2dir':
        CLI.bnk2dir(args.source)
    elif args.tool == 'wpk2dir':
        CLI.wpk2dir(args.source)
    elif args.tool == 'zipfantome':
        CLI.zipfantome(args.source)
    elif args.tool == 'unzipfantome':
        CLI.unzipfantome(args.source)
    elif args.tool == 'geb':
        CLI.geb(args.source)


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
