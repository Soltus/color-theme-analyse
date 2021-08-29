# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build cover history  ____________

中国标准时间 2021-08-29 21:18:38  ->  1.2.833中国标准时间 2021-08-29 21:19:16  ->  1.2.843中国标准时间 2021-08-29 21:19:43  ->  1.2.844

'''