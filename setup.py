'''
官方推荐使用静态的 setup.cfg 但动态的 setup.py 对我们来说更熟悉，学习成本低，两个文件也可以共存
MANIFEST.in 需要放在和 setup.py 同级的顶级目录下，setuptools 会自动读取该文件，需要注意 MANIFEST.in 指令是按顺序执行的，因此 exclude 要放在 include 后面
建议 MANIFEST.in 只用于构建 tar.gz 而不用于 whl ，即 setup.py 设置 [include_package_data=False]，至少在熟练掌握构建前应当这样做

//关于setuptools：setuptools 是 distutils 增强版，不包括在标准库中

//关于包格式：egg 包是过时的，whl 包是新的标准

//关于打包：

        [1]
        python setup.py sdist  # ****************************************** 生成 dist/*.tar.gz [源码];
        [2]
        python setup.py bdist_wheel  # ************************************ 生成 dist/*.whl [通用包];
        [3]
        如果你的项目不是跨平台的，应当构建指定平台的包：
        python setup.py bdist_wheel --plat-name win32  # ****************** [win32平台构建]
        python setup.py bdist_wheel --plat-name win_amd64  # ************** [win_amd64平台构建]
        [4]
        python setup.py bdist  # ****************************************** 生成 dist/*.zip [镜像构建，包含虚拟环境，不建议使用];
        [5]
        python setup.py bdist_wininst  # ********************************** 生成 dist/*.whl [Windows安装引导程序];
        ### 从 Python 3.8 开始不推荐使用 bdist_wininst ; bdist_msi从 Python 3.9 起被弃用。 ###
        [6]
        更多命令使用 python setup.py --help-commands 查看

        如果遇到 error: invalid command 'bdist_wheel' 的报错，pip install wheel 后重试

//关于上传：

        用 upload 命令上传包已经过时（不安全），官方提供了 twine 工具专门用来与 PyPI 交互。
        项目成熟之前，应当使用 twine upload dist/* --verbose --repository testpypi
        testpypi 的数据库会被定期修剪，因此可以放心上传
        频繁上传测试，命令行可以整合为一行 python setup.py bdist_wheel;twine upload dist/* --verbose --repository testpypi

//关于版本号：Python 的软件分发工具还支持 local version identifier 可用于标识不打算发布的本地开发构建.
本地版本标识符采用以下形式 <public version identifier>+<local version label> 例如：

        1.2.0.dev1+hg.5.b11e5e6f0b0b  # 5th VCS commmit since 1.2.0.dev1 release
        1.2.1+fedora.4                # Package with downstream Fedora patches applied

另请注意，使用 setuptools_scm 控制版本后，使用了本地版本标识符是无法上传到 PyPi 的，因此 local_scheme = "no-local-version" 在 pyproject.toml
使用 setuptools_scm 方案，则版本号是在setup()函数中自动生成的。 主模块的__version__如果需要和它保持一致，就需要读取已安装的当前包的版本号。
修改 Release 版本号需要使用 Git 打上版本号标签，在熟悉之前应当使用 x.x.x 形式的标签（例如 1.0.2 ）
如果不熟悉 Git 命令行操作，可以使用软件 Sourcetree 直观的提交和打标签。如果没有标签，你生成的包将始终为 0.1.dev*
（新增）你也可以用本文件提供的 GVC 模块来打标签，具体内容请跳转到 class GVC 查看
建议的版本号规则：
模块的版本号采用X.Y.Z的格式，
1、修复bug，小改动，增加z。
2、增加新特性，可向后兼容，增加y
3、有很大的改动，无法向下兼容,增加x
当前 commit 就在标签上，代码没有修改： {tag}
当前 commit 就在标签上，代码有修改： {tag}+dYYYMMMDD
当前 commit 不在标签上，代码没有修改：{next_version}.dev{distance}+{scm letter}{revision hash}
当前 commit 不在标签上，代码有修改： {next_version}.dev{distance}+{scm letter}{revision hash}.dYYYMMMDD
'''
import distutils.cmd
import distutils.log
import shutil
import os,sys
from time import strftime, sleep
from subprocess import Popen,PIPE,check_call
import shlex
import types
import ctypes, locale
locale.setlocale(locale.LC_ALL, '')
ctypes.cdll.ucrtbase._tzset()
# 调整为中国时间


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
build_time = strftime('%Z %Y-%m-%d %H:%M:%S')

