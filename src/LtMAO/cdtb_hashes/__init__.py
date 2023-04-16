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
    def sync_hashes(filename):
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

        with open(local_file, 'r') as f:
            lines = f.readlines()
            items = [line[:-1].split() for line in lines]
            CDTB.HASHTABLES[filename] = {
                item[0]: item[1] for item in items
            }
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
        CDTB.sync_hashes('hashes.binentries.txt')
        CDTB.sync_hashes('hashes.binfields.txt')
        CDTB.sync_hashes('hashes.binhashes.txt')
        CDTB.sync_hashes('hashes.bintypes.txt')
        CDTB.sync_hashes('hashes.game.txt')
        CDTB.sync_hashes('hashes.lcu.txt')
        with open(CDTB.etag_path, 'w+') as f:
            json.dump(CDTB.ETAG, f, indent=4)
        CDTB.STATUS = 'SYNCED'

    @staticmethod
    def sync_in_thread():
        threading.Thread(
            target=CDTB.sync_all,
            daemon=True
        ).start()
