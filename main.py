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
import importlib
logger = importlib.import_module('.logger','scp.lib')
logger = logger.myLogging("gitee.com/soltus")  # 这里如果报错，可以忽略
importlib.import_module('.executable_check','scp')
from multiprocessing import shared_memory  # required for Python >= 3.8
from concurrent import futures
test_3 = importlib.import_module('.test_3','scp.lib')
import socket
import time
import os
PN = 'easygui'
try:
    import easygui as g
except ImportError:
    logger.critical(f'import "{PN}" could not be resolved')
    logger.info("Try to download [{PN}] , Please wait for busy.")
    os.system("pip install easygui -i https://pypi.douban.com/simple/")
    import easygui as g

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def createServer():
    myip = get_host_ip()
    print(f'\n\n\n本地服务器创建成功：\n{myip}:5858\n\n')
    os.system(
        'cd {}/src && python -m http.server 5858'.format(os.path.dirname(__file__)))


# 无网页交互需求可以恢复被注释的代码
def openhtml():
    myip = get_host_ip()
    print(f'\n即将默认浏览器打开：\n{myip}:5858\n\n')
    os.system(f'start http://{myip}:5858')
    time.sleep(10)
    try:
        base_dir = os.path.dirname(__file__)
        # os.remove(base_dir + '\\src\\index.js')
        # os.remove(base_dir + '\\src\\index.css')
    except:
        pass
    # os.system('taskkill /f /fi "IMAGENAME eq cmd.exe')


if __name__ == '__main__':
    try:
        shm = shared_memory.SharedMemory(
            name='main_run_share', create=True, size=4096)
    except:
        shm = shared_memory.SharedMemory(name='main_run_share')
        shm.buf[1] = 0
    buf = shm.buf
    # fileopenbox()函数的返回值是你选择的那个文件的具体路径
    if buf[1] > 0:
        pass
    else:
        img = g.fileopenbox('open file' + '会导入当前文件夹的全部图片')
        if img != None:  # 有传入才处理
            buf[1] = len(img)
            for i in range(2, 10, 1):
                buf[i] = 0
            test_3.domain(img)
            if buf[2] == 1:
                with futures.ProcessPoolExecutor(max_workers=None) as prolist:
                    prolist.submit(createServer)
                    prolist.submit(openhtml)  # 多进程才能打开


# shm.close()  # 关闭共享内存
# shm.unlink()  # 释放共享内存
