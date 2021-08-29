# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    from .version import __version__, version

__doc__ = f'''

___________  build history  ____________

中国标准时间 2021-08-29 18:45:51  ->  1.2.622中国标准时间 2021-08-29 18:53:50  ->  1.2.662中国标准时间 2021-08-29 18:53:50  ->  1.2.662中国标准时间 2021-08-29 18:56:37  ->  1.2.662中国标准时间 2021-08-29 18:56:37  ->  1.2.662中国标准时间 2021-08-29 18:57:05  ->  1.2.662中国标准时间 2021-08-29 18:57:05  ->  1.2.662中国标准时间 2021-08-29 18:57:43  ->  1.2.662中国标准时间 2021-08-29 18:57:43  ->  1.2.662

'''