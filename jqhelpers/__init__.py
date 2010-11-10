import os
from pkg_resources import resource_filename #@UnresolvedImport
from subprocess import Popen, PIPE #@UnresolvedImport

__VERSION_FILE__ = "RELEASE-VERSION"

def __call_git_describe(abbrev=4):
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()
    except:
        return None

def __read_release_version():
    try:
        f = open(resource_filename(__name__, __VERSION_FILE__), "r")
        try:
            version = f.readlines()[0]
            return version.strip()
        finally:
            f.close()
    except:
        return None

def __write_release_version(version):
    f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)),__VERSION_FILE__), "w")
    f.write("%s\n" % version)
    f.close()


def get_git_version(abbrev=4):
    # Read in the version that's currently in RELEASE-VERSION.
    release_version = __read_release_version()
    # First try to get the current version using git describe.
    version = __call_git_describe(abbrev)
    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.
    if version is None:
        version = release_version
    # If we still don't have anything, that's an error.
    if version is None:
        raise ValueError("Cannot find the version number!")
    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if version != release_version:
        __write_release_version(version)
    # Finally, return the current version.
    return version

__version__ = get_git_version()
