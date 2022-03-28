# -*- coding=utf-8

# SCSD-PY001

# hi-windom/ColorThemeAnalyse

# https://gitee.com/hi-windom/color-theme-analyse

'''
# ---------------------------------
# 创建于    2021-5-18
# ---------------------------------
# Need help ?  => 694357845@qq.com
# ---------------------------------
# 如果你的 Python 版本大于 3.8.0 ，直接运行本文件，会自动帮你安装依赖
# 建议在 Conda 虚拟环境运行本文件
# 从 1.2.445 版本开始支持 Linux
# ---------------------------------
'''

################################################################
import socket
import time
import os,sys,shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DPKG_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg'))
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc','src'))
if BASE_DIR not in sys.path:
    sys.path.insert(1,BASE_DIR)
if DPKG_DIR not in sys.path:
    sys.path.insert(1,DPKG_DIR)
PY_DIR =  os.path.abspath(os.path.dirname(sys.executable))
PYSPP = os.path.abspath(os.path.join(PY_DIR, 'site-packages.zip'))
if PY_DIR not in sys.path:
    sys.path.append(PY_DIR)
    sys.path.append(PYSPP)


from MMCQsc.scp.lib.logger import *
logger = myLogging("gitee.com/soltus")

from multiprocessing import shared_memory  # required for Python >= 3.8
from concurrent import futures
from subprocess import Popen,PIPE
import shlex
import ctypes
import struct
from random import randint

from importlib.metadata import version as Version, PackageNotFoundError

try:
    __version__ = Version("MMCQsc") # if installed
except PackageNotFoundError:
    # package is not installed
    from MMCQsc.version import __version__, version

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()

    return ip


def createServer(myip,PORT):
    if os.name != 'posix':
        netlocal = '（支持局域网访问）'
    else:
        netlocal = ''
    logger.info(SRC_DIR)
    args = shlex.split(f"pyhton -m http.server {PORT}")
    '''
    cwd 工作目录，设置为正确值以确保 launch ../src/index.html
    executable 参数指定一个要执行的替换程序。这很少需要。当 shell=True， executable 替换 args 指定运行的程序。但是，原始的 args 仍然被传递给程序。大多数程序将被 args 指定的程序作为命令名对待，这可以与实际运行的程序不同。
    '''
    result =  Popen(args, bufsize=0, executable=sys.executable, close_fds=False, shell=False, cwd=SRC_DIR, startupinfo=None, creationflags=0) # shell=False cwd=SRC_DIR 非常重要
    logger.debug(f"http.server进程 PID: {result.pid}")
    logger.info(f'\n\n\n\t\t本地服务器创建成功：\n\n\t\t http://{myip}:{PORT}\n\n\t\t{netlocal}\n\n')
    logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
    result.wait()

def openhtml(myip,PORT):
    if os.name == "posix":
        logger.info(f'\n\n\n\t\t浏览器访问：\n\n\t\t http://{myip}:{PORT}\n\n')
    else:
        logger.info(f'\n\n\n\t\t即将默认浏览器打开：\n\n\t\t http://{myip}:{PORT}\n\n')
        os.system(f'start http://{myip}:{PORT}')

