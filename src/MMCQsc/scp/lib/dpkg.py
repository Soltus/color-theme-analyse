import os,sys
import string
import json
from subprocess import Popen
import shlex
import types
from MMCQsc.scp.lib.logger import *
logger = myLogging("gitee.com/soltus")

if os.name == 'posix':
    CLS = 'clear'
    DIR_SPLIT = '/'
else:
    CLS = 'cls'
    DIR_SPLIT = '\\'

def get_disk():
    disk_list = []

    for disk in string.ascii_uppercase:
        disk = disk + ':\\'
        if os.path.exists(disk):
            disk_list.append(disk)

    return disk_list


def search_files(disk=[],mode=0,debug=False):
    '''
    @param disk: ['D:\\','E:\\'] 将制定扫描盘符，默认扫描全部盘符
    @param mode: 0表示找到结果后立即停止（仅对文件查找生效），1表示贪婪模式
    @param debug: True将开启控制台输出
    '''
    values = []
    if disk == []:
        curdisks = get_disk()
    else:
        curdisks = disk

    # 搜索包含关键字的目录
    def searchDirs(root, name, dirs):
        if debug == True:
            print(f'正在扫描{root}')
        for _dir in dirs:
            if -1 != _dir.find(name) and _dir[0] != '$':
                AllDir = os.path.join(root, _dir)
                values.append(AllDir)

    # 搜索包含关键字的文件
    def searchFiles(root, name, files):
        if debug == True:
            print(f'正在扫描{root}')
        for file in files:
            if name in file:  # '$' not in AllFile 去除隐藏文件
                AllFile = os.path.join(root, file)
                values.append(AllFile)
                if mode == 1:
                    pass
                elif mode == 0:
                    return

    def _search(name):
        try:
            for disk in curdisks:
                for root, dirs, files in os.walk(disk, True):
                    searchDirs(root, name, dirs)
                    searchFiles(root, name, files)
        except:
            sys.exit(0)

    def __search(name):
        try:
            for disk in curdisks:
                for root, dirs, files in os.walk(disk, True):
                    searchDirs(root, name, dirs)
        except:
            sys.exit(0)

    def ___search(name):
        try:
            for disk in curdisks:
                for root, dirs, files in os.walk(disk, True):
                    searchFiles(root, name, files)
                if mode == 1:
                        pass
                elif mode == 0:
                    if values != []:
                        return
        except:
            sys.exit(0)
    return values,_search,__search,___search


def find_conda():
    ob = search_files()
    ob[3]('_conda.exe')
    return ob[0]

def check_conda(dir=''):
    '''
    检测当前 Conda 环境并返回值，返回值是 conda_exec, conda_env
    @param dir 默认为空，如果 conda 不在环境变量，请填写 conda 所在路径
    '''
    if dir == '':
        dir = sys.executable
    if "\\envs\\" in dir:
        conda_exec = os.path.abspath(os.path.join(os.path.dirname(dir), "../..", "Script", "conda.exe"))
        conda_env = sys.executable.split("\\")[-2]
    else:
        conda_exec = os.path.abspath(os.path.join(os.path.dirname(dir), "Script", "conda.exe"))
        conda_env = "base"
    if os.path.exists(conda_exec):
        return conda_exec, conda_env
    else:
        return '',''

