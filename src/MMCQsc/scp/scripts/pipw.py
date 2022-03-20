import os,sys
import traceback
import shlex
from subprocess import Popen
def inti():
    from MMCQsc.version import version
    global my_v
    global python
    global _path
    my_v = version
    python = os.path.abspath(sys.executable).replace('\\','/')
    _path = os.path.abspath(os.path.dirname(__file__))
    # os.environ["COMSPEC"] = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'

def reinstallBase():
    '''
    仅用于调试
    '''
    inti()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallBase.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[base]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    args = shlex.split(f"PowerShell -noprofile ./reinstallBase.vbs")
    result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0)
    exit()
    os.system(f"pip install color-theme-analyse[base]=={my_v} -i https://mirrors.tencent.com/pypi/simple --force-reinstall --user")

def reinstallDev():
    '''
    仅用于调试
    '''
    inti()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallDev.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[dev]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    args = shlex.split(f"PowerShell -noprofile ./reinstallDev.vbs")
    result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0)
    exit()
    os.system(f"pip install color-theme-analyse[dev]=={my_v} -i https://mirrors.tencent.com/pypi/simple --force-reinstall --user")

def reinstallMerge():
    '''
    仅用于调试
    '''
    inti()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallMerge.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[merge]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    # command = os.path.abspath(os.path.join(_path,"reinstallMerge.vbs"))
    args = shlex.split("cmd PowerShell -noprofile ./reinstallMerge.vbs")
    result = Popen(args, bufsize=0, close_fds=False, shell=False, env=os.environ,cwd=_path, startupinfo=None, creationflags=0)
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