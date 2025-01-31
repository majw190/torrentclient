import math

import hashlib
import time
import logging
import os

from bcoding import bencode, bdecode
from bencodepy import encode
from py1337x import py1337x

class Torrent(object):
    def __init__(self):
        self.torrent_file = {}
        self.total_length = self.piece_length = self.pieces = self.pieces_total = 0
        self.info_hash = self.peer_ID = self.announce_list = ''
        self.file_names = []

# decode .torrent file encoded in bencode format
# parse bencode binary data into a Python dictionary
def load_from_path(self, path):
    with open(path, 'rb') as file:
        contents = bdecode(file.read())  # read file before decoding it

    self.torrent_file = contents
    info_dictionary = self.torrent_file['info']
    self.piece_length = info_dictionary['piece_length']
    self.pieces = info_dictionary['pieces']

    # bencode info dictionary, understand sha-1 hash, for peer identification
    self.info_hash = hashlib.sha1(bencode(info_dictionary)).digest()
    # generate peer id (20-byte identifier for torrent client)
    self.peer_ID = self.generate_peer_ID()
    # extract the tracker URLs
    self.list = self.get_trackers()
    # process file metadata
    self.init_files()

    # how many pieces available in total
    self.pieces_total = math.ceil(self.total_length / self.piece_length)

    # log tracker list and file names for debug
    logging.debug(self.list)
    logging.debug(self.file_names)

    return self

# create directories, store file paths, compute total file sizing
def init_files(self):
    info_dictionary = self.torrent_file['info']
    # extract torrent root folder name from info dictionary
    root = info_dictionary['name']

    if 'files' in info_dictionary:
        os.makedirs(root, exist_ok=True)

        # process files / make sure directories exist before files are handled
        for file in info_dictionary['files']:
            path_file = os.path.join(root, *file["path"])
            # make sure directory exists / create directories if they don't exist
            os.makedirs(os.path.dirname(path_file), exist_ok=True)

        # init_files needs to update self.file_names + self.total_length
        self.file_names.append({"path": root, "length": info_dictionary["length"]})
        self.total_length += info_dictionary["length"]

# get tracker list from .torrent file
# when multiple trackers exist, return them. otherwise, wrap primary track URL in nested list
def get_trackers(self):
    trackers = self.torrent_file.get('announce-list')
    return trackers if trackers else [[self.torrent_file['announce']]]

# generate peer ID using SHA-1 hash
# identify client in BitTorrent network
def generate_peer_ID(self):
    timestamp = str(time.time()).encode()
    return hashlib.sha1(timestamp).digest()
