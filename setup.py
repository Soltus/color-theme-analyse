import setuptools
'''
官方推荐使用静态的 setup.cfg 但动态的 setup.py 对我们来说更熟悉，学习成本低，两个文件也可以共存
MANIFEST.in 需要放在和 setup.py 同级的顶级目录下，setuptools 会自动读取该文件，需要注意 MANIFEST.in 指令是按顺序执行的，因此 exclude 要放在 include 后面
建议 MANIFEST.in 只用于构建 tar.gz 而不用于 whl ，即 setup.py 设置 [include_package_data=False]，至少在熟练掌握构建前应当这样做
//关于setuptools：setuptools 是 distutils 增强版，不包括在标准库中
//关于包格式：egg 包是过时的，whl 包是新的标准
//关于打包：python -m build 默认帮你生成了 dist/*.tar.gz 和 dist/*.whl ，更多命令使用 python setup.py --help-commands 查看
//关于上传：用 upload 命令上传包已经过时（不安全），官方提供了 twine 工具专门用来与 PyPI 交互。
项目成熟之前，应当使用 twine upload dist/* --repository testpypi
testpypi 的数据库会被定期修剪，因此可以放心上传
//关于版本号：python的软件分发工具还支持 local version identifier 可用于标识不打算发布的本地开发构建，本地版本标识符采用以下形式 <public version identifier>+<local version label> 例如：
1.2.0.dev1+hg.5.b11e5e6f0b0b  # 5th VCS commmit since 1.2.0.dev1 release
1.2.1+fedora.4                # Package with downstream Fedora patches applied
使用了本地版本标识符是无法上传到 PyPi 的，因此 local_scheme = "no-local-version" 在 pyproject.toml
'''

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="color-theme-analyse",
    setup_requires=['setuptools_scm'], # 指定运行 setup.py 文件本身所依赖的包
    use_scm_version=True, # .gitignore 应与 setup.py 在同一文件夹 更多信息参考 https://pypi.org/project/setuptools-scm/
    # version="0.0.5", # 默认的手动指定版本
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
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Topic :: Multimedia :: Graphics"
    ],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    exclude_package_data={},
    package_data={
        '':['*.json'],
    }, # 数据文件包含在包的子目录中,也就是有__init__.py 的文件夹中
    data_files=[
        ('lib/site-packages/MMCQsc/src',['src/MMCQsc/src/index.html']),
        ('lib/site-packages/MMCQsc/src',['src/MMCQsc/src/gitee.svg']),
        ('lib/site-packages/MMCQsc/src/_css',['src/MMCQsc/src/_css/base.css','src/MMCQsc/src/_css/animate.css','src/MMCQsc/src/_css/sweet-alert.css']),
        ('lib/site-packages/MMCQsc/src/_js',['src/MMCQsc/src/_js/base.js','src/MMCQsc/src/_js/babel.min_5.8.23.js','src/MMCQsc/src/_js/react-dom.development.js','src/MMCQsc/src/_js/react.development.js','src/MMCQsc/src/_js/sweet-alert.js','src/MMCQsc/src/_js/wow.min.js','src/MMCQsc/src/_js/wow.min2.js']),
    ], # 不在包内的数据文件，格式为(安装目录，文件目录)，注意都是相对路径
    include_package_data=False, # !important
    # entry_points 一般用于开发插件，如果不了解不要乱写
    # 以jupyter-lab的中文扩展包为例：entry_points={"jupyterlab.languagepack":["zh_CN = jupyterlab_Chinese_SC"],}
    # 注意 jupyterlab_Chinese_SC 并非官方使用的原名，仅供参考
    entry_points={'console_scripts':['mmcqsc = MMCQsc']},
    # 手动添加脚本。虽然 scripts 关键字用于指向预先制作好的脚本进行安装，建议使用实现跨平台兼容性的方法 console_scripts 入口点(entry_points)
    scripts=['src/MMCQsc.cmd'],
    license="MIT",
    platforms=['Windows'],
    python_requires=">=3.8.0",
    # 关于 install_requires， 有以下五种常用的表示方法：(指定包名是必须的，而版本控制与可选依赖，则是高级形式。 这不仅仅是install_requires的形式，而是对setup.py的所有require都适用)
    # 'argparse'，只包含包名。 这种形式只检查包的存在性，不检查版本。 方便，但不利于控制风险，更新时还会遇到依赖冲突问题。
    # 'setuptools==38.2.4' 指定版本。确保了开发、测试与部署的版本一致，不会出现意外。 缺点是不利于更新，每次更新都需要改动代码。
    # 'docutils >= 0.3'，这是比较常用的形式。 当对某个库比较信任时，这种形式可以自动保持版本为最新。
    # 'Django >= 1.11, != 1.11.1, <= 2'，这是比较复杂的形式。保证了Django的大版本在1.11和2之间，也即1.11.x；并且，排除了已知有问题的版本1.11.1（仅举例）。 对于一些大型、复杂的库，这种形式是最合适的。
    # 'requests[security, socks] >= 2.18.4'，这是包含了额外的可选依赖的形式。 正常安装requests会自动安装它的install_requires中指定的依赖，而不会安装security和socks这两组依赖（这两组依赖是定义在它的extras_require中）。
    install_requires=[
        'easygui>=0.1',
        'opencv-python>=4.0',
        'numpy>=1.21',
        'pillow>=8.3',
        'rich>=0.1',
    ],
    # install_requires 在安装模块时会自动安装依赖包
    # extras_require 仅表示该模块依赖这些包，但不是必须的，需要用户手动安装。被依赖使用时，可以用类似'requests[download, advanced]'的形式来指定
    # extras_require 需要一个 dict ，其中按（自定义的）功能名称进行分组，每组一个 list
    extras_require={
        'download':['pipx>=0.1'],
        'advanced':['pyinstaller>=4.3'],
    },
    # dependency_links 已被弃用，因此使用 testPyPi 测试时，一些依赖项会无法下载（ https://test-files.pythonhosted.org 上没有），需要提前安装好依赖，然后 pip 后面加参数 --no-deps 无依赖下载
    dependency_links=[
        'https://pypi.douban.com/simple',
        'https://pypi.org/simple',
    ],
)