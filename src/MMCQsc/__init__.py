# __version__ = "0.0.1"
from importlib.metadata import version as Version, PackageNotFoundError

try:
    __version__ = Version("MMCQsc") # if installed
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-30 01:06:59  ->  1.3.1中国标准时间 2021-08-30 01:09:55  ->  1.3.13中国标准时间 2021-08-30 01:11:20  ->  1.3.15中国标准时间 2021-08-30 01:13:42  ->  1.3.25中国标准时间 2021-08-30 01:14:44  ->  1.3.27中国标准时间 2021-08-30 01:15:49  ->  1.3.37

'''