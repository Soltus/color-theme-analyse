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
    if os.name == 'posix':
        args = shlex.split(f"pip3 install color-theme-analyse[base]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30 && exit")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
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

def reinstallDev():
    '''
    仅用于调试
    '''
    inti()
    if os.name == 'posix':
        args = shlex.split(f"pip3 install color-theme-analyse[dev]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
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

def reinstallMerge():
    '''
    仅用于调试
    '''
    inti()
    if os.name == 'posix':
        args = shlex.split(f"pip3 install color-theme-analyse[merge]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30 && exit")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallMerge.ps1")).replace('\\','/')
        exec = os.path.dirname(python)
        args = shlex.split(r"PowerShell -noprofile Set-ExecutionPolicy AllSigned;clear;exit")
        p0 = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0)
        p0.wait()
        # args = shlex.split(f"PowerShell -noprofile Remove-item {bat};cls;exit")
        # p1 = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0)
        # p1.wait()
        f = open(bat, 'w')
        f.write(f'$vbs = New-Object -ComObject WScript.Shell;$repo=$vbs.popup("当前进程绑定的 Pyhton 路径位于 {python}\n请确认与项目的宿主 Python 一致。\n重装依赖包可能会导致不可控的影响，请慎重。",$null,"是否重装所有额外依赖包？",1);\
if($repo -eq 1){{cd "{exec}";.\\python -m pip install color-theme-analyse[merge]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30;clear;"Press Enter to exit.\n按回车键退出" ;[Console]::Readkey() | Out-Null ;Exit ;}}else{{exit;}}')

        '''
Const wshOKDialg = 0
Const wshOKCancelDialog = 1
Const wshAbortRetryIgnoreDialog = 2
Const wshYesNoCancelDialog = 3
Const wshYesNoDialog = 4
Const wshRetryCancelDialog = 5
Const wshStopMark = 16
Const wshQuestionMark = 32
Const wshExclamationMark = 48
Const wshInformationMark = 64
---------------------
Const wshOK = 1
Const wshCancel = 2
Const wshAbort = 3
Const wshRetry = 4
Const wshIngore = 5
Const wshYes = 6
Const wshNo = 7
Const wshDefault = -1
        '''
    except Exception as e:
        traceback.print_exc()
        raise e
    # command = os.path.abspath(os.path.join(_path,"reinstallMerge.vbs"))
    args = shlex.split(f"PowerShell -noprofile {bat}")
    p2 = Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0)
    exit()

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