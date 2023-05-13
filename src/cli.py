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
    # argv[0] is LtMAO/src/cli.py
    # curdir must be LtMAO -> new curdir = dirname(dirname(argv[0]))
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
        from LtMAO import wad_tool
        if dst == None:
            dst = src.replace('.wad.client', '.wad')
        wad_tool.unpack(src, dst)

    @staticmethod
    def ritobin(src, dst):
        from LtMAO import ext_tools, hash_manager
        ext_tools.RITOBIN.run(
            src, dst, dir_hashes=hash_manager.CustomHashes.local_dir)

    @staticmethod
    def lfi(src):
        from LtMAO import leaguefile_inspector, hash_manager, pyRitoFile
        hash_manager.read_all_hashes()
        path, size, type, json = leaguefile_inspector.read_lfi(
            src, hash_manager.HASHTABLES)
        dst = src + '.json'
        with open(dst, 'w+') as f:
            f.write(json if json != None else '{}')
        hash_manager.free_all_hashes()

    @staticmethod
    def uvee(src):
        from LtMAO import uvee
        uvee.uvee_file(src)

    @staticmethod
    def hashextract(src):
        from LtMAO import hash_manager
        import os
        import os.path
        if os.path.isdir(src):
            file_paths = []
            for root, dirs, files in os.walk(src):
                for file in files:
                    file_paths.append(os.path.join(root, file))
            hash_manager.ExtractedHashes.extract(*file_paths)
        else:
            hash_manager.ExtractedHashes.extract(src)

    @staticmethod
    def pyntex(src):
        from LtMAO import pyntex
        pyntex.parse(src)


def main():
    args = parse_arguments()
    ensure_curdir()
    if args.tool == 'wadpack':
        CLI.wadpack(args.source, args.destination)
    elif args.tool == 'wadunpack':
        CLI.wadunpack(args.source, args.destination)
    elif args.tool == 'ritobin':
        CLI.ritobin(args.source, args.destination)
    elif args.tool == 'lfi':
        CLI.lfi(args.source)
    elif args.tool == 'uvee':
        CLI.uvee(args.source)
    elif args.tool == 'hashextract':
        CLI.hashextract(args.source)
    elif args.tool == 'pyntex':
        CLI.pyntex(args.source)


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
