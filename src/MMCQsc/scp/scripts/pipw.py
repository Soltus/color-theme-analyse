import os,sys
import traceback
import shlex
from subprocess import Popen
base_list = ['numpy','pillow','rich']
dev_list = ['wheel','twine','setuptools','setuptools_scm','setuptools_scm_git_archive','Eel','auto-py-to-exe']
merge_list = base_list + dev_list

def inti(exec=''):
    from MMCQsc.version import version
    global my_v
    global _index_url
    global python
    global python_u
    global pyS
    global _path
    my_v = version
    _index_url = '--trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple'
    _path = os.path.abspath(os.path.dirname(__file__))
    if exec == '':
        python_u = os.path.abspath(sys.executable)
        python = os.path.abspath(sys.executable).replace('\\','/')
        pyS = os.path.abspath(os.path.join(os.path.dirname(python),'Scripts')).replace('\\','/')
    else:
        python_u = os.path.abspath(exec)
        python = os.path.abspath(exec).replace('\\','/')
        pyS = os.path.abspath(os.path.join(os.path.dirname(python),'Scripts')).replace('\\','/')
    _pip = os.path.abspath(os.path.join(pyS,'pip.exe'))
    __pip = os.path.abspath(os.path.join(os.path.dirname(python),'pip.exe'))
    if os.path.exists(_pip):
        pass
    elif os.path.exists(__pip):
        print(__pip)
        pyS = os.path.dirname(python) # Maybe Pycharm V env
    elif os.name == 'posix':
        pyS = os.path.dirname(python)
    else:
        raise



def reinstallBase(exec=''):
    '''
    仅用于调试
    '''
    uninstall_base(exec)
    inti(exec)
    if os.name == 'posix':
        args = shlex.split(f"pip3 install color-theme-analyse[base]=={my_v} --force-reinstall {_index_url}  --timeout 30")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallBase.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[base]=={my_v} --force-reinstall {_index_url}  --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    args = shlex.split(f"PowerShell -noprofile ./reinstallBase.vbs")
    with Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0):
        exit()

def reinstallDev(exec=''):
    '''
    仅用于调试
    '''
    uninstall_dev(exec)
    inti(exec)
    if os.name == 'posix':
        args = shlex.split(f"pip3 install color-theme-analyse[dev]=={my_v} --force-reinstall {_index_url}  --timeout 30")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallDev.bat"))
        f = open(bat, 'w')
        f.write(f"{python} -m pip install color-theme-analyse[dev]=={my_v} --force-reinstall {_index_url}  --timeout 30")
    except Exception as e:
        traceback.print_exc()
        raise e
    args = shlex.split(f"PowerShell -noprofile ./reinstallDev.vbs")
    with Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0):
        exit()

def reinstallMerge(exec='',full=False):
    '''
    仅用于调试
    '''
    inti(exec)
    _cwd = os.path.dirname(python)
    if os.name == 'posix':
        args = shlex.split(f"pip3 install color-theme-analyse[merge]=={my_v} --force-reinstall {_index_url}  --timeout 30 --ignore-installed")
        with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0) as p:
            exit()
    with os.popen(f"\"{python_u}\" -m pip freeze") as p:
        _r0 = p.read()
    uninstallMerge(exec)
    with os.popen(f"\"{python}\" -m pip freeze") as p:
        _r1 = p.read()
    diff_list = list(set(_r0.split()) - set(_r1.split()))
    fr_path = os.path.abspath(os.path.join(_cwd,"r_color_theme_analyse.txt"))
    # print(f'\n{fr_path}\n')
    fr = open(fr_path,"w",encoding='utf16')
    if full == False:
        fr.write('\n'.join(diff_list))
    else:
        fr.write('\n'.join(merge_list))
    fr.close()
    # urllib3 cffi 可能会导致安装失败
    try:
        bat = os.path.abspath(os.path.join(_path,"reinstallMerge.vbs")).replace('\\','/')
        sp_sp = '-' * 20
        f = open(bat, 'w',encoding='utf16')
        f.write(f'''cwd = CreateObject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
Set shell = CreateObject("Shell.Application")
command = "cd '{_cwd}';try{{'';'  安装清单如下：';'{sp_sp}';Get-Content '{fr_path}';'{sp_sp}';'';$vv = Read-Host '  需要绑定 color-theme-analyse 版本号（当前的默认值为 {my_v}），请输入';if($vv -eq ''){{$vv = '{my_v}'}};.\\python -m pip install setuptools {_index_url};.\\python -m pip install -r '{fr_path}' {_index_url} --timeout 30;.\\python -m pip install color-theme-analyse==$vv --force-reinstall {_index_url} --timeout 30}}catch{{Write-Warning $_}}finally{{Remove-Item '{fr_path}';'';.\\python -m pip list;'';'';'  Press Enter to exit.';'';'  回车键退出';[Console]::Readkey() | Out-Null ;Exit}}"
answer=MsgBox("当前进程绑定的 Pyhton 路径位于 {python}" & vbCrLf & "请确认与项目的宿主 Python 一致。（请不要绑定 Pycharm 的虚拟环境）" & vbCrLf & "重装依赖包可能会导致不可控的影响，请慎重。",65,"是否重装所有额外依赖包？")
if  answer = vbOK then
    Call shell.ShellExecute("powershell",command,"","",3)
End if
set fso = createobject("scripting.filesystemobject")
f = fso.deletefile(wscript.scriptname)
''')  # setuptools 对一些包的安装是必须的，因此首先安装她

    except Exception as e:
        traceback.print_exc()
        raise e

    args = shlex.split(f"PowerShell -noprofile ./reinstallMerge.vbs")
    with Popen(args, bufsize=-1, close_fds=False, shell=False, env=None,cwd=_path, startupinfo=None, creationflags=0):
        exit()

def uninstall_base(exec=''):
    inti(exec)
    for i in base_list:
        if os.name == 'posix':
            args = shlex.split(f"pip3 uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()
        else:
            args = shlex.split(f"'{python_u}' -m pip uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()
        # os.system(f"{python.replace('\\','/')} -m pip uninstall {i} -y")

def uninstall_dev(exec=''):
    inti(exec)
    for i in dev_list:
        if os.name == 'posix':
            args = shlex.split(f"pip3 uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()
        else:
            args = shlex.split(f"'{python_u}' -m pip uninstall {i} -y")
            result = Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=pyS, startupinfo=None, creationflags=0)
            result.wait()

def uninstallMerge(exec=''):
    '''
    仅用于调试
    '''
    uninstall_base(exec)
    uninstall_dev(exec)