syspath = sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'dist'))
DPKG_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg'))
if BASE_DIR not in sys.path:
    sys.path.insert(1,BASE_DIR) # 这里使用insert（插入）而不是添加append（添加），是为了避免已安装的 MMCQsc 包的版本号影响
if DPKG_DIR not in sys.path:
    sys.path.append(DPKG_DIR)

class Pgd:
    def __init__(self):
        self.url = 'https://pypi.douban.com/simple/'

    def task(self,im,re):
        self.im = im
        self.re = re
        import os
        repo = input('\n\n Unable to import package [{}] from \n\t{} , \n\n Do you want to download ? \n\n\t\tProccess ? [Y/n]\t'.format(self.im, sys.path))
        if repo in ['Y','y']:
            os.system("pip install {} -i {}".format(self.re, self.url))
            return 1
        return 0

dddd = 0
pgd = Pgd()
try:
    setuptools = __import__('setuptools', globals(), locals(), [], 0)
    wheel = __import__('wheel', globals(), locals(), [], 0)
    ''' pip list 里面如果没有 twine 请自行安装 '''
except ImportError:
    try:
        import setuptools
        import wheel
    except:
        repo = pgd.task(im="setuptools",re="setuptools")
        dddd += repo
        repo = pgd.task(im="wheel",re="wheel")
        dddd += repo
try:
    setuptools_scm = __import__('setuptools_scm', globals(), locals(), [], 0)
    setuptools_scm_git_archive = __import__('setuptools_scm_git_archive', globals(), locals(), [], 0)
except ImportError:
    try:
        import setuptools_scm
        import setuptools_scm_git_archive
    except:
        repo = pgd.task(im="setuptools_scm",re="setuptools_scm")
        dddd += repo
        repo = pgd.task(im="setuptools_scm_git_archive",re="setuptools_scm_git_archive")
        dddd += repo

if dddd:
    print(f'\n\t\t{dddd} new packages already installed .\n\n\t\ttry to launch again .\n\n')
    sys.exit()


from MMCQsc.version import version
my_v = version

MY_V = my_v.split('.')
CLEAN_TAG = False


