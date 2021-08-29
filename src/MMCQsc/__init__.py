# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build cover history  ____________

中国标准时间 2021-08-29 20:06:15  ->  1.2.690
中国标准时间 2021-08-29 20:23:47  ->  1.2.710中国标准时间 2021-08-29 21:18:38  ->  1.2.833

'''