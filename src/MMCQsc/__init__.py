# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 19:27:57  ->  1.2.674中国标准时间 2021-08-29 19:30:36  ->  1.2.675中国标准时间 2021-08-29 19:30:36  ->  1.2.675中国标准时间 2021-08-29 19:32:31  ->  1.2.676中国标准时间 2021-08-29 19:32:31  ->  1.2.676中国标准时间 2021-08-29 19:33:01  ->  1.2.677中国标准时间 2021-08-29 19:33:01  ->  1.2.677中国标准时间 2021-08-29 19:35:08  ->  1.2.678中国标准时间 2021-08-29 19:35:18  ->  1.2.679

'''