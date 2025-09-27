from LtMAO import lepath, pyRitoFile, hash_helper
import os, os.path, shutil

def unify_path(path):
    # if the path is straight up hex
    # ex: ec9584b0506c2abb -> ec9584b0506c2abb
    if pyRitoFile.wad.WADHasher.is_hash(path):
        return path
    # if the path is hashed file 
    # ex: ec9584b0506c2abb.bin -> ec9584b0506c2abb
    basename = path.split('.')[0]
    if pyRitoFile.wad.WADHasher.is_hash(basename):
        return basename
    # if the path is pure raw
    # ex: data/effects.bin -> ec9584b0506c2abb
    return pyRitoFile.wad.WADHasher.raw_to_hex(path)

def is_character_bin(path):
    path = path.lower()
    if 'characters/' in path and path.endswith('.bin'):
        chars = path.split('characters/')[1].replace('.bin', '').split('/')
        return chars[0] == chars[1]
    return False

def bum_path(path, prefix):
    if '/' in path:
        first_slash = path.index('/')
        path = path[:first_slash] + f'/{prefix}' + path[first_slash:]
    else:
        path = f'{prefix}/' + path
    return path

def flat_list_linked_bins(source_unify_file, linked_bins):
    res = []
    def list_linked_bins(unify_file):
        for linked_unify_file in linked_bins[unify_file]:
            if linked_unify_file not in res and linked_unify_file != source_unify_file:
                res.append(linked_unify_file)
                list_linked_bins(linked_unify_file)
    list_linked_bins(source_unify_file)
    return res

        
