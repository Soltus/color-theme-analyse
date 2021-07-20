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
from importlib import import_module
import json
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)
    # logger = import_module('.logger','lib')
    # logger = logger.myLogging("gitee.com/soltus")

from scp.lib.error_sc import *
from scp.lib.logger import *
logger = myLogging("gitee.com/soltus")
from scp.lib.error_sc import *


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
        conda_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "../..", "Script", "conda.exe"))
        conda_env = sys.executable.split("\\")[-2]
    else:
        conda_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "Script", "conda.exe"))
        conda_env = "base"
    return conda_path, conda_env


from subprocess import Popen
import shlex

# try:
#     raise error_sc.EnvError('e97304')
# except error_sc.EnvError as e:
#     logger.error("引发异常：" + repr(e))
#     tb = sys.exc_info()[2]
#     if tb:
#         raise error_sc.OA().with_traceback(tb)

def run_in_env(env):
    PY3_VNO = ''
    for i in sys.version_info[:3]:
        PY3_VNO += str(i)
    PY3_VNO = '.'.join(PY3_VNO)
    os.system("cls")
    logger.info("You are using Conda , Activated conda env : '{}' Python {}".format(env, PY3_VNO))
    with os.popen("conda --version") as conda_v:
        if "conda" in conda_v.read():
            logger.debug("\n\n\n\t\t使用当前 Conda 环境继续吗 (y) ？\n\t\t或者重新选择运行环境 (n) ？\n\t\t也可以输入任意字符作为新环境名，将为你自创建一个 Python 3.9.5 的新环境\n\n\t\tProccess ?  [Y/n/*]")
    while True:
        pick_env = input("main.py:93 >>> ")
        if pick_env in ['Y','y']:
            if sys.version_info.major < 3:
                logger.error(" Can NOT run in Python 2.x ")
                raise EnvError('\n\n\t''This script is only for use with ''Python 3.6 or later\n\n\t https://gitee.com/hi-windomcolor-theme-analyse/ \n\n')
            elif sys.version_info[:3] < (3,6,0):
                logger.error(" Can NOT run in Python < 3.6 ")
                raise EnvError('\n\n\t''This script is only for use with ''Python 3.6 or later\n\n\t https://gitee.com/hi-windomcolor-theme-analyse/ \n\n')
            else:
                return env
        elif pick_env in ['N','n']:
            python = sys.executable.replace(check_conda()[1],pick_env)
            print(python)
            os.system("cls")
            os.system("conda info -e")
            logger.debug("\n\n\n\t\t输入你想激活的 Conda 环境")
            pick_env = input("main.py:109 >>> ")
            logger.debug(f"请在终端执行指令 conda activate {pick_env} 手动激活环境")
            logger.warning("\n\n\t\t[ tip ] : 方向上键 ^ 可调出调出历史指令\n\n")
            exit()
        else:
            os.system("conda deactivate")
            os.system("deactivate")
            os.system("cls")
            python = sys.executable.replace(check_conda()[1],pick_env)
            change_env = file_path.replace('main','change_env')
            try:
                args = shlex.split(f"conda create -n {pick_env} python==3.9.5 -y")
                result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0)
                logger.debug(f"创建下载线程 PID: {result.pid}")
                logger.warning("\n\n\t\t[ tip ] : 快捷键 CTR + C 强制结束\n\n")
                result.wait()
            except BaseException as e:
                if isinstance(e, KeyboardInterrupt):
                    logger.warning("用户中止了下载")
                    logger.warning("当前窗口已完成使命，是时候和它告别了")
                    result.kill()
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
        logger.warning("\n\n\t\t[ tip ] : 快捷键 CTR + C 强制结束\n\n")
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
elif fun_version(PY3_VNO,"3.9.5") == -1:
    logger.warning("Recommended version : Python >= 3.9.5  However, it doesn't matter")
