# -*- coding=utf-8

# SCSD-PY001

# hi-windom/ColorThemeAnalyse

# https://gitee.com/hi-windom/color-theme-analyse

'''
# ---------------------------------
# 创建于    2021-7-20
# 更新于    2021-7-20 02:08:57
# ---------------------------------
# Need help ?  => 694357845@qq.com
# ---------------------------------
# 作者很懒，还没想好说些什么
# ---------------------------------
'''

################################################################
import os,sys
import json
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from MMCQsc.scp.lib.error_sc import *
from MMCQsc.scp.lib.logger import *
logger = myLogging("gitee.com/soltus")


def fun_version(v1,v2):
# v1 == v2 return 0
# v1 > v2 return 1
# v1 < v2 return -1

    l_1 = v1.split('.')
    l_2 = v2.split('.')
    c = 0
    while True:
        if c == len(l_1) and c == len(l_2):
            return 0
        if len(l_1) == c:
            l_1.append(0)
        if len(l_2) == c:
            l_2.append(0)
        if int(l_1[c]) > int(l_2[c]):
            return 1
        elif int(l_1[c]) < int(l_2[c]):
            return -1
        c += 1


os.system("cls")

file_path = sys.argv[0]
def check_conda():
    if "\\envs\\" in sys.executable:
        conda_exec = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "../..", "Script", "conda.exe"))
        conda_env = sys.executable.split("\\")[-2]
    else:
        conda_exec = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "Script", "conda.exe"))
        conda_env = "base"
    return conda_exec, conda_env


from subprocess import Popen
import shlex
import types

def get_dpkg(name):
    try:
        PKG_D = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg')).replace('\\','/')
        # python = sys.executable.replace(check_conda()[1],pick_env)
        # nexe = python.replace('\\','/')
        python = os.path.abspath(sys.executable).replace('\\','/')
        args = shlex.split(f"{python} -m pip install {name} --isolated --python-version 3.9 --ignore-requires-python --force-reinstall -t {PKG_D} -i https://pypi.douban.com/simple --extra-index-url https://pypi.mirrors.ustc.edu.cn --compile --timeout 30 --exists-action b --only-binary :all:")
        result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0)
        logger.debug(f"创建下载线程 PID: {result.pid}")
        logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
        result.wait()
        PKG_D = os.path.abspath(PKG_D)
        if PKG_D not in sys.path:
            sys.path.append(PKG_D)
        M_module = types.ModuleType(name)
        M_module.__file__ = os.path.abspath(os.path.join(PKG_D, name, '__init__.py'))
        M_module.__package__ = ''
        try:
            exec(f"import importlib,sys;sys.modules['{name}']=M_module;import {name};importlib.reload({name});importlib.invalidate_caches();importlib.util.resolve_name('{name}', __spec__.parent)",globals(), locals())
            # logger.info(M_module.__dict__)
            logger.info('\n' + str(M_module))
            logger.info(f"\n\n\timport {name} seccessfully\n\n")
        except Exception as e:
            logger.error(e)
            logger.error(f"从项目导入 {name} 失败 ")
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt):
            logger.warning("用户中止了下载")
            exit()