class GVC(distutils.cmd.Command):
    """适用于构建时修改内容的频繁版本迭代，允许自动完成一些操作，这在修复 bug 时期特别实用.
    由于使用了 os.getcwd() ，因此务必确保终端工作区目录为 setup.py 所在目录
    生成干净的可自动迭代的 releas/dev 版本， 例如 color_theme_analyse-1.2.721.dev4-py3-none-any
    使用方法 python setup.py GVC，要求正确配置 Git 环境
    如果 PyPi 的账号密码的配置文件正确存在，可以使用以下括号内的命令一键构建并上传（以 testPyPi 为例，--version参数自行修改）：
    [python setup.py GVC --qmode --version=1.1.1;python setup.py bdist_wheel;twine upload dist/* --verbose --repository testpypi]
    关于--version，需要注意：应该使用 --version=1.1.101 而不是 --version=1.1.001（不能含有无效的零）
    频繁的上传测试仅限于依赖真实环境模拟的项目，否则不建议这么做 """
    # 命令的描述，会出现在`python setup.py --help`里
    description = '适用于修复 bug 的频繁版本迭代（用户定义的）'
    user_options = [
        # 格式是`(长名字，短名字，描述)`，描述同样会出现在doc里
        # 注意不要和全局选项冲突，例如 verbose(v) quiet(q) help(h)
        # binary选项，长名字后面没有等号，最后的值会传给`self.<长名字>`，使用形式 --qmode 或者 -m (使用了为 True，默认应为 False)
        # 需要值的选项，长名字后面有等号，最后的值会传给`self.<长名字>`（-会用_代替），使用形式 --version=1.1.1 ，不能使用 -v=1.1.1
        ('qmode','m','queit mode without debug info'),
        ('version=', 'v', 'define git-tag and build-version'),
  ]

    def initialize_options(self):
        """设置选项的默认值, 每个选项都要有初始值，否则报错."""
        # Each user option must be listed here with their default value.
        self.version = my_v
        self.qmode = False

    def finalize_options(self):
        """接收到命令行传过来的值之后的处理， 也可以什么都不干."""
        # pass
        global MY_V
        # 无需手动定义版本号，尝试自动步进
        ''' pyproject.toml 中规定了 setuptools_scm 自动生成项目版本号到 version.py ，会影响自动步进（仅限正式版本号），这是已知缺陷 '''
        if self.version == "0.0.0":
            v_n = (int(MY_V[0]), int(MY_V[1]), int(MY_V[2]))
            self.version = f'{v_n[0]}.{v_n[1]+1}.0'
            self.version2 = f'{v_n[0]}.{v_n[1]+1}.1'
            self.___version = [self.version,self.version2]
        else:
            self.___version = self.default_nv()
        from MMCQsc.version import version as _v_
        self.write_version() # 只需要注释掉这一行，就可以实现正式版本号的自动步进（因为受git控制的__init__.py没有变化）

    def write_version(self):
        it = os.open("src/MMCQsc/__init__.py",os.O_RDWR|os.O_CREAT)
        '''
        os.lseek(fd, pos, how)
        将文件描述符 fd 的当前位置设置为 pos，位置的计算方式 how 如下：设置为 SEEK_SET 或 0 表示从文件开头计算，设置为 SEEK_CUR 或 1 表示从文件当前位置计算，设置为 SEEK_END 或 2 示文件尾计算。返回新指针位置，这个位置是从文件开头计算的，单位是字节。'''
        os.lseek(it,0,2) # 移动至文件末尾
        os.lseek(it,-6,1) # 往回移动
        fstr = f"{build_time}  ->  {self.version2}\n\n'''"
        os.write(it, fstr.encode('utf8'))



    def run(self):
        """命令运行时的操作."""
        global CLEAN_TAG
        print("======= command is running =======")

        _i = 0
        while True:
            try:
                # 删除旧的生成
                print("清除旧的打包生成...")
                if _i > 0:
                    print(f'第 {_i} 次重试')
                    sleep(1)
                if os.path.exists(DIST_DIR):
                    print(f"删除目录{DIST_DIR}")
                    shutil.rmtree(DIST_DIR,ignore_errors=False)
                    sleep(1)
                    if os.path.exists(DIST_DIR):
                        print("清除旧的打包生成未能成功！")
                    break
                else:
                    print("不存在")
                    break
            except OSError as e:
                print(e)
                if _i > 9:
                        print('\n程序放弃重试\n')
                        exit(99)
                print('请解除占用以继续，程序将等待 3 秒。如需禁用删除旧的生成请修改 setup.py \n')
                _i = _i + 1
                sleep(2)
                continue
        if CLEAN_TAG == True:
            args = ['gitup.py','--old',self.___version[0],'--new',self.___version[1],'--workdir',os.getcwd(),'--no-commit','--no-tag']
        else:
            args = ['gitup.py','--old',f'{self.___version[0]}.dev1','--new',self.___version[1],'--workdir',os.getcwd(),'--commit','--tag']
        if self.qmode == False:
            args.append('--no-quiet')
        else:
            args.append('--quiet')
        command = [f'{sys.executable}']
        if self.version:
            for i in args:
                command.append(i)
            self.announce('Running command: %s' % str(command),level=distutils.log.INFO)
            check_call(command)

    def default_nv(self) -> list:
        global CLEAN_TAG
        global MY_V
        global my_v
        args = shlex.split("git describe --tags")
        result = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0, universal_newlines=True, stdout=PIPE)
        # 如果 stdout 参数是 PIPE，此属性是一个类似 open() 返回的可读流。从流中读取子进程提供的输出。
        # 如果 encoding 或 errors 参数被指定或者 universal_newlines 参数为 True，此流为文本流，否则为字节流。如果 stdout 参数非 PIPE，此属性为 None。
        vstr = result.stdout.read()
        if self.qmode:
            pass
        else:
            print(f'latest git tag: {vstr}')
            print(f'latest version: {my_v}')
        result.wait()
        if self.version != my_v:
            v_n = (int(MY_V[0]), int(MY_V[1]), int(MY_V[2]))
            self.version2 = self.version
            self.version = f'{v_n[0]}.{v_n[1]}.{v_n[2]}'
        else:
            vlist = vstr.split('-')[0].split('.')
            if int(MY_V[2]) < int(vlist[2]):
                MY_V[2] = vlist[2]
            if int(MY_V[2]) < 999:
                if len(my_v.split('.')) > 3:
                    v_n = (int(MY_V[0]), int(MY_V[1]), int(MY_V[2]))
                    self.version = f'{v_n[0]}.{v_n[1]}.{v_n[2]+10}'
                    self.version2 = f'{v_n[0]}.{v_n[1]}.{v_n[2]+11}'
                else:
                    v_n = (int(MY_V[0]), int(MY_V[1]), int(MY_V[2]))
                    self.version = f'{v_n[0]}.{v_n[1]}.{v_n[2]+1}'
                    self.version2 = f'{v_n[0]}.{v_n[1]}.{v_n[2]+2}'
                    CLEAN_TAG = True
            else:
                v_n = (int(MY_V[0]), int(MY_V[1]), 0)
                self.version = f'{v_n[0]}.{v_n[1]+1}.{v_n[2]}'
                self.version2 = f'{v_n[0]}.{v_n[1]+1}.{v_n[2]+1}'

        return [self.version,self.version2]


