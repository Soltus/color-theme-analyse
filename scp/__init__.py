import os,sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

from scp.lib.logger import *
from scp.lib.error_sc import *
logger = myLogging("gitee.com/soltus")