def run_in_env(env):
    PY3_VNO = ''
    for i in sys.version_info[:3]:
        PY3_VNO += str(i)
    PY3_VNO = '.'.join(PY3_VNO)
    os.system("cls")
    logger.info("开始检测 Conda 环境")
    if env == 'noconda':
        logger.info('尝试安装多个扩展包到项目 [ 如果不存在缓存，将从网络下载并安装 ]')
        get_dpkg('numpy')
        get_dpkg('rich')
        get_dpkg('Pillow')
        return env
    else:
        with os.popen("conda info --json") as CONDA_SYS:
            try:
                CONDA_JSON = json.loads(CONDA_SYS.read())
                _conda_location = CONDA_JSON["conda_location"]
                _conda_exe = CONDA_JSON["env_vars"]["CONDA_EXE"]
                _env_list = CONDA_JSON["envs"]
                _env_v = {}
            except Exception:
                logger.error('无法正确检测到 Conda 环境')
                logger.warning("如果你已经安装了 Conda ，请确保正确配置环境变量并完成 Conda init 初始化终端")
                return 'noconda'
            for e in _env_list:
                with os.popen("{}\\python.exe --version".format(e)) as repo:
                    _env_path = e.strip()
                    _env = '{}'.format(e).split('\\')[-1]
                    if '{}'.format(e).split('\\')[-2] == 'envs':
                        _env = '{}'.format(e).split('\\')[-1]
                    else:
                        _env = 'base'
                    _env_v[_env] = {}
                    _env_v[_env]['version'] = repo.read().strip()
                    _env_v[_env]['path'] = _env_path
                    if '3.9.' in _env_v[_env]['version']:
                        print('\n\t' + _env + '\t' + _env_v[_env]['version'] + '\t' + _env_path)
            print('\n\n')
            logger.info("已列出所有兼容的 Conda 环境")

            _env_pyp = os.path.abspath(os.path.join(_env_v[env]['path'],'Lib','site-packages'))
            if _env_pyp is not None:
                logger.debug("\n\n\n\t\t正在使用的 Python 解释器版本 {}\n\t\t正在使用的 Python 解释器路径 {}\n\n\n\t\t使用 Conda 环境 {} ({}) 导入 Numpy 并继续 (y) ？\n\n\t\t或者不导入 Conda 基础包并继续 (n) ？\n\t\t[ 如果项目路径不存在 Numpy ，将从网络下载并安装 ]\n\n\t\t也可以输入其他任意字符，选择其他 Conda 环境导入 Numpy (*)\n\n\t\tProccess ?  [Y/n/*]".format(PY3_VNO,sys.executable,env, _env_v[env]['version']))
        while True:
            try:
                pick_env = input("\n\nmain.py:93 >>> ")
            except BaseException as e:
                if isinstance(e, KeyboardInterrupt):
                    logger.warning("用户强制退出")
                    exit()
            if pick_env in ['Y','y']:
                vtemp = []
                vtemp.append(str(sys.version_info[0]))
                vtemp.append(str(sys.version_info[1]))
                if sys.version_info.major < 3:
                    logger.error(" Can NOT run in Python 2.x ")
                    raise EnvError('\n\n\t''This script is only for use with ''Python 3.6 or later\n\n\t https://gitee.com/hi-windomcolor-theme-analyse/ \n\n')
                elif sys.version_info[:3] < (3,6,0):
                    logger.error(" Can NOT run in Python < 3.6 ")
                    raise EnvError('\n\n\t''This script is only for use with ''Python 3.6 or later\n\n\t https://gitee.com/hi-windomcolor-theme-analyse/ \n\n')
                elif vtemp != PY3_VNO.split('.')[:2]:
                    logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                    logger.error(" 应当使用 Python == {}.{} 的 Conda 环境导入 Numpy".format(sys.version_info[0],sys.version_info[1]))
                    continue
                else:
                    if _env_pyp not in sys.path:
                        sys.path.append(_env_pyp)
                    M_numpy = types.ModuleType('numpy')
                    M_numpy.__file__ = os.path.abspath(os.path.join(_env_pyp,'numpy','__init__.py'))
                    M_numpy.__package__ = ''
                    try:
                        sys.modules['numpy'] = M_numpy
                        import importlib,numpy
                        importlib.reload(numpy)
                        importlib.invalidate_caches()
                        importlib.util.resolve_name('numpy', __spec__.parent)
                        print(M_numpy)
                        # print(M_numpy.__dict__)
                        logger.info("import numpy seccessfully")
                        get_dpkg('rich')
                    except:
                        logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                        logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                        logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                        continue
                    return env
            elif pick_env in ['N','n']:
                logger.info('尝试安装多个扩展包到项目 [ 如果不存在缓存，将从网络下载并安装 ]')
                get_dpkg('numpy')
                get_dpkg('rich')
                get_dpkg('Pillow')
                return env
            else:
                python = sys.executable.replace(check_conda()[1],pick_env)
                # print(python)
                os.system("cls")
                os.system("conda info -e")
                logger.debug("\n\n\n\t\t输入你想使用的 Conda 环境名称")
                pick_env = input("main.py:109 >>> ")
                _env_pyp = os.path.abspath(os.path.join(_env_v[pick_env]['path'],'Lib','site-packages'))
                if _env_pyp not in sys.path:
                        sys.path.append(_env_pyp)
                M_numpy = types.ModuleType('numpy')
                M_numpy.__file__ = os.path.abspath(os.path.join(_env_pyp,'numpy','__init__.py'))
                M_numpy.__package__ = ''
                try:
                    sys.modules['numpy'] = M_numpy
                    import importlib,numpy
                    importlib.reload(numpy)
                    importlib.invalidate_caches()
                    importlib.util.resolve_name('numpy', __spec__.parent)
                    # logger.info(M_numpy.__dict__)
                    logger.info('\n' + str(M_numpy))
                    logger.info("\n\n\timport numpy seccessfully\n\n")
                except:
                    logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                    logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                    logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                    continue
                return env
                logger.debug(f"请在终端执行指令 conda activate {pick_env} 手动激活环境")
                logger.warning("\n\n\t\t[ tip ] : 方向上键 ^ 可调出调出历史指令\n\n")
                exit()
                os.system("conda deactivate")
                os.system("deactivate")
                os.system("cls")
                python = sys.executable.replace(check_conda()[1],pick_env)
                change_env = file_path.replace('main','change_env')
                try:
                    args = shlex.split(f"conda create -n {pick_env} python==3.9.5 -y")
                    result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0)
                    logger.debug(f"创建下载线程 PID: {result.pid}")
                    logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
                    result.wait()
                except BaseException as e:
                    if isinstance(e, KeyboardInterrupt):
                        logger.warning("用户中止了下载")
                        logger.warning("当前窗口已完成使命，是时候和它告别了")
                        exit()
                #os.system(f"conda create -n {pick_env} python==3.9.5 -y")
                # args = shlex.split(f"conda activate {pick_env}")
                # result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0)
                logger.debug(check_conda()[0])
                logger.debug(python)
                logger.debug(file_path)
                logger.debug(f"已创建的环境 : [ {pick_env} ]  请使用创建的环境重新运行\n\n")
                logger.warning("\n\n\t\t[ tip ] : 方向上键 ^ 可调出调出历史指令\n\n")
                exit()
                return pick_env


