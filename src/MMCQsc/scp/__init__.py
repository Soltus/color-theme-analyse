
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    pass