def mainFunc(mode=False):
    from MMCQsc.scp.lib import dpkg
    pgd = dpkg.Pgd(BASE_DIR,DPKG_DIR)
    new = dpkg.check_update(f"{__version__}","https://pypi.org/pypi/color-theme-analyse/json","https://mirrors.tencent.com/pypi/simple/color-theme-analyse/")
    if new == True:
        repo = input("\n\t\t是否更新到最新版？[y/n]\t")
        if repo in ['Y','y']:
            if os.name == 'posix':
                pgd.upgrade_module_linux('color-theme-analyse')
            else:
                pgd.upgrade_module_win('color-theme-analyse')
    try:
        shm = shared_memory.SharedMemory(
            name='main_run_share', create=True, size=4096)
    except:
        shm = shared_memory.SharedMemory(name='main_run_share')
        shm.buf[1] = 0
    buf = shm.buf
    if buf[1] > 0:
        pass
    else:
        try:
            if os.name == 'posix':
                response = input('请输入路径: ~$ ')
                img = os.path.abspath(response)
            else:
                if struct.calcsize("P") * 8 == 32:
                    mydll = ctypes.CDLL(os.path.join(BASE_DIR,'MMCQsc','scp','dll','CommonOpenDialogDll.dll'))
                elif struct.calcsize("P") * 8 == 64:
                    mydll = ctypes.CDLL(os.path.join(BASE_DIR,'MMCQsc','scp','dll','CommonOpenDialogDll64.dll'))

                logger.info(f'\n\n\t\t{mydll}\n\n')
                mydll.mainFunc.restype = ctypes.c_wchar_p # 设置返回值格式
                response = mydll.mainFunc()
                # logger.info(f'\n\n\t\t{response}\n\n')

            if response != None:  # 有传入才处理
                img = os.path.dirname(response)
                # print('开始检查')
                # from MMCQsc.scp import executable_check
                buf[1] = len(img)
                for i in range(2, 10, 1):
                    buf[i] = 0
                from MMCQsc.scp.scripts import executer
                result = executer.domain(img)
                if buf[2] == 1 and result == 6:
                    if mode:
                        if os.name == 'posix':
                            _browser = os.path.abspath(os.path.join(SRC_DIR, 'browser','linux'))
                            DIR_SPLIT = '/'
                        else:
                            _browser = os.path.abspath(os.path.join(SRC_DIR, 'browser','windows'))
                            DIR_SPLIT = '\\'
                        # response = os.system(f'{_browser} \"{SRC_DIR}\"')
                        _index = SRC_DIR.replace('\\','/')
                        args = [f'.{DIR_SPLIT}TaskBar',f'{_index}']
                        # print(args)
                        # input()
                        Popen(args, bufsize=0, close_fds=False, shell=True, cwd=_browser, startupinfo=None, creationflags=0)
                        time.sleep(2)
                        exit(9)
                    else:
                        with futures.ProcessPoolExecutor(max_workers=None) as prolist:
                            PORT = randint(5800,5858)
                            if os.name != 'posix':
                                myip = get_host_ip()
                            else:
                                myip = 'localhost'
                            prolist.submit(createServer,myip,PORT)
                            time.sleep(2)
                            prolist.submit(openhtml,myip,PORT)  # 多进程才能打开
            else:
                logger.error("无输入或无效输入")
                shm.close()
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                os.system('cls')
                logger.info("进程服务已停止\t原因：用户强制退出")
            else:
                logger.debug(e)
        finally:
            try:
                if mode == False:
                    os.remove(os.path.join(SRC_DIR, 'index.js'))
                    os.remove(os.path.join(SRC_DIR, 'index.css'))
                    shutil.rmtree(os.path.join(SRC_DIR, 'finish'))
                    shutil.rmtree(os.path.join(SRC_DIR, 'compress'))
                    logger.info('成功删除不重要的自动生成文件')
                logger.warning("\n\n\t\t[ tip ] : 如果当前窗口未正确返回 Shell 环境，使用 CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
            except Exception as e:
                if isinstance(e,FileNotFoundError):
                    logger.warning('未检测到自动生成文件')
                if isinstance(e,KeyboardInterrupt):
                    exit(133)
                try:
                    result in locals()
                    logger.warning('未能删除自动生成文件')
                except Exception as e:
                    pass
            shm.close()
            shm.unlink()
            return 0
    # sys.exit(102)


if __name__ == '__main__':
    # import multiprocessing as mp
    # mp.get_context('spawn')
    try:
        result = mainFunc()
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt):
            logger.warning(f"{__file__}\n\t\t用户强制退出")
            exit(103)