logger.info('尝试使用缓存')
try:
    np = __import__('numpy', globals(), locals(), [], 0)
    rich = __import__('rich', globals(), locals(), [], 0)
except ImportError:
    try:
        from MMCQsc_dpkg import numpy as np
        from MMCQsc_dpkg import rich
        from MMCQsc_dpkg.PIL import Image as PImage
    except:
        if os.name == 'posix':
            pick_env = 'noconda'
        else:
            pick_env = check_conda()[1]
        while pick_env:
            env_tmep = pick_env
            pick_env = run_in_env(pick_env)
            if pick_env == env_tmep:
                break

        PY3_VNO = ''
        for i in sys.version_info[:3]:
                PY3_VNO += str(i)
        PY3_VNO = '.'.join(PY3_VNO)
        logger.warning("You are using Python {}".format(PY3_VNO))
        if fun_version(PY3_VNO,"3.8.0") == -1:
            logger.critical("Required version : Python >= 3.8.0")
            with os.popen("conda --version") as conda_v:
                if "conda" in conda_v.read():
                    logger.info("You are using Conda , Press key 'y' to upgrade your Python")
                    logger.info("If you want to upgrade later by yourself , use command: conda install python==3.9.5")
                    logger.debug("Upgrade your Python to 3.9.5 ?  [Y/*]")
                isupdate = input("main.py:123 >>> ")
            if isupdate not in ['Y','y']:
                exit()
            os.system("cls")
            logger.info("即将开始下载，这取决于你的网络")
            try:
                args = shlex.split(f"conda conda install python==3.9.5 -n {pick_env} -y")
                result = Popen(args, bufsize=0, executable=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", close_fds=False, shell=False, env=None, startupinfo=None, creationflags=0)
                logger.debug(f"创建下载线程 PID: {result.pid}")
                logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
                result.wait()
            except BaseException as e:
                if isinstance(e, KeyboardInterrupt):
                    logger.warning("用户中止了下载")
                    logger.warning("当前窗口已完成使命，是时候和它告别了")
                    result.kill()
            finally:
                if result.returncode:
                    logger.error("下载失败，请手动升级 Python 后重试")
                else:
                    args = [sys.executable, file_path]
                    logger.debug(args)
                    logger.debug(f"请在终端执行指令 conda activate {pick_env} 手动激活环境")
                    logger.warning("\n\n\t\t[ tip ] : 方向上键 ^ 可调出调出历史指令\n\n")
                    exit()
        elif fun_version(PY3_VNO,"3.9.5") != 0:
            logger.warning("Recommended version : Python == 3.9.5  However, it doesn't matter")
