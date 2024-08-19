"""Windows implementation of userpaths.

Your application should not use this directly; "import userpaths" will
automatically select the correct implementation for the current platform.
"""

import os
import ctypes
import ctypes.wintypes


# These constants are defined in the Windows API's shlobj.h.
# For reference: MinGW-w64's mingw-w64-headers/include/shlobj.h

# Constant special item ID list values for special folders
CSIDL_APPDATA = 0x001a
CSIDL_DESKTOPDIRECTORY = 0x0010
CSIDL_LOCAL_APPDATA = 0x001c
CSIDL_MYMUSIC = 0x000d
CSIDL_MYPICTURES = 0x0027
CSIDL_MYVIDEO = 0x000e
CSIDL_PERSONAL = 0x0005
CSIDL_PROFILE = 0x0028

# Flags for SHGetFolderPath
SHGFP_TYPE_CURRENT = 0
SHGFP_TYPE_DEFAULT = 1

# Convenient shorthand for this function
SHGetFolderPathW = ctypes.windll.shell32.SHGetFolderPathW


def _get_folder_path(csidl):
    """Get the path of a folder identified by a CSIDL value."""

    # Create a buffer to hold the return value from SHGetFolderPathW
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)

    # Return the path as a string
    SHGetFolderPathW(None, csidl, None, SHGFP_TYPE_CURRENT, buf)
    return str(buf.value)


def get_appdata():
    """Return the current user's roaming Application Data folder."""
    return _get_folder_path(CSIDL_APPDATA)

def get_desktop():
    """Return the current user's Desktop folder."""
    return _get_folder_path(CSIDL_DESKTOPDIRECTORY)

def get_downloads():
    """Return the current user's Downloads folder."""
    # There is no CSIDL value for this folder. The SHGetKnownFolderPath()
    # mechanism that replaces SHGetFolderPath() on Windows Vista and newer
    # provides FOLDERID_Downloads, but is not backwards-compatible.
    profile_downloads = os.path.join(get_profile(), "Downloads")
    my_docs_downloads = os.path.join(get_my_documents(), "Downloads")

    if os.path.exists(profile_downloads):
        # Windows Vista and newer
        return profile_downloads
    else:
        # Earlier versions of Windows
        return my_docs_downloads

def get_local_appdata():
    """Return the current user's local Application Data folder."""
    return _get_folder_path(CSIDL_LOCAL_APPDATA)

def get_my_documents():
    """Return the current user's My Documents folder."""
    return _get_folder_path(CSIDL_PERSONAL)

def get_my_music():
    """Return the current user's My Music folder."""
    return _get_folder_path(CSIDL_MYMUSIC)

def get_my_pictures():
    """Return the current user's My Pictures folder."""
    return _get_folder_path(CSIDL_MYPICTURES)

def get_my_videos():
    """Return the current user's My Videos folder."""
    return _get_folder_path(CSIDL_MYVIDEO)

def get_profile():
    """Return the current user's profile folder."""
    return _get_folder_path(CSIDL_PROFILE)
