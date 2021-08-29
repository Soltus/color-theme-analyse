# __version__ = "0.0.1"
from importlib.metadata import version as Version, PackageNotFoundError

try:
    __version__ = Version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 21:18:38  ->  1.2.833
中国标准时间 2021-08-29 21:19:16  ->  1.2.843
中国标准时间 2021-08-29 21:19:43  ->  1.2.844
中国标准时间 2021-08-29 21:20:24  ->  1.2.854
中国标准时间 2021-08-29 21:26:24  ->  1.2.846
中国标准时间 2021-08-29 21:26:58  ->  1.2.846
中国标准时间 2021-08-29 21:27:26  ->  1.2.846
中国标准时间 2021-08-29 21:28:16  ->  1.2.846
中国标准时间 2021-08-29 21:29:10  ->  1.2.846
中国标准时间 2021-08-29 21:30:05  ->  1.2.846
中国标准时间 2021-08-29 21:33:00  ->  1.2.846
中国标准时间 2021-08-29 21:34:52  ->  1.2.846
中国标准时间 2021-08-29 21:35:53  ->  1.2.846
中国标准时间 2021-08-29 21:37:11  ->  1.2.846
中国标准时间 2021-08-29 21:59:34  ->  1.2.856
中国标准时间 2021-08-29 22:00:35  ->  1.2.848
中国标准时间 2021-08-29 22:01:27  ->  1.2.848
中国标准时间 2021-08-29 22:02:05  ->  1.2.850
中国标准时间 2021-08-29 22:02:50  ->  1.2.850
中国标准时间 2021-08-29 22:03:26  ->  1.2.852
中国标准时间 2021-08-29 22:03:49  ->  1.2.852
中国标准时间 2021-08-29 22:04:16  ->  1.2.862
中国标准时间 2021-08-29 22:05:28  ->  1.2.854
中国标准时间 2021-08-29 22:05:36  ->  1.2.854
中国标准时间 2021-08-29 22:05:46  ->  1.2.864
中国标准时间 2021-08-29 22:06:14  ->  1.2.856
中国标准时间 2021-08-29 22:07:03  ->  1.2.856
中国标准时间 2021-08-29 22:07:47  ->  1.2.856
中国标准时间 2021-08-29 22:10:28  ->  1.2.856
中国标准时间 2021-08-29 22:12:00  ->  1.2.858
中国标准时间 2021-08-29 22:12:42  ->  1.2.858
中国标准时间 2021-08-29 22:12:52  ->  1.2.860
中国标准时间 2021-08-29 22:13:42  ->  1.2.860
中国标准时间 2021-08-29 22:13:51  ->  1.2.862
中国标准时间 2021-08-29 22:14:02  ->  1.2.862
中国标准时间 2021-08-29 22:15:28  ->  1.2.872
中国标准时间 2021-08-29 22:15:36  ->  1.2.864
中国标准时间 2021-08-29 22:16:12  ->  1.2.864
中国标准时间 2021-08-29 22:16:22  ->  1.2.866
中国标准时间 2021-08-29 22:17:37  ->  1.2.868
中国标准时间 2021-08-29 22:17:51  ->  1.2.868
中国标准时间 2021-08-29 22:20:42  ->  1.2.870
中国标准时间 2021-08-29 22:21:34  ->  1.2.870
中国标准时间 2021-08-29 22:22:05  ->  1.2.872
中国标准时间 2021-08-29 22:22:51  ->  1.2.872
中国标准时间 2021-08-29 22:22:59  ->  1.2.874
中国标准时间 2021-08-29 22:23:30  ->  1.2.876
中国标准时间 2021-08-29 22:24:16  ->  1.2.876
中国标准时间 2021-08-29 22:25:07  ->  1.2.878
中国标准时间 2021-08-29 22:30:26  ->  1.2.880
中国标准时间 2021-08-29 22:31:20  ->  1.2.880
中国标准时间 2021-08-29 22:32:04  ->  1.2.882
中国标准时间 2021-08-29 22:32:25  ->  1.2.884
中国标准时间 2021-08-29 22:33:00  ->  1.2.884
中国标准时间 2021-08-29 22:33:40  ->  1.2.886
中国标准时间 2021-08-29 22:40:41  ->  1.2.896
中国标准时间 2021-08-29 22:48:35  ->  1.2.902
中国标准时间 2021-08-29 23:49:10  ->  1.2.906
中国标准时间 2021-08-29 23:50:36  ->  1.2.907
中国标准时间 2021-08-29 23:51:09  ->  1.2.908
中国标准时间 2021-08-29 23:55:03  ->  1.2.910
中国标准时间 2021-08-29 23:58:40  ->  1.2.453
中国标准时间 2021-08-30 00:01:36  ->  1.2.453
中国标准时间 2021-08-30 00:03:03  ->  1.2.453
中国标准时间 2021-08-30 00:03:56  ->  1.2.453
中国标准时间 2021-08-30 00:07:02  ->  1.2.922
中国标准时间 2021-08-30 00:16:42  ->  1.2.923
中国标准时间 2021-08-30 00:17:59  ->  1.2.923
中国标准时间 2021-08-30 00:21:10  ->  1.2.923
中国标准时间 2021-08-30 00:21:54  ->  1.2.924
中国标准时间 2021-08-30 00:36:02  ->  1.2.925
中国标准时间 2021-08-30 00:36:47  ->  1.2.926
中国标准时间 2021-08-30 00:37:18  ->  1.2.928
中国标准时间 2021-08-30 00:37:47  ->  1.2.929
中国标准时间 2021-08-30 00:38:15  ->  1.2.931
中国标准时间 2021-08-30 00:38:36  ->  1.2.932
中国标准时间 2021-08-30 00:39:19  ->  1.2.935
中国标准时间 2021-08-30 00:39:44  ->  1.2.936
中国标准时间 2021-08-30 00:40:12  ->  1.2.938
中国标准时间 2021-08-30 00:40:59  ->  1.2.948
中国标准时间 2021-08-30 00:41:38  ->  1.2.950
中国标准时间 2021-08-30 00:42:05  ->  1.2.960
中国标准时间 2021-08-30 00:43:06  ->  1.2.962中国标准时间 2021-08-30 00:46:05  ->  1.2.972中国标准时间 2021-08-30 00:55:11  ->  1.2.974中国标准时间 2021-08-30 00:55:29  ->  1.2.984

'''