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
        args = shlex.split(f"pip3 install color-theme-analyse[base]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple  --timeout 30 --ignore-installed urllib3")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallBase.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[base]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple  --timeout 30 --ignore-installed urllib3")
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
        args = shlex.split(f"pip3 install color-theme-analyse[dev]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple  --timeout 30 --ignore-installed urllib3")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallDev.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[dev]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple  --timeout 30 --ignore-installed urllib3")
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
    # urllib3 可能会导致安装失败，因此忽略
    if os.name == 'posix':
        args = shlex.split(f"pip3 install color-theme-analyse[merge]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple  --timeout 30 --ignore-installed urllib3")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallMerge.vbs")).replace('\\','/')
        exec = os.path.dirname(python)

        f = open(bat, 'w',encoding='utf16')
        f.write(f'''cwd = CreateObject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
Set shell = CreateObject("Shell.Application")
command = "cd '{exec}';.\\python -m pip install color-theme-analyse[merge]=={my_v} --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30;'';'';'Press Enter to exit.';'';'回车键退出';[Console]::Readkey() | Out-Null ;Exit"
answer=MsgBox("当前进程绑定的 Pyhton 路径位于 {python}" & vbCrLf & "请确认与项目的宿主 Python 一致。" & vbCrLf & "重装依赖包可能会导致不可控的影响，请慎重。",65,"是否重装所有额外依赖包？")
if  answer = vbOK then
    shell.ShellExecute "powershell",command,"","",1
End if
''')

    except Exception as e:
        traceback.print_exc()
        raise e
    # command = os.path.abspath(os.path.join(_path,"reinstallMerge.vbs"))
    args = shlex.split(f"PowerShell -noprofile ./reinstallMerge.vbs")
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