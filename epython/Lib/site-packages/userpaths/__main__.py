"""Test program for the userpaths module."""

# For Python 2 compatibility
from __future__ import print_function

# This will import the correct implementation for the current platform
from . import *


path_functions = [
    # Description           Function
    ("App Data",            get_appdata),
    ("Desktop",             get_desktop),
    ("Downloads",           get_downloads),
    ("Local App Data",      get_local_appdata),
    ("My Documents",        get_my_documents),
    ("My Music",            get_my_music),
    ("My Pictures",         get_my_pictures),
    ("My Videos",           get_my_videos),
    ("User Profile",        get_profile),
]


def test_userpaths():
    for desc, get_path in path_functions:
        print("{0:14} = {1}".format(desc, get_path()))


if __name__ == "__main__":
    test_userpaths()
