# __version__ = "0.0.1"
from importlib.metadata import version as Version, PackageNotFoundError

try:
    __version__ = Version("MMCQsc") # if installed
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-30 01:06:59  ->  1.3.1中国标准时间 2021-08-30 01:09:55  ->  1.3.13中国标准时间 2021-08-30 01:11:20  ->  1.3.15中国标准时间 2021-08-30 01:13:42  ->  1.3.25中国标准时间 2021-08-30 01:14:44  ->  1.3.27中国标准时间 2021-08-30 01:15:49  ->  1.3.37中国标准时间 2021-08-30 01:16:33  ->  1.3.39中国标准时间 2021-08-30 01:17:31  ->  1.3.49中国标准时间 2021-08-30 01:18:31  ->  1.3.51中国标准时间 2021-08-30 01:20:56  ->  1.3.61中国标准时间 2021-08-30 01:21:59  ->  1.3.63中国标准时间 2021-08-30 01:27:23  ->  1.3.73中国标准时间 2021-08-30 01:28:34  ->  1.3.75中国标准时间 2021-08-30 01:29:45  ->  1.3.85中国标准时间 2021-08-30 01:32:24  ->  1.3.87中国标准时间 2021-08-30 01:36:52  ->  1.3.97中国标准时间 2021-08-30 01:38:03  ->  1.3.99中国标准时间 2021-08-30 01:40:16  ->  1.3.109中国标准时间 2021-08-30 01:43:39  ->  1.3.111中国标准时间 2021-08-30 01:47:59  ->  1.3.121中国标准时间 2021-08-30 01:49:08  ->  1.3.133中国标准时间 2021-08-30 01:50:12  ->  1.3.145中国标准时间 2021-08-30 01:50:46  ->  1.3.157中国标准时间 2021-08-30 01:51:17  ->  1.3.169中国标准时间 2021-08-30 01:58:07  ->  1.3.181中国标准时间 2021-08-30 02:00:05  ->  1.3.193中国标准时间 2021-08-30 02:03:18  ->  1.3.205中国标准时间 2021-08-30 18:33:09  ->  1.3.217中国标准时间 2021-08-30 18:35:37  ->  1.3.229中国标准时间 2021-11-03 16:24:20  ->  1.3.242中国标准时间 2021-11-03 16:25:13  ->  1.3.254中国标准时间 2021-11-03 16:26:25  ->  1.3.266中国标准时间 2022-03-14 21:07:18  ->  1.3.268中国标准时间 2022-03-14 21:16:05  ->  1.3.268中国标准时间 2022-03-14 21:16:47  ->  1.3.268中国标准时间 2022-03-14 21:20:40  ->  1.3.268中国标准时间 2022-03-14 21:25:21  ->  1.3.268中国标准时间 2022-03-14 21:27:26  ->  1.3.268中国标准时间 2022-03-14 21:31:25  ->  1.3.302中国标准时间 2022-03-14 21:40:20  ->  1.3.302中国标准时间 2022-03-14 21:51:53  ->  1.3.320中国标准时间 2022-03-14 22:01:20  ->  1.3.330中国标准时间 2022-03-14 22:03:11  ->  1.3.330中国标准时间 2022-03-14 22:03:52  ->  1.3.330中国标准时间 2022-03-14 22:05:32  ->  1.3.330中国标准时间 2022-03-14 22:06:45  ->  1.3.330中国标准时间 2022-03-14 22:07:04  ->  1.3.330中国标准时间 2022-03-14 22:08:41  ->  1.3.330中国标准时间 2022-03-14 22:09:19  ->  1.3.330中国标准时间 2022-03-14 22:10:56  ->  1.3.330中国标准时间 2022-03-14 22:12:20  ->  1.3.400中国标准时间 2022-03-14 22:16:39  ->  1.3.500

'''