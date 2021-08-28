# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version, version_tuple

__doc__ = f'''
MMCQsc version: [{version}]
build time: [[build_time]]
'''