# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 05:44:05  ->  (1, 2, 561)中国标准时间 2021-08-29 05:45:07  ->  (1, 2, 563)

'''