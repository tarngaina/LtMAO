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


def main():
    args = parse_arguments()
    ensure_curdir()
    if args.tool == 'wadpack':
        from LtMAO import wad_tool
        src = args.source
        dst = args.destination
        if dst == None:
            dst = src
            if dst.endswith('.wad'):
                dst += '.client'
            else:
                if not dst.endswith('.wad.client'):
                    dst += '.wad.client'
        wad_tool.pack(src, dst)
    elif args.tool == 'wadunpack':
        from LtMAO import wad_tool
        src = args.source
        dst = args.destination
        if dst == None:
            dst = src.replace('.wad.client', '.wad')
        wad_tool.unpack(src, dst)


if __name__ == '__main__':
    try:
        main()
        input()
        sys.exit(0)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)
        input()
        sys.exit(-1)
