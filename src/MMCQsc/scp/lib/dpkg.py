import os,sys
import string
import json
from subprocess import Popen
import shlex
import types
import ctypes
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
    :param disk: ['D:\\','E:\\'] 将制定扫描盘符，默认扫描全部盘符
    :param mode: 0表示找到结果后立即停止（仅对文件查找生效），1表示贪婪模式
    :param debug: True将开启控制台输出
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
                with os.popen(f"{e}\\python.exe --version") as repo:
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

    l_1 = v1.split('.')[0:3]
    l_2 = v2.split('.')[0:3]
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
    def __init__(self,root:str,dpkg:str):
        '''root 填 BASE_DIR，dpkg 填 DPKG_DIR'''
        self.url = 'https://pypi.douban.com/simple/'
        self.BASE_DIR = os.path.abspath(root)
        self.DPKG_DIR = os.path.abspath(dpkg)
        self.executable = os.path.abspath(sys.executable).replace('\\','/')

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def task(self,im,re,yes=False):
        self.im = im
        self.re = re
        _cwd = os.path.abspath(os.path.dirname(self.executable))
        if yes:
            repo = 'y'
        else:
            repo = input('\n\n Unable to import package [{}] from \n\t{} , \n\n Do you want to download ? \n\n\t\tProccess ? [Y/n]\t'.format(self.im, sys.path))
        if repo in ['Y','y']:
            # os.system(CLS)
            os.system(f"powershell cd '{_cwd}';./python -m pip install {self.re} -i {self.url}")
            return 1
        return 0

    def get_dpkg(self,name):
        """
        获取动态包
        """
        if self.is_admin():
            pass
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        try:
            PKG_D = self.DPKG_DIR.replace('\\','/')
            if self.DPKG_DIR not in sys.path:
                sys.path.insert(1,self.DPKG_DIR)
            python = self.executable
            # command = f'\"powershell \\\"pip install {name} --upgrade --force-reinstall -t {PKG_D} -i https://pypi.douban.com/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --compile --timeout 30 --exists-action b --only-binary :all:\\\"\"'
            # args = shlex.split(f'''powershell runas /trustlevel:0x40000''')
            # args.append(command)
            args = shlex.split(f"{python} -m pip install {name} --isolated --force-reinstall -t {PKG_D} -i https://pypi.douban.com/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --compile --timeout 30 --exists-action b --only-binary :all:")
            result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=False, env=None, startupinfo=None, creationflags=0)
            logger.debug(f"创建下载线程 PID: {result.pid}")
            logger.warning("\n\n\t\t[ tip ] : 快捷键 CTRL + C 强制结束当前任务，CTRL + PAUSE_BREAK 强制结束所有任务并退出 Python\n\n")
            result.wait()
            return 1

            M_module = types.ModuleType(name)
            M_module.__file__ = os.path.abspath(os.path.join(PKG_D, name, '__init__.py'))  # type: ignore
            M_module.__package__ = ''
            try:
                exec(f"import importlib,sys;from importlib import util;sys.modules['{name}']=M_module;import {name};importlib.reload({name});importlib.invalidate_caches();util.resolve_name('{name}', __spec__.parent)",globals(), locals())
                # logger.info(M_module.__dict__)
                logger.info('\n' + str(M_module))
                logger.info(f"\n\n\timport {name} seccessfully\n\n")
                return 1
            except Exception as e:
                logger.error(e)
                logger.error(f"旁加载 {name} 失败 ")
                return 0
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                logger.warning("用户中止了下载")
                return 0
        return 0

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
        logger.warning(f"You are using Python {PY3_VNO}")
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

    def upgrade_module_win(self,name):
        python = self.executable
        logger.warning(f"\n\n\t\t{python}\n\n")
        import traceback
        _path = os.path.abspath(os.path.join(__file__,"../..","scripts"))
        try:
            bat = os.path.abspath(os.path.join(_path,"upgrade.bat"))
            f = open(bat, 'w')
            f.write(f"{python} -m pip install {name} --upgrade --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
        except Exception as e:
            traceback.print_exc()
            raise e
        args = shlex.split(f"PowerShell ./upgrade.vbs")
        result = Popen(args, bufsize=0, close_fds=False, shell=True, env=None,cwd=_path, startupinfo=None, creationflags=0)
        exit()

    def upgrade_module_linux(self,name):
        python = self.executable
        logger.warning(f"\n\n\t\t{python}\n\n")
        import traceback
        try:
            args = shlex.split(f"pip3 install {name} --upgrade --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30")
            with Popen(args, bufsize=0, close_fds=False, shell=False, env=None,cwd=None, startupinfo=None, creationflags=0) as p:
                exit()
        except Exception as e:
            traceback.print_exc()
            raise e
        return

from re import sub
import requests
from html.parser import HTMLParser
from urllib import parse

class MyHP(HTMLParser):
    def __init__(self,v,tcurl):
        HTMLParser.__init__(self)
        self.__text = []
        self.__v = v
        self.__url = 'null'
        self.TCURL = tcurl

    def handle_data(self,data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')
        elif tag == 'a':
            if self.__v in attrs[0][1]:
                self.__url = parse.urljoin(self.TCURL,attrs[0][1])

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()

    def get_url(self):
        return self.__url

def check_update(nv,json_url,mirrors_url) -> bool:
    TCURL = mirrors_url
    r = requests.get(json_url)
    data = r.json()
    # print(f"{len(data['releases'])}个可用版本\n当前版本：{nv}")
    v_l = []
    new = False
    for version, files in data['releases'].items():
        for f in files:
            if f.get('packagetype') in ['bdist_wheel'] and f.get('requires_python'):
                v_l.append(version)

                if py_version(version,nv) == 1 and 'dev' not in version:
                    new =True
                    r = requests.get(TCURL)
                    parser = MyHP(version,TCURL)
                    parser.feed(bytes.decode(r.content))
                    # print(parser.text()) # 等效于 r.text
                    _url2 = parser.get_url()
                    _url1 = f.get('url')
                    r.close()
                    del parser
                    print(f"\n- 新版 {version} 现已可用！Python版本要求{f['requires_python']} - {f.get('upload_time')}\n官方下载地址：{_url1}\n镜像下载地址：{_url2}")
    return new
