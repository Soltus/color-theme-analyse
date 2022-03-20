import os,sys
import traceback
import shlex
from subprocess import Popen
from MMCQsc.version import version
my_v = version
python = os.path.abspath(sys.executable).replace('\\','/')
_path = os.path.abspath(os.path.dirname(__file__))
def reinstallBase():
    '''
    仅用于调试
    '''
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallBase.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[base]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    args = shlex.split(f"PowerShell ./reinstallBase.vbs")
    result = Popen(args, bufsize=0, close_fds=False, shell=True, env=None,cwd=_path, startupinfo=None, creationflags=0)
    exit()
    os.system(f"pip install color-theme-analyse[base]=={my_v} -i https://mirrors.tencent.com/pypi/simple --force-reinstall --user")

def reinstallDev():
    '''
    仅用于调试
    '''
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallDev.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[dev]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    args = shlex.split(f"PowerShell ./reinstallDev.vbs")
    result = Popen(args, bufsize=0, close_fds=False, shell=True, env=None,cwd=_path, startupinfo=None, creationflags=0)
    exit()
    os.system(f"pip install color-theme-analyse[dev]=={my_v} -i https://mirrors.tencent.com/pypi/simple --force-reinstall --user")

def reinstallMerge():
    '''
    仅用于调试
    '''
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallMerge.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[merge]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    args = shlex.split(f"PowerShell ./reinstallMerge.vbs")
    result = Popen(args, bufsize=0, close_fds=False, shell=True, env=None,cwd=_path, startupinfo=None, creationflags=0)
    exit()
    os.system(f"pip install color-theme-analyse[merge]=={my_v} -i https://mirrors.tencent.com/pypi/simple --force-reinstall --user")

def uninstall_base():
    os.system("pip uninstall numpy -y")
    os.system("pip uninstall pillow -y")
    os.system("pip uninstall rich -y")

def uninstall_dev():
    os.system("pip uninstall wheel -y")
    os.system("pip uninstall twine -y")
    os.system("pip uninstall pyinstaller -y")
    os.system("pip uninstall setuptools -y")
    os.system("pip uninstall setuptools_scm -y")
    os.system("pip uninstall setuptools_scm_git_archive -y")

def uninstallMerge():
    '''
    仅用于调试
    '''
    uninstall_base()
    uninstall_dev()