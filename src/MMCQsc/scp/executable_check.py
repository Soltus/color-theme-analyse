# -*- coding=utf-8

# SCSD-PY001

# hi-windom/ColorThemeAnalyse

# https://gitee.com/hi-windom/color-theme-analyse

'''
# ---------------------------------
# 创建于    2021-7-20
# ---------------------------------
# Need help ?  => 694357845@qq.com
# ---------------------------------
# 作者很懒，还没想好说些什么
# ---------------------------------
'''

################################################################
import os,sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DPKG_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg'))
if BASE_DIR not in sys.path:
    sys.path.insert(1,BASE_DIR)
if DPKG_DIR not in sys.path:
    sys.path.append(DPKG_DIR)
from MMCQsc.scp.lib.error_sc import *
from MMCQsc.scp.lib.logger import *
logger = myLogging("gitee.com/soltus")
from MMCQsc.scp.lib import dpkg
pgd = dpkg.Pgd(BASE_DIR,DPKG_DIR)
import shutil
if os.name == 'posix':
    CLS = 'clear'
    LOCAL_LIB_POSIX = os.path.abspath(os.path.join(BASE_DIR, '../..'))
    O_DLL = os.path.join(BASE_DIR,'MMCQsc', 'scp', 'dll')
    D_DLL = os.path.join(LOCAL_LIB_POSIX, 'site-packages', 'MMCQsc', 'scp', 'dll')
    O_SRC = os.path.join(BASE_DIR,'MMCQsc', 'src')
    D_SRC = os.path.join(LOCAL_LIB_POSIX, 'site-packages', 'MMCQsc', 'src')
    if os.path.exists(O_DLL) == False:
        shutil.move(D_DLL, O_DLL)
    elif os.path.exists(D_DLL):
        shutil.rmtree(O_DLL)
        shutil.move(D_DLL, O_DLL)
    if os.path.exists(O_SRC) == False:
        shutil.move(D_SRC, O_SRC)
    elif os.path.exists(D_SRC):
        shutil.rmtree(O_SRC)
        shutil.move(D_SRC, O_SRC)
else:
    CLS = 'cls'


# os.system(CLS)

file_path = sys.argv[0]



from subprocess import Popen
import shlex
import types



def run_in_env(env):
    """
    提供交互式环境解决方案
    """
    PY3_VNO = ''
    for i in sys.version_info[:3]:
        PY3_VNO += str(i)
    PY3_VNO = '.'.join(PY3_VNO)
    # os.system(CLS)

    logger.info("开始检测 Conda 环境")
    if env is None:
        logger.info('尝试安装多个扩展包到项目 [ 如果不存在缓存，将从网络下载并安装 ]')
        pgd.get_dpkg('numpy')
        pgd.get_dpkg('rich')
        pgd.get_dpkg('Pillow')
        return env
    else:
        _env_v = dpkg.list_conda_env(py=['3.9'],conda_exec='conda')

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
                    logger.error(" 不同 Python 版本的扩展包无法共享 ")
                    logger.error(" 应当使用 Python == {}.{} 的 Conda 环境导入扩展包".format(sys.version_info[0],sys.version_info[1]))
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
                        from importlib import util
                        importlib.reload(numpy)
                        importlib.invalidate_caches()
                        util.resolve_name('numpy', __spec__.parent)
                        print(M_numpy)
                        # print(M_numpy.__dict__)
                        logger.info("import numpy seccessfully")
                        pgd.get_dpkg('rich')
                    except:
                        logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                        logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                        logger.error(" 不同 Python 版本的 Numpy 无法共享 ")
                        continue
                    return env
            elif pick_env in ['N','n']:
                logger.info('尝试安装多个扩展包到项目 [ 如果不存在缓存，将从网络下载并安装 ]')
                pgd.get_dpkg('numpy')
                pgd.get_dpkg('rich')
                pgd.get_dpkg('Pillow')
                return env
            else:
                python = sys.executable.replace(dpkg.check_conda()[1],pick_env)
                # print(python)
                os.system(CLS)
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
                    from importlib import util
                    importlib.reload(numpy)
                    importlib.invalidate_caches()
                    util.resolve_name('numpy', __spec__.parent)
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
                os.system(CLS)
                python = sys.executable.replace(dpkg.check_conda()[1],pick_env)
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
                logger.debug(dpkg.check_conda()[0])
                logger.debug(python)
                logger.debug(file_path)
                logger.debug(f"已创建的环境 : [ {pick_env} ]  请使用创建的环境重新运行\n\n")
                logger.warning("\n\n\t\t[ tip ] : 方向上键 ^ 可调出调出历史指令\n\n")
                exit()
                return pick_env


logger.info('尝试使用缓存')
try:
    from MMCQsc_dpkg import numpy as np
    from MMCQsc_dpkg import rich
    from MMCQsc_dpkg.PIL import Image as PImage
    logger.info("旁加载缓存成功")
except ImportError:
    try:
        np = __import__('numpy', globals(), locals(), [], 0)
        rich = __import__('rich', globals(), locals(), [], 0)
        PIL = __import__('PIL', globals(), locals(), [], 0)
        logger.info("全局加载缓存成功")
    except:
        if os.name == 'posix':
            pick_env = None
        else:
            pick_env = dpkg.check_conda()[1]
        while pick_env:
            env_tmep = pick_env
            pick_env = run_in_env(pick_env)
            if pick_env == env_tmep:
                break

        PY3_VNO = ''
        for i in sys.version_info[:3]:
                PY3_VNO += str(i)
        PY3_VNO = '.'.join(PY3_VNO)
        pgd.up_python(PY3_VNO,'3.10.5','3.9.1','3.9.5',pick_env)