class Bum:
    def __init__(self):
        self.source_dirs = [] # list of input dir
        self.source_files = {} # map input path by unify path
        self.source_bins = {}  # source_files but only if input path is a bin
        self.scanned_tree = {} # map contain entry, entry contain list of unify path mentioned, unify path mentioned contain exist state and rel path
        self.entry_prefix = {} # map prefix by entry hash
        self.entry_name = {} # map entry raw name by entry hash
        self.linked_bins = {} # map linked bins by source bin

    def reset(self):
        self.source_dirs = []
        self.source_files = {}
        self.source_bins = {}
        self.scanned_tree = {}
        self.entry_prefix = {}
        self.entry_name = {}
        self.linked_bins = {}

    def add_source_dirs(self, source_dirs):
        self.source_dirs += source_dirs
        # scan to get path in source dirs
        for source_dir in self.source_dirs:
            full_files = lepath.walk(source_dir, lambda f: True, topdown=False)
            for full_file in full_files:
                short_file = lepath.rel(full_file, source_dir)
                unify_file = unify_path(short_file)
                # we dont overwrite new path, because priority is topdown
                if unify_file not in self.source_files:
                    self.source_files[unify_file] = (full_file, short_file)
                    if short_file.endswith('.bin'):
                        self.source_bins[unify_file] = False

    def scan(self):
        self.scanned_tree = {}
        # setting for bin entry, just a display
        self.scanned_tree['All_BINs'] = {} 
        self.entry_prefix['All_BINs'] = 'Uneditable'
        self.entry_name['All_BINs'] = 'All_BINs'

        # scan functions
        def scan_value(value, value_type, entry_hash):
            if value_type == pyRitoFile.bin.BINType.STRING:
                value_lower = value.lower()
                if 'assets/' in value_lower or 'data/' in value_lower:
                    unify_file = unify_path(value)
                    # set the scanned file exist state
                    if unify_file in self.source_files:
                        self.scanned_tree[entry_hash][unify_file] = (True, value)
                    else:
                        self.scanned_tree[entry_hash][unify_file] = (False, value)
            elif value_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                for v in value.data:
                    scan_value(v, value_type, entry_hash)
            elif value_type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                if value.data != None:
                    for f in value.data:
                        scan_field(f, entry_hash)

        def scan_field(field, entry_hash):
            if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                for v in field.data:
                    scan_value(v, field.value_type, entry_hash)
            elif field.type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                if field.data != None:
                    for f in field.data:
                        scan_field(f, entry_hash)
            elif field.type == pyRitoFile.bin.BINType.MAP:
                for key, value in field.data.items():
                    scan_value(key, field.key_type, entry_hash)
                    scan_value(value, field.value_type, entry_hash)
            elif field.type == pyRitoFile.bin.BINType.OPTION and field.value_type == pyRitoFile.bin.BINType.STRING:
                if field.data != None:
                    scan_value(field.data, field.value_type, entry_hash)
            else:
                scan_value(field.data, field.type, entry_hash)

        def scan_bin(bin_path, unify_file):
            bin = pyRitoFile.bin.BIN().read(bin_path)
            self.linked_bins[unify_file] = []
            for link in bin.links:
                if is_character_bin(link):
                    continue
                unify_link = unify_path(link)
                # set the scanned bin exist state
                if unify_link in self.source_files:
                    self.scanned_tree['All_BINs'][unify_link] = (True, link)
                    # scan inside the linked bin
                    scan_bin(self.source_files[unify_link][0], unify_link)
                    # this is for easier combine bin, not that important
                    self.linked_bins[unify_file].append(unify_link)
                else:
                    self.scanned_tree['All_BINs'][unify_link] = (False, link)
            for entry in bin.entries:
                entry_hash = entry.hash
                self.scanned_tree[entry_hash] = {}
                self.entry_prefix[entry_hash] = 'bum'
                for field in entry.data:
                    scan_field(field, entry_hash)
                # unhash entry to another dict for ui display
                if entry_hash not in self.entry_name:
                    self.entry_name[entry_hash] = pyRitoFile.bin.BINHasher.hex_to_raw(hash_helper.Storage.hashtables, entry_hash)

        hash_helper.Storage.read_all_hashes()
        for unify_file in self.source_bins:
            if self.source_bins[unify_file]:
                full, rel = self.source_files[unify_file]
                # source bin is obviously existed
                self.scanned_tree['All_BINs'][unify_file] = (True, rel)
                scan_bin(full, unify_file)
        hash_helper.Storage.free_all_hashes()
        self.scanned_tree = dict(sorted(self.scanned_tree.items(), key=lambda item: self.entry_name[item[0]]))

    def bum(self, output_dir, ignore_missing=False, combine_linked=False):
        def bum_value(value, value_type, entry_hash):
            if value_type == pyRitoFile.bin.BINType.STRING:
                value_lower = value.lower()
                if 'assets/' in value_lower or 'data/' in value_lower:
                    unify_file = unify_path(value_lower)
                    if unify_file in self.scanned_tree[entry_hash]:
                        existed, path = self.scanned_tree[entry_hash][unify_file]
                        # only bum if the file is exsisted
                        if existed:
                            return bum_path(value, self.entry_prefix[entry_hash])
            elif value_type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                value.data = [bum_value(v, value_type, entry_hash) for v in value.data]
            elif value_type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                if value.data != None:
                    for f in value.data:
                        bum_field(f, entry_hash)
            return value

        def bum_field(field, entry_hash):
            if field.type in (pyRitoFile.bin.BINType.LIST, pyRitoFile.bin.BINType.LIST2):
                field.data = [bum_value(value, field.value_type, entry_hash) for value in field.data]
            elif field.type in (pyRitoFile.bin.BINType.EMBED, pyRitoFile.bin.BINType.POINTER):
                if field.data != None:
                    for f in field.data:
                        bum_field(f, entry_hash)
            elif field.type == pyRitoFile.bin.BINType.MAP:
                field.data = {
                    bum_value(key, field.key_type, entry_hash): bum_value(value, field.value_type, entry_hash)
                    for key, value in field.data.items()
                }
            elif field.type == pyRitoFile.bin.BINType.OPTION and field.value_type == pyRitoFile.bin.BINType.STRING:
                if field.data != None:
                    field.data = bum_value(field.data, field.value_type, entry_hash)
            else:
                field.data = bum_value(field.data, field.type, entry_hash)
                
        def bum_bin(bin_path):
            bin = pyRitoFile.bin.BIN().read(bin_path)
            for entry in bin.entries:
                entry_hash = entry.hash
                for field in entry.data:
                    bum_field(field, entry_hash)
            bin.write(bin_path)

        # error checks
        if len(self.scanned_tree) == 0:
            raise Exception('bumpath: Error: No entry scanned, make sure you select at least one source BIN.')
        if not ignore_missing:
            for entry_hash in self.scanned_tree:
                for unify_file in self.scanned_tree[entry_hash]:
                    existed, short_file = self.scanned_tree[entry_hash][unify_file]
                    if not existed:
                        raise Exception(f'bumpath: Error: {entry_hash}/{short_file} is missing/not found in Source Folders.')
        # actual bum
        bum_files = {}
        for entry_hash in self.scanned_tree:
            prefix = self.entry_prefix[entry_hash]
            for unify_file in self.scanned_tree[entry_hash]:
                existed, short_file = self.scanned_tree[entry_hash][unify_file]
                # bum outside
                if not short_file.endswith('.bin'):
                    short_file = bum_path(short_file, prefix)
                if not existed:
                    continue
                source_file = self.source_files[unify_file][0]
                output_file = lepath.join(output_dir, short_file.lower())
                if len(os.path.basename(output_file)) > 255:
                    extension = os.path.splitext(short_file)[1]
                    basename = pyRitoFile.wad.WADHasher.raw_to_hex(short_file)
                    if extension != '':
                        basename += extension
                    output_file = lepath.join(output_dir, basename)
                # copy
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                shutil.copy(source_file, output_file)
                # bum inside bins
                if output_file.endswith('.bin'):
                    bum_bin(output_file)
                bum_files[unify_file] = output_file
                print(f'bumpath: Finish: Bum {output_file}')
        # combine bin
        if combine_linked:
            for unify_file in self.source_bins:
                if self.source_bins[unify_file]:
                    # read source bin
                    source_bin = pyRitoFile.bin.BIN().read(bum_files[unify_file])
                    # get all linked bin in flat 
                    linked_unify_files = flat_list_linked_bins(unify_file, self.linked_bins)
                    # remove scanned linked bin in source bin links
                    new_links = []
                    for link in source_bin.links:
                        if not unify_path(link) in linked_unify_files:
                            new_links.append(link)
                    source_bin.links = new_links
                    # append linked bin entries to source bin entries
                    # and delete linked bin file
                    for linked_unify_file in linked_unify_files:
                        bum_file = bum_files[linked_unify_file]
                        source_bin.entries += pyRitoFile.bin.BIN().read(bum_file).entries
                        os.remove(bum_file)
                    # write source bin
                    source_bin.write(bum_files[unify_file])
                    print(f'bumpath: Finish: Combine all linked BINs to {bum_files[unify_file]}.')
        # remove empty dirs
        for root, dirs, files in os.walk(output_dir, topdown=False):
            if len(os.listdir(root)) == 0:
                os.rmdir(root)
        print(f'bumpath: Finish: Bum {output_dir}.')
