# __version__ = "0.0.1"
from importlib.metadata import version as Version, PackageNotFoundError

try:
    __version__ = Version("MMCQsc") # if installed
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-30 01:06:59  ->  1.3.1
中国标准时间 2021-11-03 16:26:25  ->  1.3.266
中国标准时间 2022-03-14 21:07:18  ->  1.3.268
中国标准时间 2022-03-14 21:40:20  ->  1.3.302
中国标准时间 2022-03-14 21:51:53  ->  1.3.320
中国标准时间 2022-03-14 22:43:32  ->  1.3.520
中国标准时间 2022-03-15 02:05:14  ->  1.4.001
中国标准时间 2022-03-15 02:06:22  ->  1.4.101
中国标准时间 2022-03-15 15:29:59  ->  1.5.1
中国标准时间 2022-03-15 16:37:18  ->  1.31.1
中国标准时间 2022-03-15 16:39:07  ->  1.32.1
中国标准时间 2022-03-15 16:39:56  ->  1.33.1
中国标准时间 2022-03-15 16:40:06  ->  1.34.1
中国标准时间 2022-03-15 16:40:27  ->  1.34.1
中国标准时间 2022-03-15 16:40:47  ->  1.35.1
中国标准时间 2022-03-15 16:40:57  ->  1.36.1
中国标准时间 2022-03-15 16:41:59  ->  1.36.1
中国标准时间 2022-03-15 16:42:10  ->  1.37.1
中国标准时间 2022-03-15 16:42:28  ->  1.37.1
中国标准时间 2022-03-15 16:42:39  ->  1.38.1
中国标准时间 2022-03-15 16:55:24  ->  1.38.1
中国标准时间 2022-03-15 16:55:47  ->  1.39.1
中国标准时间 2022-03-15 16:56:06  ->  1.40.1
中国标准时间 2022-03-15 16:57:23  ->  1.41.1中国标准时间 2022-03-15 17:01:38  ->  1.42.1中国标准时间 2022-03-15 17:07:45  ->  1.45.1中国标准时间 2022-03-19 21:47:22  ->  1.47.1中国标准时间 2022-03-19 21:47:44  ->  1.48.1中国标准时间 2022-03-19 21:51:55  ->  1.49.1中国标准时间 2022-03-19 21:52:15  ->  1.49.1中国标准时间 2022-03-19 21:54:48  ->  1.50.1中国标准时间 2022-03-19 21:57:41  ->  1.51.1中国标准时间 2022-03-19 22:02:58  ->  1.52.1中国标准时间 2022-03-19 22:05:10  ->  1.53.1中国标准时间 2022-03-19 22:18:26  ->  1.54.1中国标准时间 2022-03-19 22:21:00  ->  1.55.1中国标准时间 2022-03-19 22:29:08  ->  1.56.1中国标准时间 2022-03-19 22:30:57  ->  1.57.1中国标准时间 2022-03-19 22:35:28  ->  1.58.1中国标准时间 2022-03-19 22:41:23  ->  1.5.1中国标准时间 2022-03-19 22:43:59  ->  1.5.1中国标准时间 2022-03-19 22:44:33  ->  1.5.1中国标准时间 2022-03-19 23:23:15  ->  1.61.1中国标准时间 2022-03-19 23:26:18  ->  1.62.1

'''