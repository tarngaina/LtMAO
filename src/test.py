from LtMAO.pyRitoFile import bin_hash

alphabet = 'abcdefghijklmnopqrtsuvwxyz0123456789/_'

from itertools import chain, product
def bruteforce(charset, maxlength, startvalue):
    startvalue_len = len(startvalue)
    if maxlength < startvalue_len:
        raise Exception(f'Wrong maxlength {maxlength}, startvalue_len {startvalue_len}')
    return (
        ''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i) for i in range(len(startvalue), maxlength + 1)) 
        if candidate > startvalue 
    )

import os, os.path
path_dir = 'D:/hash_maps/'
max_num = -1
for file in os.listdir(path_dir):
    num = int(file.split('.txt')[0])
    if num > max_num:
        max_num = num 
max_num += 1
os.makedirs(path_dir, exist_ok=True)
path_file = os.path.join(path_dir, f'{max_num}.txt')
f = open(path_file, 'w+')
f.close()
f = open(path_file, 'a+')
count = 0
for a in bruteforce(alphabet, 200, tuple('a')):
    f.write(f'{a} {bin_hash(a)}\n')
    count += 1
    if count > 5000000:
        max_num += 1
        f.close()
        path_file = os.path.join(path_dir, f'{max_num}.txt')
        f = open(path_file, 'a+')
        count = 0