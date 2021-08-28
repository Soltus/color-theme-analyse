# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________
中国标准时间 2021-08-29 03:41:41  ->  (1, 2, 501)中国标准时间 2021-08-29 04:10:12  ->  (1, 2, 501)中国标准时间 2021-08-29 04:13:36  ->  (1, 2, 501)中国标准时间 2021-08-29 04:15:35  ->  (1, 2, 501)

'''