# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 05:44:05  ->  (1, 2, 561)中国标准时间 2021-08-29 05:45:07  ->  (1, 2, 563)中国标准时间 2021-08-29 05:45:20  ->  (1, 2, 565)中国标准时间 2021-08-29 05:56:36  ->  (1, 2, 565)中国标准时间 2021-08-29 05:56:50  ->  (1, 2, 565)中国标准时间 2021-08-29 06:00:20  ->  (1, 2, 565)中国标准时间 2021-08-29 06:02:41  ->  (1, 2, 565)中国标准时间 2021-08-29 06:03:44  ->  (1, 2, 565)中国标准时间 2021-08-29 06:04:26  ->  (1, 2, 565)中国标准时间 2021-08-29 06:05:04  ->  (1, 2, 565)中国标准时间 2021-08-29 06:05:25  ->  (1, 2, 565)中国标准时间 2021-08-29 06:05:56  ->  (1, 2, 565)中国标准时间 2021-08-29 06:09:05  ->  (1, 2, 565)中国标准时间 2021-08-29 13:11:05  ->  (1, 2, 565)中国标准时间 2021-08-29 13:22:59  ->  (1, 2, 565)中国标准时间 2021-08-29 13:26:18  ->  (1, 2, 565)中国标准时间 2021-08-29 13:36:44  ->  (1, 2, 565)中国标准时间 2021-08-29 13:39:18  ->  (1, 2, 565)中国标准时间 2021-08-29 14:47:26  ->  (1, 2, 565)中国标准时间 2021-08-29 14:49:03  ->  (1, 2, 565)中国标准时间 2021-08-29 15:07:05  ->  (1, 2, 565)中国标准时间 2021-08-29 15:08:09  ->  (1, 2, 565)中国标准时间 2021-08-29 15:09:06  ->  (1, 2, 565)中国标准时间 2021-08-29 15:11:12  ->  (1, 2, 565)中国标准时间 2021-08-29 15:12:04  ->  (1, 2, 565)

'''