# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 04:27:34  ->  (1, 2, 504)中国标准时间 2021-08-29 04:31:33  ->  (1, 2, 506)中国标准时间 2021-08-29 04:32:46  ->  (1, 2, 508)中国标准时间 2021-08-29 04:34:12  ->  (1, 2, 510)中国标准时间 2021-08-29 04:34:52  ->  (1, 2, 512)中国标准时间 2021-08-29 04:42:09  ->  (1, 2, 514)中国标准时间 2021-08-29 04:43:02  ->  (1, 2, 516)

'''