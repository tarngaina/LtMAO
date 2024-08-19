"""Cross-platform access to a user's special folders.

The userpaths module provides cross-platform access to a user's special
folders (or directories) like My Documents, Desktop, and Application Data.
See the function list below for available paths.

Note: The userpaths module was originally designed from a Windows-centric
perspective. Because of the many differences between the two systems, there
are some Windows paths that do not have a direct equivalent on Unix, and
vice versa. In these cases, userpaths attempts to return the nearest
functional equivalent, but it is up to the user to ensure their application
is using the appropriate path for what it seeks to do.
"""

import sys

# Import the appropriate implementation for the current system
if sys.platform.startswith("win"):
    from .windows import *
else:
    # Presume anything else is a Unix-like system
    from .unix import *


# Synonym for get_my_documents() for compatibility with winpaths
get_personal = get_my_documents


# These functions are defined in the individual platform modules
__all__ = [
    "get_appdata",
    "get_desktop",
    "get_downloads",
    "get_local_appdata",
    "get_my_documents",
    "get_my_music",
    "get_my_pictures",
    "get_my_videos",
    "get_personal",
    "get_profile",
]