def list_conda_env(py=['3.9'],conda_exec=''):
    if conda_exec == '':
        pass
    elif conda_exec == 'conda':
        luu = os.path.dirname(find_conda()[0])
        lu = os.path.join(luu,'Scripts')
        sys.path.append(luu)
        sys.path.append(lu)
    else:
        luu = os.path.abspath(conda_exec)
        lu = os.path.join(luu,'Scripts')
        sys.path.append(luu)
        sys.path.append(lu)
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
                return None
            for e in _env_list:
                with os.popen("{}\\python.exe --version".format(e)) as repo:
                    _env_path = e.strip()
                    _env = '{}'.format(e).split('\\')[-1]
                    if '{}'.format(e).split('\\')[-2] == 'envs':
                        _env = '{}'.format(e).split('\\')[-1]
                    else:
                        _env = 'base'

                    for v in py:
                        if str(v) in repo.read().strip():
                            _env_v[_env] = {}
                            _env_v[_env]['version'] = repo.read().strip()
                            _env_v[_env]['path'] = _env_path
                            print('\n\t' + _env + '\t' + _env_v[_env]['version'] + '\t' + _env_path)

            print('\n\n')
            logger.info("已列出所有兼容的 Conda 环境")
            return _env_v


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
    def __init__(self,root,dpkg):
        '''root 填 BASE_DIR，dpkg 填 DPKG_DIR'''
        self.url = 'https://pypi.douban.com/simple/'
        self.BASE_DIR = os.path.abspath(root)
        self.DPKG_DIR = os.path.abspath(dpkg)
        self.executable = os.path.abspath(sys.executable).replace('\\','/')

    def task(self,im,re):
        self.im = im
        self.re = re
        _cwd = os.path.dirname(self.executable)
        repo = input('\n\n Unable to import package [{}] from \n\t{} , \n\n Do you want to download ? \n\n\t\tProccess ? [Y/n]\t'.format(self.im, sys.path))
        if repo in ['Y','y']:
            os.system(CLS)
            os.system("cd {};./Scripts/pip.exe install {} -i {}".format(_cwd, self.re, self.url))
            return 1
        return 0

    def get_dpkg(self,name):
        """
        获取动态包
        """
        try:
            PKG_D = self.DPKG_DIR
            # python = sys.executable.replace(check_conda()[1],pick_env)
            # nexe = python.replace('\\','/')
            python = self.executable
            print(python)
            args = shlex.split(f"{python} -m pip install {name} --isolated --python-version 3.9 --ignore-requires-python --force-reinstall -t {PKG_D} -i https://pypi.douban.com/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --compile --timeout 30 --exists-action b --only-binary :all:")
            result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0)
            logger.debug(f"创建下载线程 PID: {result.pid}")
            logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
            result.wait()

            M_module = types.ModuleType(name)
            M_module.__file__ = os.path.abspath(os.path.join(PKG_D, name, '__init__.py'))  # type: ignore
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

    def up_python(self,av,bv,cv,dv,conda_env=None):
        '''
        @param av: 当前版本
        @param bv: 建议版本
        @param cv: 最低版本
        @param dv: 目标版本
        @param conda_env: 当前 conda 环境，没有则留空
        '''
        PY3_VNO = av
        if conda_env is not None:
            pick_env = ' -n ' + conda_env
        else:
            pick_env = ''
        logger.warning("You are using Python {}".format(PY3_VNO))
        if py_version(PY3_VNO,cv) == -1:
            logger.critical(f"Required version : Python >= {cv}")
            with os.popen("conda --version") as conda_v:
                if "conda" in conda_v.read():
                    logger.info("You are using Conda , Press key 'y' to upgrade your Python")
                    logger.info(f"If you want to upgrade later by yourself , use command: conda install python=={dv}")
                    logger.debug(f"Upgrade your Python to {dv} ?  [Y/*]")
                isupdate = input("main.py:123 >>> ")
            if isupdate not in ['Y','y']:
                exit()
            os.system(CLS)
            logger.info("即将开始下载，这取决于你的网络")
            try:
                args = shlex.split(f"conda conda install python=={dv} -y{pick_env}")
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
                    args = [sys.executable, sys.argv[0]]
                    logger.debug(args)
                    logger.debug(f"请在终端执行指令 conda activate {pick_env} 手动激活环境")
                    logger.warning("\n\n\t\t[ tip ] : 方向上键 ^ 可调出调出历史指令\n\n")
                    exit()
        elif py_version(PY3_VNO,bv) != 0:
            logger.warning(f"Recommended version : Python == {bv}  However, it doesn't matter")