# -*- coding=utf-8

# SCSD-PY001

# hi-windom/ColorThemeAnalyse

# https://gitee.com/hi-windom/color-theme-analyse

'''
# ---------------------------------
# 创建于    2021-5-18
# 更新于    2021-7-20 02:09:40
# ---------------------------------
# Need help ?  => 694357845@qq.com
# ---------------------------------
# 如果你的 Python 版本大于 3.8.0 ，直接运行本文件，会自动帮你安装依赖
# 建议在 Conda 虚拟环境运行本文件
# ---------------------------------
'''

################################################################
import socket
import time
import os,sys,shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc','src'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
PY_DIR =  os.path.abspath(os.path.dirname(sys.executable))
PY39P = os.path.abspath(os.path.join(PY_DIR, 'python39.zip'))
PYSPP = os.path.abspath(os.path.join(PY_DIR, 'site-packages.zip'))
if PY_DIR not in sys.path:
    sys.path.append(PY_DIR)
    sys.path.append(PY39P)
    sys.path.append(PYSPP)

from MMCQsc.scp.lib.logger import *
logger = myLogging("gitee.com/soltus")

from multiprocessing import shared_memory  # required for Python >= 3.8
from concurrent import futures
from subprocess import Popen,PIPE
import shlex
import ctypes
mydll = ctypes.CDLL(f"{BASE_DIR}\\MMCQsc\\scp\\dll\\CommonOpenDialogDll.dll")

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


def createServer():
    myip = get_host_ip()
    logger.info(SRC_DIR)
    args = shlex.split(f"pyhton -m http.server 5858")
    '''
    cwd 工作目录，设置为正确值以确保 launch ../src/index.html
    executable 参数指定一个要执行的替换程序。这很少需要。当 shell=True， executable 替换 args 指定运行的程序。但是，原始的 args 仍然被传递给程序。大多数程序将被 args 指定的程序作为命令名对待，这可以与实际运行的程序不同。
    '''
    result =  Popen(args, bufsize=0, executable=sys.executable, close_fds=False, shell=False, cwd=SRC_DIR, startupinfo=None, creationflags=0) # shell=False cwd=SRC_DIR 非常重要
    logger.debug(f"http.server进程 PID: {result.pid}")
    logger.info(f'\n\n\n\t\t本地服务器创建成功：\n\n\t\t{myip}:5858\n\n\t\t（支持局域网访问）\n\n')
    logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
    result.wait()

def openhtml():
    myip = get_host_ip()
    time.sleep(2)
    logger.info(f'\n\n\n\t\t即将默认浏览器打开：\n\n\t\t{myip}:5858\n\n')
    os.system(f'start http://{myip}:5858')

def mainFunc():
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
            from MMCQsc.scp import executable_check
            logger.info('\n\n\t\t请留意最小化的新窗口\n\n')
            img = ctypes.c_wchar_p(mydll.mainFunc()).value
            if img != None:  # 有传入才处理
                buf[1] = len(img)
                for i in range(2, 10, 1):
                    buf[i] = 0
                from MMCQsc.scp.scripts import executer
                result = executer.domain(img)
                if buf[2] == 1 and result == 6:
                    with futures.ProcessPoolExecutor(max_workers=None) as prolist:
                        prolist.submit(createServer)
                        prolist.submit(openhtml)  # 多进程才能打开
            else:
                logger.error("无输入或无效输入")
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                os.system('cls')
                logger.info("http.server 进程服务已停止\t原因：用户强制退出")
        finally:
            try:
                os.remove(os.path.join(SRC_DIR + '\\index.js'))
                os.remove(os.path.join(SRC_DIR + '\\index.css'))
                shutil.rmtree(os.path.join(SRC_DIR + '\\finish'))
                shutil.rmtree(os.path.join(SRC_DIR + '\\compress'))
                logger.info('成功删除不重要的自动生成文件')
                logger.warning("\n\n\t\t[ tip ] : 如需在当前窗口返回 Shell 环境，使用 CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
            except:
                if result:
                    logger.warning('未能删除自动生成文件')
            finally:
                sys.exit()


if __name__ == '__main__':
    try:
        result = mainFunc()
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt):
            logger.warning("{}\n\t\t用户强制退出".format(__file__))
            sys.exit()