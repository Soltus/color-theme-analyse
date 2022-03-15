import os,sys
from subprocess import Popen
import shlex
import types
from MMCQsc.scp.lib.logger import *
logger = myLogging("gitee.com/soltus")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DPKG_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg'))
if os.name == 'posix':
    CLS = 'clear'
    DIR_SPLIT = '/'
else:
    CLS = 'cls'
    DIR_SPLIT = '\\'

def check_conda():
    """
    检测 Conda 环境并返回值
    """
    if "\\envs\\" in sys.executable:
        conda_exec = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "../..", "Script", "conda.exe"))
        conda_env = sys.executable.split("\\")[-2]
    else:
        conda_exec = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "Script", "conda.exe"))
        conda_env = "base"
    return conda_exec, conda_env

def py_version(v1,v2):
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

class Pgd:
    def __init__(self):
        self.url = 'https://pypi.douban.com/simple/'

    def task(self,im,re):
        self.im = im
        self.re = re
        import os
        repo = input('\n\n Unable to import package [{}] from \n\t{} , \n\n Do you want to download ? \n\n\t\tProccess ? [Y/n]\t'.format(self.im, sys.path))
        if repo in ['Y','y']:
            os.system(CLS)
            os.system("pip install {} -i {}".format(self.re, self.url))
            return 1
        return 0

    def get_dpkg(self,name):
        """
        获取动态包
        """
        try:
            PKG_D = DPKG_DIR
            # python = sys.executable.replace(check_conda()[1],pick_env)
            # nexe = python.replace('\\','/')
            python = os.path.abspath(sys.executable).replace('\\','/')
            print(python)
            args = shlex.split(f"{python} -m pip install {name} --isolated --python-version 3.9 --ignore-requires-python --force-reinstall -t {PKG_D} -i https://pypi.douban.com/simple --extra-index-url https://pypi.mirrors.ustc.edu.cn --compile --timeout 30 --exists-action b --only-binary :all:")
            result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0)
            logger.debug(f"创建下载线程 PID: {result.pid}")
            logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
            result.wait()
            PKG_D = os.path.abspath(PKG_D)
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