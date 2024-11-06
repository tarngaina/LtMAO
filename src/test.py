from cProfile import Profile
from pstats import Stats

def profiler(func):
    with Profile() as pr:
        pr.enable()
        func()
        pr.disable()
        stats = Stats(pr)
        stats.sort_stats('tottime').print_stats(5)

def find_all_listcomps():
    import ast, os, os.path, sys
    with open('./find_all_listcomps.txt', 'w', encoding='utf-8') as sys.stdout:
        for root, dirs, files in os.walk('./src'):
            for file in files:
                if file.endswith('.py'):
                    file = os.path.join(root, file).replace('\\', '/')
                    with open(file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    print(file)
                    last_lineno = 0
                    for node in ast.walk(ast.parse(''.join(lines))):
                        if isinstance(node, ast.ListComp):
                            for lineno in range(node.lineno, node.end_lineno + 1):
                                if lineno > last_lineno:
                                    print(lineno, lines[lineno - 1], sep='\t', end='')
                                    last_lineno = lineno
                            print()

def lol2fbx_mesh_test():
    from LtMAO.lemon3d import lemon_fbx
    lemon_fbx.fbx_to_skin('D:/test/briar_base.fbx')

def read_bin_test():
    from LtMAO import pyRitoFile
    
    pyRitoFile.write_bin('D:/test/base_srx2.materials.bin', pyRitoFile.read_bin('D:/test/base_srx.materials.bin'))

def read_write_anm_test():
    from LtMAO import pyRitoFile
    
    pyRitoFile.write_anm('D:/test/rRecall_legacy.SKINS_Aatrox_Skin33.anm', pyRitoFile.read_anm('D:/test/Recall_legacy.SKINS_Aatrox_Skin33.anm'))

def test_fbx_to_skin():
    from LtMAO.lemon3d import lemon_fbx

    lemon_fbx.fbx_to_skin('D:/test/savior.fbx')

def main():
    test_fbx_to_skin()


if __name__ == '__main__':
    main()