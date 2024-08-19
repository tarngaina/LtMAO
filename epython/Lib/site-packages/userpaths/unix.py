"""Unix implementation of userpaths.

Your application should not use this directly; "import userpaths" will
automatically select the correct implementation for the current platform.
"""

import os

# Paths within a user's home directory are, to my knowledge, not as
# standardized on Unix as they are on Windows. The paths returned by this
# module are based on the following references, in order of preference:
#
#  1. Published standards like the XDG Base Directory Specification [1].
#
#  2. De facto standards used by major applications. These are generally
#     safe to use regardless of the operating system distribution. For
#     example, the Desktop and Downloads directories are widely used by
#     major desktop environments and web browsers, respectively.
#
#  3. Other paths commonly found on major operating system distributions.
#     These are not guaranteed to exist on all systems, but are used widely
#     enough that users would reasonably expect us to return them if they
#     exist. For example, many Linux distributions now create Documents,
#     Pictures, Music, and Video folders similar to those found on Windows.
#
# The userpaths module was originally designed from a Windows-centric
# perspective. Because of the many differences between the two systems,
# there are some Windows paths that do not have a direct equivalent on
# Unix, and vice versa. In these cases, userpaths attempts to return the
# nearest functional equivalent, but it is up to the user to ensure their
# application is using the appropriate path for what it seeks to do.
#
# If you know of other applicable standards, or better equivalents than
# the ones used here, please feel free to submit a patch.
#
# References:
# [1] https://specifications.freedesktop.org/basedir-spec/latest/


def _prefer(path):
    """Return os.path.expanduser(path) if it exists, or $HOME otherwise."""

    path = os.path.expanduser(path)

    if os.path.isdir(path):
        return path
    else:
        return os.path.expanduser("~")


def _xdg_dir(env_name, default_value):
    """Return $env_name if specified, otherwise default_value."""

    if env_name:
        value = os.getenv(env_name)
    else:
        value = None

    if value:
        return value
    else:
        return os.path.expanduser(default_value)


def get_appdata():
    """Return the current user's roaming Application Data folder."""
    # Standardized in the XDG Base Directory Specification
    # FIXME: Is this actually the nearest equivalent in the XDG spec?
    return _xdg_dir("XDG_CONFIG_HOME", "~/.config")

def get_desktop():
    """Return the current user's Desktop folder."""
    # De facto standard among major desktop environments (GNOME, KDE, Xfce...)
    return _prefer("~/Desktop")

def get_downloads():
    """Return the current user's Downloads folder."""
    # De facto standard used by Firefox, Chrome, and other browsers
    return _prefer("~/Downloads")

def get_local_appdata():
    """Return the current user's local Application Data folder."""
    # Standardized in the XDG Base Directory Specification
    # FIXME: Is this actually the nearest equivalent in the XDG spec?
    return _xdg_dir("XDG_CONFIG_HOME", "~/.config")

def get_my_documents():
    """Return the current user's My Documents folder."""
    # Common on recent Linux distributions
    return _prefer("~/Documents")

def get_my_music():
    """Return the current user's My Music folder."""
    # Common on recent Linux distributions
    return _prefer("~/Music")

def get_my_pictures():
    """Return the current user's My Pictures folder."""
    # Common on recent Linux distributions
    return _prefer("~/Pictures")

def get_my_videos():
    """Return the current user's My Videos folder."""
    # Common on recent Linux distributions
    return _prefer("~/Videos")

def get_profile():
    """Return the current user's profile folder."""
    # On Unix this is simply the user's home directory, though note it is not
    # an exact equivalent since the %USERPROFILE% folder on Windows has a more
    # defined formal structure
    return os.path.expanduser("~")