import setuptools.command.build_py
class BuildPyCommand(setuptools.command.build_py.build_py):
    """python setup.py build_py"""

    def run(self):
        setuptools.command.build_py.build_py.run(self)





# 读取许可证
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    print('许可证已加载\n')

print('如果第一次构建或者删除了缓存，则需要等待，这取决于当前环境\n')
print('开始执行，若长时间无响应，请检查是否有误\n')

setuptools.setup(
    name="color-theme-analyse", # 在 PyPI 上搜索的项目名称
    cmdclass={'GVC': GVC,'build_py': BuildPyCommand,}, # ---> 直接运行/调试本文件而不附加合适的参数时，这里报错是正常情况！请跳转到本文件的头部查看合适的指令 <---
    setup_requires=[], # 指定运行 setup.py 文件本身所依赖的包 , 国内由于众所周知的原因会假死，因此留空即可
    use_scm_version=True, # .gitignore 应与 setup.py 在同一文件夹 更多信息参考 https://pypi.org/project/setuptools-scm/
    # version='1.1.1', # 默认的手动指定版本
    author="Soltus",
    author_email="694357845@qq.com",
    description="SCSD-PY001 info: This is a simple demo of pictures color theme batch analysis use MMCQ with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/hi-windom/color-theme-analyse",
    project_urls={
        "Bug Tracker": "https://gitee.com/hi-windom/color-theme-analyse/issues",
    },
    classifiers=[
        # 提供分类项目的分类器列表。有关完整的列表，请参阅https://pypi.org/classifiers/
        # 尽管分类器列表可以声明项目支持的Python版本，但此信息仅用于搜索和浏览Pypi上的项目，而不用于安装项目。
        # 要实际限制项目可以安装的Python版本，请使用 python_requires
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        'Operating System :: POSIX :: Linux',
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Topic :: Multimedia :: Graphics"
    ],
    package_dir={'':'src'},
    packages=setuptools.find_packages('src'),
    namespace_packages=[],
    exclude_package_data={},
    package_data={
        '':['*.reg','*.json','*.pyd','*.vbs'],
    }, # 数据文件包含在包的子目录中,也就是有__init__.py 的文件夹中
    data_files=[
        ('lib/site-packages/MMCQsc/scp/dll',['src/MMCQsc/scp/dll/CommonOpenDialogDll.dll','src/MMCQsc/scp/dll/CommonOpenDialogDll64.dll']),
        ('lib/site-packages/MMCQsc/src',['src/MMCQsc/src/index.html','src/MMCQsc/src/gitee.svg']),
        ('lib/site-packages/MMCQsc/src/_css',['src/MMCQsc/src/_css/base.css','src/MMCQsc/src/_css/animate.css','src/MMCQsc/src/_css/sweet-alert.css']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/base.js','src/MMCQsc/src/_js/babel.min_5.8.23.js','src/MMCQsc/src/_js/react-dom.development.js','src/MMCQsc/src/_js/react.development.js','src/MMCQsc/src/_js/sweet-alert.js','src/MMCQsc/src/_js/wow.min.js','src/MMCQsc/src/_js/wow.min2.js']),
    ], # 不在包内的数据文件，格式为(安装目录，文件目录)，注意都是相对路径
    include_package_data=False, # !important
    # entry_points 可以自动将模块入口生成为跨平台的可执行文件(windows平台生成.exe)，也可用于开发插件，如果不了解不要乱写
    # 插件开发以 jupyter-lab 的中文扩展包为例：
    # entry_points={"jupyterlab.languagepack":["zh_CN = jupyterlab_Chinese_SC"],}
    # 注意 jupyterlab_Chinese_SC 并非官方使用的原名，仅供参考
    # 可执行文件以 'console_scripts':['RunMMCQsc = MMCQsc.scp.main:mainFunc'] 为例：
    # console_scripts 是 Python 定义的，可以理解为生成控制台程序脚本
    # RunMMCQsc 为文件名，表示生成 RunMMCQsc.exe 文件，pip install 后该文件就躺在 python.exe 所在文件夹的 Scripts 子文件夹里面
    # MMCQsc.scp.main:mainFunc 只需要知道 mainFunc 是 MMCQsc/scp/main.py 里的一个函数
    entry_points={'console_scripts':[
        'RunMMCQsc = MMCQsc.scp.main:mainFunc',
        'DoMMCQsc = MMCQsc.color_theme_analyse:MainFunc',
        'MMCQsc = MMCQsc.color_theme_analyse:Menu',
        'MMCQscM = MMCQsc.__main__:run',
        'MMCQ-sc = MMCQsc.__main__:run',
        'MMCQscP = MMCQsc.scp.scripts.pipw:uninstallMerge',
        'MMCQscR = MMCQsc.scp.scripts.pipw:reinstallMerge']},
    # 手动添加脚本。虽然 scripts 关键字用于指向预先制作好的脚本进行安装，建议使用实现跨平台兼容性的方法 console_scripts 入口点(entry_points) 替代
    scripts=['src/MMCQsc.cmd'],
    license="MIT",
    platforms=['Windows'],
    python_requires=">=3.9.0,<=3.10.0",
    # 关于 install_requires， 有以下五种常用的表示方法：(指定包名是必须的，而版本控制与可选依赖，则是高级形式。 这不仅仅是install_requires的形式，而是对setup.py的所有require都适用)
    # 'argparse'，只包含包名。 这种形式只检查包的存在性，不检查版本。 方便，但不利于控制风险，更新时还会遇到依赖冲突问题。
    # 'setuptools==38.2.4' 指定版本。确保了开发、测试与部署的版本一致，不会出现意外。 缺点是不利于更新，每次更新都需要改动代码。
    # 'docutils >= 0.3'，这是比较常用的形式。 当对某个库比较信任时，这种形式可以自动保持版本为最新。
    # 'Django >= 1.11, != 1.11.1, <= 2'，这是比较复杂的形式。保证了Django的大版本在1.11和2之间，也即1.11.x；并且，排除了已知有问题的版本1.11.1（仅举例）。 对于一些大型、复杂的库，这种形式是最合适的。
    # 'requests[security, socks] >= 2.18.4'，这是包含了额外的可选依赖的形式。 正常安装requests会自动安装它的install_requires中指定的依赖，而不会安装security和socks这两组依赖（这两组依赖是定义在它的extras_require中）。
    install_requires=[],
    # install_requires 在安装模块时会自动安装依赖包
    # extras_require 仅表示该模块依赖这些包，但不是必须的，需要用户手动安装。被依赖使用时，可以用类似'requests[download, advanced]'的形式来指定
    # 下载时可以使用 pip install color-theme-analyse[base] 的命令安装额外的依赖组base
    # 下载时可以使用 pip install color-theme-analyse[base,dev] 的命令安装额外的依赖组base和dev
    # extras_require 需要一个 dict ，其中按（自定义的）功能名称进行分组，每组一个 list
    extras_require={
        'base':['numpy>=1.21','pillow>=8.3','rich>=0.1',],
        'dev':['wheel','twine','setuptools','setuptools_scm','setuptools_scm_git_archive','Eel','auto-py-to-exe>=2.16.0; platform_system == "Windows"'],
        'merge':['numpy>=1.21','pillow>=8.3','rich>=0.1','wheel','twine','setuptools','setuptools_scm','setuptools_scm_git_archive','Eel','auto-py-to-exe>=2.16.0; platform_system == "Windows"'],
    },
    # dependency_links 已被弃用，因此使用 testPyPi 测试时，一些依赖项会无法下载（ https://test-files.pythonhosted.org 上没有），需要提前安装好依赖，然后 pip 后面加参数 --no-deps 无依赖下载
    dependency_links=[
        'https://pypi.douban.com/simple',
        'https://pypi.org/simple',
    ],
)


if __name__ == '__main__':
    if is_admin():
        print('看上去一切顺利，如果构建结果未能正确反映项目结构，尝试删除 .eggs 和 build 文件夹然后重试')
        sys.path = syspath
        j = 0
        while True:
            sleep(1)
            j += 1
            if os.path.exists(DIST_DIR):
                dd = DIST_DIR.replace('\\', '/')
                args = shlex.split(f"start {dd}") # 打开 dist 文件夹
                s = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True)
                s.wait()
                break
            if j >= 6:
                break
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)