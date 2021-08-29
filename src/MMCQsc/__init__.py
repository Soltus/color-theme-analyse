# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 05:44:05  ->  (1, 2, 561)中国标准时间 2021-08-29 05:45:07  ->  (1, 2, 563)中国标准时间 2021-08-29 05:45:20  ->  (1, 2, 565)中国标准时间 2021-08-29 05:56:36  ->  (1, 2, 565)中国标准时间 2021-08-29 05:56:50  ->  (1, 2, 565)中国标准时间 2021-08-29 06:00:20  ->  (1, 2, 565)中国标准时间 2021-08-29 06:02:41  ->  (1, 2, 565)中国标准时间 2021-08-29 06:03:44  ->  (1, 2, 565)中国标准时间 2021-08-29 06:04:26  ->  (1, 2, 565)中国标准时间 2021-08-29 06:05:04  ->  (1, 2, 565)中国标准时间 2021-08-29 06:05:25  ->  (1, 2, 565)中国标准时间 2021-08-29 06:05:56  ->  (1, 2, 565)中国标准时间 2021-08-29 06:09:05  ->  (1, 2, 565)中国标准时间 2021-08-29 13:11:05  ->  (1, 2, 565)中国标准时间 2021-08-29 13:22:59  ->  (1, 2, 565)中国标准时间 2021-08-29 13:26:18  ->  (1, 2, 565)中国标准时间 2021-08-29 13:36:44  ->  (1, 2, 565)中国标准时间 2021-08-29 13:39:18  ->  (1, 2, 565)中国标准时间 2021-08-29 14:47:26  ->  (1, 2, 565)中国标准时间 2021-08-29 14:49:03  ->  (1, 2, 565)中国标准时间 2021-08-29 15:07:05  ->  (1, 2, 565)中国标准时间 2021-08-29 15:08:09  ->  (1, 2, 565)中国标准时间 2021-08-29 15:09:06  ->  (1, 2, 565)中国标准时间 2021-08-29 15:11:12  ->  (1, 2, 565)中国标准时间 2021-08-29 15:12:04  ->  (1, 2, 565)中国标准时间 2021-08-29 15:12:48  ->  (1, 2, 565)中国标准时间 2021-08-29 15:14:23  ->  (1, 2, 565)中国标准时间 2021-08-29 15:23:16  ->  (1, 2, 565)中国标准时间 2021-08-29 15:23:50  ->  (1, 2, 565)中国标准时间 2021-08-29 15:28:48  ->  (1, 2, 565)中国标准时间 2021-08-29 15:33:24  ->  (1, 2, 565)中国标准时间 2021-08-29 15:34:16  ->  (1, 2, 565)中国标准时间 2021-08-29 15:37:40  ->  (1, 2, 565)中国标准时间 2021-08-29 15:42:01  ->  (1, 2, 565)中国标准时间 2021-08-29 15:43:49  ->  (1, 2, 565)中国标准时间 2021-08-29 15:57:53  ->  (1, 2, 565)中国标准时间 2021-08-29 15:59:21  ->  (1, 2, 565)中国标准时间 2021-08-29 15:59:47  ->  (1, 2, 565)中国标准时间 2021-08-29 16:00:50  ->  (1, 2, 565)中国标准时间 2021-08-29 16:06:27  ->  (1, 2, 565)中国标准时间 2021-08-29 16:06:46  ->  (1, 2, 565)中国标准时间 2021-08-29 16:07:35  ->  (1, 2, 565)中国标准时间 2021-08-29 16:08:39  ->  (1, 2, 565)中国标准时间 2021-08-29 16:10:41  ->  (1, 2, 565)中国标准时间 2021-08-29 16:11:35  ->  (1, 2, 565)中国标准时间 2021-08-29 16:12:03  ->  (1, 2, 565)中国标准时间 2021-08-29 16:12:27  ->  (1, 2, 565)中国标准时间 2021-08-29 17:41:48  ->  1.2.564.dev8中国标准时间 2021-08-29 17:57:28  ->  1.2.600中国标准时间 2021-08-29 18:02:33  ->  1.2.601中国标准时间 2021-08-29 18:43:41  ->  1.2.622中国标准时间 2021-08-29 18:45:51  ->  1.2.622

'''