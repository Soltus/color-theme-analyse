# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 05:20:49  ->  (1, 2, 547)中国标准时间 2021-08-29 05:21:30  ->  (1, 2, 547)中国标准时间 2021-08-29 05:25:47  ->  (1, 2, 547)中国标准时间 2021-08-29 05:26:16  ->  (1, 2, 550)中国标准时间 2021-08-29 05:36:16  ->  (1, 2, 553)中国标准时间 2021-08-29 05:42:01  ->  (1, 2, 556)中国标准时间 2021-08-29 05:43:26  ->  (1, 2, 559)中国标准时间 2021-08-29 05:44:05  ->  (1, 2, 561)

'''