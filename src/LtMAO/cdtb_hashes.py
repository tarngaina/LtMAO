import requests
import os
import os.path
import threading
import json


def to_human(size): return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + \
    ["", " KB", " MB", " GB", " TB", " PB",
        " EB"][max(size.bit_length()-1, 0)//10]


class CDTB:
    STATUS = 'NOT_SYNCED'
    LOG = print

    local_dir = './prefs/ctdb_hashes/'
    etag_path = './prefs/ctdb_hashes/etag.json'

    def local_file(
        filename): return f'./prefs/ctdb_hashes/{filename}'

    def github_file(
        filename): return f'https://raw.githubusercontent.com/CommunityDragon/CDTB/master/cdragontoolbox/{filename}'

    ETAG = {}
    HASHTABLES = {}

    @staticmethod
    def sync_hashes(*filenames):
        for filename in filenames:
            CDTB.LOG(f'Running: Sync hash: {filename}')
            local_file = CDTB.local_file(filename)
            github_file = CDTB.github_file(filename)

            get = requests.get(github_file, stream=True)
            get.raise_for_status()

            etag_local = CDTB.ETAG.get(filename, None)
            etag_github = get.headers['Etag']
            if etag_local == None or etag_local != etag_github or not os.path.exists(local_file):
                CDTB.ETAG[filename] = etag_github
                bytes_downloaded = 0
                with open(local_file, 'wb') as f:
                    for chunk in get.iter_content(1024**2):
                        bytes_downloaded += len(chunk)
                        CDTB.LOG(
                            f'Downloading: {local_file}: {to_human(bytes_downloaded)}')
                        f.write(chunk)
            CDTB.LOG(f'Done: Sync hash: {filename}')

    @staticmethod
    def sync_all():
        CDTB.STATUS = 'SYNCING'
        if not os.path.exists(CDTB.local_dir):
            os.makedirs(CDTB.local_dir)
        CDTB.ETAG = {}
        if os.path.exists(CDTB.etag_path):
            with open(CDTB.etag_path, 'r') as f:
                CDTB.ETAG = json.load(f)
        CDTB.sync_hashes('hashes.binentries.txt', 'hashes.binfields.txt',
                         'hashes.binhashes.txt', 'hashes.bintypes.txt', 'hashes.game.txt', 'hashes.lcu.txt')
        with open(CDTB.etag_path, 'w+') as f:
            json.dump(CDTB.ETAG, f, indent=4)
        CDTB.STATUS = 'SYNCED'

    @staticmethod
    def sync_in_thread():
        threading.Thread(
            target=CDTB.sync_all,
            daemon=True
        ).start()

    @staticmethod
    def read_hashes(*filenames):
        for filename in filenames:
            local_file = CDTB.local_file(filename)
            if filename not in CDTB.HASHTABLES:
                CDTB.HASHTABLES[filename] = {}
            with open(local_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line[:-1].split()
                    hash = line[0]
                    name = line[1]
                    if hash not in CDTB.HASHTABLES[filename]:
                        CDTB.HASHTABLES[filename][hash] = name

    @staticmethod
    def read_all():
        CDTB.read_hashes('hashes.binentries.txt', 'hashes.binfields.txt',
                         'hashes.binhashes.txt', 'hashes.bintypes.txt', 'hashes.game.txt', 'hashes.lcu.txt')

    @staticmethod
    def free_hashes(*filenames):
        for filename in filenames:
            CDTB.HASHTABLES.pop(filename)

    @staticmethod
    def free_all():
        CDTB.HASHTABLES = {}
