# __version__ = "0.0.1"
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("MMCQsc")
except PackageNotFoundError:
    # package is not installed
    pass

__doc__ = '''
官方推荐使用静态的 setup.cfg 但动态的 setup.py 对我们来说更熟悉，学习成本低，两个文件也可以共存
MANIFEST.in 需要放在和 setup.py 同级的顶级目录下，setuptools 会自动读取该文件，需要注意 MANIFEST.in 指令是按顺序执行的，因此 exclude 要放在 include 后面
建议 MANIFEST.in 只用于构建 tar.gz 而不用于 whl ，即 setup.py 设置 [include_package_data=False]，至少在熟练掌握构建前应当这样做

//关于setuptools：setuptools 是 distutils 增强版，不包括在标准库中

//关于包格式：egg 包是过时的，whl 包是新的标准

//关于打包：

        [1]
        python setup.py sdist 生成 dist/*.tar.gz [源码];
        [2]
        python setup.py bdist_wheel 生成 dist/*.whl [通用包];
        [3]
        如果你的项目不是跨平台的，应当构建指定平台的包：
        python setup.py bdist_wheel --plat-name win32 [win32平台构建]
        python setup.py bdist_wheel --plat-name win_amd64 [win_amd64平台构建]
        [4]
        python setup.py bdist 生成 dist/*.zip [镜像构建，包含虚拟环境，不建议使用];
        [5]
        python setup.py bdist_wininst 生成 dist/*.whl [Windows安装引导程序];
        ### 从 Python 3.8 开始不推荐使用 bdist_wininst ; bdist_msi从 Python 3.9 起被弃用。 ###
        [6]
        更多命令使用 python setup.py --help-commands 查看

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
修改 Release 版本号需要使用 Git 打上版本号标签，在熟悉之前应当使用 x.x.x 形式的标签（例如 1.0.2 ）
如果不熟悉 Git 命令行操作，可以使用软件 Sourcetree 直观的提交和打标签。如果没有标签，你生成的包将始终为 0.1.dev*
建议的版本号规则：
模块的版本号采用X.Y.Z的格式，
1、修复bug，小改动，增加z。
2、增加新特性，可向后兼容，增加y
3、有很大的改动，无法向下兼容,增加x
'''