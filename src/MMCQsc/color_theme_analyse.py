import os,sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

if root_path not in sys.path:
    sys.path.append(root_path)
from . import hello_soltus

if __name__ == '__main__':
    from scp import executable_check
    from scp import main
    result = main.mainFunc()
