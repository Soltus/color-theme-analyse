import os,sys
import traceback
import shlex
from subprocess import Popen
def inti(exec=''):
    from MMCQsc.version import version
    global my_v
    global python
    global pyS
    global _path
    my_v = version
    _path = os.path.abspath(os.path.dirname(__file__))
    if exec == '':
        python = os.path.abspath(sys.executable).replace('\\','/')
        pyS = os.path.abspath(os.path.join(os.path.dirname(python),'Scripts')).replace('\\','/')
    else:
        python = os.path.abspath(exec).replace('\\','/')
        pyS = os.path.abspath(os.path.join(os.path.dirname(python),'Scripts')).replace('\\','/')


def reinstallBase(exec=''):
    '''
    仅用于调试
    '''
    uninstall_base(exec)
    inti(exec)
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

def reinstallDev(exec=''):
    '''
    仅用于调试
    '''
    # uninstall_dev(exec)
    inti(exec)
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

def reinstallMerge(exec=''):
    '''
    仅用于调试
    '''
    # uninstallMerge(exec)
    inti(exec)
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
command = "cd '{pyS}';try{{'';'';$vv = Read-Host '需要绑定 color-theme-analyse 版本号（当前的默认值为 {my_v}），请输入';if($vv -eq ''){{$vv = '{my_v}'}};.\\pip install color-theme-analyse[merge]==$vv --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30}}catch{{Write-Warning $_}}finally{{'';'';'Press Enter to exit.';'';'回车键退出';[Console]::Readkey() | Out-Null ;Exit}}"
answer=MsgBox("当前进程绑定的 Pyhton 路径位于 {python}" & vbCrLf & "请确认与项目的宿主 Python 一致。" & vbCrLf & "重装依赖包可能会导致不可控的影响，请慎重。",65,"是否重装所有额外依赖包？")
if  answer = vbOK then
    Call shell.ShellExecute("powershell",command,"","",1)
End if
set fso = createobject("scripting.filesystemobject")
f = fso.deletefile(wscript.scriptname)
''')

    except Exception as e:
        traceback.print_exc()
        raise e

    args = shlex.split(f"PowerShell -noprofile ./reinstallMerge.vbs")
    p2 = Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0)
    exit()

def uninstall_base(exec=''):
    inti(exec)
    _list = ['numpy','pillow','rich']
    for i in _list:
        if os.name == 'posix':
            args = shlex.split(f"pip3 uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()
        else:
            args = shlex.split(f"PowerShell -noprofile ./pip uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()
        # os.system(f"{python.replace('\\','/')} -m pip uninstall {i} -y")

def uninstall_dev(exec=''):
    inti(exec)
    _list = ['wheel','twine','auto-py-to-exe','setuptools','setuptools_scm','setuptools_scm_git_archive']
    for i in _list:
        if os.name == 'posix':
            args = shlex.split(f"pip3 uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()
        else:
            args = shlex.split(f"PowerShell -noprofile ./pip uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()

def uninstallMerge(exec=''):
    '''
    仅用于调试
    '''
    uninstall_base(exec)
    uninstall_dev(exec)